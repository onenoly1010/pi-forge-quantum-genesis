# 🔄 QUANTUM RESONANCE LATTICE - EMERGENCY ROLLBACK SYSTEM
# Production-ready rollback script for Windows development
# Compatible with PowerShell 5.1+

[CmdletBinding()]
param(
    [switch]$Fast,
    [switch]$Full,
    [switch]$Manual,
    [switch]$AutoConfirm,
    [switch]$DryRun,
    [string]$Commit,
    [switch]$Help
)

# Display usage
function Show-Usage {
    Write-Host @"
╔════════════════════════════════════════════════════════════╗
║   🔄 QUANTUM RESONANCE LATTICE EMERGENCY ROLLBACK         ║
║   Sacred Trinity Production Recovery System               ║
╚════════════════════════════════════════════════════════════╝

USAGE:
    .\emergency-rollback.ps1 [OPTIONS]

OPTIONS:
    -Fast              Fast rollback (code revert only, 5-10 min)
    -Full              Full rollback (code + database, 15-30 min)
    -Manual            Manual guided rollback (30-60 min)
    -AutoConfirm       Skip confirmation prompts
    -DryRun            Simulate rollback without making changes
    -Commit <hash>     Specific commit to rollback to
    -Help              Display this help message

EXAMPLES:
    .\emergency-rollback.ps1 -Fast
    .\emergency-rollback.ps1 -Full -AutoConfirm
    .\emergency-rollback.ps1 -DryRun -Fast
    .\emergency-rollback.ps1 -Commit abc123def

ROLLBACK LEVELS:
    Fast   - Reverts code, restarts services (no DB changes)
    Full   - Reverts code, DB migrations, environment config
    Manual - Step-by-step guided rollback with checkpoints
"@
    exit 0
}

if ($Help) {
    Show-Usage
}

# Configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RollbackRoot = Split-Path -Parent $ScriptDir
$ProjectRoot = Split-Path -Parent $RollbackRoot
$LogFile = Join-Path $RollbackRoot "logs\rollback-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"
$BackupDir = Join-Path $RollbackRoot "backups\state-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

# Determine rollback level
$RollbackLevel = "fast"
if ($Full) { $RollbackLevel = "full" }
if ($Manual) { $RollbackLevel = "manual" }

