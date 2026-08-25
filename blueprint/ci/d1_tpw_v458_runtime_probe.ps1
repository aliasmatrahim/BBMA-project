$ErrorActionPreference = 'Stop'

$src = Join-Path $PWD 'blueprint\source\BBMA_EA.mq4'
if (-not (Test-Path $src)) { throw 'EA source missing' }
$sourceText = Get-Content $src -Raw
if ($sourceText -notmatch 'Version 4\.5\.8 - D1 TP-Wajib Lifecycle Stage') { throw 'Unexpected EA build identifier' }
if ($sourceText -notmatch '#property\s+version\s+"4\.58"') { throw 'Unexpected EA property version' }
if ($sourceText -notmatch 'EnableD1TPWLifecycle\s*=\s*false;') { throw 'D1 TPW lifecycle gate is not OFF' }
if ($sourceText -notmatch 'EnableC044Lifecycle\s*=\s*false;') { throw 'C044 lifecycle gate is not OFF' }

$blob = (git rev-parse HEAD:blueprint/source/BBMA_EA.mq4).Trim()
if ($blob -ne 'a166ffb23aba5e6b4011a28d9de8896cd00e33a1') { throw "Unexpected source blob: $blob" }
$sha256 = (& python -c "import subprocess,hashlib; d=subprocess.check_output(['git','cat-file','blob','$blob']); print(hashlib.sha256(d).hexdigest())").Trim()
if ($LASTEXITCODE -ne 0) { throw 'Unable to hash canonical Git blob' }
if ($sha256 -ne 'ba2e5815d1b221d7bba46ed0be4793aa5bc6154e29e9b19562dfffbd28c8f0bc') { throw "Unexpected canonical source SHA256: $sha256" }
$workingTreeSha = (Get-FileHash $src -Algorithm SHA256).Hash.ToLower()
Write-Host "EA_BLOB=$blob"
Write-Host "EA_CANONICAL_SHA256=$sha256"
Write-Host "EA_WORKTREE_SHA256=$workingTreeSha"
Write-Host 'LIFECYCLE_GATES=OFF_OFF'

$meta = Get-ChildItem 'C:\Program Files*' -Filter metaeditor.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
$terminal = Get-ChildItem 'C:\Program Files*' -Filter terminal.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $meta -or -not $terminal) {
  $setup = Join-Path $env:RUNNER_TEMP 'mt4setup.exe'
  Write-Host 'Downloading official MT4 installer...'
  & curl.exe -L --fail --retry 3 --retry-delay 3 --connect-timeout 20 --max-time 180 'https://download.mql5.com/cdn/web/metaquotes.software.corp/mt4/mt4setup.exe' -o $setup
  if ($LASTEXITCODE -ne 0 -or -not (Test-Path $setup) -or (Get-Item $setup).Length -lt 1000000) { throw 'Official MT4 installer download failed' }
  Write-Host 'Launching official MT4 installer...'
  $installer = Start-Process -FilePath $setup -ArgumentList '/auto' -PassThru
  for ($i=0; $i -lt 84; $i++) {
    Start-Sleep -Seconds 5
    $meta = Get-ChildItem 'C:\Program Files*' -Filter metaeditor.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    $terminal = Get-ChildItem 'C:\Program Files*' -Filter terminal.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($meta -and $terminal) { break }
    if ($installer.HasExited -and $i -gt 12) { break }
  }
  if ($installer -and -not $installer.HasExited) { try { $installer.Kill() } catch {} }
}
if (-not $meta -or -not $terminal) { throw 'Official MT4 terminal/metaeditor not found' }
Write-Host "MT4_METAEDITOR=$($meta.FullName)"
Write-Host "MT4_TERMINAL=$($terminal.FullName)"

$installDir = Split-Path $terminal.FullName -Parent
$portable = Join-Path $env:RUNNER_TEMP 'mt4portable-v458'
if (Test-Path $portable) { Remove-Item $portable -Recurse -Force }
New-Item -ItemType Directory -Path $portable | Out-Null
Copy-Item "$installDir\*" $portable -Recurse -Force
$portableTerminal = Join-Path $portable 'terminal.exe'
$portableMeta = Join-Path $portable 'metaeditor.exe'
if (-not (Test-Path $portableTerminal) -or -not (Test-Path $portableMeta)) { throw 'Portable MT4 copy failed' }

