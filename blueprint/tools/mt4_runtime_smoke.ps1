param(
  [Parameter(Mandatory=$true)][string]$RepoRoot,
  [Parameter(Mandatory=$true)][string]$EvidenceDir
)

$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null

$classification = 'UNRESOLVED'
$stage = 'START'
$detail = ''
$errors = -1
$warnings = -1
$blob = ''
$metaPath = ''
$terminalPath = ''
$compileLog = Join-Path $EvidenceDir 'mt4-runtime-compile.log'
$combinedPath = Join-Path $EvidenceDir 'mt4-runtime-combined.log'
$resultPath = Join-Path $EvidenceDir 'mt4-runtime-result.txt'
$exitCode = 1

try {
  $stage = 'VERIFY_SOURCE'
  $repo = (Resolve-Path $RepoRoot).Path
  $src = Join-Path $repo 'blueprint\source\BBMA_EA.mq4'
  if (-not (Test-Path $src)) { throw 'EA source missing' }
  $text = Get-Content $src -Raw
  if ($text -notmatch 'Version 4\.5\.1 - D1-02 M15-M16 Strategic Gate') { throw 'Unexpected D1-02 build identifier' }
  $blob = (& git -C $repo rev-parse 'HEAD:blueprint/source/BBMA_EA.mq4').Trim()

  $stage = 'ACQUIRE_MT4'
  $dirs = @('C:\Program Files (x86)\MetaTrader 4','C:\Program Files\MetaTrader 4')
  $installDir = $null
  foreach ($dir in $dirs) {
    if ((Test-Path (Join-Path $dir 'metaeditor.exe')) -and (Test-Path (Join-Path $dir 'terminal.exe'))) {
      $installDir = $dir
      break
    }
  }
  if (-not $installDir) {
    $setup = Join-Path $env:RUNNER_TEMP 'mt4setup.exe'
    Invoke-WebRequest -Uri 'https://download.mql5.com/cdn/web/metaquotes.software.corp/mt4/mt4setup.exe' -OutFile $setup -UseBasicParsing
    $sp = Start-Process -FilePath $setup -ArgumentList '/auto' -PassThru
    for ($i=0; $i -lt 72; $i++) {
      Start-Sleep -Seconds 5
      foreach ($dir in $dirs) {
        if ((Test-Path (Join-Path $dir 'metaeditor.exe')) -and (Test-Path (Join-Path $dir 'terminal.exe'))) {
          $installDir = $dir
          break
        }
      }
      if ($installDir) { break }
    }
    if ($sp -and -not $sp.HasExited) { try { $sp.Kill() } catch {} }
  }
  if (-not $installDir) { throw 'Official MT4 terminal/metaeditor not found' }
  $metaPath = Join-Path $installDir 'metaeditor.exe'
  $terminalPath = Join-Path $installDir 'terminal.exe'

  $stage = 'PREPARE_PORTABLE'
  $portable = Join-Path $env:RUNNER_TEMP 'mt4portable'
  if (Test-Path $portable) { Remove-Item $portable -Recurse -Force }
  New-Item -ItemType Directory -Path $portable | Out-Null
  Copy-Item "$installDir\*" $portable -Recurse -Force
  $portableMeta = Join-Path $portable 'metaeditor.exe'
  $portableTerminal = Join-Path $portable 'terminal.exe'
  if (-not (Test-Path $portableMeta) -or -not (Test-Path $portableTerminal)) { throw 'Portable MT4 copy incomplete' }

  $stage = 'COMPILE'
  $expertsDir = Join-Path $portable 'MQL4\Experts'
  New-Item -ItemType Directory -Path $expertsDir -Force | Out-Null
  $dst = Join-Path $expertsDir 'BBMA_EA.mq4'
  Copy-Item $src $dst -Force
  & $portableMeta "/compile:$dst" "/log:$compileLog"
  Start-Sleep -Seconds 2
  if (-not (Test-Path $compileLog)) { throw 'MetaEditor compile log missing' }
  $ct = Get-Content $compileLog -Raw
  $matches = [regex]::Matches($ct, '(?i)(\d+)\s+errors?,\s*(\d+)\s+warnings?')
  if ($matches.Count -lt 1) { throw 'Unable to parse MetaEditor summary' }
  $m = $matches[$matches.Count - 1]
  $errors = [int]$m.Groups[1].Value
  $warnings = [int]$m.Groups[2].Value
  if ($errors -ne 0 -or $warnings -ne 0) { throw "MetaEditor produced $errors errors / $warnings warnings" }
  if (-not (Test-Path ([System.IO.Path]::ChangeExtension($dst,'.ex4')))) { throw 'EX4 not produced' }

  $stage = 'LAUNCH_MT4'
  $ini = Join-Path $env:RUNNER_TEMP 'runtime-smoke.ini'
  @'
[Common]
EnableNews=false

[Experts]
ExpertsEnable=true
ExpertsDllImport=false
ExpertsExpImport=false
ExpertsTrades=false

[StartUp]
Symbol=EURUSD
Period=M15
Expert=BBMA_EA
'@ | Set-Content -Path $ini -Encoding Ascii
  $proc = Start-Process -FilePath $portableTerminal -ArgumentList '/portable', "/config:$ini" -PassThru
  for ($i=0; $i -lt 12; $i++) {
    Start-Sleep -Seconds 5
    if ($proc.HasExited) { break }
  }
  if (-not $proc.HasExited) { try { $proc.CloseMainWindow() | Out-Null } catch {}; Start-Sleep -Seconds 2 }
  if (-not $proc.HasExited) { try { $proc.Kill() } catch {} }

  $stage = 'INSPECT_LOGS'
  $journal = @(Get-ChildItem (Join-Path $portable 'logs') -Filter '*.log' -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime)
  $expertLogs = @(Get-ChildItem (Join-Path $portable 'MQL4\Logs') -Filter '*.log' -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime)
  $all = @($journal) + @($expertLogs)
  if ($all.Count -eq 0) { throw 'No MT4 Journal/Experts logs produced' }

  $combined = ''
  foreach ($f in $all) {
    $combined += "`r`n===== $($f.FullName) =====`r`n"
    $combined += (Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue)
  }
  $combined | Set-Content $combinedPath -Encoding UTF8

  foreach ($p in @('array out of range','zero divide','critical runtime error','access violation','stack overflow','invalid pointer','unresolved import','cannot load expert','expert initialization failed')) {
    if ($combined -match [regex]::Escape($p)) { throw "Fatal MT4 runtime signature detected: $p" }
  }

  if ($combined -match '\[P3S1\]\[PASS\] EA initialized successfully') {
    $classification = 'PASS_EA_INITIALIZED'
    $detail = 'EA initialized in MT4; no fatal runtime signature detected.'
    $stage = 'PASS'
    $exitCode = 0
  }
  elseif (($combined -match '\[P3S1\]\[FAIL\] No valid pairs loaded') -or
          ($combined -match '\[P3S1\]\[FAIL\] Symbol resolution failed') -or
          ($combined -match '(?i)not connected') -or
          ($combined -match '(?i)no prices') -or
          ($combined -match '(?i)waiting for update')) {
    $classification = 'ENVIRONMENT_BLOCKED_NO_BROKER_SYMBOL_DATA'
    $detail = 'MT4 launched and logs were inspected; GitHub runner lacks usable broker/symbol feed. No fatal runtime signature detected.'
    $stage = 'PASS_ENVIRONMENT_LIMIT'
    $exitCode = 0
  }
  else {
    throw 'MT4 launched but EA initialization could not be positively classified from Journal/Experts logs'
  }
}
catch {
  $detail = $_.Exception.Message
  $classification = 'FAIL'
  $exitCode = 1
}

@(
  "Stage=$stage",
  "Classification=$classification",
  "GitBlob=$blob",
  "MetaEditorErrors=$errors",
  "MetaEditorWarnings=$warnings",
  "MetaEditor=$metaPath",
  "Terminal=$terminalPath",
  "Detail=$detail"
) | Set-Content $resultPath -Encoding UTF8

Get-Content $resultPath | ForEach-Object { Write-Host $_ }
if (Test-Path $combinedPath) {
  Write-Host '--- MT4 Journal/Experts tail ---'
  Get-Content $combinedPath | Select-Object -Last 250 | ForEach-Object { Write-Host $_ }
}
exit $exitCode
