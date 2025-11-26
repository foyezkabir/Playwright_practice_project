# Automated test execution with timestamp-based Allure reports
# This script runs tests and generates unique reports for each run

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Generate timestamp in dd.mm.yyyy_HH.mm.ss format
$timestamp = Get-Date -Format "dd.MM.yyyy_HH.mm.ss"
$resultsDir = "allure-results-$timestamp"
$reportDir = "allure-report-$timestamp"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting test execution at $timestamp" -ForegroundColor Cyan
Write-Host "Results will be saved to: $resultsDir" -ForegroundColor Yellow
Write-Host "Report will be generated at: $reportDir" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# Run tests with timestamp-based results directory
pytest tests/test_reset_pass.py tests/test_signup.py tests/test_login.py tests/test_agency.py --alluredir="$resultsDir"

# Check if tests ran successfully
if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq 1) {
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "Generating Allure report..." -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    
    # Generate Allure report
    allure generate "$resultsDir" --clean -o "$reportDir"
    
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "Test execution completed!" -ForegroundColor Green
    Write-Host "Results saved in: $resultsDir" -ForegroundColor Yellow
    Write-Host "Report generated in: $reportDir" -ForegroundColor Yellow
    Write-Host "`nTo view the report, run:" -ForegroundColor Cyan
    Write-Host "  allure open $reportDir" -ForegroundColor White
    Write-Host "========================================" -ForegroundColor Green
    
    # Optional: Automatically open the report
    $openReport = Read-Host "`nDo you want to open the report now? (y/n)"
    if ($openReport -eq 'y' -or $openReport -eq 'Y') {
        allure open "$reportDir"
    }
} else {
    Write-Host "`n========================================" -ForegroundColor Red
    Write-Host "Test execution failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
}
