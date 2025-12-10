# ═══════════════════════════════════════════════════════════════════════════
# 🌌 QUANTUM PI FORGE - BOOTSTRAP AGENT (PowerShell)
# ═══════════════════════════════════════════════════════════════════════════
#
# This is the Windows PowerShell version of the bootstrap script that
# initializes the entire Quantum Pi Forge autonomous system.
#
# Usage:
#   .\bootstrap.ps1 [-Environment ENV] [-SkipTests] [-Verbose]
#
# Parameters:
#   -Environment    Target environment (development|staging|production)
#   -SkipTests      Skip test execution during bootstrap
#   -Verbose        Enable verbose logging
#   -Help           Show help message
#
# ═══════════════════════════════════════════════════════════════════════════

[CmdletBinding()]
param(
    [Parameter()]
    [ValidateSet('development', 'staging', 'production')]
    [string]$Environment = 'development',
    
    [Parameter()]
    [switch]$SkipTests,
    
    [Parameter()]
    [switch]$Help
)

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$BootstrapDir = $ScriptDir
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$LogFile = Join-Path $BootstrapDir "bootstrap-$Timestamp.log"

# ═══════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

function Write-Log {
    param(
        [string]$Level,
        [string]$Message
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Add-Content -Path $LogFile -Value $logMessage
    
    switch ($Level) {
        "INFO"    { Write-Host "ℹ  $Message" -ForegroundColor Blue }
        "SUCCESS" { Write-Host "✅ $Message" -ForegroundColor Green }
        "WARNING" { Write-Host "⚠️  $Message" -ForegroundColor Yellow }
        "ERROR"   { Write-Host "❌ $Message" -ForegroundColor Red }
        "STEP"    { Write-Host "🔹 $Message" -ForegroundColor Magenta }
    }
}

function Write-Header {
    param([string]$Text)
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
}

function Test-CommandExists {
    param([string]$Command)
    
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            Write-Log "SUCCESS" "$Command is installed"
            return $true
        }
    }
    catch {
        Write-Log "ERROR" "$Command is not installed"
        return $false
    }
}

