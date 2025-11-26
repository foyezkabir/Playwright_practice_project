# Allure Reporting Guide

## Overview
Allure Framework is a flexible, lightweight multi-language test reporting tool that provides clear graphical reports with detailed test execution information, screenshots, and history tracking.

## Installation

### 1. Install Python Packages
```powershell
pip install -r requirements.txt
```

This installs:
- `allure-pytest` - Pytest plugin for Allure
- `allure-python-commons` - Common utilities for Allure Python integrations

### 2. Install Allure CLI

**Option A: Using Scoop (Recommended for Windows)**
```powershell
scoop install allure
```

**Option B: Using npm**
```powershell
npm install -g allure-commandline
```

**Option C: Manual Installation**
1. Download from: https://github.com/allure-framework/allure2/releases
2. Extract to a directory (e.g., `C:\allure`)
3. Add to PATH: `C:\allure\bin`

### 3. Verify Installation
```powershell
allure --version
```

## Running Tests with Allure

### Method 1: Using Helper Script (Recommended)
```powershell
# Run all tests and generate report
.\run_tests_with_allure.ps1

# Run specific test file
.\run_tests_with_allure.ps1 -TestPath "tests/test_client.py"

# Run in headed mode (browser visible)
.\run_tests_with_allure.ps1 -Headed
```

### Method 2: Manual Commands
```powershell
# 1. Run tests (results saved to allure-results/)
pytest tests/ -v

# 2. Generate HTML report
allure generate allure-results --clean -o allure-report

# 3. Open report in browser
allure open allure-report
```

### Method 3: View Existing Report
```powershell
# If you already have results and just want to generate/view report
.\generate_allure_report.ps1
```

## Allure Report Features

### 1. **Overview Dashboard**
- Total tests executed
- Pass/Fail/Skip statistics
- Success rate pie chart
- Duration timeline
- Test trends over multiple runs

### 2. **Suites View**
- Organized by test files/modules
- Hierarchical test structure
- Quick filtering by status

### 3. **Graphs**
- Test execution timeline
- Duration trends
- Status distribution
- Categories breakdown

### 4. **Timeline**
- Visual representation of test execution
- Parallel execution visualization
- Duration comparison

### 5. **Behaviors (BDD)**
- Tests organized by features
- Epic/Feature/Story hierarchy
- User story mapping

### 6. **Test Details**
Each test includes:
- ✅ Test description
- ⏱️ Execution time
- 📸 **Screenshots on failure** (automatically attached)
- 📝 Step-by-step execution log
- 🔄 Retry information
- 📊 History trends
- 🏷️ Categories and tags

## Allure Decorators for Enhanced Reports

### Adding Test Information
```python
import allure

@allure.feature("Client Management")
@allure.story("Client Creation")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Create client with mandatory fields")
@allure.description("Verify that user can create a client with only mandatory fields")
@with_client_login()
def test_TC_06(page: Page):
    client_page = page._client_page
    # Test code...
```

### Adding Test Steps
```python
@allure.step("Fill client basic information")
def fill_client_info(client_page, name, company):
    client_page.fill_english_name(name)
    client_page.click_company_dropdown()
    client_page.select_dropdown_option(company)

@with_client_login()
def test_create_client(page: Page):
    client_page = page._client_page
    
    with allure.step("Open client creation modal"):
        client_page.click_add_client_button()
    
    fill_client_info(client_page, "Test Client", "Test Company")
    
    with allure.step("Submit form"):
        client_page.click_create_button()
```

### Attaching Additional Information
```python
# Attach text data
allure.attach("Test data: xyz", name="Test Input", attachment_type=allure.attachment_type.TEXT)

# Attach JSON data
import json
allure.attach(json.dumps(data), name="API Response", attachment_type=allure.attachment_type.JSON)

# Attach file
allure.attach.file("path/to/file.txt", name="Config File", attachment_type=allure.attachment_type.TEXT)

# Screenshots are automatically attached on failure via conftest.py
```

### Severity Levels
```python
@allure.severity(allure.severity_level.BLOCKER)    # Must fix immediately
@allure.severity(allure.severity_level.CRITICAL)   # Core functionality
@allure.severity(allure.severity_level.NORMAL)     # Default
@allure.severity(allure.severity_level.MINOR)      # Nice to have
@allure.severity(allure.severity_level.TRIVIAL)    # Cosmetic issues
```

