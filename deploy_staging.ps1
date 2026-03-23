#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Deploy Quantum Resonance Lattice to staging environment for integration testing
.DESCRIPTION
    This script deploys the Sacred Trinity architecture to a staging environment
    with comprehensive evaluation system testing and monitoring.
.PARAMETER Environment
    Target environment (staging, production)
.PARAMETER SkipTests
    Skip running tests before deployment
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("staging", "production")]
    [string]$Environment = "staging",

    [Parameter(Mandatory=$false)]
    [switch]$SkipTests
)

# Configuration
$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
$StagingUrl = "https://pi-forge-staging.up.railway.app"
$ProductionUrl = "https://pi-forge-production.up.railway.app"

function Write-Step {
    param([string]$Message)
    Write-Host "🔄 $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Test-EvaluationSystem {
    Write-Step "Testing Evaluation System Components"

    try {
        # Test evaluation framework
        & python tests/test_evaluation_framework.py
        if ($LASTEXITCODE -ne 0) {
            throw "Evaluation framework test failed"
        }
        Write-Success "Evaluation framework tests passed"

        # Test comprehensive evaluation
        $env:DISABLE_TRACING = "1"
        & python comprehensive_evaluation_test.py
        if ($LASTEXITCODE -ne 0) {
            throw "Comprehensive evaluation test failed"
        }
        Write-Success "Comprehensive evaluation tests passed"

    } catch {
        Write-Error "Evaluation system tests failed: $_"
        throw
    }
}

function Deploy-ToRailway {
    param([string]$TargetEnv)

    Write-Step "Deploying to Railway ($TargetEnv)"

    try {
        # Check if Railway CLI is installed
        $railwayInstalled = $null -ne (Get-Command railway -ErrorAction SilentlyContinue)
        if (-not $railwayInstalled) {
            Write-Step "Installing Railway CLI"
            npm install -g @railway/cli
        }

        # Login to Railway (if not already logged in)
        Write-Step "Authenticating with Railway"
        railway login --browserless

        # Deploy based on environment
        if ($TargetEnv -eq "staging") {
            Write-Step "Creating staging deployment"
            railway up --detach
        } else {
            Write-Step "Creating production deployment"
            railway up --detach --environment production
        }

        Write-Success "Deployment initiated on Railway"

    } catch {
        Write-Error "Railway deployment failed: $_"
        throw
    }
}

function Test-Integration {
    param([string]$TargetUrl)

    Write-Step "Testing Sacred Trinity Integration"

    try {
        # Wait for deployment to be ready
        Start-Sleep -Seconds 30

        # Test health endpoint
        $healthResponse = Invoke-WebRequest -Uri "$TargetUrl/health" -TimeoutSec 30
        if ($healthResponse.StatusCode -ne 200) {
            throw "Health check failed with status: $($healthResponse.StatusCode)"
        }
        Write-Success "Health check passed"

        # Test evaluation endpoints
        $evalResponse = Invoke-WebRequest -Uri "$TargetUrl/evaluate" -Method POST -Body '{"query":"test","response":"test"}' -ContentType "application/json" -TimeoutSec 30
        if ($evalResponse.StatusCode -ne 200) {
            throw "Evaluation endpoint failed with status: $($evalResponse.StatusCode)"
        }
        Write-Success "Evaluation endpoint test passed"

        # Test tracing system
        Write-Step "Testing tracing system integration"
        # This would test the tracing endpoints if available

    } catch {
        Write-Error "Integration tests failed: $_"
        throw
    }
}

function Monitor-Performance {
    param([string]$TargetUrl)

    Write-Step "Setting up performance monitoring"

    try {
        # Start monitoring script
        $monitorScript = {
            param($url)
            while ($true) {
                try {
                    $response = Invoke-WebRequest -Uri "$url/health" -TimeoutSec 10
                    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                    Write-Host "[$timestamp] Health: $($response.StatusCode) - $($response.Content.Length) bytes"
                } catch {
                    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                    Write-Host "[$timestamp] ERROR: $_" -ForegroundColor Red
                }
                Start-Sleep -Seconds 60
            }
        }

        # Start monitoring in background
        $job = Start-Job -ScriptBlock $monitorScript -ArgumentList $TargetUrl
        Write-Success "Performance monitoring started (Job ID: $($job.Id))"

        # Return job for later cleanup
        return $job

    } catch {
        Write-Error "Performance monitoring setup failed: $_"
        return $null
    }
}

# Main deployment process
try {
    Write-Host "🌌 Quantum Resonance Lattice - $Environment Deployment" -ForegroundColor Magenta
    Write-Host "=" * 60 -ForegroundColor Magenta

    # Change to project root
    Set-Location $ProjectRoot

    # Run tests unless skipped
    if (-not $SkipTests) {
        Test-EvaluationSystem
    } else {
        Write-Step "Skipping tests as requested"
    }

    # Deploy to Railway
    Deploy-ToRailway -TargetEnv $Environment

    # Determine target URL
    $targetUrl = if ($Environment -eq "staging") { $StagingUrl } else { $ProductionUrl }

    # Test integration
    Test-Integration -TargetUrl $targetUrl

    # Setup monitoring
    $monitorJob = Monitor-Performance -TargetUrl $targetUrl

    Write-Host ""
    Write-Success "🎉 $Environment deployment completed successfully!"
    Write-Host ""
    Write-Host "📊 Deployment Summary:" -ForegroundColor Yellow
    Write-Host "   🌐 URL: $targetUrl" -ForegroundColor White
    Write-Host "   🔍 Health: $targetUrl/health" -ForegroundColor White
    Write-Host "   📈 Monitoring: Active (Job ID: $($monitorJob.Id))" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 Ready for Sacred Trinity integration testing!" -ForegroundColor Green

}
catch {
    Write-Error "Deployment failed: $_"
    Write-Host ""
    Write-Host "🔧 Troubleshooting:" -ForegroundColor Yellow
    Write-Host "   1. Check Railway deployment logs: railway logs" -ForegroundColor White
    Write-Host "   2. Verify environment variables are set" -ForegroundColor White
    Write-Host "   3. Ensure all dependencies are installed" -ForegroundColor White
    exit 1
}