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

foreach ($needle in @('UpdateExtremeLifecycle(', 'ResetExtremeLifecycle(', 'ResolveOppositeExtremeSupersession(')) {
    if (-not $m08.Contains($needle)) { throw "M08 canonical Extreme owner function missing: $needle" }
}

$forbiddenM09 = @(
    'InstallMHVSupersessionParent(',
    'ResetExtremeLifecycle(parent',
    'DetectExtreme(pair, parentDirection',
    'IsExtremeReversalDirection(data, parentDirection)'
)
foreach ($needle in $forbiddenM09) {
    if ($m09.Contains($needle)) { throw "M09 single-writer violation remains: $needle" }
}

foreach ($needle in @('IsMHVParentExtremeMature(', 'ParentConfirmationCandleTime', 'MarkCanonicalMLVSuperseded(', 'AttachCanonicalMHVParent(')) {
    if (-not $m09.Contains($needle)) { throw "M09 canonical-parent consumer invariant missing: $needle" }
}

foreach ($needle in @(
    'string               CanonicalEventID;',
    'NMJE_ReEntryEventID(',
    'NMJE_ExtremeEventID(',
    'NMJE_MLVEventID(',
    'NMJE_D1OwnerEventID(',
    'NMJE_H4OwnerEventID('
)) {
    if (-not $src.Contains($needle)) { throw "Canonical event identity invariant missing: $needle" }
}
foreach ($forbidden in @('MathRand(', 'GetTickCount(', 'TimeCurrent()')) {
    if ($m12n.Contains($forbidden) -and $m12n.Contains('EventID')) {
        throw "Non-deterministic identity input detected in M12N: $forbidden"
    }
}

foreach ($needle in @('UpdateNestedJourneyObservation(', 'NMJE_PrintValidatedDecisionShadow(')) {
    if (-not $m12n.Contains($needle)) { throw "NMJE observer/shadow invariant missing: $needle" }
}
foreach ($needle in @('OrderSend(', 'OrderClose(', 'ProcessEntry(', 'RunEntryPreflightAndExecute(')) {
    if ($m12n.Contains($needle)) { throw "NMJE authority leak detected in M12N: $needle" }
}

if (-not $m15.Contains('PriorityEngine_Atomic(')) { throw 'M15 final authority entry point missing' }
if (-not $m16.Contains('InvalidationEngine_Atomic(')) { throw 'M16 revalidation authority entry point missing' }

# Step-4 shadow provenance may be frozen and compared, but it must not yet gate execution.
foreach ($needle in @('NMJESnapshotPresent', 'FreezeNMJEShadowSnapshot(', 'ValidateNMJEShadowSnapshot(')) {
    if (-not $src.Contains($needle)) { throw "N3 shadow provenance invariant missing: $needle" }
}
if (-not $m16.Contains('[N3-NMJE-SHADOW][M16]')) { throw 'N3 M16 shadow diagnostic missing' }

# Guard against accidental enforcement before explicit N3 activation work.
foreach ($needle in @('REJ_NMJE', 'EnableNMJEExecutionGate', 'EnableNestedExecutionGate', 'N3_POLICY_ACTIVE')) {
    if ($src.Contains($needle)) { throw "Unapproved N3 execution authority marker found: $needle" }
}

$shadowCall = 'ValidateNMJEShadowSnapshot(pairIndex, decision'
$shadowPos = $m16.IndexOf($shadowCall)
if ($shadowPos -lt 0) { throw 'N3 shadow validation call missing from M16' }
$shadowTailLen = [Math]::Min(1800, $m16.Length - $shadowPos)
$shadowTail = $m16.Substring($shadowPos, $shadowTailLen)
if ($shadowTail.Contains('DEC_INVALIDATED') -or $shadowTail.Contains('DEC_REJECTED') -or $shadowTail.Contains('DEC_EXPIRED')) {
    throw 'N3 shadow result is too close to rejection state mutation; inspect authority leakage'
}

Write-Host 'NMJE_N3_STATIC_GUARD=PASS'
Write-Host 'M08_CANONICAL_EXTREME_WRITER=PASS'
Write-Host 'M09_EXTREME_SINGLE_WRITER=PASS'
Write-Host 'CANONICAL_EVENT_IDENTITY=PASS'
Write-Host 'M12N_NO_EXECUTION_AUTHORITY=PASS'
Write-Host 'M15_M16_AUTHORITY_BOUNDARY=PASS'
Write-Host 'N3_SHADOW_PROVENANCE_NO_GATE=PASS'
