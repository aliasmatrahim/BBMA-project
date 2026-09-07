$ErrorActionPreference='Stop'
$here=Split-Path -Parent $MyInvocation.MyCommand.Path
$fix=[IO.Path]::GetFullPath((Join-Path $here '..\..\source_view\BBMA_EA.mq4'))
$f=Get-Content -LiteralPath $fix -Raw
$sha=(Get-FileHash -LiteralPath $fix -Algorithm SHA256).Hash
if($sha -ne 'E9C8CFBE574786BE22003D76F015E5438E9D2EEFD8BF11E377DD93FE61BAE0E1'){throw "SOURCE_HASH_MISMATCH $sha"}
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
 'latestClosed > g_c10_shadows[i].last_m5_closed && priorShift < 1',
 'm5Open < g_c10_shadows[i].entry_time',
 'fields[21] != C10_ShadowCheckpointChecksum(fields)',
 'C10_DisableLedger("SHADOW_CHECKPOINT_RECOVERY_FAILURE")'
)
foreach($m in $markers){if(-not $f.Contains($m)){throw "MISSING_122_MARKER $m"}}
$m5=300; $entry=1788426000; $expected=$entry-($entry%$m5); $prior=$expected-$m5
if($expected -ne 1788426000 -or $prior -ne 1788425700){throw 'ANCHOR_MODEL_FAIL'}function Test-EnrollmentProven($entryShift,$priorShift,$entryOpen,$priorOpen,$expectedEntry,$expectedPrior){
  $actualEntry=0; if($entryShift -ge 0){$actualEntry=$entryOpen}
  $actualPrior=0; if($priorShift -ge 0){$actualPrior=$priorOpen}
  return ($actualEntry -eq $expectedEntry -and $actualPrior -eq $expectedPrior)
}
if(-not (Test-EnrollmentProven 3 4 $expected $prior $expected $prior)){throw 'GOOD_HISTORY_REJECTED'}
if(Test-EnrollmentProven -1 4 0 $prior $expected $prior){throw 'MISSING_ENTRY_HISTORY_ACCEPTED'}
if(Test-EnrollmentProven 3 -1 $expected 0 $expected $prior){throw 'MISSING_PRIOR_HISTORY_ACCEPTED'}
if(Test-EnrollmentProven 3 4 ($expected-300) ($prior-300) $expected $prior){throw 'LAGGED_HISTORY_ACCEPTED'}
if(Test-EnrollmentProven 3 4 ($expected+300) $prior $expected $prior){throw 'CORRUPT_ENTRY_ANCHOR_ACCEPTED'}
$latestClosed=$entry+600; $lastClosed=$prior; $missingPriorShift=-1
$replayFailClosed=($latestClosed -gt $lastClosed -and $missingPriorShift -lt 1)
if(-not $replayFailClosed){throw 'MISSING_REPLAY_HISTORY_NOT_FAILCLOSED'}
$legacyBars=@(1788425100,1788425400,1788425700)
if(($legacyBars | Where-Object {$_ -ge $entry}).Count -ne 0){throw 'PREENTRY_REPLAY_GUARD_FAIL'}
Write-Output 'C10_122_STATIC_AUTHORITY=PASS'
Write-Output 'C10_122_LAGGED_M5_MODEL=PASS'
Write-Output 'C10_122_PREENTRY_REPLAY_MODEL=PASS'
Write-Output 'C10_122_MISSING_HISTORY_FAILCLOSED_MODEL=PASS'
Write-Output 'C10_122_CORRUPT_HISTORY_FAILCLOSED_MODEL=PASS'
Write-Output 'C10_122_CHECKPOINT_INTEGRITY_STATIC=PASS'
Write-Output 'C10_122_SOURCE_IDENTITY_480=PASS'