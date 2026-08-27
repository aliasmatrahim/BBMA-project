param(
  [Parameter(Mandatory=$true)][ValidateSet('BASELINE','R1_D1TPW','R2_C044')][string]$Profile,
  [Parameter(Mandatory=$true)][string[]]$LogPath,
  [Parameter(Mandatory=$true)][string]$OutputDir,
  [switch]$HostedSmokeOnly,
  [switch]$BrokerConnected,
  [switch]$SessionAuthenticated
)

$ErrorActionPreference = 'Stop'
$ExpectedBlob = 'dc83e62748c93171d89a312e9f7a53c06d97e261'
$ExpectedSha = '0a42ee2e6c32810f655b592d8738f500e8b63b4e08c4c874e82452f75ce94b2e'
$BuildMarker = 'Version 4.5.9 - P0 Execution Identity Persistence Fix'
$VersionMarker = '#property version   "4.59"'
$Schema = 'BBMA_V459_RUNTIME_BUNDLE_V1'

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$Source = Join-Path $RepoRoot 'blueprint\source\BBMA_EA.mq4'
if (!(Test-Path $Source)) { throw "Canonical source missing: $Source" }

$Blob = (& git -C $RepoRoot hash-object 'blueprint/source/BBMA_EA.mq4').Trim()
$Sha = (Get-FileHash $Source -Algorithm SHA256).Hash.ToLower()
$Text = Get-Content $Source -Raw
if ($Blob -ne $ExpectedBlob) { throw "Unexpected canonical blob: $Blob" }
if ($Sha -ne $ExpectedSha) { throw "Unexpected canonical SHA256: $Sha" }
if (!$Text.Contains($BuildMarker)) { throw 'v4.59 build marker missing' }
if (!$Text.Contains($VersionMarker)) { throw 'v4.59 property version marker missing' }

$ExpectedGates = switch ($Profile) {
  'BASELINE' { @{ d1_tpw = $false; c044 = $false } }
  'R1_D1TPW' { @{ d1_tpw = $true;  c044 = $false } }
  'R2_C044'  { @{ d1_tpw = $false; c044 = $true  } }
}

$Out = [System.IO.Path]::GetFullPath($OutputDir)
$RawDir = Join-Path $Out 'raw'
New-Item -ItemType Directory -Path $RawDir -Force | Out-Null

$Files = @()
$ObserverSeen = $false
$ConnectedSeen = $false
$Copied = @{}
foreach ($Item in $LogPath) {
  $Resolved = Resolve-Path $Item -ErrorAction Stop
  foreach ($PathInfo in $Resolved) {
    $Full = $PathInfo.Path
    if (!(Test-Path $Full -PathType Leaf)) { continue }
    $Base = [System.IO.Path]::GetFileName($Full)
    $Name = $Base
    $n = 1
    while ($Copied.ContainsKey($Name)) {
      $Stem = [System.IO.Path]::GetFileNameWithoutExtension($Base)
      $Ext = [System.IO.Path]::GetExtension($Base)
      $Name = "$Stem-$n$Ext"
      $n++
    }
    $Copied[$Name] = $true
    $Dest = Join-Path $RawDir $Name
    Copy-Item $Full $Dest -Force
    $Files += $Name
    $LogText = Get-Content $Full -Raw -ErrorAction SilentlyContinue
    if ($LogText -match '\[V459-OBS\]\[START\]') { $ObserverSeen = $true }
    if ($LogText -match '\[V459-OBS\]\[ENV\].*Connected=Y') { $ConnectedSeen = $true }
  }
}
if ($Files.Count -eq 0) { throw 'No runtime log files were collected' }

# Explicit switches remain authoritative. Observer connectivity may only raise
# BrokerConnected when the caller did not mark this as hosted smoke.
$BrokerConnectedValue = [bool]$BrokerConnected
if (!$HostedSmokeOnly -and $ConnectedSeen) { $BrokerConnectedValue = $true }
$SessionAuthenticatedValue = [bool]$SessionAuthenticated

$Manifest = [ordered]@{
  schema = $Schema
  created_utc = [DateTime]::UtcNow.ToString('o')
  profile = $Profile
  canonical_source = [ordered]@{
    path = 'blueprint/source/BBMA_EA.mq4'
    blob = $ExpectedBlob
    sha256 = $ExpectedSha
    build = $BuildMarker
    property_version = '4.59'
  }
  expected_gates = $ExpectedGates
  hosted_smoke_only = [bool]$HostedSmokeOnly
  broker_connected = $BrokerConnectedValue
  session_authenticated = $SessionAuthenticatedValue
  observer_seen = $ObserverSeen
  observer_tag = '[V459-OBS]'
  p0_identity_store = [ordered]@{
    hash_prefix = 'BBXH'
    ticket_prefix = 'BBXT'
    authoritative = 'terminal-global-variables'
    broker_comment = 'fallback-only'
  }
  files = @($Files | Sort-Object)
}
$Manifest | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $Out 'manifest.json') -Encoding UTF8

Write-Host "V459_RUNTIME_BUNDLE=PASS"
Write-Host "PROFILE=$Profile"
Write-Host "FILES=$($Files.Count)"
Write-Host "OBSERVER_SEEN=$ObserverSeen"
Write-Host "BROKER_CONNECTED=$BrokerConnectedValue"
Write-Host "SESSION_AUTHENTICATED=$SessionAuthenticatedValue"
Write-Host "OUTPUT=$Out"
