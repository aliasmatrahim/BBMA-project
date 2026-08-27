param(
  [string]$WorkDir = ''
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$ExpectedBlob = 'dc83e62748c93171d89a312e9f7a53c06d97e261'
$ExpectedSha = '0a42ee2e6c32810f655b592d8738f500e8b63b4e08c4c874e82452f75ce94b2e'

if ([string]::IsNullOrWhiteSpace($WorkDir)) {
  $baseTemp = $env:RUNNER_TEMP
  if ([string]::IsNullOrWhiteSpace($baseTemp)) { $baseTemp = $env:TEMP }
  $WorkDir = Join-Path $baseTemp 'bbma-v459-native-matrix'
}
$WorkDir = [System.IO.Path]::GetFullPath($WorkDir)
if (Test-Path $WorkDir) { Remove-Item $WorkDir -Recurse -Force }
New-Item -ItemType Directory -Path $WorkDir -Force | Out-Null

function Run-Python([string]$Script) {
  & python $Script
  if ($LASTEXITCODE -ne 0) { throw "Python gate failed: $Script" }
}

Run-Python (Join-Path $RepoRoot 'blueprint\tests\test_v459_runtime_variant_builder.py')
Run-Python (Join-Path $RepoRoot 'blueprint\tests\test_v459_runtime_analyzer.py')
& python -m py_compile `
  (Join-Path $RepoRoot 'blueprint\tools\v459_runtime_variant_builder.py') `
  (Join-Path $RepoRoot 'blueprint\tools\v459_runtime_analyzer.py') `
  (Join-Path $RepoRoot 'blueprint\tests\test_v459_runtime_variant_builder.py') `
  (Join-Path $RepoRoot 'blueprint\tests\test_v459_runtime_analyzer.py')
if ($LASTEXITCODE -ne 0) { throw 'v4.59 Python compile gate failed' }

$Source = Join-Path $RepoRoot 'blueprint\source\BBMA_EA.mq4'
$Blob = (& git -C $RepoRoot hash-object 'blueprint/source/BBMA_EA.mq4').Trim()
$Sha = (Get-FileHash $Source -Algorithm SHA256).Hash.ToLower()
if ($Blob -ne $ExpectedBlob) { throw "Unexpected v4.59 source blob: $Blob" }
if ($Sha -ne $ExpectedSha) { throw "Unexpected v4.59 source SHA256: $Sha" }

$Builder = Join-Path $RepoRoot 'blueprint\tools\v459_runtime_variant_builder.py'
$Variants = @(
  @{ Key='baseline'; Name='BASELINE' },
  @{ Key='r1-d1tpw'; Name='R1_D1TPW' },
  @{ Key='r2-c044'; Name='R2_C044' }
)
foreach ($v in $Variants) {
  $mq4 = Join-Path $WorkDir ("BBMA_EA_V459_{0}.mq4" -f $v.Name)
  $meta = Join-Path $WorkDir ("BBMA_EA_V459_{0}.json" -f $v.Name)
  & python $Builder --repo-root $RepoRoot --profile $v.Key --output $mq4 --metadata $meta
  if ($LASTEXITCODE -ne 0) { throw "Variant build failed: $($v.Name)" }
  $v.Mq4 = $mq4
  $v.Meta = $meta
}

$Observer = Join-Path $RepoRoot 'blueprint\runtime\V459_Runtime_Observer.mq4'
$ObserverText = Get-Content $Observer -Raw
foreach ($forbidden in @('OrderSend(', 'OrderClose(', 'OrderModify(', 'OrderDelete(')) {
  if ($ObserverText.Contains($forbidden)) { throw "Observer broker-write primitive found: $forbidden" }
}
if (!$ObserverText.Contains('[V459-OBS]')) { throw 'V459 observer tag missing' }
foreach ($required in @('BBXH|S', 'BBXT|S', 'D1TPW|S', 'C044|S')) {
  if (!$ObserverText.Contains($required)) { throw "Observer GV coverage missing: $required" }
}

$Meta = Get-ChildItem 'C:\Program Files*' -Filter metaeditor.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
if (!$Meta) {
  $Setup = Join-Path $WorkDir 'mt4setup.exe'
  & curl.exe -L --fail --retry 3 --retry-delay 3 --connect-timeout 30 --max-time 240 'https://download.mql5.com/cdn/web/metaquotes.software.corp/mt4/mt4setup.exe' -o $Setup
  if ($LASTEXITCODE -ne 0 -or !(Test-Path $Setup)) { throw 'Official MT4 installer download failed' }
  if ((Get-Item $Setup).Length -lt 1000000) { throw 'MT4 installer unexpectedly small' }
  $proc = Start-Process -FilePath $Setup -ArgumentList '/auto' -PassThru
  for ($i = 0; $i -lt 90; $i++) {
    Start-Sleep -Seconds 5
    $Meta = Get-ChildItem 'C:\Program Files*' -Filter metaeditor.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($Meta) { break }
    if ($proc.HasExited -and $i -gt 12) { break }
  }
  if ($proc -and !$proc.HasExited) { try { $proc.Kill() } catch {} }
}
if (!$Meta) { throw 'Official MetaEditor not found' }
$MetaEditor = $Meta.FullName

function Compile-Mq4([string]$Path, [string]$Label) {
  $Log = Join-Path $WorkDir ("compile-{0}.log" -f $Label)
  & $MetaEditor "/compile:$Path" "/log:$Log"
  Start-Sleep -Seconds 2
  if (!(Test-Path $Log)) { throw "Compile log missing: $Label" }
  $Text = Get-Content $Log -Raw
  $Matches = [regex]::Matches($Text, '(?i)(\d+)\s+errors?,\s*(\d+)\s+warnings?')
  if ($Matches.Count -lt 1) { throw "Compile summary missing: $Label`n$Text" }
  $Last = $Matches[$Matches.Count - 1]
  $Errors = [int]$Last.Groups[1].Value
  $Warnings = [int]$Last.Groups[2].Value
  $Ex4 = [System.IO.Path]::ChangeExtension($Path, '.ex4')
  if (!(Test-Path $Ex4)) { throw "EX4 missing: $Label" }
  if ($Errors -ne 0 -or $Warnings -ne 0) { throw "Native compile failed ${Label}: $Errors errors / $Warnings warnings" }
  return [ordered]@{ label=$Label; mq4=$Path; ex4=$Ex4; log=$Log; errors=$Errors; warnings=$Warnings }
}

$Rows = @()
foreach ($v in $Variants) {
  $Rows += Compile-Mq4 $v.Mq4 $v.Name
}
$ObserverCopy = Join-Path $WorkDir 'V459_Runtime_Observer.mq4'
Copy-Item $Observer $ObserverCopy -Force
$Rows += Compile-Mq4 $ObserverCopy 'OBSERVER'

$Result = [ordered]@{
  schema = 'BBMA_V459_NATIVE_COMPILE_MATRIX_V1'
  status = 'PASS'
  canonical_blob = $ExpectedBlob
  canonical_sha256 = $ExpectedSha
  build = 'Version 4.5.9 - P0 Execution Identity Persistence Fix'
  property_version = '4.59'
  profiles = @('BASELINE','R1_D1TPW','R2_C044')
  observer_read_only = $true
  rows = $Rows
}
$ResultPath = Join-Path $WorkDir 'v459-native-compile-matrix-result.json'
$Result | ConvertTo-Json -Depth 8 | Set-Content $ResultPath -Encoding UTF8

Write-Host 'V459_NATIVE_COMPILE_MATRIX=PASS'
Write-Host "SOURCE_BLOB=$ExpectedBlob"
Write-Host "SOURCE_SHA256=$ExpectedSha"
Write-Host 'ERRORS=0'
Write-Host 'WARNINGS=0'
Write-Host "RESULT=$ResultPath"
