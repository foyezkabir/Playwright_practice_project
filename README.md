# Black Pigeon Automation Project

This project automates end-to-end testing for the Black Pigeon web application using Playwright and Pytest.

## Features
- Automated browser tests for login, signup, agency management, email verification, password reset, and more
- **Job Description (JD) Management**: Complete automation for JD creation, editing, deletion, search, filtering, and bulk operations
- Screenshots on test failures
- **Multiple Report Formats**: HTML reports, Excel reports, and interactive Allure reports
- Random data generation for test isolation

## Project Structure
```
├── complete_automation.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── report.html
├── inputs/
├── locators/
│   ├── loc_jd.py                    # JD page element locators
│   └── ...
├── pages/
│   ├── jd_page.py                   # JD page object model
│   └── ...
├── random_values_generator/
│   ├── random_jd_data.py            # JD test data generation
│   └── ...
├── screenshots/
│   ├── jd_screenshots/              # JD test failure screenshots
│   └── ...
├── tests/
│   ├── test_jd.py                   # JD automation test cases
│   └── ...
├── utils/
│   ├── jd_helper.py                 # JD helper functions
│   ├── jd_data_manager.py           # JD data management utilities
│   ├── jd_file_test_helper.py       # JD file upload test utilities
│   └── ...
├── images_for_test/
│   └── jd_files/                    # Test files for JD upload functionality
```

## Setup Instructions

### 1. Clone the Repository
```powershell
git clone <your-repo-url>
cd "Projects - Shadhin/black pigeon"
```

### 2. Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

### 3. Install Requirements
```powershell
pip install -r requirements.txt
```

### 4. Install Playwright Browsers
```powershell
python -m playwright install
```

### 5. Run Tests
```powershell
pytest
```
Or for a specific test:
```powershell
pytest -k test_agency_01_verify_agency_modal_appearing_in_first_time_login
```

### 6. View Test Reports
After running tests, you can view reports in multiple formats:

**HTML Report** (Basic):
```powershell
# Open report.html in browser
start report.html
```

**Allure Report** (Interactive - Recommended):
```powershell
# Quick method - Run tests and generate report
.\run_tests_with_allure.ps1

# Or generate report from existing results
.\generate_allure_report.ps1

# Or run specific test with Allure
pytest tests/test_client.py -v
.\generate_allure_report.ps1
```

**First Time Allure Setup**:
1. Install Allure CLI (choose one method):
   ```powershell
   # Using Scoop (recommended)
   scoop install allure
   
   # Using npm
   npm install -g allure-commandline
   ```

2. See `docs/ALLURE_REPORTING_GUIDE.md` for comprehensive Allure documentation

**Allure Report Features**:
- 📊 Visual dashboard with test statistics
- 📈 Historical trends and test duration graphs
- 🔍 Detailed test case information with steps
- 📷 Automatic screenshot attachment on failures
- 🏷️ Test categorization by features and stories
- ⚡ Flaky test detection
- 🎯 Test retries and execution timeline

## JD (Job Description) Automation

The JD automation module provides comprehensive testing for job description management functionality within the Black Pigeon system.

### JD Test Coverage

#### Core CRUD Operations
- **JD Creation**: Test JD creation with valid/invalid data, mandatory field validation
- **JD Editing**: Test JD updates, pre-filled form validation, edit cancellation
- **JD Deletion**: Test single and bulk deletion with confirmation dialogs
- **JD Viewing**: Test JD list display, detail views, empty state handling

#### Search and Filter Functionality
- **Search**: Text search across JD titles, companies, and keywords
- **Filters**: Company, work style, hiring status, employment type, salary range filters
- **Filter Combinations**: Multiple filter combinations and clearing functionality
- **Pagination**: Navigation through large JD datasets

#### File Operations
- **File Upload**: Bulk JD import via file upload with format validation
- **File Validation**: Test valid formats (PDF, DOC, DOCX) and invalid format rejection
- **File Size Validation**: Test file size limits and error handling

#### Validation Testing
- **Mandatory Fields**: Position title, company, work style, workplace validation
- **Data Format**: Salary ranges, age ranges, character limits validation
- **Business Rules**: Cross-field validation and business logic testing

### Running JD Tests

#### Run All JD Tests
```powershell
pytest tests/test_jd.py -v
```

#### Run Specific JD Test Categories
```powershell
# JD Creation Tests
pytest tests/test_jd.py -k "create" -v

# JD Search Tests  
pytest tests/test_jd.py -k "search" -v

# JD Filter Tests
pytest tests/test_jd.py -k "filter" -v

# JD Validation Tests
pytest tests/test_jd.py -k "validation" -v

# JD File Upload Tests
pytest tests/test_jd.py -k "upload" -v
```

