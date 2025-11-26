# PowerShell script to run tests and generate Allure report

param(
    [string]$TestPath = "tests/",
    [switch]$Headed
)

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Black Pigeon - Test Execution with Allure" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "`nActivating virtual environment..." -ForegroundColor Green
    & "venv\Scripts\Activate.ps1"
} else {
    Write-Host "`nVirtual environment not found!" -ForegroundColor Red
    Write-Host "Please create it first: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Build pytest command
$pytestCmd = "pytest $TestPath -v"
if ($Headed) {
    $pytestCmd += " --headed"
}

# Run tests
Write-Host "`nRunning tests: $pytestCmd" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan
Invoke-Expression $pytestCmd

$testExitCode = $LASTEXITCODE

# Check if allure-results were generated
if (Test-Path "allure-results") {
    Write-Host "`n==================================================" -ForegroundColor Cyan
    Write-Host "  Generating Allure Report" -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
    
    # Check if allure is installed
    $allureCommand = Get-Command allure -ErrorAction SilentlyContinue
    
    if ($allureCommand) {
        Write-Host "`nGenerating Allure report..." -ForegroundColor Green
        allure generate allure-results --clean -o allure-report
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`nAllure report generated successfully!" -ForegroundColor Green
            Write-Host "To view the report, run: allure open allure-report" -ForegroundColor Yellow
            Write-Host "Or run: .\generate_allure_report.ps1" -ForegroundColor Yellow
        }
    } else {
        Write-Host "`nAllure CLI not found!" -ForegroundColor Yellow
        Write-Host "Install Allure CLI to generate reports:" -ForegroundColor Cyan
        Write-Host "  scoop install allure" -ForegroundColor White
    }
} else {
    Write-Host "`nNo test results generated!" -ForegroundColor Red
}

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "  Test Execution Completed" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

exit $testExitCode
