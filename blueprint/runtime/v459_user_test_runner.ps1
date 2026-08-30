param(
  [ValidateSet('PREPARE','RUN','STATUS')][string]$Mode = 'RUN',
  [ValidateSet('AUTO','R1','R2','R3','R4','R5','R6')][string]$Stage = 'AUTO',
  [string]$SettingsPath = (Join-Path $PSScriptRoot 'v459_user_test_settings.json')
)

$ErrorActionPreference = 'Stop'
$ExpectedBlob = 'dc83e62748c93171d89a312e9f7a53c06d97e261'
$ExpectedSha = '0a42ee2e6c32810f655b592d8738f500e8b63b4e08c4c874e82452f75ce94b2e'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$Control = Join-Path $RepoRoot 'blueprint\tools\v459_user_test_control.py'
$Builder = Join-Path $RepoRoot 'blueprint\tools\v459_runtime_variant_builder.py'
$Collector = Join-Path $RepoRoot 'blueprint\runtime\collect_v459_runtime_bundle.ps1'
$Analyzer = Join-Path $RepoRoot 'blueprint\tools\v459_runtime_analyzer.py'
$ObserverSource = Join-Path $RepoRoot 'blueprint\runtime\V459_Runtime_Observer.mq4'

function Invoke-PythonJson([string[]]$Arguments) {
  $lines = & python @Arguments 2>&1
  if ($LASTEXITCODE -ne 0) { throw ($lines -join [Environment]::NewLine) }
  return (($lines -join [Environment]::NewLine) | ConvertFrom-Json)
}

function Assert-CanonicalIdentity {
  $source = Join-Path $RepoRoot 'blueprint\source\BBMA_EA.mq4'
  if (!(Test-Path $source -PathType Leaf)) { throw "Canonical source missing: $source" }
  $blob = (& git -C $RepoRoot hash-object 'blueprint/source/BBMA_EA.mq4').Trim()
  $sha = (Get-FileHash $source -Algorithm SHA256).Hash.ToLower()
  if ($blob -ne $ExpectedBlob) { throw "Canonical v4.59 blob mismatch: $blob" }
  if ($sha -ne $ExpectedSha) { throw "Canonical v4.59 SHA256 mismatch: $sha" }
}

