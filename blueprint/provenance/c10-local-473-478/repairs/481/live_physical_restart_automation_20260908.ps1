$ErrorActionPreference='Stop'
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class NtC10Auto481 { [DllImport("ntdll.dll")] public static extern int NtSuspendProcess(IntPtr h); }
'@
$root='C:\Users\Afiq Mat Rahim\Documents\Codex\2026-08-29\teruskan-kerja-ea-yang-tertangguh-tadi\work\c3-mt4-portable-1476-build472'
$exe=Join-Path $root 'terminal.exe'
$cfg='D:\BBMA\c10_live_i81_build481.ini'
$files=Join-Path $root 'MQL4\Files\BBMA_C10'
$cp=Join-Path $files 'bbma_shadow_checkpoint_C10D2_S1_I81.csv'
$runlog='D:\BBMA\c10_live_i81_full_restart_acceptance.log'
$verifier='D:\BBMA\Workspace\c10-build481-worktree\blueprint\provenance\c10-local-473-478\repairs\481\verify_runtime_closure.py'
$expectedBuild='4.81'
$expectedHash='D6B0ADB94BB4EFB2829B33519550D349FABCB8C77251B6477E17489651F2089D'
$deadline=(Get-Date).AddHours(72)
function Log($s){
  $line=([DateTime]::Now.ToString('s')+' '+$s)
  Add-Content $runlog $line
  Write-Output $line
}
function GetIsoProc(){
  Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -eq $exe -and $_.CommandLine -like '*c10_live_i81_build481.ini*'} | Select-Object -First 1
}
function StartIso(){
  $p=Start-Process -FilePath $exe -WorkingDirectory $root -ArgumentList '/portable',$cfg -PassThru
  Log ('START_ISOLATED PID='+$p.Id)
  Start-Sleep -Seconds 8
  return $p
}
function StartIsoFast(){
  $p=Start-Process -FilePath $exe -WorkingDirectory $root -ArgumentList '/portable',$cfg -PassThru
  Log ('START_ISOLATED_FAST PID='+$p.Id)
  return $p
}
function ActiveRow(){
  if(!(Test-Path $cp)){return $null}
  try { return (Import-Csv $cp -ErrorAction Stop | Where-Object {$_.RecordType -eq 'ACTIVE'} | Select-Object -First 1) } catch { return $null }
}
function MqlLogPath(){
  $day=(Get-Date -Format 'yyyyMMdd')
  return (Join-Path $root ('MQL4\Logs\'+$day+'.log'))
}
Log 'AUTOMATION_481_START Build=4.81 InstanceID=81 Authority=NONE ExpertsTrades=false'
$iso=GetIsoProc
if(!$iso){StartIso | Out-Null}
$active=$null
while((Get-Date)-lt $deadline){
  $iso=GetIsoProc
  if(!$iso){
    Log 'ISOLATED_TERMINAL_MISSING_RESTART'
    StartIso | Out-Null
  }
  $active=ActiveRow
  if($active){break}
  Start-Sleep -Milliseconds 100
}
if(!$active){
  Log 'FAIL TIMEOUT_NO_ACTIVE'
  exit 3
}
$pre=$active
if($pre.BuildID -ne $expectedBuild -or $pre.SourceHash -ne $expectedHash){
  Log ('FAIL ACTIVE_IDENTITY_MISMATCH Build='+$pre.BuildID+' Hash='+$pre.SourceHash)
  exit 5
}
$iso=GetIsoProc
$p=Get-Process -Id $iso.ProcessId
[void][NtC10Auto481]::NtSuspendProcess($p.Handle)
$stamp=Get-Date -Format 'yyyyMMdd_HHmmss'
$ev=Join-Path $root ('evidence\C10_481_LIVE_PHYSICAL_RESTART_'+$stamp)
New-Item -ItemType Directory -Force -Path $ev | Out-Null
Copy-Item $cfg (Join-Path $ev 'launch_config.ini') -Force
$setFile=Join-Path $root 'MQL4\Presets\BBMA_C10DB_SHADOW_20PAIR_I81.set'
if(Test-Path $setFile){Copy-Item $setFile (Join-Path $ev 'launch_parameters.set') -Force}
Copy-Item $cp (Join-Path $ev 'checkpoint_pre_restart_ACTIVE.csv') -Force
Get-ChildItem $files -File -ErrorAction SilentlyContinue | Copy-Item -Destination $ev -Force
$did=$pre.DecisionID
$identity=@(
  ('DecisionID='+$did),
  ('BuildID='+$pre.BuildID),
  ('SourceHash='+$pre.SourceHash),
  ('ConfigFingerprint='+$pre.ConfigFingerprint),
  'InstanceID=81',
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
Log ('PHYSICAL_RESTART PID='+$restart.Id)
$postMatch=$false
$recoverySeen=$false
$readySeen=$false
$postDeadline=(Get-Date).AddSeconds(60)
while((Get-Date)-lt $postDeadline){
  if(Test-Path $cp){
    $rows=Import-Csv $cp -ErrorAction SilentlyContinue
    $r=$rows | Where-Object {$_.DecisionID -eq $did -and $_.RecordType -eq 'ACTIVE'} | Select-Object -First 1
    if($r -and !$postMatch){
      $postMatch=$true
      Copy-Item $cp (Join-Path $ev 'checkpoint_post_restart.csv') -Force
    }
  }
  $mqlLog=MqlLogPath
  if(Test-Path $mqlLog){
    $all=Get-Content $mqlLog -ErrorAction SilentlyContinue
    $post=@($all | Select-Object -Skip $preRestartLines)
    $postText=$post -join "`n"
    if($postText -match '\[C10\]\[SHADOW_RECOVERY\] Active=1'){$recoverySeen=$true}
    $readyRegex='\[C10\]\[READY\].*Config='+[regex]::Escape($pre.ConfigFingerprint)+'.*Authority=NONE'
    if($postText -match $readyRegex){$readySeen=$true}
  }
  if($postMatch){break}
  Start-Sleep -Milliseconds 100
}
if(!$postMatch){
  Log 'FAIL POST_RESTART_ACTIVE_NOT_RECOVERED'
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
Get-ChildItem $files -File -ErrorAction SilentlyContinue | Copy-Item -Destination $ev -Force
if(!(Test-Path (Join-Path $ev 'mql4_post_restart.log'))){
  Set-Content (Join-Path $ev 'mql4_post_restart.log') ''
}
$verifyOut=Join-Path $ev 'verifier_stdout.txt'
& 'C:\WINDOWS\py.exe' -3.12 $verifier $ev --json 2>&1 | Tee-Object -FilePath $verifyOut
$verifyCode=$LASTEXITCODE
if($verifyCode -eq 0){
  Set-Content 'D:\BBMA\C10_481_LIVE_PHYSICAL_RESTART_PASS.flag' $ev
  Remove-Item 'D:\BBMA\C10_481_LIVE_PHYSICAL_RESTART_FAIL.flag' -Force -ErrorAction SilentlyContinue
  Log ('FINAL_RESULT=PASS Evidence='+$ev)
  exit 0
}
Set-Content 'D:\BBMA\C10_481_LIVE_PHYSICAL_RESTART_FAIL.flag' $ev
Remove-Item 'D:\BBMA\C10_481_LIVE_PHYSICAL_RESTART_PASS.flag' -Force -ErrorAction SilentlyContinue
Log ('FINAL_RESULT=FAIL VerifierExit='+$verifyCode+' Evidence='+$ev)
exit 4
