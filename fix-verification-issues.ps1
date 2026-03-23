#!/usr/bin/env pwsh
# Quick Fix Script for Verification Issues

Write-Host "`n🔧 FIXING VERIFICATION ISSUES`n" -ForegroundColor Cyan

# Fix 1: Remove BOM from server/app.py
Write-Host "1. Fixing BOM in server/app.py..." -ForegroundColor Yellow
$path = "server\app.py"
$bytes = [System.IO.File]::ReadAllBytes($path)
if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    $newBytes = $bytes[3..($bytes.Length-1)]
    [System.IO.File]::WriteAllBytes($path, $newBytes)
    Write-Host "   ✅ Removed BOM from server/app.py" -ForegroundColor Green
} else {
    Write-Host "   ✅ No BOM found (already clean)" -ForegroundColor Green
}

# Fix 2: Create frontend/index.html
Write-Host "`n2. Creating frontend/index.html..." -ForegroundColor Yellow
if (Test-Path "index.html") {
    Copy-Item "index.html" "frontend\index.html" -Force
    Write-Host "   ✅ Copied index.html to frontend/" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Root index.html not found, skipping" -ForegroundColor DarkYellow
}

# Fix 3: Create .env if missing
Write-Host "`n3. Checking .env file..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "   ✅ Created .env from .env.example" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  .env.example not found" -ForegroundColor DarkYellow
    }
} else {
    Write-Host "   ✅ .env already exists" -ForegroundColor Green
}

# Fix 4: Verify Python syntax
Write-Host "`n4. Verifying Python syntax..." -ForegroundColor Yellow
python -m py_compile "server\app.py" 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ server/app.py syntax OK" -ForegroundColor Green
} else {
    Write-Host "   ❌ server/app.py still has syntax errors" -ForegroundColor Red
}

# Summary
Write-Host "`n📊 VERIFICATION STATUS" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray

$checks = @(
    @{ Name = "server/app.py BOM removed"; Test = { -not ((Get-Content "server\app.py" -AsByteStream -TotalCount 3)[0] -eq 0xEF) } }
    @{ Name = "frontend/index.html exists"; Test = { Test-Path "frontend\index.html" } }
    @{ Name = ".env file exists"; Test = { Test-Path ".env" } }
    @{ Name = "Python syntax valid"; Test = { python -m py_compile "server\app.py" 2>&1 | Out-Null; $LASTEXITCODE -eq 0 } }
)

$passed = 0
foreach ($check in $checks) {
    $result = & $check.Test
    if ($result) {
        Write-Host "✅ $($check.Name)" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "❌ $($check.Name)" -ForegroundColor Red
    }
}

Write-Host "`n🎯 Result: $passed/$($checks.Count) checks passed`n" -ForegroundColor $(if ($passed -eq $checks.Count) { "Green" } else { "Yellow" })

if ($passed -eq $checks.Count) {
    Write-Host "✅ All issues fixed! Run verify_production.py again.`n" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some issues remain. Check output above.`n" -ForegroundColor Yellow
}
