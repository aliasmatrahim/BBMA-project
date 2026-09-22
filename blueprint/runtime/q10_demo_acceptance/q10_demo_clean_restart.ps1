param(
    [Parameter(Mandatory=$true)][string]$TerminalPath,
    [Parameter(Mandatory=$true)][string]$ConfigPath,
    [Parameter(Mandatory=$true)][string]$EvidenceDir,
    [Parameter(Mandatory=$true)][string]$StatePath,
    [string]$PrimaryTerminalPath = "",
    [int]$GraceSeconds = 30,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Fail-Closed([string]$Reason) {
    $result = [ordered]@{
        schema = "BBMA_Q10_CLEAN_RESTART_V1"
        status = "BLOCKED"
        reason = $Reason
        terminal = $TerminalPath
        config = $ConfigPath
        dry_run = [bool]$DryRun
    }
    $result | ConvertTo-Json -Depth 6
    exit 2
}

function Sha256([string]$Path) {
    if(!(Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
}

function Snapshot-Logs([string]$TerminalRoot, [string]$Destination, [string]$Label) {
    $records = @()
    $dirs = @(
        (Join-Path $TerminalRoot "logs"),
        (Join-Path $TerminalRoot "MQL4\Logs")
    )
    foreach($dir in $dirs) {
        if(!(Test-Path -LiteralPath $dir -PathType Container)) { continue }
        $files = Get-ChildItem -LiteralPath $dir -File -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 12
        foreach($f in $files) {
            $records += [ordered]@{
                label = $Label
                path = $f.FullName
                bytes = $f.Length
                last_write = $f.LastWriteTime.ToString("o")
                sha256 = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash
            }
        }
    }
    if(!$DryRun) {
        New-Item -ItemType Directory -Force -Path $Destination | Out-Null
        $records | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Destination ($Label + "_logs.json")) -Encoding UTF8
    }
    return ,$records
}

$terminal = [IO.Path]::GetFullPath($TerminalPath)
$config = [IO.Path]::GetFullPath($ConfigPath)
$root = Split-Path -Parent $terminal

if(!(Test-Path -LiteralPath $terminal -PathType Leaf)) {
    Fail-Closed "TERMINAL_MISSING"
}
if(!(Test-Path -LiteralPath $config -PathType Leaf)) {
    Fail-Closed "CONFIG_MISSING"
}
if(!(Test-Path -LiteralPath $StatePath -PathType Leaf)) {
    Fail-Closed "STATE_MISSING"
}
$state = Get-Content -LiteralPath $StatePath -Raw | ConvertFrom-Json
if(!$state.demo_auth -or $state.demo_auth.status -ne "PASS") {
    Fail-Closed "DEMO_AUTH_NOT_PASS"
}
if(!$state.candidate -or $state.candidate.status -ne "PASS") {
    Fail-Closed "CANDIDATE_NOT_PASS"
}
if($state.runtime_artifacts -and $state.runtime_artifacts.terminal) {
    $stateTerminal = [IO.Path]::GetFullPath([string]$state.runtime_artifacts.terminal)
    if(![string]::Equals($terminal, $stateTerminal, [StringComparison]::OrdinalIgnoreCase)) {
        Fail-Closed "STATE_TERMINAL_MISMATCH"
    }
}
if($GraceSeconds -lt 5 -or $GraceSeconds -gt 300) {
    Fail-Closed "GRACE_SECONDS_OUT_OF_RANGE"
}
if($PrimaryTerminalPath) {
    $primary = [IO.Path]::GetFullPath($PrimaryTerminalPath)
    if([string]::Equals($terminal, $primary, [StringComparison]::OrdinalIgnoreCase)) {
        Fail-Closed "DEDICATED_EQUALS_PRIMARY"
    }
}

$configText = Get-Content -LiteralPath $config -Raw
if($configText -match '(?im)^\s*(Login|Password)\s*=') {
    Fail-Closed "CREDENTIAL_FIELD_PRESENT"
}

$running = @(Get-CimInstance Win32_Process -Filter "Name='terminal.exe'" |
    Where-Object {
        $_.ExecutablePath -and
        [string]::Equals([IO.Path]::GetFullPath($_.ExecutablePath), $terminal, [StringComparison]::OrdinalIgnoreCase)
    })

if($running.Count -gt 1) {
    Fail-Closed "MULTIPLE_DEDICATED_TERMINALS"
}

$evidence = [IO.Path]::GetFullPath($EvidenceDir)
$plan = [ordered]@{
    schema = "BBMA_Q10_CLEAN_RESTART_V1"
    status = "READY"
    terminal = $terminal
    config = $config
    config_sha256 = (Sha256 $config)
    evidence_dir = $evidence
    state_path = [IO.Path]::GetFullPath($StatePath)
    state_sha256 = (Sha256 $StatePath)
    grace_seconds = $GraceSeconds
    existing_pids = @($running | ForEach-Object { $_.ProcessId })
    close_method = "CloseMainWindow"
    force_kill = $false
    credentials_in_config = $false
    dry_run = [bool]$DryRun
}

if($DryRun) {
    $plan | ConvertTo-Json -Depth 6
    exit 0
}

New-Item -ItemType Directory -Force -Path $evidence | Out-Null
$before = Snapshot-Logs $root $evidence "pre_restart"

if($running.Count -eq 1) {
    $pidToClose = [int]$running[0].ProcessId
    $process = Get-Process -Id $pidToClose -ErrorAction Stop

    $requested = $process.CloseMainWindow()
    if(!$requested) {
        Fail-Closed "GRACEFUL_CLOSE_NOT_ACCEPTED"
    }

    $deadline = (Get-Date).AddSeconds($GraceSeconds)
    while((Get-Date) -lt $deadline) {
        Start-Sleep -Milliseconds 500
        if(!(Get-Process -Id $pidToClose -ErrorAction SilentlyContinue)) { break }
    }

    if(Get-Process -Id $pidToClose -ErrorAction SilentlyContinue) {
        # Deliberately no forced-termination fallback.
        # Evidence flushing cannot be proven after a forced kill, so fail closed.
        Fail-Closed "GRACEFUL_CLOSE_TIMEOUT"
    }
}

# Snapshot only after the process is fully gone so MT4 has had a chance to flush logs.
$afterClose = Snapshot-Logs $root $evidence "post_close"

$stillRunning = @(Get-CimInstance Win32_Process -Filter "Name='terminal.exe'" |
    Where-Object {
        $_.ExecutablePath -and
        [string]::Equals([IO.Path]::GetFullPath($_.ExecutablePath), $terminal, [StringComparison]::OrdinalIgnoreCase)
    })
if($stillRunning.Count -ne 0) {
    Fail-Closed "DEDICATED_PROCESS_STILL_PRESENT"
}

$proc = Start-Process -FilePath $terminal -WorkingDirectory $root -ArgumentList @("/portable", $config) -PassThru
Start-Sleep -Seconds 2
if(!(Get-Process -Id $proc.Id -ErrorAction SilentlyContinue)) {
    Fail-Closed "RESTART_PROCESS_EXITED_EARLY"
}

$record = [ordered]@{
    schema = "BBMA_Q10_CLEAN_RESTART_V1"
    status = "PASS"
    terminal = $terminal
    config = $config
    config_sha256 = (Sha256 $config)
    evidence_dir = $evidence
    state_path = [IO.Path]::GetFullPath($StatePath)
    state_sha256 = (Sha256 $StatePath)
    previous_pids = $plan.existing_pids
    new_pid = $proc.Id
    close_method = "CloseMainWindow"
    force_kill = $false
    credentials_in_config = $false
    pre_restart_log_count = @($before).Count
    post_close_log_count = @($afterClose).Count
}
$record | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $evidence "restart_result.json") -Encoding UTF8
$record | ConvertTo-Json -Depth 6
exit 0
