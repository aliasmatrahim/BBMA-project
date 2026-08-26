param(
  [string]$RepoRoot = $PWD,
  [string]$WorkDir = (Join-Path $env:RUNNER_TEMP 'bbma-v458-runtime-prep')
)
$ErrorActionPreference = 'Stop'
$RepoRoot = [System.IO.Path]::GetFullPath($RepoRoot)
$WorkDir = [System.IO.Path]::GetFullPath($WorkDir)
if (Test-Path $WorkDir) { Remove-Item $WorkDir -Recurse -Force }
New-Item -ItemType Directory -Path $WorkDir -Force | Out-Null

Push-Location $RepoRoot
try {
  & python blueprint/tests/test_v458_runtime_variant_builder.py
  if ($LASTEXITCODE -ne 0) { throw 'variant builder selftest failed' }
  & python blueprint/tests/test_v458_runtime_analyzer.py
  if ($LASTEXITCODE -ne 0) { throw 'runtime analyzer selftest failed' }
  & python -m py_compile blueprint/tools/v458_runtime_variant_builder.py blueprint/tools/v458_runtime_analyzer.py blueprint/tools/n2_nmje_auto_research_pipeline.py
  if ($LASTEXITCODE -ne 0) { throw 'python compile checks failed' }

  $profiles = @(
    @{ Name='BASELINE'; Key='baseline' },
    @{ Name='R1_D1TPW'; Key='r1-d1tpw' },
    @{ Name='R2_C044'; Key='r2-c044' }
  )
  foreach ($p in $profiles) {
    $out = Join-Path $WorkDir ($p.Name + '.mq4')
    $meta = Join-Path $WorkDir ($p.Name + '.json')
    & python blueprint/tools/v458_runtime_variant_builder.py --repo-root $RepoRoot --profile $p.Key --output $out --metadata $meta
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $out)) { throw "variant build failed: $($p.Name)" }
  }

  $obs = Join-Path $RepoRoot 'blueprint/runtime/V458_Runtime_Observer.mq4'
  if (-not (Test-Path $obs)) { throw 'runtime observer missing' }
  $obsText = Get-Content $obs -Raw
  foreach ($forbidden in @('OrderSend(','OrderClose(','OrderModify(','OrderDelete(')) {
    if ($obsText.Contains($forbidden)) { throw "observer contains broker-write primitive: $forbidden" }
  }
  Write-Host 'OBSERVER_READ_ONLY_STATIC=PASS'

  $metaEditor = Get-ChildItem 'C:\Program Files*' -Filter metaeditor.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
  $terminal = Get-ChildItem 'C:\Program Files*' -Filter terminal.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
  if (-not $metaEditor -or -not $terminal) {
    $setup = Join-Path $WorkDir 'mt4setup.exe'
    & curl.exe -L --fail --retry 3 --retry-delay 3 --connect-timeout 20 --max-time 180 'https://download.mql5.com/cdn/web/metaquotes.software.corp/mt4/mt4setup.exe' -o $setup
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $setup) -or (Get-Item $setup).Length -lt 1000000) { throw 'official MT4 installer download failed' }
    $installer = Start-Process -FilePath $setup -ArgumentList '/auto' -PassThru
    for ($i=0; $i -lt 84; $i++) {
      Start-Sleep -Seconds 5
      $metaEditor = Get-ChildItem 'C:\Program Files*' -Filter metaeditor.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
      $terminal = Get-ChildItem 'C:\Program Files*' -Filter terminal.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
      if ($metaEditor -and $terminal) { break }
      if ($installer.HasExited -and $i -gt 12) { break }
    }
    if ($installer -and -not $installer.HasExited) { try { $installer.Kill() } catch {} }
  }
  if (-not $metaEditor -or -not $terminal) { throw 'official MT4 MetaEditor/terminal unavailable' }

  $installDir = Split-Path $terminal.FullName -Parent
  $portable = Join-Path $WorkDir 'mt4portable'
  New-Item -ItemType Directory -Path $portable -Force | Out-Null
  Copy-Item "$installDir\*" $portable -Recurse -Force
  $portableMeta = Join-Path $portable 'metaeditor.exe'
  $experts = Join-Path $portable 'MQL4\Experts'
  New-Item -ItemType Directory -Path $experts -Force | Out-Null

  $compileTargets = @()
  foreach ($p in $profiles) {
    $src = Join-Path $WorkDir ($p.Name + '.mq4')
    $dst = Join-Path $experts ($p.Name + '.mq4')
    Copy-Item $src $dst -Force
    $compileTargets += @{ Name=$p.Name; Path=$dst }
  }
  $obsDst = Join-Path $experts 'V458_Runtime_Observer.mq4'
  Copy-Item $obs $obsDst -Force
  $compileTargets += @{ Name='OBSERVER'; Path=$obsDst }

  foreach ($t in $compileTargets) {
    $log = Join-Path $WorkDir ($t.Name + '.compile.log')
    & $portableMeta "/compile:$($t.Path)" "/log:$log"
    Start-Sleep -Seconds 2
    if (-not (Test-Path $log)) { throw "compile log missing: $($t.Name)" }
    $txt = Get-Content $log -Raw
    $matches = [regex]::Matches($txt, '(?i)(\d+)\s+errors?,\s*(\d+)\s+warnings?')
    if ($matches.Count -lt 1) { throw "unable to parse compile summary: $($t.Name)" }
    $last = $matches[$matches.Count - 1]
    $err = [int]$last.Groups[1].Value
    $warn = [int]$last.Groups[2].Value
    if ($err -ne 0 -or $warn -ne 0) { throw "$($t.Name) compile=$err errors/$warn warnings" }
    $ex4 = [System.IO.Path]::ChangeExtension($t.Path, '.ex4')
    if (-not (Test-Path $ex4)) { throw "EX4 missing: $($t.Name)" }
    Write-Host "METAEDITOR_0E0W_$($t.Name)=PASS"
  }
  Write-Host 'V458_NATIVE_COMPILE_MATRIX=PASS'
}
finally {
  Pop-Location
}
