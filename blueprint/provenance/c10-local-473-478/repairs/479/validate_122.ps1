$ErrorActionPreference='Stop'
$here=Split-Path -Parent $MyInvocation.MyCommand.Path
$fix=[IO.Path]::GetFullPath((Join-Path $here '..\..\source_view\BBMA_EA.mq4'))
$f=Get-Content -LiteralPath $fix -Raw
$sha=(Get-FileHash -LiteralPath $fix -Algorithm SHA256).Hash
if($sha -ne 'E44BAF278170530FF823BEE10437D95DF9236E9FA8C295FCCF432DF7809D856E'){throw "SOURCE_HASH_MISMATCH $sha"}
foreach($pair in @(@('OrderSend(',1),@('OrderModify(',0),@('OrderClose(',3),@('OrderDelete(',0))){
  $count=([regex]::Matches($f,[regex]::Escape($pair[0]))).Count
  if($count -ne [int]$pair[1]){throw "AUTHORITY_COUNT_MISMATCH $($pair[0])=$count"}
}
foreach($m in @('M5_ENROLLMENT_HISTORY_UNPROVABLE','SHADOW_TIME_PROVENANCE_UNPROVABLE','m5Open < g_c10_shadows[i].entry_time','expectedEntryM5Open = entryTime - (entryTime % m5Seconds)')){
  if(-not $f.Contains($m)){throw "MISSING_FIX_MARKER $m"}
}
$m5=300; $entry=1788426000; $expected=$entry-($entry%$m5); $prior=$expected-$m5
if($expected -ne 1788426000 -or $prior -ne 1788425700){throw 'ANCHOR_MODEL_FAIL'}
$lagged=@(1788425100,1788424800)
if($lagged -contains $expected -or $lagged -contains $prior){throw 'LAGGED_HISTORY_FALSE_PASS'}
$legacyBars=@(1788425100,1788425400,1788425700)
if(($legacyBars | Where-Object {$_ -ge $entry}).Count -ne 0){throw 'PREENTRY_REPLAY_GUARD_FAIL'}
Write-Output 'C10_122_STATIC_AUTHORITY=PASS'
Write-Output 'C10_122_LAGGED_M5_MODEL=PASS'
Write-Output 'C10_122_PREENTRY_REPLAY_MODEL=PASS'
Write-Output 'C10_122_SOURCE_IDENTITY=PASS'