$expertsDir = Join-Path $portable 'MQL4\Experts'
New-Item -ItemType Directory -Path $expertsDir -Force | Out-Null
$dst = Join-Path $expertsDir 'BBMA_EA.mq4'
Copy-Item $src $dst -Force
$compileLog = Join-Path $env:RUNNER_TEMP 'd1-tpw-v458-runtime-compile.log'
& $portableMeta "/compile:$dst" "/log:$compileLog"
Start-Sleep -Seconds 2
if (-not (Test-Path $compileLog)) { throw 'MetaEditor compile log missing' }
$compileText = Get-Content $compileLog -Raw
$compileText | Write-Host
$matches = [regex]::Matches($compileText, '(?i)(\d+)\s+errors?,\s*(\d+)\s+warnings?')
if ($matches.Count -lt 1) { throw 'Unable to parse MetaEditor summary' }
$last = $matches[$matches.Count - 1]
$errors = [int]$last.Groups[1].Value
$warnings = [int]$last.Groups[2].Value
if ($errors -ne 0 -or $warnings -ne 0) { throw "MetaEditor produced $errors errors / $warnings warnings" }
$ex4 = [System.IO.Path]::ChangeExtension($dst, '.ex4')
if (-not (Test-Path $ex4)) { throw 'EX4 not produced' }
Write-Host 'METAEDITOR_0E0W=PASS'

$ini = Join-Path $env:RUNNER_TEMP 'd1-tpw-v458-runtime.ini'
@('[Common]','EnableNews=false','','[Experts]','ExpertsEnable=true','ExpertsDllImport=false','ExpertsExpImport=false','ExpertsTrades=false','','[StartUp]','Symbol=EURUSD','Period=M15','Expert=BBMA_EA') | Set-Content -Path $ini -Encoding Ascii

Write-Host 'Launching MT4 with Expert trading disabled...'
$proc = Start-Process -FilePath $portableTerminal -ArgumentList '/portable', "/config:$ini" -PassThru
for ($i=0; $i -lt 12; $i++) {
  Start-Sleep -Seconds 5
  if ($proc.HasExited) { break }
}
if (-not $proc.HasExited) { try { $proc.CloseMainWindow() | Out-Null } catch {}; Start-Sleep -Seconds 2 }
if (-not $proc.HasExited) { try { $proc.Kill() } catch {} }

$journal = @(Get-ChildItem (Join-Path $portable 'logs') -Filter '*.log' -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime)
$expertLogs = @(Get-ChildItem (Join-Path $portable 'MQL4\Logs') -Filter '*.log' -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime)
$allLogs = @($journal) + @($expertLogs)
$combinedPath = Join-Path $env:RUNNER_TEMP 'd1-tpw-v458-runtime-combined.log'
$combined = ''
foreach ($f in $allLogs) {
  $combined += "`r`n===== $($f.FullName) =====`r`n"
  $combined += (Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue)
}
$combined | Set-Content $combinedPath -Encoding UTF8
if ($combined -ne '') {
  ($combined -split "`r?`n" | Select-Object -Last 300) | ForEach-Object { Write-Host $_ }
}

$fatalPatterns = @('array out of range','zero divide','critical runtime error','access violation','stack overflow','invalid pointer','unresolved import','cannot load expert','expert initialization failed','init failed')
foreach ($p in $fatalPatterns) {
  if ($combined -match [regex]::Escape($p)) { throw "Fatal MT4 runtime signature detected: $p" }
}

$class = 'HOSTED_ENVIRONMENT_UNCLASSIFIED_NO_FATAL_SIGNATURE'
if ($combined -match '\[P3S1\]\[PASS\] EA initialized successfully') {
  $class = 'ATTACH_OK_TRADING_DISABLED'
} elseif (($combined -match '\[P3S1\]\[FAIL\] No valid pairs loaded') -or ($combined -match '\[P3S1\]\[FAIL\] Symbol resolution failed') -or ($combined -match '(?i)not connected') -or ($combined -match '(?i)no connection') -or ($combined -match '(?i)no prices') -or ($combined -match '(?i)waiting for update') -or ($combined -match '(?i)authorization failed')) {
  $class = 'ENVIRONMENT_BLOCKED_NO_BROKER_SYMBOL_DATA'
} elseif ($allLogs.Count -eq 0) {
  $class = 'HOSTED_ENVIRONMENT_NO_MT4_LOGS_NO_FATAL_SIGNATURE'
}
Write-Host "MT4_RUNTIME_CLASS=$class"

$summaryPath = Join-Path $env:RUNNER_TEMP 'd1-tpw-v458-runtime-summary.txt'
@(
  "STATUS=$class",
  "SOURCE_BLOB=$blob",
  "SOURCE_CANONICAL_SHA256=$sha256",
  "SOURCE_WORKTREE_SHA256=$workingTreeSha",
  'METAEDITOR=0E0W',
  'D1_TPW_GATE=OFF',
  'C044_GATE=OFF',
  'EXPERT_TRADING=DISABLED',
  "MT4_LOG_COUNT=$($allLogs.Count)"
) | Set-Content $summaryPath -Encoding UTF8

Write-Host "SUMMARY_PATH=$summaryPath"
Write-Host "COMBINED_LOG=$combinedPath"
Write-Host 'PROBE_COMPLETED=PASS'
