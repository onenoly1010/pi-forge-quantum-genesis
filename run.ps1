# Quantum Resonance Lattice Launcher
# Activates virtual environment and starts the Sacred Trinity server

Write-Host "🌌 Activating Quantum Development Environment..." -ForegroundColor Cyan

# Change to the project directory
Set-Location $PSScriptRoot

# Activate virtual environment
& ".\.venv\Scripts\activate.ps1"

Write-Host "🚀 Starting Quantum Lattice Server..." -ForegroundColor Green

# Start the server synchronously to see any errors
try {
    & ".\.venv\Scripts\python.exe" "server\main.py"
} catch {
    Write-Host "❌ Error starting server: $($_.Exception.Message)" -ForegroundColor Red
}