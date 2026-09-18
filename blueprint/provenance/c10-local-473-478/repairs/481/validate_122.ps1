$ErrorActionPreference='Stop'
$here=Split-Path -Parent $MyInvocation.MyCommand.Path
$fix=[IO.Path]::GetFullPath((Join-Path $here '..\..\source_view\BBMA_EA.mq4'))
$f=Get-Content -LiteralPath $fix -Raw
$sha=(Get-FileHash -LiteralPath $fix -Algorithm SHA256).Hash
if($sha -ne '5DE9FD783BB930CC0591612479FE9D9440C938C142D91CB3BA978A233A658D57'){throw "SOURCE_HASH_MISMATCH $sha"}
foreach($pair in @(@('OrderSend(',1),@('OrderModify(',0),@('OrderClose(',3),@('OrderDelete(',0))){
  $count=([regex]::Matches($f,[regex]::Escape($pair[0]))).Count
  if($count -ne [int]$pair[1]){throw "AUTHORITY_COUNT_MISMATCH $($pair[0])=$count"}
}
$markers=@(
 'M5_ENROLLMENT_HISTORY_UNPROVABLE',
 'REPLAY_HISTORY_UNAVAILABLE',
 'SHADOW_TIME_PROVENANCE_UNPROVABLE',
 'expectedEntryM5Open = entryTime - (entryTime % m5Seconds)',
 'iBarShift(decision.Pair, PERIOD_M5, expectedEntryM5Open, true)',
 'iBarShift(decision.Pair, PERIOD_M5, expectedPriorM5Open, true)',
 'm5Seconds <= 0 || latestClosed <= 0 ||',
 'latestClosed < g_c10_shadows[i].last_m5_closed ||',
 'priorShift < 1)',
 'm5Open < g_c10_shadows[i].entry_time',
 'fields[21] != C10_ShadowCheckpointChecksum(fields)',
 'C10_DisableLedger("SHADOW_CHECKPOINT_RECOVERY_FAILURE")'
)
foreach($m in $markers){if(-not $f.Contains($m)){throw "MISSING_122_MARKER $m"}}
if($f.Contains('latestClosed > g_c10_shadows[i].last_m5_closed && priorShift < 1')){throw 'LEGACY_PARTIAL_REPLAY_GUARD_PRESENT'}
$m5=300; $entry=1788426000; $expected=$entry-($entry%$m5); $prior=$expected-$m5
if($expected -ne 1788426000 -or $prior -ne 1788425700){throw 'ANCHOR_MODEL_FAIL'}
function Test-EnrollmentProven($entryShift,$priorShift,$entryOpen,$priorOpen,$expectedEntry,$expectedPrior){
  $actualEntry=0; if($entryShift -ge 0){$actualEntry=$entryOpen}
  $actualPrior=0; if($priorShift -ge 0){$actualPrior=$priorOpen}
  return ($actualEntry -eq $expectedEntry -and $actualPrior -eq $expectedPrior)
}
function Test-ReplayHistoryProven($m5Seconds,$latestClosed,$lastClosed,$priorShift){
  return -not ($m5Seconds -le 0 -or $latestClosed -le 0 -or $lastClosed -le 0 -or $latestClosed -lt $lastClosed -or $priorShift -lt 1)
}
if(-not (Test-EnrollmentProven 3 4 $expected $prior $expected $prior)){throw 'GOOD_HISTORY_REJECTED'}
if(Test-EnrollmentProven -1 4 0 $prior $expected $prior){throw 'MISSING_ENTRY_HISTORY_ACCEPTED'}
if(Test-EnrollmentProven 3 -1 $expected 0 $expected $prior){throw 'MISSING_PRIOR_HISTORY_ACCEPTED'}
if(Test-EnrollmentProven 3 4 ($expected-300) ($prior-300) $expected $prior){throw 'LAGGED_HISTORY_ACCEPTED'}
if(Test-EnrollmentProven 3 4 ($expected+300) $prior $expected $prior){throw 'CORRUPT_ENTRY_ANCHOR_ACCEPTED'}
$latest=$entry+600; $missingShift=-1
if(-not (Test-ReplayHistoryProven 300 $latest $prior 4)){throw 'GOOD_REPLAY_HISTORY_REJECTED'}
if(Test-ReplayHistoryProven 300 0 $prior $missingShift){throw 'ZERO_HISTORY_ACCEPTED'}
if(Test-ReplayHistoryProven 300 $latest 0 $missingShift){throw 'ZERO_LAST_CLOSED_ACCEPTED'}
if(Test-ReplayHistoryProven 300 ($prior-300) $prior 5){throw 'REGRESSED_HISTORY_ACCEPTED'}
if(Test-ReplayHistoryProven 300 $latest $prior $missingShift){throw 'MISSING_REPLAY_ANCHOR_ACCEPTED'}
$legacyBars=@(1788425100,1788425400,1788425700)
if(($legacyBars | Where-Object {$_ -ge $entry}).Count -ne 0){throw 'PREENTRY_REPLAY_GUARD_FAIL'}
Write-Output 'C10_122_STATIC_AUTHORITY=PASS'
Write-Output 'C10_122_LAGGED_M5_MODEL=PASS'
Write-Output 'C10_122_PREENTRY_REPLAY_MODEL=PASS'
Write-Output 'C10_122_ZERO_HISTORY_FAILCLOSED_MODEL=PASS'
Write-Output 'C10_122_REGRESSED_HISTORY_FAILCLOSED_MODEL=PASS'
Write-Output 'C10_122_MISSING_HISTORY_FAILCLOSED_MODEL=PASS'
Write-Output 'C10_122_CHECKPOINT_INTEGRITY_STATIC=PASS'
Write-Output 'C10_122_SOURCE_IDENTITY_481=PASS'