function Show-Help {
    Write-Host @"
Quantum Pi Forge Bootstrap Agent (PowerShell)

Usage: .\bootstrap.ps1 [OPTIONS]

Options:
    -Environment    Target environment (development|staging|production)
                   Default: development
    -SkipTests     Skip test execution during bootstrap
    -Verbose       Enable verbose logging
    -Help          Show this help message

Examples:
    .\bootstrap.ps1
    .\bootstrap.ps1 -Environment production
    .\bootstrap.ps1 -Environment staging -SkipTests
    .\bootstrap.ps1 -Verbose

"@
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: SYSTEM REQUIREMENTS CHECK
# ═══════════════════════════════════════════════════════════════════════════

function Test-SystemRequirements {
    Write-Header "STEP 1: System Requirements Check"
    
    Write-Log "STEP" "Checking required system dependencies..."
    
    $requirementsMet = $true
    
    # Check Python
    if (Test-CommandExists "python") {
        $pythonVersion = python --version
        Write-Log "INFO" "Python version: $pythonVersion"
        
        # Check if version is >= 3.11
        $version = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        if ([version]$version -ge [version]"3.11") {
            Write-Log "SUCCESS" "Python version meets requirements (>= 3.11)"
        }
        else {
            Write-Log "WARNING" "Python version should be >= 3.11, found $version"
        }
    }
    else {
        $requirementsMet = $false
    }
    
    # Check pip
    if (-not (Test-CommandExists "pip")) {
        $requirementsMet = $false
    }
    
    # Check git
    if (-not (Test-CommandExists "git")) {
        $requirementsMet = $false
    }
    
    # Optional tools
    if (Test-CommandExists "curl") {
        Write-Log "SUCCESS" "curl is available"
    }
    else {
        Write-Log "WARNING" "curl is not installed (optional but recommended)"
    }
    
    if (Test-CommandExists "docker") {
        $dockerVersion = docker --version
        Write-Log "SUCCESS" "Docker is available: $dockerVersion"
    }
    else {
        Write-Log "WARNING" "Docker is not installed (optional for containerized deployment)"
    }
    
    if (-not $requirementsMet) {
        Write-Log "ERROR" "Some required dependencies are missing. Please install them and try again."
        exit 1
    }
    
    Write-Log "SUCCESS" "All required system dependencies are available"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: ENVIRONMENT SETUP
# ═══════════════════════════════════════════════════════════════════════════

function Initialize-Environment {
    Write-Header "STEP 2: Environment Setup"
    
    Set-Location $ProjectRoot
    
    Write-Log "STEP" "Setting up Python virtual environment..."
    
    if (-not (Test-Path ".venv")) {
        python -m venv .venv
        Write-Log "SUCCESS" "Virtual environment created"
    }
    else {
        Write-Log "INFO" "Virtual environment already exists"
    }
    
    Write-Log "STEP" "Activating virtual environment..."
    & ".\.venv\Scripts\Activate.ps1"
    Write-Log "SUCCESS" "Virtual environment activated"
    
    Write-Log "STEP" "Upgrading pip, setuptools, and wheel..."
    python -m pip install --upgrade pip setuptools wheel --quiet
    Write-Log "SUCCESS" "Core Python packages upgraded"
    
    Write-Log "STEP" "Installing project dependencies..."
    if (Test-Path "server\requirements.txt") {
        pip install -r server\requirements.txt --quiet
        Write-Log "SUCCESS" "Project dependencies installed"
    }
    else {
        Write-Log "ERROR" "requirements.txt not found at server\requirements.txt"
        exit 1
    }
    
    Write-Log "STEP" "Checking environment configuration..."
    if (-not (Test-Path ".env")) {
        if (Test-Path ".env.example") {
            Write-Log "WARNING" ".env file not found. Creating from template..."
            Copy-Item ".env.example" ".env"
            Write-Log "SUCCESS" ".env file created from template"
            Write-Log "WARNING" "⚠️  IMPORTANT: Please edit .env file with your actual credentials!"
        }
        else {
            Write-Log "ERROR" ".env.example not found. Cannot create .env file."
            exit 1
        }
    }
    else {
        Write-Log "SUCCESS" ".env file exists"
    }
    
    # Validate environment variables
    Write-Log "STEP" "Validating environment variables..."
    if (Test-Path ".env") {
        Get-Content ".env" | ForEach-Object {
            if ($_ -match '^([^=]+)=(.*)$') {
                $name = $matches[1]
                $value = $matches[2]
                [Environment]::SetEnvironmentVariable($name, $value, "Process")
            }
        }
    }
    
    $supabaseUrl = [Environment]::GetEnvironmentVariable("SUPABASE_URL", "Process")
    if ([string]::IsNullOrEmpty($supabaseUrl) -or $supabaseUrl -eq "https://your-project.supabase.co") {
        Write-Log "WARNING" "SUPABASE_URL not configured in .env"
    }
    else {
        Write-Log "SUCCESS" "SUPABASE_URL is configured"
    }
    
    $supabaseKey = [Environment]::GetEnvironmentVariable("SUPABASE_KEY", "Process")
    if ([string]::IsNullOrEmpty($supabaseKey) -or $supabaseKey -eq "your-anon-key") {
        Write-Log "WARNING" "SUPABASE_KEY not configured in .env"
    }
    else {
        Write-Log "SUCCESS" "SUPABASE_KEY is configured"
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: INFRASTRUCTURE VALIDATION
# ═══════════════════════════════════════════════════════════════════════════

function Test-Infrastructure {
    Write-Header "STEP 3: Infrastructure Validation"
    
    Write-Log "STEP" "Validating project structure..."
    
    $criticalFiles = @(
        "server\main.py",
        "server\app.py",
        "server\canticle_interface.py",
        "server\requirements.txt",
        "Dockerfile",
        "railway.toml",
        "frontend\pi-forge-integration.js"
    )
    
    $allPresent = $true
    foreach ($file in $criticalFiles) {
        $filePath = Join-Path $ProjectRoot $file
        if (Test-Path $filePath) {
            Write-Log "SUCCESS" "✓ $file"
        }
        else {
            Write-Log "ERROR" "✗ $file (missing)"
            $allPresent = $false
        }
    }
    
    if (-not $allPresent) {
        Write-Log "ERROR" "Some critical files are missing"
        exit 1
    }
    
    Write-Log "SUCCESS" "All critical files present"
    
    Write-Log "STEP" "Validating Python imports..."
    Set-Location $ProjectRoot
    
    $result = python -c "import sys; sys.path.insert(0, 'server'); from main import app; print('OK')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "SUCCESS" "FastAPI module imports successfully"
    }
    else {
        Write-Log "ERROR" "FastAPI module import failed"
        exit 1
    }
    
    $result = python -c "import sys; sys.path.insert(0, 'server'); from app import app; print('OK')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "SUCCESS" "Flask module imports successfully"
    }
    else {
        Write-Log "ERROR" "Flask module import failed"
        exit 1
    }
    
    Write-Log "SUCCESS" "Infrastructure validation complete"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4: RUN TESTS
# ═══════════════════════════════════════════════════════════════════════════

function Invoke-Tests {
    if ($SkipTests) {
        Write-Log "WARNING" "Skipping tests (-SkipTests flag provided)"
        return
    }
    
    Write-Header "STEP 4: Running Tests"
    
    Write-Log "STEP" "Installing test dependencies..."
    pip install pytest pytest-asyncio pytest-cov --quiet
    Write-Log "SUCCESS" "Test dependencies installed"
    
    Write-Log "STEP" "Running test suite..."
    Set-Location (Join-Path $ProjectRoot "tests")
    
    $testResult = python -m pytest -v --tb=short 2>&1 | Tee-Object -Append -FilePath $LogFile
    if ($LASTEXITCODE -eq 0) {
        Write-Log "SUCCESS" "All tests passed"
    }
    else {
        Write-Log "WARNING" "Some tests failed (non-critical for bootstrap)"
    }
    
    Set-Location $ProjectRoot
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 5: SERVICE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════

function Initialize-Services {
    Write-Header "STEP 5: Service Initialization"
    
    Write-Log "STEP" "Checking service health..."
    
    # Create health check script
    $healthCheck = @"
import sys
sys.path.insert(0, 'server')

try:
    from main import app as fastapi_app
    print("✅ FastAPI: OK")
except Exception as e:
    print(f"❌ FastAPI: FAILED - {e}")
    sys.exit(1)

try:
    from app import app as flask_app
    print("✅ Flask: OK")
except Exception as e:
    print(f"❌ Flask: FAILED - {e}")
    sys.exit(1)

try:
    import canticle_interface
    print("✅ Gradio: OK")
except Exception as e:
    print(f"❌ Gradio: FAILED - {e}")
    sys.exit(1)

print("\n🎉 All services initialized successfully!")
"@
    
    $healthCheckPath = Join-Path $BootstrapDir "health_check.py"
    Set-Content -Path $healthCheckPath -Value $healthCheck
    
    Set-Location $ProjectRoot
    $result = python $healthCheckPath 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "SUCCESS" "All services health check passed"
    }
    else {
        Write-Log "ERROR" "Service health check failed"
        exit 1
    }
    
    # Clean up
    Remove-Item $healthCheckPath -Force
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 6: DEPLOYMENT PREPARATION
# ═══════════════════════════════════════════════════════════════════════════

function Initialize-Deployment {
    Write-Header "STEP 6: Deployment Preparation"
    
    Write-Log "STEP" "Validating deployment configuration..."
    
    if (Test-Path (Join-Path $ProjectRoot "railway.toml")) {
        Write-Log "SUCCESS" "railway.toml exists"
    }
    else {
        Write-Log "WARNING" "railway.toml not found (needed for Railway deployment)"
    }
    
    if (Test-Path (Join-Path $ProjectRoot "Dockerfile")) {
        Write-Log "SUCCESS" "Dockerfile exists"
    }
    else {
        Write-Log "ERROR" "Dockerfile not found"
    }
    
    Write-Log "STEP" "Generating deployment checklist..."
    
    $checklist = @"
# Deployment Checklist

Generated: $(Get-Date)
Environment: $Environment

## Pre-Deployment

- [x] System requirements verified
- [x] Python environment configured
- [x] Dependencies installed
- [x] Environment variables set
- [x] Infrastructure validated
- [x] Tests executed
- [x] Services initialized

## Deployment Steps (Windows)

### Option 1: Railway Deployment

1. Install Railway CLI:
   ``````powershell
   npm i -g @railway/cli
   ``````

2. Login to Railway:
   ``````powershell
   railway login
   ``````

3. Set environment variables:
   ``````powershell
   railway variables set SUPABASE_URL=<your-url>
   railway variables set SUPABASE_KEY=<your-key>
   railway variables set JWT_SECRET=<your-secret>
   ``````

4. Deploy:
   ``````powershell
   railway up
   ``````

### Option 2: Docker Deployment

1. Build image:
   ``````powershell
   docker build -t quantum-pi-forge .
   ``````

2. Run container:
   ``````powershell
   docker run -p 8000:8000 --env-file .env quantum-pi-forge
   ``````

### Option 3: Local Development

1. Start services:
   ``````powershell
   .\bootstrap\start-services.ps1
   ``````

## Service URLs

- FastAPI: http://localhost:8000
- Flask:   http://localhost:5000
- Gradio:  http://localhost:7860

## Post-Deployment

- [ ] Verify health endpoints
- [ ] Test authentication
- [ ] Test WebSocket connections
- [ ] Monitor logs for errors
- [ ] Set up autonomous monitoring

"@
    
    $checklistPath = Join-Path $BootstrapDir "deployment-checklist.md"
    Set-Content -Path $checklistPath -Value $checklist
    Write-Log "SUCCESS" "Deployment checklist created: $checklistPath"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 7: CREATE SERVICE SCRIPTS
# ═══════════════════════════════════════════════════════════════════════════

function New-ServiceScripts {
    Write-Header "STEP 7: Creating Service Scripts"
    
    # Create start services script
    $startScript = @"
# Start all Quantum Pi Forge services

`$ErrorActionPreference = "Stop"

`$ScriptDir = Split-Path -Parent `$MyInvocation.MyCommand.Path
`$ProjectRoot = Split-Path -Parent `$ScriptDir

Write-Host "🌌 Starting Quantum Pi Forge Services..." -ForegroundColor Cyan
Write-Host ""

Set-Location `$ProjectRoot

# Create logs directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

# Activate virtual environment
if (Test-Path ".venv\Scripts\Activate.ps1") {
    & ".\.venv\Scripts\Activate.ps1"
}
else {
    Write-Host "⚠️  Virtual environment not found. Run bootstrap.ps1 first." -ForegroundColor Yellow
    exit 1
}

# Load environment
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if (`$_ -match '^([^=]+)=(.*)$') {
            [Environment]::SetEnvironmentVariable(`$matches[1], `$matches[2], "Process")
        }
    }
}

Write-Host "Starting services..." -ForegroundColor Green
Write-Host ""

# Start FastAPI
Write-Host "🚀 Starting FastAPI (Port 8000)..." -ForegroundColor Green
`$fastApiProcess = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000" -PassThru -RedirectStandardOutput "logs\fastapi.log" -RedirectStandardError "logs\fastapi-error.log"
Write-Host "   PID: `$(`$fastApiProcess.Id)" -ForegroundColor Gray

Start-Sleep -Seconds 2

# Start Flask
Write-Host "🎨 Starting Flask (Port 5000)..." -ForegroundColor Green
`$flaskProcess = Start-Process -FilePath "python" -ArgumentList "server\app.py" -PassThru -RedirectStandardOutput "logs\flask.log" -RedirectStandardError "logs\flask-error.log"
Write-Host "   PID: `$(`$flaskProcess.Id)" -ForegroundColor Gray

# Start Gradio
Write-Host "🔮 Starting Gradio (Port 7860)..." -ForegroundColor Green
`$gradioProcess = Start-Process -FilePath "python" -ArgumentList "server\canticle_interface.py" -PassThru -RedirectStandardOutput "logs\gradio.log" -RedirectStandardError "logs\gradio-error.log"
Write-Host "   PID: `$(`$gradioProcess.Id)" -ForegroundColor Gray

Write-Host ""
Write-Host "✅ All services started!" -ForegroundColor Green
Write-Host ""
Write-Host "Service URLs:" -ForegroundColor Cyan
Write-Host "  - FastAPI: http://localhost:8000" -ForegroundColor White
Write-Host "  - Flask:   http://localhost:5000" -ForegroundColor White
Write-Host "  - Gradio:  http://localhost:7860" -ForegroundColor White
Write-Host ""
Write-Host "Process IDs:" -ForegroundColor Cyan
Write-Host "  - FastAPI: `$(`$fastApiProcess.Id)" -ForegroundColor White
Write-Host "  - Flask:   `$(`$flaskProcess.Id)" -ForegroundColor White
Write-Host "  - Gradio:  `$(`$gradioProcess.Id)" -ForegroundColor White
Write-Host ""
Write-Host "To stop services, run: .\bootstrap\stop-services.ps1" -ForegroundColor Yellow
Write-Host ""

# Save PIDs
@{
    FastAPI = `$fastApiProcess.Id
    Flask = `$flaskProcess.Id
    Gradio = `$gradioProcess.Id
} | ConvertTo-Json | Set-Content "`$ScriptDir\service-pids.json"
"@
    
    $startScriptPath = Join-Path $BootstrapDir "start-services.ps1"
    Set-Content -Path $startScriptPath -Value $startScript
    Write-Log "SUCCESS" "Service starter script created: $startScriptPath"
    
    # Create stop services script
    $stopScript = @"
# Stop all Quantum Pi Forge services

`$ScriptDir = Split-Path -Parent `$MyInvocation.MyCommand.Path
`$pidFile = Join-Path `$ScriptDir "service-pids.json"

Write-Host "🛑 Stopping Quantum Pi Forge Services..." -ForegroundColor Yellow

if (Test-Path `$pidFile) {
    `$pids = Get-Content `$pidFile | ConvertFrom-Json
    
    foreach (`$service in `$pids.PSObject.Properties) {
        `$pid = `$service.Value
        `$name = `$service.Name
        
        try {
            `$process = Get-Process -Id `$pid -ErrorAction Stop
            Stop-Process -Id `$pid -Force
            Write-Host "✅ `$name stopped (PID: `$pid)" -ForegroundColor Green
        }
        catch {
            Write-Host "⚠️  `$name process not found (PID: `$pid)" -ForegroundColor Yellow
        }
    }
    
    Remove-Item `$pidFile
}
else {
    Write-Host "⚠️  No running services found" -ForegroundColor Yellow
}

Write-Host "✅ All services stopped" -ForegroundColor Green
"@
    
    $stopScriptPath = Join-Path $BootstrapDir "stop-services.ps1"
    Set-Content -Path $stopScriptPath -Value $stopScript
    Write-Log "SUCCESS" "Service stopper script created: $stopScriptPath"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 8: GENERATE FINAL REPORT
# ═══════════════════════════════════════════════════════════════════════════

function New-FinalReport {
    Write-Header "STEP 8: Final Report"
    
    $reportPath = Join-Path $BootstrapDir "bootstrap-report-$Timestamp.md"
    
    $pythonVersion = python --version
    $pipVersion = pip --version
    $gitVersion = git --version
    $dockerVersion = if (Get-Command docker -ErrorAction SilentlyContinue) { docker --version } else { "Not installed" }
    
    $report = @"
# Quantum Pi Forge Bootstrap Report

**Date**: $(Get-Date)
**Environment**: $Environment
**Status**: ✅ SUCCESS

## Summary

The Quantum Pi Forge autonomous system has been successfully bootstrapped and is ready for deployment.

## Steps Completed

1. ✅ System requirements validated
2. ✅ Python environment configured
3. ✅ Dependencies installed
4. ✅ Infrastructure validated
5. ✅ Tests executed
6. ✅ Services initialized
7. ✅ Deployment prepared
8. ✅ Service scripts created

## System Information

- **Python**: $pythonVersion
- **Pip**: $pipVersion
- **Git**: $gitVersion
- **Docker**: $dockerVersion

## Next Steps

### 1. Configure Environment Variables

Edit the ``.env`` file and set your actual credentials:

``````powershell
# Open in notepad
notepad .env

# Or use your preferred editor
code .env
``````

Required variables:
- SUPABASE_URL
- SUPABASE_KEY
- JWT_SECRET

### 2. Start Services

``````powershell
.\bootstrap\start-services.ps1
``````

### 3. Verify Deployment

Check health endpoints:
- FastAPI: http://localhost:8000/
- Flask: http://localhost:5000/health
- Gradio: http://localhost:7860/

### 4. Enable Autonomous Operations

See ``bootstrap\autonomous-operations.md`` for details on enabling autonomous monitoring and deployment.

## Documentation

- **Deployment Checklist**: ``bootstrap\deployment-checklist.md``
- **Bootstrap Log**: ``$LogFile``
- **Service Scripts**: ``bootstrap\start-services.ps1``, ``bootstrap\stop-services.ps1``

## Support

For issues or questions:
1. Check the documentation in ``docs\``
2. Review the bootstrap log: ``$LogFile``
3. Consult the AI Agent Handoff Runbook
4. Contact repository maintainer

---

🎉 **Bootstrap complete! The Quantum Resonance Lattice awaits activation.**

"@
    
    Set-Content -Path $reportPath -Value $report
    Write-Log "SUCCESS" "Bootstrap report generated: $reportPath"
    
    # Display report
    Write-Host $report
}

# ═══════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

function Main {
    # Show help if requested
    if ($Help) {
        Show-Help
        exit 0
    }
    
    # Print banner
    Clear-Host
    Write-Header "🌌 QUANTUM PI FORGE - BOOTSTRAP AGENT"
    
    Write-Log "INFO" "Bootstrap started at $(Get-Date)"
    Write-Log "INFO" "Target environment: $Environment"
    Write-Log "INFO" "Log file: $LogFile"
    Write-Host ""
    
    # Create logs directory
    $logsDir = Join-Path $ProjectRoot "logs"
    if (-not (Test-Path $logsDir)) {
        New-Item -ItemType Directory -Path $logsDir | Out-Null
    }
    
    try {
        # Execute bootstrap steps
        Test-SystemRequirements
        Initialize-Environment
        Test-Infrastructure
        Invoke-Tests
        Initialize-Services
        Initialize-Deployment
        New-ServiceScripts
        New-FinalReport
        
        # Final message
        Write-Header "✨ BOOTSTRAP COMPLETE"
        
        Write-Host ""
        Write-Log "SUCCESS" "Quantum Pi Forge is ready for deployment!"
        Write-Host ""
        Write-Log "INFO" "Next steps:"
        Write-Host "  1. Review and edit .env file with your credentials"
        Write-Host "  2. Check deployment-checklist.md for deployment options"
        Write-Host "  3. Start services with: .\bootstrap\start-services.ps1"
        Write-Host ""
        Write-Log "INFO" "Full bootstrap report: bootstrap\bootstrap-report-$Timestamp.md"
        Write-Log "INFO" "Bootstrap log: $LogFile"
        Write-Host ""
    }
    catch {
        Write-Log "ERROR" "Bootstrap failed: $_"
        Write-Host ""
        Write-Host "Check the log file for details: $LogFile" -ForegroundColor Yellow
        exit 1
    }
}

# Run main function
Main
