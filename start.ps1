# MistralBot - Start All Services
# Run this from the project root: .\start.ps1

Write-Host "Starting MistralBot Backend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "uvicorn main:app --reload --port 8000 --app-dir backend" -WorkingDirectory (Get-Location)

Write-Host "Starting MistralBot Frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm start" -WorkingDirectory ".\frontend"

Write-Host ""
Write-Host "Services are starting:" -ForegroundColor Green
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Yellow
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
