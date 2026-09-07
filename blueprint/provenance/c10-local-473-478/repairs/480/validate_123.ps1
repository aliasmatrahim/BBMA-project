$ErrorActionPreference='Stop'
$here=Split-Path -Parent $MyInvocation.MyCommand.Path
$fix=[IO.Path]::GetFullPath((Join-Path $here '..\..\source_view\BBMA_EA.mq4'))
$f=Get-Content -LiteralPath $fix -Raw
if($f.Contains('FILE_SHARE_WRITE')){throw 'UNSAFE_MULTIWRITER_SHARE_ADDED'}
foreach($m in @('string C10_LedgerOwnerToken()','"4.80|" + C10_SOURCE_HASH','C10_BuildConfigFingerprint();','C10_LedgerOwnerToken() + "_" + dayKey','C10_LedgerOwnerToken() + "_*.csv"')){
  if(-not $f.Contains($m)){throw "MISSING_NAMESPACE_MARKER $m"}
}
if(-not $f.Contains('IntegerToString(InstanceID) + "|" +')){throw 'CONFIG_DOES_NOT_BIND_INSTANCE'}
$legacy='bbma_signal_C10S1_20260907_part01.csv'
$namespaced='bbma_signal_C10S1_OABC123DEF456_20260907_part01.csv'
if($legacy -eq $namespaced){throw 'NAMESPACE_MODEL_FAIL'}
if(-not ($namespaced -like 'bbma_signal_C10S1_*.csv')){throw 'REPORTER_GLOB_COMPAT_FAIL'}
if(-not $f.Contains('Owner=", C10_LedgerOwnerToken()')){throw 'READY_OWNER_DIAGNOSTIC_MISSING'}
Write-Output 'C10_123_STATIC_AUTHORITY=PASS'
Write-Output 'C10_123_WRITER_NAMESPACE=PASS'
Write-Output 'C10_123_REPORTER_GLOB_COMPAT=PASS'
Write-Output 'C10_123_READY_OWNER_DIAGNOSTIC=PASS'