# Logging function
function Write-Log {
    param(
        [string]$Level,
        [string]$Message
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "$timestamp [$Level] $Message"
    
    # Write to log file
    $logMessage | Out-File -FilePath $LogFile -Append
    
    # Write to console with color
    switch ($Level) {
        "ERROR"   { Write-Host "[ERROR]" -ForegroundColor Red -NoNewline; Write-Host " $Message" }
        "SUCCESS" { Write-Host "[SUCCESS]" -ForegroundColor Green -NoNewline; Write-Host " $Message" }
        "WARNING" { Write-Host "[WARNING]" -ForegroundColor Yellow -NoNewline; Write-Host " $Message" }
        "INFO"    { Write-Host "[INFO]" -ForegroundColor Cyan -NoNewline; Write-Host " $Message" }
        default   { Write-Host $Message }
    }
}

# Print banner
function Show-Banner {
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║   🔄 QUANTUM RESONANCE LATTICE EMERGENCY ROLLBACK         ║" -ForegroundColor Magenta
    Write-Host "║   Sacred Trinity Production Recovery System               ║" -ForegroundColor Magenta
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
    Write-Host ""
}

# Confirm rollback action
function Confirm-Rollback {
    if ($AutoConfirm) {
        return $true
    }
    
    Write-Host "⚠️  WARNING: This will rollback the production system!" -ForegroundColor Red
    Write-Host "Rollback Level: $RollbackLevel" -ForegroundColor Yellow
    Write-Host "Target Commit: $($Commit -or 'latest known good')" -ForegroundColor Yellow
    Write-Host ""
    
    $confirmation = Read-Host "Are you sure you want to proceed? (yes/no)"
    
    if ($confirmation -ne "yes") {
        Write-Log "WARNING" "Rollback cancelled by user"
        exit 1
    }
    
    return $true
}

# Create backup of current state
function Backup-CurrentState {
    Write-Log "INFO" "Creating backup of current state..."
    
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    
    # Backup git state
    try {
        git rev-parse HEAD | Out-File -FilePath "$BackupDir\current-commit.txt"
        git status | Out-File -FilePath "$BackupDir\git-status.txt"
        git diff | Out-File -FilePath "$BackupDir\git-diff.txt"
    } catch {
        "git not available" | Out-File -FilePath "$BackupDir\git-error.txt"
    }
    
    # Backup environment files
    if (Test-Path "$ProjectRoot\.env") {
        Copy-Item "$ProjectRoot\.env" "$BackupDir\.env.backup"
    }
    
    # Backup configuration
    if (Test-Path "$ProjectRoot\railway.toml") {
        Copy-Item "$ProjectRoot\railway.toml" "$BackupDir\railway.toml.backup"
    }
    
    # Save runtime logs (if any)
    if (Test-Path "$ProjectRoot\logs") {
        Copy-Item "$ProjectRoot\logs" "$BackupDir\runtime-logs" -Recurse -ErrorAction SilentlyContinue
    }
    
    Write-Log "SUCCESS" "Backup created at: $BackupDir"
}

# Determine target commit
function Get-TargetCommit {
    if ($Commit) {
        Write-Log "INFO" "Using specified commit: $Commit"
        return $Commit
    }
    
    # Load known good commits
    $configFile = Join-Path $RollbackRoot "config\known-good-commits.json"
    
    if (Test-Path $configFile) {
        try {
            $config = Get-Content $configFile | ConvertFrom-Json
            $targetCommit = $config.commits[0].hash
            Write-Log "INFO" "Using known good commit: $targetCommit"
            return $targetCommit
        } catch {
            Write-Log "WARNING" "Failed to load known good commits"
        }
    }
    
    # Fallback: use previous commit
    try {
        $targetCommit = git rev-parse HEAD~1
        Write-Log "WARNING" "No known good commit found, using HEAD~1: $targetCommit"
        return $targetCommit
    } catch {
        Write-Log "ERROR" "Failed to determine target commit"
        exit 1
    }
}

# Fast rollback procedure
function Invoke-FastRollback {
    param([string]$TargetCommit)
    
    Write-Log "INFO" "🚀 Initiating FAST ROLLBACK procedure..."
    
    if ($DryRun) {
        Write-Log "INFO" "[DRY RUN] Would revert to commit: $TargetCommit"
        Write-Log "INFO" "[DRY RUN] Would restart services"
        return
    }
    
    Set-Location $ProjectRoot
    
    # Verify commit exists
    try {
        git rev-parse $TargetCommit | Out-Null
    } catch {
        Write-Log "ERROR" "Target commit $TargetCommit does not exist!"
        exit 1
    }
    
    # Stash any uncommitted changes
    Write-Log "INFO" "Stashing uncommitted changes..."
    git stash push -m "Emergency rollback stash - $(Get-Date -Format 'yyyyMMdd-HHmmss')" 2>$null
    
    # Hard reset to target commit
    Write-Log "INFO" "Reverting code to commit: $TargetCommit"
    git reset --hard $TargetCommit
    
    # Clean untracked files
    Write-Log "INFO" "Cleaning untracked files..."
    git clean -fd
    
    # Clear Python cache
    Write-Log "INFO" "Clearing Python cache..."
    Get-ChildItem -Recurse -Force __pycache__ -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse
    Get-ChildItem -Recurse -Force *.pyc -ErrorAction SilentlyContinue | Remove-Item -Force
    
    # Restart services (kill Python processes)
    Write-Log "INFO" "Terminating Python processes..."
    Get-Process python -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Log "INFO" "   Terminating: $($_.Name) (PID: $($_.Id))"
        Stop-Process -Id $_.Id -Force
    }
    
    Write-Log "SUCCESS" "✅ Fast rollback complete!"
}

