# PowerShell script to generate and open Allure report

Write-Host "Generating Allure Report..." -ForegroundColor Cyan

# Check if allure command is available
$allureCommand = Get-Command allure -ErrorAction SilentlyContinue

if (-not $allureCommand) {
    Write-Host "`nAllure CLI is not installed!" -ForegroundColor Red
    Write-Host "`nPlease install Allure CLI:" -ForegroundColor Yellow
    Write-Host "1. Using Scoop (Recommended for Windows):" -ForegroundColor Green
    Write-Host "   scoop install allure" -ForegroundColor White
    Write-Host "`n2. Manual installation:" -ForegroundColor Green
    Write-Host "   - Download from: https://github.com/allure-framework/allure2/releases" -ForegroundColor White
    Write-Host "   - Extract and add to PATH" -ForegroundColor White
    Write-Host "`n3. Using npm:" -ForegroundColor Green
    Write-Host "   npm install -g allure-commandline" -ForegroundColor White
    exit 1
}

# Check if allure-results directory exists
if (-not (Test-Path "allure-results")) {
    Write-Host "`nNo test results found!" -ForegroundColor Red
    Write-Host "Please run tests first: pytest tests/" -ForegroundColor Yellow
    exit 1
}

# Generate report
Write-Host "`nGenerating Allure report from results..." -ForegroundColor Green
allure generate allure-results --clean -o allure-report

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nAllure report generated successfully!" -ForegroundColor Green
    Write-Host "Opening report in browser..." -ForegroundColor Cyan
    
    # Open the report
    allure open allure-report
} else {
    Write-Host "`nFailed to generate Allure report!" -ForegroundColor Red
    exit 1
}
