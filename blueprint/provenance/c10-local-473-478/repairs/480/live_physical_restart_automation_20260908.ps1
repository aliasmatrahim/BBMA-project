$ErrorActionPreference='Stop'
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class NtC10AutoV2 { [DllImport("ntdll.dll")] public static extern int NtSuspendProcess(IntPtr h); }
'@
$root='C:\Users\Afiq Mat Rahim\Documents\Codex\2026-08-29\teruskan-kerja-ea-yang-tertangguh-tadi\work\c3-mt4-portable-1476-build472'
$exe=Join-Path $root 'terminal.exe'
$cfg='D:\BBMA\c10_live_i80.ini'
$files=Join-Path $root 'MQL4\Files\BBMA_C10'
$cp=Join-Path $files 'bbma_shadow_checkpoint_C10D2_S1_I80.csv'
$runlog='D:\BBMA\c10_live_i80_full_restart_acceptance_v2.log'
$verifier='D:\BBMA\Workspace\c10-build480-worktree\blueprint\provenance\c10-local-473-478\repairs\480\verify_runtime_closure.py'
$expectedBuild='4.80'
$expectedHash='5C672778E35AA2602702824778F8F7F6EE4BCDCDFB99B7E32679A17CC0DA2DC6'
$deadline=(Get-Date).AddHours(24)
function Log($s){
  $line=([DateTime]::Now.ToString('s')+' '+$s)
  Add-Content $runlog $line
  Write-Output $line
}
function GetIsoProc(){
  Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -eq $exe} | Select-Object -First 1
}
function StartIso(){
  $p=Start-Process -FilePath $exe -WorkingDirectory $root -ArgumentList '/portable',$cfg -PassThru
  Log ('START_ISOLATED PID='+$p.Id)
  Start-Sleep -Seconds 8
  return $p
}function StartIsoFast(){
  $p=Start-Process -FilePath $exe -WorkingDirectory $root -ArgumentList '/portable',$cfg -PassThru
  Log ('START_ISOLATED_FAST PID='+$p.Id)
  return $p
}
function ActiveLine(){
  if(!(Test-Path $cp)){return $null}
  $line=Get-Content $cp -ErrorAction SilentlyContinue | Where-Object {$_ -match ',"ACTIVE",'} | Select-Object -First 1
  return $line
}
function MqlLogPath(){
  $day=(Get-Date -Format 'yyyyMMdd')
  return (Join-Path $root ('MQL4\Logs\'+$day+'.log'))
}
Log 'AUTOMATION_V2_START Build=4.80 InstanceID=80 Authority=NONE ExpertsTrades=false'
$iso=GetIsoProc
if(!$iso){StartIso | Out-Null}
$active=$null
while((Get-Date)-lt $deadline){
  $iso=GetIsoProc
  if(!$iso){
    Log 'ISOLATED_TERMINAL_MISSING_RESTART'
    StartIso | Out-Null
  }
  $active=ActiveLine
  if($active){break}
  Start-Sleep -Milliseconds 100
}
if(!$active){
  Log 'FAIL TIMEOUT_NO_ACTIVE'
  exit 3
}
$pre=ConvertFrom-Csv $active
if($pre.BuildID -ne $expectedBuild -or $pre.SourceHash -ne $expectedHash){
  Log ('FAIL ACTIVE_IDENTITY_MISMATCH Build='+$pre.BuildID+' Hash='+$pre.SourceHash)
  exit 5
}$iso=GetIsoProc
$p=Get-Process -Id $iso.ProcessId
[void][NtC10AutoV2]::NtSuspendProcess($p.Handle)
$stamp=Get-Date -Format 'yyyyMMdd_HHmmss'
$ev=Join-Path $root ('evidence\C10_480_LIVE_PHYSICAL_RESTART_'+$stamp)
New-Item -ItemType Directory -Force -Path $ev | Out-Null
Copy-Item $cfg (Join-Path $ev 'launch_config.ini') -Force
$setFile=Join-Path $root 'MQL4\Presets\BBMA_C10DB_SHADOW_20PAIR_I80.set'
if(Test-Path $setFile){Copy-Item $setFile (Join-Path $ev 'launch_parameters.set') -Force}
Copy-Item $cp (Join-Path $ev 'checkpoint_pre_restart_ACTIVE.csv') -Force
Get-ChildItem $files -File -ErrorAction SilentlyContinue | Copy-Item -Destination $ev -Force
$did=$pre.DecisionID
$identity=@(
  ('DecisionID='+$did),
  ('BuildID='+$pre.BuildID),
  ('SourceHash='+$pre.SourceHash),
  ('ConfigFingerprint='+$pre.ConfigFingerprint),
  'InstanceID=80',
  'Authority=NONE',
  'ExpertsTrades=false'
)
Set-Content (Join-Path $ev 'identity.txt') $identity
Log ('ACTIVE_CAPTURED DecisionID='+$did+' PID='+$iso.ProcessId+' Evidence='+$ev)
Stop-Process -Id $iso.ProcessId -Force
Start-Sleep -Seconds 4
$mqlLog=MqlLogPath
$preRestartLines=0
if(Test-Path $mqlLog){
  Copy-Item $mqlLog (Join-Path $ev 'mql4_pre_restart.log') -Force
  $preRestartLines=(Get-Content $mqlLog -ErrorAction SilentlyContinue).Count
}
Set-Content (Join-Path $ev 'pre_restart_log_line_count.txt') $preRestartLines
$restart=StartIsoFast
Log ('PHYSICAL_RESTART PID='+$restart.Id)$postMatch=$false
$postDeadline=(Get-Date).AddSeconds(45)
while((Get-Date)-lt $postDeadline){
  if(Test-Path $cp){
    $rows=Import-Csv $cp -ErrorAction SilentlyContinue
    $r=$rows | Where-Object {$_.DecisionID -eq $did -and $_.RecordType -eq 'ACTIVE'} | Select-Object -First 1
    if($r){
      $postMatch=$true
      Copy-Item $cp (Join-Path $ev 'checkpoint_post_restart.csv') -Force
      break
    }
  }
  Start-Sleep -Milliseconds 100
}
if(!$postMatch){
  Log 'FAIL POST_RESTART_EXACT_ACTIVE_NOT_FOUND'
  $rp=GetIsoProc
  if($rp){Stop-Process -Id $rp.ProcessId -Force}
  exit 6
}
Start-Sleep -Seconds 8
$rp=GetIsoProc
if($rp){Stop-Process -Id $rp.ProcessId -Force}
Start-Sleep -Seconds 4
$mqlLog=MqlLogPath
if(Test-Path $mqlLog){
  Copy-Item $mqlLog (Join-Path $ev 'mql4_runtime.log') -Force
  $all=Get-Content $mqlLog -ErrorAction SilentlyContinue
  $post=@($all | Select-Object -Skip $preRestartLines)
  Set-Content (Join-Path $ev 'mql4_post_restart.log') $post
}
Get-ChildItem $files -File -ErrorAction SilentlyContinue | Copy-Item -Destination $ev -Forceif(!(Test-Path (Join-Path $ev 'mql4_post_restart.log'))){
  Set-Content (Join-Path $ev 'mql4_post_restart.log') ''
}
$verifyOut=Join-Path $ev 'verifier_stdout.txt'
& 'C:\WINDOWS\py.exe' -3.12 $verifier $ev --json 2>&1 | Tee-Object -FilePath $verifyOut
$verifyCode=$LASTEXITCODE
if($verifyCode -eq 0){
  Set-Content 'D:\BBMA\C10_480_LIVE_PHYSICAL_RESTART_PASS.flag' $ev
  Remove-Item 'D:\BBMA\C10_480_LIVE_PHYSICAL_RESTART_FAIL.flag' -Force -ErrorAction SilentlyContinue
  Log ('FINAL_RESULT=PASS Evidence='+$ev)
  exit 0
}
Set-Content 'D:\BBMA\C10_480_LIVE_PHYSICAL_RESTART_FAIL.flag' $ev
Remove-Item 'D:\BBMA\C10_480_LIVE_PHYSICAL_RESTART_PASS.flag' -Force -ErrorAction SilentlyContinue
Log ('FINAL_RESULT=FAIL VerifierExit='+$verifyCode+' Evidence='+$ev)
exit 4
