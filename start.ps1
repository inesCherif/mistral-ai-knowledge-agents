# MistralBot - Start All Services
# Just double-click this file or run: .\start.ps1 from ANYWHERE

$ProjectRoot = $PSScriptRoot

Write-Host "=== MistralBot Launcher ===" -ForegroundColor Magenta
Write-Host ""

# Kill anything on port 8000 first to avoid conflicts
Write-Host "Cleaning up port 8000..." -ForegroundColor Gray
$proc = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($proc) {
    Stop-Process -Id $proc.OwningProcess -Force -ErrorAction SilentlyContinue
    Write-Host "Killed existing process on port 8000." -ForegroundColor Yellow
}

Write-Host "Starting Backend (FastAPI on port 8000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "uvicorn main:app --reload --port 8000 --app-dir backend" -WorkingDirectory $ProjectRoot

Start-Sleep -Seconds 2

Write-Host "Starting Frontend (React on port 3000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm start" -WorkingDirectory "$ProjectRoot\frontend"

Write-Host ""
Write-Host "Both services are starting in new windows!" -ForegroundColor Green
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Yellow
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor Yellow