function Get-ControlledTerminalProcesses([string]$TerminalPath) {
  $target = [System.IO.Path]::GetFullPath($TerminalPath)
  return @(Get-CimInstance Win32_Process -Filter "Name='terminal.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.ExecutablePath -and ([System.IO.Path]::GetFullPath($_.ExecutablePath) -ieq $target) })
}

function Compile-Mq4([string]$MetaEditor, [string]$Mq4Path, [string]$LogPath) {
  if (Test-Path $LogPath) { Remove-Item $LogPath -Force }
  & $MetaEditor "/compile:$Mq4Path" "/log:$LogPath"
  if (!(Test-Path $LogPath -PathType Leaf)) { throw "MetaEditor compile log missing: $LogPath" }
  $text = Get-Content $LogPath -Raw
  $matches = [regex]::Matches($text, '(?i)(\d+)\s+errors?,\s*(\d+)\s+warnings?')
  if ($matches.Count -lt 1) { throw "MetaEditor compile summary missing: $LogPath" }
  $last = $matches[$matches.Count - 1]
  $errors = [int]$last.Groups[1].Value
  $warnings = [int]$last.Groups[2].Value
  $ex4 = [System.IO.Path]::ChangeExtension($Mq4Path, '.ex4')
  if ($errors -ne 0 -or $warnings -ne 0 -or !(Test-Path $ex4 -PathType Leaf)) {
    throw "Native compile failed for $Mq4Path ($errors errors, $warnings warnings)"
  }
}

function Install-TestPrograms($Settings, [string]$Profile, [string]$RunDir) {
  $profileKey = switch ($Profile) {
    'R1_D1TPW' { 'r1-d1tpw' }
    'R2_C044'  { 'r2-c044' }
    default    { 'baseline' }
  }
  $expertDir = Join-Path $Settings.data_path 'MQL4\Experts'
  New-Item -ItemType Directory -Path $expertDir -Force | Out-Null
  $ea = Join-Path $expertDir 'BBMA_EA_V459_USERTEST.mq4'
  $meta = Join-Path $RunDir 'variant-metadata.json'
  & python $Builder --repo-root $RepoRoot --profile $profileKey --output $ea --metadata $meta
  if ($LASTEXITCODE -ne 0) { throw "v4.59 variant builder failed for $Profile" }
  $observer = Join-Path $expertDir 'V459_Runtime_Observer.mq4'
  Copy-Item $ObserverSource $observer -Force
  Compile-Mq4 $Settings.metaeditor_path $ea (Join-Path $RunDir 'compile-ea.log')
  Compile-Mq4 $Settings.metaeditor_path $observer (Join-Path $RunDir 'compile-observer.log')
}

function Get-LogFiles($Settings) {
  $files = @()
  foreach ($dir in @((Join-Path $Settings.data_path 'logs'), (Join-Path $Settings.data_path 'MQL4\Logs'))) {
    if (Test-Path $dir -PathType Container) {
      $files += @(Get-ChildItem $dir -Filter '*.log' -File -ErrorAction SilentlyContinue)
    }
  }
  return @($files | Sort-Object FullName -Unique)
}

function Get-LogOffsets($Settings) {
  $offsets = @{}
  foreach ($file in Get-LogFiles $Settings) {
    $offsets[$file.FullName] = @(Get-Content $file.FullName -ErrorAction SilentlyContinue).Count
  }
  return $offsets
}

function Get-NewLogLines($Settings, $Offsets) {
  $rows = @()
  foreach ($file in Get-LogFiles $Settings) {
    $skip = 0
    if ($Offsets.ContainsKey($file.FullName)) { $skip = [int]$Offsets[$file.FullName] }
    $content = @(Get-Content $file.FullName -ErrorAction SilentlyContinue)
    if ($content.Count -gt $skip) { $rows += @($content | Select-Object -Skip $skip) }
  }
  return $rows
}

function Export-NewLogs($Settings, $Offsets, [string]$Destination, [string]$RunId) {
  New-Item -ItemType Directory -Path $Destination -Force | Out-Null
  $written = @()
  $index = 0
  foreach ($file in Get-LogFiles $Settings) {
    $skip = 0
    if ($Offsets.ContainsKey($file.FullName)) { $skip = [int]$Offsets[$file.FullName] }
    $content = @(Get-Content $file.FullName -ErrorAction SilentlyContinue)
    if ($content.Count -le $skip) { continue }
    $index++
    $safe = ($file.BaseName -replace '[^A-Za-z0-9._-]', '_')
    $dest = Join-Path $Destination ("{0}-{1:D2}-{2}.log" -f $RunId, $index, $safe)
    @($content | Select-Object -Skip $skip) | Set-Content $dest -Encoding UTF8
    $written += $dest
  }
  return $written
}

function Scan-NewLogs($Settings, $Offsets, [string]$CurrentStage, [string]$RunDir) {
  $scanFile = Join-Path $RunDir 'live-scan.log'
  @(Get-NewLogLines $Settings $Offsets) | Set-Content $scanFile -Encoding UTF8
  return Invoke-PythonJson @($Control, 'scan', '--stage', $CurrentStage, $scanFile)
}

function Write-StartupIni($Settings, [string]$ProfileName, [string]$Path) {
  $text = @"
[Common]
KeepPrivate=1
NewsEnable=0

[Charts]
Profile=$ProfileName

[Experts]
Enabled=1
AllowLiveTrading=1
AllowDllImport=0
"@
  [System.IO.File]::WriteAllText($Path, $text, [System.Text.Encoding]::ASCII)
}

function Start-TestTerminal($Settings, [string]$IniPath) {
  $args = @('/config:"' + $IniPath + '"')
  if ($Settings.portable_mode) { $args += '/portable' }
  return Start-Process -FilePath $Settings.terminal_path -ArgumentList $args -PassThru
}

function Confirm-DemoPreflight($Settings, $Offsets, [string]$CurrentStage, [string]$RunDir) {
  $ini = Join-Path $RunDir 'mt4-demo-preflight.ini'
  Write-StartupIni $Settings $Settings.preflight_profile $ini
  $process = Start-TestTerminal $Settings $ini
  $deadline = [DateTime]::UtcNow.AddSeconds([int]$Settings.startup_timeout_seconds)
  $confirmed = $false
  try {
    while ([DateTime]::UtcNow -lt $deadline) {
      Start-Sleep -Seconds ([int]$Settings.poll_seconds)
      if ($process.HasExited) { throw 'MT4 exited during observer-only demo preflight' }
      $scan = Scan-NewLogs $Settings $Offsets $CurrentStage $RunDir
      if ($scan.live_account_seen) { throw 'Observer reported Demo=N; trading profile was not opened' }
      if ($scan.observer_seen -and $scan.demo -and $scan.connected -and $scan.trade_allowed) {
        $confirmed = $true
        break
      }
    }
    if (!$confirmed) { throw 'Demo preflight timed out before Demo=Y, Connected=Y and TradeAllowed=Y' }
  }
  finally {
    if (!(Stop-TestTerminal $process ([int]$Settings.clean_shutdown_timeout_seconds))) {
      throw 'MT4 did not close cleanly after demo preflight; force-kill is disabled'
    }
  }
  Write-Host 'V459_OBSERVER_ONLY_DEMO_PREFLIGHT=PASS'
}

function Stop-TestTerminal($Process, [int]$TimeoutSeconds) {
  if (!$Process -or $Process.HasExited) { return $true }
  if (!$Process.CloseMainWindow()) { return $false }
  if (!$Process.WaitForExit($TimeoutSeconds * 1000)) { return $false }
  return $true
}

function Save-State([string]$Path, $State) {
  $State | ConvertTo-Json -Depth 8 | Set-Content $Path -Encoding UTF8
}

function New-DefaultState {
  return [pscustomobject]@{
    schema = 'BBMA_V459_USER_TEST_STATE_V1'
    stages = [pscustomobject]@{
      R1 = [pscustomobject]@{ status='PENDING'; last_report=$null }
      R2 = [pscustomobject]@{ status='PENDING'; last_report=$null }
      R3 = [pscustomobject]@{ status='PENDING'; last_report=$null }
      R4 = [pscustomobject]@{ status='PENDING'; last_report=$null }
      R5 = [pscustomobject]@{ status='PENDING'; last_report=$null }
      R6 = [pscustomobject]@{ status='PENDING'; last_report=$null }
    }
  }
}

if (!(Test-Path $SettingsPath -PathType Leaf)) {
  throw "Settings missing. Copy v459_user_test_settings.example.json to v459_user_test_settings.json first."
}
$SettingsPath = (Resolve-Path $SettingsPath).Path
$Settings = Get-Content $SettingsPath -Raw | ConvertFrom-Json
if ($Settings.require_demo_account -ne $true) { throw 'require_demo_account must remain true' }
$WorkRoot = [System.IO.Path]::GetFullPath($Settings.work_root)
$StatePath = Join-Path $WorkRoot 'state.json'

if ($Mode -eq 'STATUS') {
  if (Test-Path $StatePath) { Get-Content $StatePath -Raw } else { Write-Host 'No user-test run has started.' }
  exit 0
}

$validateArgs = @($Control, 'validate', $SettingsPath)
if ($Mode -eq 'PREPARE') { $validateArgs += '--allow-missing-profiles' }
& python @validateArgs
if ($LASTEXITCODE -ne 0) { throw 'Settings validation failed' }
Assert-CanonicalIdentity
New-Item -ItemType Directory -Path $WorkRoot -Force | Out-Null

if ((Get-ControlledTerminalProcesses $Settings.terminal_path).Count -gt 0) {
  throw 'The dedicated BBMA MT4 terminal is already running. Close it cleanly before PREPARE/RUN.'
}

if ($Mode -eq 'PREPARE') {
  $prepareDir = Join-Path $WorkRoot 'prepare'
  New-Item -ItemType Directory -Path $prepareDir -Force | Out-Null
  Install-TestPrograms $Settings 'BASELINE' $prepareDir
  Write-Host 'V459_USER_TEST_PREPARE=PASS'
  Write-Host 'Next: log in to a DEMO account, create one observer-only preflight profile plus six R1-R6 profiles, then run RUN_BBMA_USER_TESTS.cmd.'
  exit 0
}

$Plan = Invoke-PythonJson @($Control, 'plan', $SettingsPath, $StatePath, '--stage', $Stage)
if ($Plan.stage -eq 'COMPLETE') {
  Write-Host 'V459_USER_TEST_SUITE=PASS'
  Write-Host 'All R1-R6 stages are already PASS.'
  exit 0
}

$CurrentStage = [string]$Plan.stage
$Profile = [string]$Plan.profile
$ProfileName = [string]$Plan.mt4_profile
$RunId = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
$RunDir = Join-Path $WorkRoot ("runs\{0}\{1}" -f $CurrentStage, $RunId)
$EvidenceDir = Join-Path $WorkRoot ("evidence\{0}" -f $CurrentStage)
$BundleDir = Join-Path $RunDir 'bundle'
New-Item -ItemType Directory -Path $RunDir -Force | Out-Null
New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null

Install-TestPrograms $Settings $Profile $RunDir
$Offsets = Get-LogOffsets $Settings
Confirm-DemoPreflight $Settings $Offsets $CurrentStage $RunDir
$Offsets = Get-LogOffsets $Settings
$IniPath = Join-Path $RunDir 'mt4-startup.ini'
Write-StartupIni $Settings $ProfileName $IniPath
$Terminal = Start-TestTerminal $Settings $IniPath
$Restarted = $false
$SafetyConfirmed = $false
$BlockedReason = $null
$Deadline = [DateTime]::UtcNow.AddMinutes([int]$Settings.monitor_minutes)
$StartupDeadline = [DateTime]::UtcNow.AddSeconds([int]$Settings.startup_timeout_seconds)

try {
  while ([DateTime]::UtcNow -lt $Deadline) {
    Start-Sleep -Seconds ([int]$Settings.poll_seconds)
    if ($Terminal.HasExited) {
      $BlockedReason = 'MT4 terminal exited unexpectedly'
      break
    }
    $Scan = Scan-NewLogs $Settings $Offsets $CurrentStage $RunDir
    if ($Scan.live_account_seen) {
      $BlockedReason = 'Observer reported Demo=N; live-account execution is forbidden'
      break
    }
    if (!$SafetyConfirmed -and $Scan.observer_seen -and $Scan.demo -and $Scan.connected -and $Scan.trade_allowed) {
      $SafetyConfirmed = $true
      Write-Host "V459_DEMO_SAFETY=PASS STAGE=$CurrentStage"
    }
    if (!$SafetyConfirmed -and [DateTime]::UtcNow -ge $StartupDeadline) {
      $BlockedReason = 'Timed out waiting for Demo=Y, Connected=Y and TradeAllowed=Y observer evidence'
      break
    }
    if ($SafetyConfirmed -and !$Restarted -and $Settings.auto_restart_on_checkpoint -and
        ($CurrentStage -eq 'R1' -or $CurrentStage -eq 'R2') -and $Scan.checkpoint_seen -and $Scan.open_order_seen) {
      Write-Host "V459_CHECKPOINT=SEEN STAGE=$CurrentStage; starting one clean restart"
      if (!(Stop-TestTerminal $Terminal ([int]$Settings.clean_shutdown_timeout_seconds))) {
        $BlockedReason = 'MT4 did not close cleanly at checkpoint; force-kill is disabled'
        break
      }
      $Terminal = Start-TestTerminal $Settings $IniPath
      $Restarted = $true
    }
  }
}
finally {
  if ($Terminal -and !$Terminal.HasExited) {
    if (!(Stop-TestTerminal $Terminal ([int]$Settings.clean_shutdown_timeout_seconds)) -and !$BlockedReason) {
      $BlockedReason = 'MT4 did not close cleanly; force-kill is disabled'
    }
  }
}

$NewLogs = @(Export-NewLogs $Settings $Offsets $EvidenceDir $RunId)
if ($NewLogs.Count -eq 0 -and !$BlockedReason) { $BlockedReason = 'No new MT4 runtime log lines were captured' }

if ($BlockedReason) {
  $blocked = [ordered]@{ schema='BBMA_V459_USER_TEST_STAGE_REPORT_V1'; stage=$CurrentStage; status='BLOCKED'; reason=$BlockedReason; run_id=$RunId }
  $blockedPath = Join-Path $RunDir 'stage-report.json'
  $blocked | ConvertTo-Json -Depth 6 | Set-Content $blockedPath -Encoding UTF8
  $state = if (Test-Path $StatePath) { Get-Content $StatePath -Raw | ConvertFrom-Json } else { New-DefaultState }
  $state.stages.$CurrentStage.status = 'BLOCKED'
  $state.stages.$CurrentStage.last_report = $blockedPath
  Save-State $StatePath $state
  Write-Host "V459_USER_TEST_STAGE=BLOCKED STAGE=$CurrentStage REASON=$BlockedReason"
  exit 3
}

$AllEvidence = @(Get-ChildItem $EvidenceDir -Filter '*.log' -File | Select-Object -ExpandProperty FullName)
& $Collector -Profile $Profile -LogPath $AllEvidence -OutputDir $BundleDir -BrokerConnected -SessionAuthenticated
if ($LASTEXITCODE -ne 0) { throw 'Runtime bundle collector failed' }
$AnalyzerReport = Join-Path $RunDir 'analyzer-report.json'
& python $Analyzer $BundleDir --output $AnalyzerReport | Out-Null
$AnalyzerExit = $LASTEXITCODE
if ($AnalyzerExit -ne 0 -and $AnalyzerExit -ne 2) { throw 'Runtime analyzer failed unexpectedly' }
$StageReport = Join-Path $RunDir 'stage-report.json'
$Summary = Invoke-PythonJson @($Control, 'summarize', $AnalyzerReport, '--stage', $CurrentStage)
$Summary | ConvertTo-Json -Depth 10 | Set-Content $StageReport -Encoding UTF8

$state = if (Test-Path $StatePath) { Get-Content $StatePath -Raw | ConvertFrom-Json } else { New-DefaultState }
$state.stages.$CurrentStage.status = $Summary.status
$state.stages.$CurrentStage.last_report = $StageReport
Save-State $StatePath $state

$ZipPath = Join-Path $RunDir ("BBMA-V459-{0}-{1}.zip" -f $CurrentStage, $RunId)
Compress-Archive -Path @($BundleDir, $AnalyzerReport, $StageReport, (Join-Path $RunDir 'variant-metadata.json'), (Join-Path $RunDir 'compile-ea.log'), (Join-Path $RunDir 'compile-observer.log')) -DestinationPath $ZipPath -Force
Write-Host "V459_USER_TEST_STAGE=$($Summary.status) STAGE=$CurrentStage"
Write-Host "EVIDENCE_ZIP=$ZipPath"
if ($Summary.status -eq 'FAIL') { exit 2 }
if ($Summary.status -eq 'BLOCKED') { exit 3 }
if ($Summary.status -eq 'INCOMPLETE') { exit 4 }
exit 0
