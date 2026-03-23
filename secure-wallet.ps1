param(
    [Parameter(Mandatory=$false)]
    [string]$Action = "rotate-secrets"
)

function Generate-SecureToken {
    param([int]$Length)
    $bytes = New-Object byte[] $Length
    [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    return [BitConverter]::ToString($bytes).Replace("-", "").ToLower()
}

function Rotate-Secrets {
    Write-Host "🔐 Generating secure secrets..." -ForegroundColor Cyan
    Write-Host ""

    $jwtSecret = Generate-SecureToken 32  # 64 hex chars
    $sessionSecret = Generate-SecureToken 24  # 48 hex chars

    Write-Host "📋 Copy these to Railway and Vercel environment variables:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Railway Variables:" -ForegroundColor Green
    Write-Host "JWT_SECRET=$jwtSecret"
    Write-Host "SESSION_SECRET=$sessionSecret"
    Write-Host "ENVIRONMENT=production"
    Write-Host ""
    Write-Host "You'll also need to add:" -ForegroundColor Yellow
    Write-Host "SUPABASE_URL=<from-supabase-dashboard>"
    Write-Host "SUPABASE_KEY=<from-supabase-dashboard>"
    Write-Host "PI_NETWORK_APP_ID=<from-pi-developer-portal>"
    Write-Host "PI_NETWORK_API_KEY=<from-pi-developer-portal>"
    Write-Host "PI_NETWORK_WEBHOOK_SECRET=<from-pi-developer-portal>"
    Write-Host ""
    Write-Host "Vercel Variables:" -ForegroundColor Green
    Write-Host "NEXT_PUBLIC_API_URL=https://pi-forge-quantum-genesis.railway.app"
    Write-Host "PI_APP_SECRET=<from-pi-developer-portal>"
    Write-Host "NEXT_PUBLIC_PI_APP_ID=<from-pi-developer-portal>"
    Write-Host ""

    # Save to file for reference
    $output = @"
# Generated $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
JWT_SECRET=$jwtSecret
SESSION_SECRET=$sessionSecret
ENVIRONMENT=production

# Add these manually from your dashboards:
# SUPABASE_URL=
# SUPABASE_KEY=
# PI_NETWORK_APP_ID=
# PI_NETWORK_API_KEY=
# PI_NETWORK_WEBHOOK_SECRET=
"@

    $output | Out-File -FilePath ".env.generated" -Encoding UTF8
    Write-Host "💾 Secrets saved to .env.generated" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Add the missing values from your dashboards!" -ForegroundColor Red
}

switch ($Action) {
    "rotate-secrets" { Rotate-Secrets }
    default {
        Write-Host "Usage: .\secure-wallet.ps1 rotate-secrets" -ForegroundColor Yellow
    }
}