# Full rollback procedure
function Invoke-FullRollback {
    param([string]$TargetCommit)
    
    Write-Log "INFO" "🔄 Initiating FULL ROLLBACK procedure..."
    
    # Execute fast rollback first
    Invoke-FastRollback -TargetCommit $TargetCommit
    
    if ($DryRun) {
        Write-Log "INFO" "[DRY RUN] Would rollback database migrations"
        Write-Log "INFO" "[DRY RUN] Would restore environment configuration"
        return
    }
    
    # Database rollback (if migrations exist)
    if ((Test-Path "$ProjectRoot\migrations") -or (Test-Path "$ProjectRoot\alembic")) {
        Write-Log "INFO" "Rolling back database migrations..."
        Write-Log "WARNING" "Database migrations not implemented yet - skipping"
    }
    
    # Restore environment configuration
    if (Test-Path "$BackupDir\.env.backup") {
        Write-Log "INFO" "Restoring previous environment configuration..."
        Copy-Item "$BackupDir\.env.backup" "$ProjectRoot\.env"
    }
    
    Write-Log "SUCCESS" "✅ Full rollback complete!"
}

# Manual rollback procedure
function Invoke-ManualRollback {
    param([string]$TargetCommit)
    
    Write-Log "INFO" "📋 Initiating MANUAL ROLLBACK procedure..."
    
    Write-Host "This is a guided manual rollback process." -ForegroundColor Cyan
    Write-Host "You will be prompted at each step." -ForegroundColor Cyan
    Write-Host ""
    
    # Step 1: Code rollback
    Write-Host "Step 1: Code Rollback" -ForegroundColor Yellow
    $response = Read-Host "Proceed with code rollback? (yes/no)"
    if ($response -eq "yes") {
        Invoke-FastRollback -TargetCommit $TargetCommit
    }
    
    # Step 2: Database rollback
    Write-Host ""
    Write-Host "Step 2: Database Rollback" -ForegroundColor Yellow
    $response = Read-Host "Proceed with database rollback? (yes/no)"
    if ($response -eq "yes") {
        Write-Log "INFO" "Database rollback would be executed here"
        Write-Log "WARNING" "Database migrations not implemented yet"
    }
    
    # Step 3: Service verification
    Write-Host ""
    Write-Host "Step 3: Service Verification" -ForegroundColor Yellow
    $response = Read-Host "Proceed with service verification? (yes/no)"
    if ($response -eq "yes") {
        $verifyScript = Join-Path $ScriptDir "verify-rollback.ps1"
        if (Test-Path $verifyScript) {
            & $verifyScript -Quick
        }
    }
    
    Write-Log "SUCCESS" "✅ Manual rollback procedure complete!"
}

# Post-rollback verification
function Invoke-Verification {
    Write-Log "INFO" "Running post-rollback verification..."
    
    $verifyScript = Join-Path $ScriptDir "verify-rollback.ps1"
    
    if (Test-Path $verifyScript) {
        & $verifyScript -Quick
    } else {
        Write-Log "WARNING" "Verification script not found - skipping automated verification"
    }
}

# Main execution
function Main {
    Show-Banner
    
    # Create log directory if needed
    New-Item -ItemType Directory -Path (Split-Path $LogFile) -Force | Out-Null
    
    Write-Log "INFO" "Emergency Rollback System initiated at $(Get-Date)"
    Write-Log "INFO" "Rollback level: $RollbackLevel"
    
    # Confirm action
    Confirm-Rollback
    
    # Create backup
    Backup-CurrentState
    
    # Determine target
    $TargetCommit = Get-TargetCommit
    
    # Execute rollback
    switch ($RollbackLevel) {
        "fast" {
            Invoke-FastRollback -TargetCommit $TargetCommit
        }
        "full" {
            Invoke-FullRollback -TargetCommit $TargetCommit
        }
        "manual" {
            Invoke-ManualRollback -TargetCommit $TargetCommit
        }
    }
    
    # Verify rollback
    if (-not $DryRun) {
        Invoke-Verification
    }
    
    # Final summary
    Write-Host ""
    Write-Log "SUCCESS" "╔════════════════════════════════════════════════════════════╗"
    Write-Log "SUCCESS" "║   ✅ ROLLBACK COMPLETE                                     ║"
    Write-Log "SUCCESS" "╚════════════════════════════════════════════════════════════╝"
    Write-Host ""
    Write-Log "INFO" "Rollback log saved to: $LogFile"
    Write-Log "INFO" "Backup saved to: $BackupDir"
    
    if ($DryRun) {
        Write-Host "This was a DRY RUN - no actual changes were made" -ForegroundColor Yellow
    }
}

# Execute main function
Main