#### Run Specific JD Test Cases
```powershell
# Test JD creation with valid data
pytest tests/test_jd.py::test_TC_01_create_jd_with_valid_data -v

# Test mandatory field validation
pytest tests/test_jd.py::test_TC_05_position_title_required_validation -v

# Test search functionality
pytest tests/test_jd.py::test_TC_16_search_jd_by_position_title -v
```

### JD Test Data

The JD automation uses dynamic test data generation to ensure test isolation and prevent conflicts:

#### Test Data Types
- **Complete JD Data**: Full JD with all optional fields populated
- **Minimal JD Data**: Only mandatory fields for basic testing
- **Invalid Data Cases**: Various invalid data scenarios for validation testing
- **Bulk Data**: Large datasets for performance and pagination testing

#### Test Data Generation
```python
from random_values_generator.random_jd_data import (
    generate_complete_jd_data,
    generate_minimal_jd_data,
    generate_invalid_jd_data_cases
)

# Generate test data
jd_data = generate_complete_jd_data()
minimal_jd = generate_minimal_jd_data()
invalid_cases = generate_invalid_jd_data_cases()
```

### JD Test Files and Assets

#### Test Files for Upload Testing
Located in `images_for_test/jd_files/`:
- **Valid Files**: PDF, DOC, DOCX files for successful upload testing
- **Invalid Files**: Unsupported formats for error handling testing
- **Size Test Files**: Files of various sizes for size validation testing

#### JD Screenshots
Test failure screenshots are automatically captured in `screenshots/jd_screenshots/` with descriptive filenames including test case and timestamp.

### JD Helper Functions

The JD automation includes comprehensive helper functions for common workflows:

```python
from utils.jd_helper import (
    do_jd_login,
    do_create_jd,
    do_search_and_verify_jd,
    do_apply_jd_filters,
    do_delete_jd
)

# Example usage
jd_page = do_jd_login(page, email, password, agency_id)
jd_page, success = do_create_jd(page, jd_data, agency_id)
jd_page = do_search_and_verify_jd(page, "Software Engineer")
```

### JD Test Configuration

JD tests use the same configuration as other tests but include specific fixtures:

#### JD-Specific Fixtures
- `jd_test_data`: Module-scoped test data for consistent testing
- `fresh_jd_data`: Function-scoped unique data for each test
- `jd_bulk_data`: Large datasets for bulk operation testing
- `jd_validation_data`: Invalid data cases for validation testing
- `jd_cleanup_tracker`: Session-scoped cleanup tracking

#### JD Test Markers
```python
@pytest.mark.screenshot  # Automatic screenshot on failure
@pytest.mark.cleanup     # Test data cleanup required
```

## Notes
- All test configuration is in `pytest.ini`.
- Screenshots are saved in the `screenshots/` folder on failures.
- You can adjust browser type and slowmo in `pytest.ini`.

## Troubleshooting

### General Issues
- If Playwright browsers are not installed, run `python -m playwright install` again.
- If you see import errors, ensure your virtual environment is activated.

### JD-Specific Issues

#### JD Test Failures
- **Modal Not Opening**: Ensure the "Add JD" button is visible and clickable
- **Form Validation Errors**: Check that mandatory fields are properly filled
- **Search Not Working**: Verify search input is properly focused and search term is entered
- **Filter Issues**: Ensure filter panel opens and filter options are available

#### JD File Upload Issues
- **File Upload Fails**: Check file exists in `images_for_test/jd_files/` directory
- **Invalid Format Errors**: Ensure test files have correct extensions for validation testing
- **File Size Issues**: Verify test files are appropriate sizes for size validation tests

#### JD Data Issues
- **Test Data Conflicts**: Use `fresh_jd_data` fixture for tests requiring unique data
- **Cleanup Issues**: Check `jd_cleanup_tracker` fixture is properly implemented
- **Random Data Errors**: Ensure `random_jd_data.py` functions are working correctly

#### JD Page Navigation Issues
- **Agency Context**: Ensure correct agency_id is used for JD page navigation
- **Login Issues**: Verify login credentials and agency permissions
- **URL Issues**: Check JD page URL format matches expected pattern

#### Common JD Test Debugging Steps
1. **Check Screenshots**: Review failure screenshots in `screenshots/jd_screenshots/`
2. **Verify Test Data**: Ensure test data is valid and properly formatted
3. **Check Page State**: Verify page is in expected state before test actions
4. **Review Logs**: Check console output for detailed error messages
5. **Validate Locators**: Ensure JD locators in `loc_jd.py` are accurate

#### JD Performance Issues
- **Slow Tests**: Reduce `slowmo` setting in pytest.ini for faster execution
- **Timeout Issues**: Increase timeout values in `utils/config.py` if needed
- **Memory Issues**: Use smaller datasets for bulk operation testing

## Useful Links
- [Playwright Python Docs](https://playwright.dev/python/docs/intro)
- [Pytest Docs](https://docs.pytest.org/en/stable/)

---
For any issues, please contact the project maintainer.
