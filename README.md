# Black Pigeon Automation Project (BPRP-QA)

[![Playwright Tests](https://github.com/foyezkabir/Playwright_practice_project/actions/workflows/playwright-tests.yml/badge.svg)](https://github.com/foyezkabir/Playwright_practice_project/actions/workflows/playwright-tests.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.54.0-green.svg)](https://playwright.dev/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

Comprehensive end-to-end test automation suite for the Black Pigeon web application using **Playwright** and **Pytest**. This project implements a robust Page Object Model architecture with centralized locators, enhanced assertions, and multiple reporting formats.

## 🎯 Project Overview

- **Test Target**: `https://bprp-qa.shadhinlab.xyz`
- **Architecture**: Page Object Model (POM) with centralized locators
- **Browser Support**: Chromium, Firefox, WebKit
- **Python Version**: 3.8+
- **Framework**: Playwright + Pytest
- **Test Isolation**: Random data generation for conflict-free execution

## ✨ Key Features

### Core Capabilities
- 🔐 **Authentication Testing**: Login, signup, email verification, password reset
- 🏢 **Agency Management**: Complete CRUD operations with validation testing
- 👤 **User Management**: User creation, role assignment, permissions testing
- 🏭 **Company Management**: Company profile, information editing, validation
- 💼 **Client Management**: Client CRUD operations, search, filtering
- 🎯 **Talent Management**: Talent profiles, skills, experience tracking
- 📋 **Job Description (JD) Management**: JD creation, editing, search, filtering, bulk operations

### Advanced Features
- 📸 **Auto Screenshot Capture**: Automatic screenshot on test failures with timestamps
- 📊 **Multiple Report Formats**: HTML (basic), Excel (detailed), Allure (interactive)
- 🎲 **Dynamic Test Data**: Random data generation for test isolation
- ✅ **Enhanced Assertions**: Custom assertion framework with built-in screenshot capture
- 🔍 **Detailed Validation Testing**: Field-level validation for all forms
- 🎭 **Cross-browser Testing**: Support for Chromium, Firefox, and WebKit
- 📦 **File Upload Testing**: Format and size validation with test assets
- 🧹 **Automatic Cleanup**: Session-based cleanup tracking for test data

## 📁 Project Structure

```
playwright-automation/
│
├── .github/                          # GitHub configurations
│   └── copilot-instructions.md      # Project-specific Copilot guidance
│
├── conftest.py                       # Pytest fixtures and hooks
├── pytest.ini                        # Pytest configuration
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore patterns
│
├── 📜 PowerShell Scripts
│   ├── generate_allure_report.ps1   # Generate Allure reports
│   └── run_tests_with_timestamp.ps1 # Run tests with timestamped reports
│
├── 📊 Reports & Results
│   ├── report.html                  # HTML test report
│   ├── reports/                     # Excel reports directory
│   ├── allure-results/              # Allure test results
│   └── allure-report/               # Allure HTML reports
│
├── 📸 screenshots/                   # Test failure screenshots (organized by feature)
│   ├── agency_screenshots/
│   ├── client_screenshots/
│   ├── jd_screenshots/
│   ├── talent_screenshots/
│   └── ...
│
├── 🖼️ images_for_test/              # Test assets for file upload testing
│   ├── jd_files/                    # JD-specific test files
│   ├── doc app.jpg
│   ├── file-PDF_1MB.pdf
│   ├── pexels-6MB.jpg
│   └── ...
│
├── 📚 docs/                          # Comprehensive documentation
│   ├── ALLURE_REPORTING_GUIDE.md
│   ├── CLIENT_LOGIN_DECORATOR_GUIDE.md
│   ├── CLIENT_MODAL_FIELD_DOCUMENTATION.md
│   ├── JD_TEST_EXECUTION_GUIDE.md
│   └── JD_TROUBLESHOOTING_GUIDE.md
│
├── 🎯 locators/                      # Centralized element locators
│   ├── loc_agency.py                # Agency page locators
│   ├── loc_client.py                # Client page locators
│   ├── loc_company.py               # Company page locators
│   ├── loc_email_verify.py          # Email verification locators
│   ├── loc_jd.py                    # Job description locators
│   ├── loc_login.py                 # Login page locators
│   ├── loc_reset_pass.py            # Password reset locators
│   ├── loc_signup.py                # Signup page locators
│   ├── loc_talent.py                # Talent page locators
│   └── loc_user_management.py       # User management locators
│
├── 📄 pages/                         # Page Object Model classes
│   ├── agency_page.py               # Agency page objects
│   ├── client_page.py               # Client page objects
│   ├── company_page.py              # Company page objects
│   ├── email_verify_page.py         # Email verification objects
│   ├── jd_page.py                   # Job description objects
│   ├── login_page.py                # Login page objects
│   ├── reset_pass_page.py           # Password reset objects
│   ├── signup_page.py               # Signup page objects
│   ├── talent_page.py               # Talent page objects
│   └── user_management_page.py      # User management objects
│
├── 🧪 tests/                         # Test cases organized by feature
│   ├── test_agency.py               # Agency CRUD and validation tests
│   ├── test_client.py               # Client management tests
│   ├── test_company_core.py         # Company core functionality tests
│   ├── test_company_info_edit.py    # Company information editing tests
│   ├── test_email_verification.py   # Email verification flow tests
│   ├── test_jd.py                   # Job description comprehensive tests
│   ├── test_login.py                # Login functionality tests
│   ├── test_reset_pass.py           # Password reset flow tests
│   ├── test_signup.py               # Signup registration tests
│   ├── test_talent.py               # Talent management tests
│   └── test_user_management.py      # User management tests
│
├── 🛠️ utils/                         # Helper utilities and configurations
│   ├── config.py                    # Global configuration settings
│   ├── enhanced_assertions.py       # Custom assertion framework
│   ├── screenshot_helper.py         # Screenshot capture utilities
│   │
│   ├── Feature-specific helpers
│   ├── agency_helper.py             # Agency test helpers
│   ├── client_helper.py             # Client test helpers
│   ├── company_helper.py            # Company test helpers
│   ├── email_verify_helper.py       # Email verification helpers
│   ├── jd_helper.py                 # JD test helpers
│   ├── jd_data_manager.py           # JD data management utilities
│   ├── jd_file_test_helper.py       # JD file upload helpers
│   ├── jd_test_data.py              # JD test data utilities
│   ├── jd_test_helpers.py           # Additional JD utilities
│   ├── login_helper.py              # Login test helpers
│   ├── reset_pass_helper.py         # Password reset helpers
│   ├── signup_helper.py             # Signup test helpers
│   ├── talent_helper.py             # Talent test helpers
│   └── user_management_helper.py    # User management helpers
│
└── 🎲 random_values_generator/       # Test data generation modules
    ├── random_agency_name.py        # Agency name generator
    ├── random_company_name.py       # Company name generator
    ├── random_email.py              # Email address generator
    ├── random_jd_data.py            # JD test data generator
    ├── random_role_name.py          # Role name generator
    ├── random_talent_name.py        # Talent name generator
    └── random_user_data.py          # User data generator
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** installed
- **Git** installed
- **PowerShell** (for Windows scripts)
- **Node.js** (optional, for Allure via npm)

### Installation Steps

#### 1. Clone the Repository
```powershell
git clone <your-repo-url>
cd <repository-folder>
```

#### 2. Create and Activate Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate

# Activate (Windows CMD)
.\venv\Scripts\activate.bat

# Activate (Linux/Mac)
source venv/bin/activate
```

#### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

**Installed Packages:**
- `playwright==1.54.0` - Browser automation framework
- `pytest==8.4.1` - Testing framework
- `pytest-playwright==0.7.0` - Playwright pytest integration
- `allure-pytest==2.13.5` - Allure report integration
- `requests==2.32.4` - HTTP library for API testing
- `openpyxl` - Excel report generation (via conftest.py)
- Additional utilities: `python-slugify`, `colorama`, `Pygments`

#### 4. Install Playwright Browsers
```powershell
# Install all browsers (Chromium, Firefox, WebKit)
python -m playwright install

# Or install specific browser
python -m playwright install chromium
```

#### 5. Configure Test Environment (Optional)
Edit `utils/config.py` to customize:
```python
BASE_URL = "https://bprp-qa.shadhinlab.xyz"
BROWSER_NAME = "chromium"  # chromium, firefox, webkit
HEADLESS = False           # Run with visible browser
DEFAULT_TIMEOUT = 15000    # 15 seconds
SLOW_MO = 1000            # Slow down by 1 second for visibility
```

## 🧪 Running Tests

### Basic Test Execution

#### Run All Tests
```powershell
pytest
```

#### Run Specific Test File
```powershell
pytest tests/test_agency.py
pytest tests/test_jd.py
pytest tests/test_client.py
```

#### Run Specific Test Function
```powershell
pytest tests/test_agency.py::test_TC_01_create_agency_with_valid_data
pytest tests/test_jd.py::test_TC_16_search_jd_by_position_title
```

#### Run Tests by Keyword
```powershell
# Run all tests containing "create"
pytest -k "create"

# Run all tests containing "validation"
pytest -k "validation"

# Run agency tests only
pytest -k "agency"
```

#### Run Tests with Verbosity
```powershell
# Verbose output
pytest -v

# Extra verbose with full details
pytest -vv

# Show print statements
pytest -s
```

### Advanced Test Execution

#### Run Tests in Parallel (Faster)
```powershell
# Install pytest-xdist
pip install pytest-xdist

# Run with 4 workers
pytest -n 4
```

#### Run Tests in Headless Mode
```powershell
# Modify pytest.ini or use command line
pytest --browser=chromium --headed=false
```

#### Run Tests with Different Browsers
```powershell
pytest --browser=chromium
pytest --browser=firefox
pytest --browser=webkit
```

#### Run Tests with Custom Markers
```powershell
# Run tests marked with screenshot
pytest -m screenshot

# Run tests marked with cleanup
pytest -m cleanup
```

### PowerShell Scripts (Recommended)

#### Run Tests with Timestamped Reports
```powershell
.\run_tests_with_timestamp.ps1
```
**Features:**
- Runs full test suite
- Generates unique Allure report with timestamp
- Preserves historical test results
- Opens report automatically in browser

#### Generate Allure Report from Existing Results
```powershell
.\generate_allure_report.ps1
```
**Features:**
- Generates report from `allure-results/`
- Opens report in browser
- Validates Allure CLI installation

## 📊 Test Reports

This project generates three types of reports for comprehensive test analysis:

### 1. HTML Report (Built-in)
**Location**: `report.html`

```powershell
# Automatically generated after test run
# Open in browser
start report.html
```

**Features:**
- Self-contained HTML file
- Test execution summary
- Pass/fail statistics
- Error messages and tracebacks
- Quick overview of test results

### 2. Excel Report (Custom)
**Location**: `reports/test_report_<timestamp>.xlsx`

```powershell
# Automatically generated via conftest.py hooks
```

**Features:**
- ✅ Detailed test case descriptions (extracted from docstrings)
- 📊 Pass/Fail status with color coding
- 🎨 Professional formatting with borders and alignment
- 📝 Multiple sheets for different test categories
- 📈 Summary statistics and metrics
- 🕐 Execution timestamps
- 🔗 Test file organization

**Sheet Structure:**
- Test Case ID
- Test Case Name
- Description (from docstrings with "Verify" prefix)
- Status (PASS/FAIL)
- Execution Timestamp

### 3. Allure Report (Interactive - Recommended)
**Location**: `allure-report/index.html`

#### First Time Setup

**Option 1: Using Scoop (Recommended for Windows)**
```powershell
# Install Scoop if not already installed
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Install Allure
scoop install allure
```

**Option 2: Using npm**
```powershell
npm install -g allure-commandline --save-dev
```

**Option 3: Manual Installation**
1. Download from [Allure releases](https://github.com/allure-framework/allure2/releases)
2. Extract and add to PATH

#### Generating Allure Reports

**Method 1: PowerShell Script (Easiest)**
```powershell
# Run tests and generate timestamped report
.\run_tests_with_timestamp.ps1

# Generate report from existing results
.\generate_allure_report.ps1
```

**Method 2: Manual Commands**
```powershell
# Run tests with Allure results
pytest --alluredir=allure-results

# Generate and open report
allure generate allure-results --clean -o allure-report
allure open allure-report
```

**Method 3: Serve Report (Auto-refresh)**
```powershell
# Serve report with auto-refresh
allure serve allure-results
```

#### Allure Report Features

**📊 Overview Dashboard**
- Test execution statistics
- Success rate and trends
- Duration metrics
- Environment information

**📈 Trend Analysis**
- Historical test results
- Flaky test detection
- Duration trends over time
- Success/failure patterns

**🔍 Test Case Details**
- Step-by-step execution breakdown
- Parameter values
- Timing information
- Severity and priority levels

**📷 Attachments**
- Automatic screenshot capture on failures
- Trace files
- Log files
- Custom attachments

**🏷️ Categorization**
- Feature-based organization
- Story grouping
- Epic categorization
- Custom tags and markers

**⚡ Additional Features**
- Timeline view of test execution
- Retry information
- Test suites overview
- Package/module organization
- Behavior-driven documentation

**📖 Documentation**
For comprehensive Allure guide, see `docs/ALLURE_REPORTING_GUIDE.md`

## 🎯 Test Modules Overview

### 1. Authentication & Access Control
**Files**: `test_login.py`, `test_signup.py`, `test_email_verification.py`, `test_reset_pass.py`

**Coverage:**
- ✅ User registration with validation
- ✅ Login functionality (multiple user roles)
- ✅ Email verification flow
- ✅ Password reset with OTP
- ✅ Session management
- ✅ Access control validation

### 2. Agency Management
**Files**: `test_agency.py`, `pages/agency_page.py`, `locators/loc_agency.py`

**Coverage:**
- ✅ Agency CRUD operations
- ✅ Agency profile information
- ✅ Field validation (name, website, file uploads)
- ✅ Image upload with format/size validation
- ✅ Agency search and filtering
- ✅ Pagination handling

**Validation Tests (TC_07-TC_16):**
- Agency name required validation
- Minimum length validation (3 characters)
- Special character validation
- Website URL format validation
- Image format validation (JPG, PNG, JPEG, GIF)
- Image size validation (max 5MB)

### 3. Client Management
**Files**: `test_client.py`, `pages/client_page.py`, `locators/loc_client.py`

**Coverage:**
- ✅ Client creation and editing
- ✅ Client information management
- ✅ Contact details validation
- ✅ Client search functionality
- ✅ Client status management
- ✅ Bulk operations

### 4. Company Management
**Files**: `test_company_core.py`, `test_company_info_edit.py`, `pages/company_page.py`

**Coverage:**
- ✅ Company profile creation
- ✅ Company information editing
- ✅ Company details validation
- ✅ Industry and category management
- ✅ Company settings

### 5. Job Description (JD) Management
**Files**: `test_jd.py`, `pages/jd_page.py`, `locators/loc_jd.py`

**Core CRUD Operations:**
- ✅ JD creation with complete data
- ✅ JD editing and updates
- ✅ Single and bulk JD deletion
- ✅ JD detail viewing
- ✅ JD list display and empty states

**Search & Filter Functionality:**
- ✅ Text search (position title, company, keywords)
- ✅ Company filter
- ✅ Work style filter (Remote, Onsite, Hybrid)
- ✅ Hiring status filter
- ✅ Employment type filter
- ✅ Salary range filter
- ✅ Multiple filter combinations
- ✅ Filter clearing functionality
- ✅ Pagination navigation

**File Operations:**
- ✅ Bulk JD import via file upload
- ✅ Format validation (PDF, DOC, DOCX)
- ✅ Invalid format rejection
- ✅ File size validation

**Validation Testing:**
- ✅ Mandatory fields (position title, company, work style, workplace)
- ✅ Data format validation (salary ranges, age ranges)
- ✅ Character limit validation
- ✅ Business rule validation
- ✅ Cross-field validation

**Documentation:**
- See `docs/JD_TEST_EXECUTION_GUIDE.md` for detailed execution instructions
- See `docs/JD_TROUBLESHOOTING_GUIDE.md` for debugging help

### 6. Talent Management
**Files**: `test_talent.py`, `pages/talent_page.py`, `locators/loc_talent.py`

**Coverage:**
- ✅ Talent profile creation
- ✅ Skills and experience management
- ✅ Talent search and filtering
- ✅ Resume upload and management
- ✅ Talent status updates

### 7. User Management
**Files**: `test_user_management.py`, `pages/user_management_page.py`

**Coverage:**
- ✅ User creation with roles
- ✅ User permission management
- ✅ Role assignment
- ✅ User status management (active/inactive)
- ✅ User search and filtering

## 🏗️ Architecture & Design Patterns

### Page Object Model (POM)
All browser interactions are encapsulated in page classes to maintain clean separation between test logic and UI interactions.

```python
# Example: Agency Page Object
class AgencyPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = AgencyLocators(page)
    
    def click_create_new_agency(self):
        self.locators.create_agency_button.click()
    
    def fill_agency_name(self, name: str):
        self.locators.agency_name_input.fill(name)
```

### Centralized Locators
Element selectors are defined in dedicated locator files, making maintenance easier and reducing duplication.

```python
# Example: Agency Locators
class AgencyLocators:
    def __init__(self, page: Page):
        self.page = page
        self.agency_name_input = page.locator("input[name='agency_name']")
        self.agency_name_required_error = page.get_by_text("Agency name is required")
        self.create_agency_button = page.get_by_role("button", name="Create Agency")
```

### Enhanced Assertion Framework
Custom assertion system with automatic screenshot capture on failures.

```python
from utils.enhanced_assertions import enhanced_assert_visible

# Automatic screenshot on assertion failure
enhanced_assert_visible(
    page,
    locator=agency_page.locators.agency_name_required_error,
    message="Agency name required error should be visible",
    test_name="test_TC_08_name_required"
)
```

**Features:**
- ✅ Automatic screenshot capture with timestamp
- ✅ Test name auto-detection from function context
- ✅ Organized screenshot storage by feature
- ✅ Built-in wait for dynamic elements
- ✅ Detailed error messages with context

### Helper Function Architecture
Complex workflows are abstracted into reusable helper functions.

```python
from utils.agency_helper import do_agency_login, do_create_agency

# Login and navigate to agency page
agency_page = do_agency_login(page, "test@example.com", "Password123")

# Create agency with validation
agency_page = do_create_agency(page, agency_data, verify_creation=True)
```

**Helper Categories:**
- **Login Helpers**: Handle authentication for different user types
- **CRUD Helpers**: Streamline create/read/update/delete operations
- **Validation Helpers**: Specialized validation checking
- **File Upload Helpers**: File upload and validation testing
- **Data Management Helpers**: Test data creation and cleanup

### Dynamic Test Data Generation
Random data generators ensure test isolation and prevent conflicts.

```python
from random_values_generator.random_agency_name import generate_agency_name
from random_values_generator.random_email import generate_random_email
from random_values_generator.random_jd_data import generate_complete_jd_data

# Generate unique test data
agency_name = generate_agency_name()  # "Agency_ab12cd34"
email = generate_random_email()       # "user_ef56gh78@test.com"
jd_data = generate_complete_jd_data() # Complete JD with all fields
```

**Generators Available:**
- `random_agency_name.py` - Unique agency names
- `random_company_name.py` - Company names
- `random_email.py` - Email addresses
- `random_jd_data.py` - Job description data
- `random_role_name.py` - User roles
- `random_talent_name.py` - Talent profiles
- `random_user_data.py` - User information

### Pytest Fixtures & Hooks
`conftest.py` provides project-wide fixtures and hooks for:

**Test Lifecycle Management:**
```python
@pytest.fixture(scope="function")
def page(context):
    """Provides a fresh page for each test"""
    page = context.new_page()
    yield page
    page.close()
```

**Automatic Screenshot Capture:**
```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captures screenshot on test failure"""
    # Auto-capture implementation
```

**Report Generation:**
- HTML report generation via pytest-html
- Excel report generation with test descriptions
- Allure report integration

**Test Data Fixtures:**
- Module-scoped fixtures for shared data
- Function-scoped fixtures for isolation
- Session-scoped cleanup tracking

### Configuration Management
`utils/config.py` centralizes all configuration settings:

```python
# Browser Configuration
BROWSER_NAME = "chromium"
HEADLESS = False
SLOW_MO = 1000

# Timeout Configuration
DEFAULT_TIMEOUT = 15000
NETWORK_IDLE_TIMEOUT = 5000
TOAST_WAIT_TIME = 1500

# Screenshot Configuration
SCREENSHOT_ON_FAILURE = True
FULL_PAGE_SCREENSHOT = True
SCREENSHOT_DELAY = 1

# Base URL
BASE_URL = "https://bprp-qa.shadhinlab.xyz"
```

### Test Markers
Custom pytest markers for test categorization:

```python
# In pytest.ini
markers =
    screenshot: automatically capture screenshot on failure
    cleanup: test cases that clean up test data

# Usage in tests
@pytest.mark.screenshot
@pytest.mark.cleanup
def test_TC_01_create_agency():
    """Verify agency creation with valid data"""
    pass
```

## 🔧 Configuration

### Pytest Configuration (`pytest.ini`)
```ini
[pytest]
markers =
    screenshot: automatically capture screenshot on failure
    cleanup: test cases that clean up test data

addopts = 
    --html=report.html 
    --self-contained-html 
    --alluredir=allure-results 
    --browser=chromium 
    --tb=short 
    --strict-markers 
    -v 
    --clean-alluredir

testpaths = tests 
--slowmo=1000
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

**Key Settings:**
- `--browser=chromium` - Default browser (change to firefox/webkit)
- `--slowmo=1000` - Slow down operations by 1 second for visibility
- `--tb=short` - Shorter traceback format
- `-v` - Verbose output
- `--clean-alluredir` - Clean Allure results before each run

### Application Configuration (`utils/config.py`)
```python
# Environment
BASE_URL = "https://bprp-qa.shadhinlab.xyz"

# Browser Settings
BROWSER_NAME = "chromium"  # chromium, firefox, webkit
HEADLESS = False           # Set True for CI/CD
SLOW_MO = 1000            # Milliseconds to slow down operations

# Timeouts
DEFAULT_TIMEOUT = 15000        # 15 seconds
NETWORK_IDLE_TIMEOUT = 5000    # 5 seconds
TOAST_WAIT_TIME = 1500         # 1.5 seconds
TOAST_TIMEOUT = 5000           # 5 seconds
ERROR_MESSAGE_WAIT = 2000      # 2 seconds

# Screenshot Settings
SCREENSHOT_ON_FAILURE = True
FULL_PAGE_SCREENSHOT = True
SCREENSHOT_DELAY = 1
SCREENSHOT_DATE_FORMAT = "%d-%m-%Y"
SCREENSHOT_TIME_FORMAT = "%H.%M.%S"

# Screenshot Organization
SCREENSHOT_BASE_DIR = "screenshots"
FAILURE_SCREENSHOT_DIR = "failures"

# Performance
PAGE_LOAD_STRATEGY = "networkidle"  # or "domcontentloaded" or "load"
```

### Dependencies (`requirements.txt`)
```
# Core Framework
playwright==1.54.0
pytest==8.4.1
pytest-playwright==0.7.0
pytest-base-url==2.1.0

# Reporting
allure-pytest==2.13.5
allure-python-commons==2.13.5

# Utilities
requests==2.32.4
python-slugify==8.0.4
colorama==0.4.6
Pygments==2.19.2

# Additional Dependencies
certifi==2025.8.3
charset-normalizer==3.4.2
greenlet==3.2.3
idna==3.10
iniconfig==2.1.0
packaging==25.0
pluggy==1.6.0
pyee==13.0.0
text-unidecode==1.3
typing_extensions==4.14.1
urllib3==2.5.0
```

## 🎨 Best Practices

### Test Naming Convention
```python
def test_TC_##_descriptive_name():
    """Verify [specific functionality being tested]"""
    pass
```

**Example:**
```python
def test_TC_01_create_agency_with_valid_data():
    """Verify that agency can be created with valid data"""
    pass
```

### Locator Strategy Priority
1. **Text Locators**: `page.get_by_text("exact text")` for messages
2. **Role Locators**: `page.get_by_role("button", name="exact name")` for buttons
3. **CSS/XPath**: `page.locator()` only when no alternatives exist

**Always use exact text - never use `exact=False`**

### Assertion Pattern
```python
# Direct enhanced assertion (recommended)
enhanced_assert_visible(
    page,
    agency_page.locators.success_message,
    "Success message should be visible",
    "test_TC_01_create_agency"
)
```

### Test Structure
```python
def test_TC_01_feature_description():
    """Verify specific behavior."""
    # 1. Setup/Login
    agency_page = do_agency_login(page, email, password)
    time.sleep(2)
    
    # 2. Perform Actions
    agency_page.click_create_button()
    agency_page.fill_form(data)
    agency_page.click_save()
    time.sleep(2)
    
    # 3. Assert Results
    enhanced_assert_visible(page, agency_page.locators.success_msg, "Success", "test_name")
    
    # 4. Cleanup
    agency_page.click_close_button()
```

### Helper Function Usage
```python
# Use helpers for complex workflows
from utils.agency_helper import do_create_agency_with_verification

# One line replaces 10+ lines of setup
agency_page = do_create_agency_with_verification(page, agency_data)
```

### Test Data Management
```python
# Module-scoped fixture for shared data
@pytest.fixture(scope="module")
def agency_test_data():
    return generate_agency_name()

# Function-scoped for unique data per test
@pytest.fixture(scope="function")
def fresh_agency_data():
    return generate_agency_name()
```

## 📝 Documentation

Comprehensive guides available in `docs/` directory:

- **`ALLURE_REPORTING_GUIDE.md`** - Complete Allure setup and usage
- **`CLIENT_LOGIN_DECORATOR_GUIDE.md`** - Client authentication patterns
- **`CLIENT_MODAL_FIELD_DOCUMENTATION.md`** - Client form field reference
- **`JD_TEST_EXECUTION_GUIDE.md`** - Job description test execution
- **`JD_TROUBLESHOOTING_GUIDE.md`** - JD test debugging help

## 🐛 Troubleshooting

### Installation Issues

#### Playwright Browsers Not Installed
```powershell
python -m playwright install
# Or specific browser
python -m playwright install chromium
```

#### Import Errors
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### Allure Command Not Found
```powershell
# Check installation
allure --version

# Install via Scoop
scoop install allure

# Or via npm
npm install -g allure-commandline
```

### Test Execution Issues

#### Tests Hanging or Timing Out
- Increase timeout in `utils/config.py`: `DEFAULT_TIMEOUT = 30000`
- Check network connectivity to test environment
- Verify test environment is accessible

#### Screenshots Not Captured
- Verify `SCREENSHOT_ON_FAILURE = True` in `utils/config.py`
- Check `screenshots/` directory permissions
- Ensure tests are using `@pytest.mark.screenshot`

#### Modal Not Opening
- Verify element is visible: `element.is_visible()`
- Add wait: `page.wait_for_selector("selector", state="visible")`
- Check for overlapping elements or z-index issues

#### Element Not Found Errors
- Update locators in `locators/loc_*.py` files
- Use Playwright inspector: `pytest --headed --slowmo=1000`
- Verify element exists on page: use browser DevTools

#### Validation Errors Not Appearing
- Wait for validation: `time.sleep(1)` after form submit
- Check specific error locators in locator files
- Verify validation is triggered (form must be submitted)

### Data Issues

#### Test Data Conflicts
- Use function-scoped fixtures for unique data
- Clear test data between runs
- Use random data generators consistently

#### Login Failures
- Verify credentials in helper files
- Check user permissions and roles
- Ensure test environment is available

#### File Upload Issues
- Verify files exist in `images_for_test/` directory
- Check file paths are correct (absolute or relative)
- Ensure file format matches expectations

### Performance Issues

#### Slow Test Execution
```python
# Reduce slowmo in pytest.ini
--slowmo=0

# Run in headless mode
HEADLESS = True  # in utils/config.py

# Use parallel execution
pytest -n 4  # requires pytest-xdist
```

#### Memory Issues
- Close browser contexts after tests
- Limit parallel execution workers
- Clear test data regularly

### Debugging Tips

**1. Use Playwright Inspector**
```powershell
$env:PWDEBUG=1
pytest tests/test_agency.py::test_TC_01
```

**2. Enable Verbose Logging**
```powershell
pytest -vv -s
```

**3. Check Screenshots**
```powershell
# Screenshots saved in feature-specific folders
dir screenshots\agency_screenshots\
```

**4. Review Test Reports**
- HTML: `report.html`
- Excel: `reports/test_report_*.xlsx`
- Allure: `allure-report/index.html`

**5. Validate Page State**
```python
# Add debug prints
print(f"Current URL: {page.url}")
print(f"Page title: {page.title()}")

# Take manual screenshot
page.screenshot(path="debug.png")
```

**6. Use Trace Viewer**
```python
# Enable tracing in conftest.py
context.tracing.start(screenshots=True, snapshots=True)
# ... test execution ...
context.tracing.stop(path="trace.zip")

# View trace
playwright show-trace trace.zip
```

## 🚀 CI/CD Integration

### ✅ GitHub Actions - Fully Implemented

This project includes a complete CI/CD pipeline using GitHub Actions that automatically runs tests on every push and pull request.

**Workflow File**: `.github/workflows/playwright-tests.yml`

#### Features
- 🔄 **Automatic Test Execution**: Runs on push to master/main/develop branches and all PRs
- 🌐 **GitHub Pages Deployment**: Allure reports automatically published
- 📦 **Artifact Upload**: Reports and screenshots stored for 30 days
- 🔀 **Multi-Browser Support**: Configurable browser matrix
- ⏱️ **Historical Tracking**: Keeps last 20 test reports
- 🔔 **Email Notifications**: Automatic failure notifications

#### Quick Setup (3 Steps)

1. **Enable GitHub Pages**
   - Go to repository **Settings** → **Pages**
   - Source: `gh-pages` branch, `/ (root)` folder
   - Save

2. **Set Permissions**
   - Go to **Settings** → **Actions** → **General**
   - Workflow permissions: **"Read and write permissions"**
   - Save

3. **Push to Trigger**
   ```powershell
   git push origin master
   ```

#### View Results
- **Actions Tab**: See live test execution and logs
- **GitHub Pages**: `https://<username>.github.io/<repo>/allure-report`
- **Artifacts**: Download reports, screenshots from Actions tab

#### Configuration
The workflow automatically:
- ✅ Detects CI environment and runs in headless mode
- ✅ Installs Python 3.11 and dependencies
- ✅ Installs Playwright browsers
- ✅ Runs all tests with Allure reporting
- ✅ Uploads artifacts (reports, screenshots)
- ✅ Deploys Allure report to GitHub Pages

**Automatic Headless Mode** (Already implemented):
```python
# In utils/config.py - automatically detects CI environment
import os
HEADLESS = os.getenv("CI", "false").lower() == "true"
```

📖 **Complete Guide**: See `docs/CI_CD_SETUP_GUIDE.md` for detailed setup instructions, troubleshooting, and customization options.

## 📊 Test Coverage Summary

| Module | Test File | Test Cases | Coverage |
|--------|-----------|------------|----------|
| Authentication | `test_login.py` | 10+ | Login, logout, session |
| Signup | `test_signup.py` | 8+ | Registration, validation |
| Email Verify | `test_email_verification.py` | 5+ | OTP, verification flow |
| Password Reset | `test_reset_pass.py` | 12+ | Reset flow, OTP validation |
| Agency | `test_agency.py` | 16+ | CRUD, validation, file upload |
| Client | `test_client.py` | 15+ | Client management, search |
| Company | `test_company_*.py` | 20+ | Profile, info editing |
| Job Description | `test_jd.py` | 25+ | CRUD, search, filter, bulk ops |
| Talent | `test_talent.py` | 10+ | Talent profiles, skills |
| User Management | `test_user_management.py` | 8+ | User CRUD, roles |

**Total Test Cases: 120+**

## 🔐 Security & Credentials

**⚠️ Important Notes:**
- Test credentials are hardcoded for QA environment only
- Never commit production credentials
- Use environment variables for sensitive data in production
- Rotate test credentials regularly

**Test Accounts:**
```python
# Located in helper files (utils/*_helper.py)
# Agency users
EMAIL_AGENCY = "50st3o@mepost.pw"
PASSWORD = "Kabir123#"

# Other test users
EMAIL_CLIENT = "gi7j8d@mepost.pw"
# Additional test users in respective helpers
```

## 🤝 Contributing

### Code Style Guidelines
- Follow PEP 8 Python style guide
- Use type hints where applicable
- Add docstrings to all test functions
- Start test descriptions with "Verify"
- Keep functions focused and single-purpose

### Adding New Tests
1. Create test file in `tests/` directory
2. Create page object in `pages/` directory
3. Define locators in `locators/` directory
4. Add helper functions in `utils/` directory
5. Add random data generator if needed
6. Follow existing naming conventions
7. Add comprehensive docstrings
8. Use enhanced assertions for verification
9. Implement cleanup if test creates data

### Pull Request Guidelines
- Write clear, descriptive commit messages
- Include test coverage for new features
- Update README if adding new functionality
- Ensure all tests pass before submitting
- Add screenshots for UI changes
- Update documentation as needed

## 📚 Learning Resources

### Playwright Documentation
- [Playwright Python](https://playwright.dev/python/docs/intro) - Official documentation
- [Playwright API](https://playwright.dev/python/docs/api/class-playwright) - API reference
- [Best Practices](https://playwright.dev/python/docs/best-practices) - Recommended patterns
- [Locators Guide](https://playwright.dev/python/docs/locators) - Element selection

### Pytest Documentation
- [Pytest Documentation](https://docs.pytest.org/en/stable/) - Official guide
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html) - Fixture guide
- [Pytest Markers](https://docs.pytest.org/en/stable/mark.html) - Marker usage

### Allure Documentation
- [Allure Framework](https://docs.qameta.io/allure/) - Official documentation
- [Allure Pytest](https://docs.qameta.io/allure/#_pytest) - Pytest integration
- [Allure Reports](https://docs.qameta.io/allure-report/) - Report features

## 🎯 Project Highlights

### Why This Framework?
✅ **Maintainable**: Page Object Model with centralized locators  
✅ **Scalable**: Easy to add new tests and features  
✅ **Reliable**: Enhanced assertions with auto-screenshot  
✅ **Comprehensive**: Multiple report formats for different needs  
✅ **Isolated**: Random data generation prevents conflicts  
✅ **Well-Documented**: Extensive inline and external documentation  
✅ **CI/CD Ready**: Headless mode and environment configurations  
✅ **Best Practices**: Follows industry standards and patterns  

### Technology Stack
- **Test Framework**: Pytest 8.4.1
- **Automation Tool**: Playwright 1.54.0
- **Language**: Python 3.8+
- **Reporting**: Allure, HTML, Excel
- **Version Control**: Git
- **CI/CD**: GitHub Actions compatible

## 📞 Support & Contact

### Getting Help
1. Check this README for common issues
2. Review documentation in `docs/` directory
3. Check test execution logs and screenshots
4. Review Allure reports for detailed insights

### Reporting Issues
When reporting issues, include:
- Test name and file location
- Error message and traceback
- Screenshots from failure (if available)
- Steps to reproduce
- Environment details (OS, Python version, Playwright version)

## 📄 License

This project is created for automated testing of the Black Pigeon application (BPRP-QA).

## 🏆 Acknowledgments

Built with:
- [Playwright](https://playwright.dev/) - Modern browser automation
- [Pytest](https://pytest.org/) - Python testing framework
- [Allure](https://docs.qameta.io/allure/) - Beautiful test reports

---

**Project Status**: ✅ Active Development  
**Last Updated**: December 2025  
**Version**: 1.0.0  

For questions or support, please contact the project maintainer.
