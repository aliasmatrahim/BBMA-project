$ErrorActionPreference = 'Stop'

$sourcePath = Join-Path $PSScriptRoot '..\source\BBMA_EA.mq4'
$sourcePath = [System.IO.Path]::GetFullPath($sourcePath)
if (-not (Test-Path $sourcePath)) { throw "EA source not found: $sourcePath" }
$src = Get-Content -LiteralPath $sourcePath -Raw

function Get-ModuleSlice([string]$text, [string]$startMarker, [string]$endMarker) {
    $s = $text.IndexOf($startMarker)
    if ($s -lt 0) { throw "Missing module marker: $startMarker" }
    $e = $text.IndexOf($endMarker, $s + $startMarker.Length)
    if ($e -lt 0) { throw "Missing end module marker: $endMarker" }
    return $text.Substring($s, $e - $s)
}

$m08 = Get-ModuleSlice $src 'MODULE 08: EXTREME DETECTOR' 'MODULE 09:'
$m09 = Get-ModuleSlice $src 'MODULE 09:' 'MODULE 10:'
$m12n = Get-ModuleSlice $src 'MODULE 12N: NESTED MTF JOURNEY ENGINE' 'MODULE 13:'
$m15 = Get-ModuleSlice $src 'MODULE 15: PRIORITY ENGINE' 'MODULE 16:'
$m16 = Get-ModuleSlice $src 'MODULE 16: CONFLICT & INVALIDATION ENGINE' 'MODULE 17:'

# M08 must retain canonical lifecycle writer functions.
foreach ($needle in @('UpdateExtremeLifecycle(', 'ResetExtremeLifecycle(', 'ResolveOppositeExtremeSupersession(')) {
    if (-not $m08.Contains($needle)) { throw "M08 canonical Extreme owner function missing: $needle" }
}

# N3 target invariant: M09 must not privately detect/install/reset canonical Extreme owners.
$forbiddenM09 = @(
    'InstallMHVSupersessionParent(',
    'ResetExtremeLifecycle(parent',
    'DetectExtreme(pair, parentDirection',
    'IsExtremeReversalDirection(data, parentDirection)'
)
foreach ($needle in $forbiddenM09) {
    if ($m09.Contains($needle)) { throw "M09 single-writer violation remains: $needle" }
}

# M09 must still consume canonical parent identity and own MLV state.
foreach ($needle in @('IsMHVParentExtremeMature(', 'ParentConfirmationCandleTime', 'MarkCanonicalMLVSuperseded(', 'AttachCanonicalMHVParent(')) {
    if (-not $m09.Contains($needle)) { throw "M09 canonical-parent consumer invariant missing: $needle" }
}

# Until N3 enforcement is explicitly implemented, M12N stays non-executing infrastructure.
foreach ($needle in @('UpdateNestedJourneyObservation(', 'NMJE_PrintValidatedDecisionShadow(')) {
    if (-not $m12n.Contains($needle)) { throw "NMJE observer/shadow invariant missing: $needle" }
}
foreach ($needle in @('OrderSend(', 'OrderClose(', 'ProcessEntry(', 'RunEntryPreflightAndExecute(')) {
    if ($m12n.Contains($needle)) { throw "NMJE authority leak detected in M12N: $needle" }
}

# M15/M16 authority boundary must remain present.
if (-not $m15.Contains('PriorityEngine_Atomic(')) { throw 'M15 final authority entry point missing' }
if (-not $m16.Contains('InvalidationEngine_Atomic(')) { throw 'M16 revalidation authority entry point missing' }

Write-Host 'NMJE_N3_STATIC_GUARD=PASS'
Write-Host 'M08_CANONICAL_EXTREME_WRITER=PASS'
Write-Host 'M09_EXTREME_SINGLE_WRITER=PASS'
Write-Host 'M12N_NO_EXECUTION_AUTHORITY=PASS'
Write-Host 'M15_M16_AUTHORITY_BOUNDARY=PASS'
