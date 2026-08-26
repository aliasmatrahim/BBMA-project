param(
  [Parameter(Mandatory=$true)][string]$MT4DataPath,
  [Parameter(Mandatory=$true)][string]$OutputDir,
  [ValidateSet('BASELINE','R1_D1TPW','R2_C044')][string]$Profile = 'BASELINE',
  [int]$SinceHours = 72,
  [switch]$SessionAuthenticated,
  [switch]$HostedSmokeOnly,
  [string]$VariantMetadata = '',
  [string]$AssertionsPath = ''
)

$ErrorActionPreference = 'Stop'
$CanonicalBlob = 'a166ffb23aba5e6b4011a28d9de8896cd00e33a1'
$CanonicalSha256 = 'ba2e5815d1b221d7bba46ed0be4793aa5bc6154e29e9b19562dfffbd28c8f0bc'
$Schema = 'BBMA_V458_RUNTIME_BUNDLE_V1'

$root = (Resolve-Path $MT4DataPath).Path
$out = [System.IO.Path]::GetFullPath($OutputDir)
$raw = Join-Path $out 'raw'
New-Item -ItemType Directory -Force -Path $raw | Out-Null
$cutoff = (Get-Date).AddHours(-1 * [Math]::Max(1, $SinceHours))

$sourceDirs = @(
  @{ Name='terminal'; Path=(Join-Path $root 'logs') },
  @{ Name='mql4'; Path=(Join-Path $root 'MQL4\Logs') }
)

$copied = @()
foreach ($entry in $sourceDirs) {
  if (-not (Test-Path $entry.Path)) { continue }
  Get-ChildItem -Path $entry.Path -Filter '*.log' -File | Where-Object { $_.LastWriteTime -ge $cutoff } | ForEach-Object {
    $destName = $entry.Name + '__' + $_.Name
    $dest = Join-Path $raw $destName
    Copy-Item $_.FullName $dest -Force
    $copied += $destName
  }
}

if ($copied.Count -eq 0) {
  throw "No MT4 log files found in the requested time window."
}

$variant = $null
if ($VariantMetadata) {
  if (-not (Test-Path $VariantMetadata)) { throw "Variant metadata not found: $VariantMetadata" }
  $variant = Get-Content -Raw $VariantMetadata | ConvertFrom-Json
  if ($variant.canonical_blob -ne $CanonicalBlob) { throw 'Variant metadata canonical blob mismatch.' }
  if ($variant.canonical_sha256 -ne $CanonicalSha256) { throw 'Variant metadata canonical SHA-256 mismatch.' }
  Copy-Item $VariantMetadata (Join-Path $out 'variant_metadata.json') -Force
}

if ($AssertionsPath) {
  if (-not (Test-Path $AssertionsPath)) { throw "Assertions file not found: $AssertionsPath" }
  # Assertions are evidence indexes only; the analyzer still validates required references.
  Copy-Item $AssertionsPath (Join-Path $out 'assertions.json') -Force
}

$combined = ''
foreach ($name in $copied) {
  $p = Join-Path $raw $name
  try { $combined += [System.IO.File]::ReadAllText($p) + "`n" } catch { }
}
$brokerConnected = [bool]($combined -match '\[V458-OBS\]\[ENV\].*Connected=Y')
$observerSeen = [bool]($combined -match '\[V458-OBS\]\[START\]')

$gates = switch ($Profile) {
  'BASELINE'  { @{ d1_tpw = $false; c044 = $false } }
  'R1_D1TPW' { @{ d1_tpw = $true;  c044 = $false } }
  'R2_C044'  { @{ d1_tpw = $false; c044 = $true  } }
}

$manifest = [ordered]@{
  schema = $Schema
  created_utc = (Get-Date).ToUniversalTime().ToString('o')
  profile = $Profile
  canonical_source = [ordered]@{
    path = 'blueprint/source/BBMA_EA.mq4'
    build = 'Version 4.5.8 - D1 TP-Wajib Lifecycle Stage'
    property_version = '4.58'
    blob = $CanonicalBlob
    sha256 = $CanonicalSha256
  }
  expected_gates = $gates
  variant_metadata_present = [bool]$variant
  observer_seen = $observerSeen
  broker_connected = $brokerConnected
  session_authenticated = [bool]$SessionAuthenticated
  hosted_smoke_only = [bool]$HostedSmokeOnly
  log_window_hours = [Math]::Max(1, $SinceHours)
  files = @($copied | Sort-Object)
  privacy = 'Manifest intentionally omits account number/login. Raw MT4 logs may contain broker-generated identifiers.'
}

$manifest | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 (Join-Path $out 'manifest.json')
Write-Host "BUNDLE=$out"
Write-Host "PROFILE=$Profile"
Write-Host "LOG_FILES=$($copied.Count)"
Write-Host "OBSERVER_SEEN=$observerSeen"
Write-Host "BROKER_CONNECTED=$brokerConnected"
Write-Host "SESSION_AUTHENTICATED=$([bool]$SessionAuthenticated)"
Write-Host "HOSTED_SMOKE_ONLY=$([bool]$HostedSmokeOnly)"