### Linking to Test Management
```python
@allure.link("https://jira.example.com/ISSUE-123", name="Related Issue")
@allure.issue("ISSUE-123", "Bug Ticket")
@allure.testcase("TC-456", "Test Case in TMS")
```

## Project Configuration

### pytest.ini Configuration
```ini
addopts = --alluredir=allure-results --clean-alluredir
```

- `--alluredir=allure-results` - Directory to save test results
- `--clean-alluredir` - Clean old results before new test run

### conftest.py Integration
Automatically captures screenshots on test failure and attaches to Allure report:
```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Attach screenshot to Allure on failure
    if rep.failed and 'page' in item.funcargs:
        page = item.funcargs['page']
        screenshot_bytes = page.screenshot()
        allure.attach(screenshot_bytes, ...)
```

## Directory Structure
```
project/
├── allure-results/     # Generated after running tests (JSON data)
├── allure-report/      # Generated HTML report
├── screenshots/        # Traditional screenshot folder (still works)
├── tests/             # Test files
└── conftest.py        # Allure hooks configuration
```

## Viewing Historical Trends

### 1. Keep History
To see trends over multiple test runs, preserve the `history` folder:
```powershell
# Before generating new report, copy history
Copy-Item -Path "allure-report\history" -Destination "allure-results\history" -Recurse -Force

# Then generate report
allure generate allure-results --clean -o allure-report
```

### 2. Automatic History (using serve)
```powershell
# This automatically maintains history
allure serve allure-results
```

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run tests
  run: pytest tests/ -v

- name: Generate Allure Report
  if: always()
  run: allure generate allure-results -o allure-report

- name: Upload Allure Report
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: allure-report
    path: allure-report/
```

## Troubleshooting

### Issue: "allure: command not found"
**Solution:** Install Allure CLI (see Installation section)

### Issue: "No test results found"
**Solution:** Run tests first with `pytest tests/`

### Issue: Screenshots not appearing
**Solution:** 
- Check conftest.py has allure import
- Verify test failures trigger screenshot capture
- Check allure-results/ contains attachments

### Issue: Old test results persist
**Solution:** Use `--clean-alluredir` flag in pytest.ini

### Issue: Report not updating
**Solution:** 
```powershell
# Clean and regenerate
Remove-Item -Recurse -Force allure-report
allure generate allure-results --clean -o allure-report
```

## Best Practices

1. **Use Descriptive Test Names**: Allure uses docstrings and function names
2. **Add Allure Decorators**: Enhance reports with @allure.feature, @allure.story
3. **Use Steps**: Break down complex tests with @allure.step
4. **Set Severity Levels**: Help prioritize test failures
5. **Keep History**: Track trends over time
6. **Screenshot on Failure**: Already automated in conftest.py
7. **Attach Relevant Data**: Use allure.attach for logs, API responses
8. **Organize Tests**: Use features/stories for better structure

## Quick Commands Reference
```powershell
# Run tests with Allure
pytest tests/ -v

# Generate report
allure generate allure-results --clean -o allure-report

# Open report
allure open allure-report

# Serve report (with auto-refresh)
allure serve allure-results

# Clean results
Remove-Item -Recurse -Force allure-results, allure-report

# Run specific test with Allure
pytest tests/test_client.py::test_TC_01 -v

# Run with headed browser
pytest tests/ -v --headed
```

## Benefits Over HTML Report

| Feature | HTML Report | Allure Report |
|---------|-------------|---------------|
| Screenshots | ✅ | ✅ (Better organized) |
| Test History | ❌ | ✅ |
| Trends | ❌ | ✅ |
| Timeline View | ❌ | ✅ |
| BDD Organization | ❌ | ✅ |
| Test Steps | ❌ | ✅ |
| Severity Levels | ❌ | ✅ |
| Categories | ❌ | ✅ |
| Attachments | ✅ | ✅ (Better) |
| Interactive UI | ❌ | ✅ |

## Additional Resources
- Official Documentation: https://docs.qameta.io/allure/
- GitHub: https://github.com/allure-framework/allure2
- Allure Pytest Plugin: https://github.com/allure-framework/allure-python
