# Company Profile Test Automation

## Overview
This test suite implements comprehensive end-to-end testing for the **Client Company Profile** workflow in the Black Pigeon BPRP-QA application. It covers company creation, validation, editing, and client management functionality.

## Test Credentials
- **URL**: `https://bprp-qa.shadhinlab.xyz/`
- **Email**: `nua26i@onemail.host`
- **Password**: `Kabir123#`

## Test Files Structure

### 1. Locators (`locators/loc_company.py`)
Contains all element locators for company-related functionality:
- **Navigation locators**: Company tab, agency cards, breadcrumbs
- **Form locators**: Input fields, dropdowns, buttons
- **Validation locators**: Success messages, error messages
- **Action locators**: View details, edit, delete buttons

### 2. Page Objects (`pages/company_page.py`)
Implements the Page Object Model for company interactions:
- **Navigation methods**: Login, tab switching, conditional navigation
- **Form interaction methods**: Fill fields, select options, submit forms
- **Validation methods**: Check errors, verify success messages
- **Action methods**: Edit, delete, create clients

### 3. Helper Functions (`utils/company_helper.py`)
Utility functions for common company test workflows:
- **Login helpers**: `do_company_login()`
- **Navigation helpers**: `navigate_to_company_creation_form()`
- **Creation helpers**: `create_company_with_basic_info()`, `create_company_with_full_info()`
- **Assertion helpers**: `assert_company_created_successfully()`, validation error assertions
- **Action helpers**: Edit company, create clients, find companies in list

### 4. Test Data Generator (`random_values_generator/random_company_name.py`)
Generates unique test data to avoid conflicts:
- **Unique names**: `generate_company_name()` with timestamps
- **Industry-specific names**: `generate_company_name_with_industry()`
- **Test constants**: Predefined test cases for validation scenarios

### 5. Test Cases (`tests/test_company.py`)
Comprehensive test suite covering all requirements:

## Test Cases Overview

### Setup & Navigation Tests
- **TC_01**: Login and conditional navigation to company creation form
- **TC_02**: Happy path - Create company with valid data (Innovatech Solutions)

### Validation Tests  
- **TC_03**: Duplicate company name validation
- **TC_04**: Required field validation (empty company name)
- **TC_05**: Format validation (min/max length, special characters)
- **TC_09**: Industry field required validation

### CRUD Operations
- **TC_06**: Edit company information
- **TC_07**: Create client under a company
- **TC_08**: Create company with all optional fields

### Advanced Scenarios
- **TC_10**: Multiple companies workflow
- **TC_11**: Performance testing
- **TC_12**: Error handling and recovery

## Key Features

### Conditional Navigation Logic
The tests handle two navigation scenarios based on account state:

**Single Agency (Agency Details Page)**:
```
Login → Agency Details Page → Company Tab → Add New Company
```

**Multiple Agencies (All Agencies Page)**:
```
Login → All Agencies Page → Select "Test this agency" → Company Tab → Add New Company
```

### Validation Coverage
- **Company Name Validation**:
  - Required field validation
  - Duplicate name detection
  - Minimum length (3 characters)
  - Maximum length (80 characters)
  - Special character restrictions
- **Industry Validation**: Required field
- **Optional Fields**: Website, Address, Owner, Division

### Enhanced Assertions
Uses `enhanced_assert_visible()` for:
- Automatic screenshot capture on failures
- Proper timing for toast messages
- Detailed error reporting with test context

### Test Data Management
- **Unique names**: Timestamp-based generation prevents conflicts
- **Cleanup considerations**: Test data can be reviewed/cleaned up
- **Reusable fixtures**: Shared test data across test methods

## Running the Tests

### Individual Test Cases
```bash
# Run specific test
pytest tests/test_company.py::test_TC_01_login_and_navigate_to_company_creation -v

# Run happy path test
pytest tests/test_company.py::test_TC_02_create_company_happy_path -v

# Run validation tests
pytest tests/test_company.py -k "validation" -v
```

### Full Test Suite
```bash
# Run all company tests
pytest tests/test_company.py -v

# Run with detailed output
pytest tests/test_company.py -v -s
```

### Debug Mode
```bash
# Run with screenshots and detailed logs
pytest tests/test_company.py --headed --slowmo=1000 -v
```

## Expected Test Flow

1. **TC_01**: Establishes login and navigation patterns
2. **TC_02**: Creates a company (stored in `created_company_name` fixture)
3. **TC_03**: Tests duplicate validation using the company from TC_02
4. **TC_04-TC_05**: Validation edge cases
5. **TC_06**: Edits the company from TC_02
6. **TC_07**: Creates a client under the edited company
7. **TC_08-TC_12**: Additional scenarios and edge cases

## Screenshot Management
Failed assertions automatically capture screenshots to:
```
screenshots/general_screenshots/test_name_DD-MM-YYYY_HH.MM.SS.png
```

## Validation Messages Reference
The system validates against these specific messages:
- **Success**: "Company created successfully", "Company info updated successfully"
- **Errors**: "Company name already exists", "Company name is required", "Industry is required"
- **Format**: Min/max length errors, special character restrictions

## Integration Points
- **Login Flow**: Integrates with existing `utils/login_helper.py`
- **Enhanced Assertions**: Uses project's `utils/enhanced_assertions.py`
- **Configuration**: Respects `utils/config.py` and `pytest.ini` settings
- **Reporting**: Compatible with existing HTML reporting system

This test suite provides comprehensive coverage of the company profile workflow while following the established project patterns and conventions.
