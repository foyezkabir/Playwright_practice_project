# Copilot Instructions for Black Pigeon Automation Project

## STRICT REQUIREMENTS - MUST FOLLOW
⚠️ **CRITICAL:** These project structure conventions are MANDATORY and must be followed in any way:
- **Project Structure:** MUST follow the existing project structure - never reorganize or move core directories (`pages/`, `locators/`, `tests/`, `utils/`, etc.)
- **File Structure:** MUST follow the current file naming and organization patterns - maintain existing file locations and naming conventions
- **Code Structure:** MUST follow the established code architecture - Page Object Model, centralized locators, helper functions, and import organization patterns are non-negotiable
- **Locator Strategy:** Use `page.get_by_text("exact text")` for validation messages and success messages. Use `page.get_by_role("button", name="exact name")` for buttons. Only use `page.locator()` when no other alternatives exist. Always include exact text in locators - never use `exact=False`.

## Project Overview
- End-to-end test automation suite for Black Pigeon web app (BPRP-QA) using Playwright + Pytest
- Test target: `https://bprp-qa.shadhinlab.xyz` with real user accounts and data
- Architecture: Page Object Model with centralized locators, helper utilities, and enhanced assertions
- Major components: `pages/` (page objects), `locators/` (selectors), `tests/` (test cases), `utils/` (helpers), `random_values_generator/` (test data), `screenshots/` (artifacts)

## Critical Patterns & Conventions
- **Page Object Model:** All browser interactions go through page classes (`pages/agency_page.py`). Never use raw selectors in tests.
- **Centralized Locators:** Element selectors live in `locators/loc_*.py` files. Example: `self.locators.agency_name_input` not `page.locator("input[name='agency']")`
- **Specific Validation Locators:** Each validation message has its own locator: `self.agency_name_required_error = page.get_by_text("Agency name is required")`
- **Direct Enhanced Assertions:** Use `enhanced_assert_visible(page, agency_page.locators.specific_error, "Message", "test_name")` directly in tests
- **Test Naming:** Functions follow `test_TC_##_descriptive_name` pattern with docstrings starting with "Verify"
- **Data Generation:** Use `random_values_generator/` for unique test data to avoid conflicts between test runs
- **Import Organization:** All helper imports at top of test files, never inline imports

## Essential Workflows
- **Environment Setup:** `python -m venv venv` → `.\venv\Scripts\Activate` → `pip install -r requirements.txt` → `python -m playwright install`
- **Run Tests:** `pytest` (all) | `pytest -k test_agency` (subset) | `pytest tests/test_agency.py::test_TC_04` (specific)
- **Debug Failures:** Check `screenshots/` folder (organized by feature) and `report.html` for detailed results
- **Configuration:** All browser/timing settings in `pytest.ini` and `utils/config.py` - never hardcode in tests

## Current Validation Test Pattern (TC_07-TC_12)
```python
def test_TC_08(page: Page):
    """Verify that submitting form without agency name shows validation error."""
    agency_page = do_agency_login(page, "50st3o@mepost.pw", "Kabir123#")
    time.sleep(2)
    agency_page.click_create_new_agency()
    time.sleep(1)
    
    # Leave agency name empty and try to save
    agency_page.click_agency_save_button()
    time.sleep(2)
    
    # Check for specific validation error directly
    enhanced_assert_visible(page, agency_page.locators.agency_name_required_error, "Agency name required error should be visible", "test_TC_08_name_required")
    
    # Close modal
    agency_page.click_close_modal_button()
```

## Validation Message Locators
- **Agency Name Required:** `self.agency_name_required_error = page.get_by_text("Agency name is required")`
- **Agency Name Min Length:** `self.agency_name_min_length_error = page.get_by_text("Agency name must be at least 3 characters")`
- **Special Characters:** `self.agency_name_special_char_error = page.get_by_text("Agency Name not start or end with special characters.")`
- **Website Validation:** `self.invalid_website_url_error = page.get_by_text("Please enter a valid website URL")`
- **File Format:** `self.file_format_error = page.get_by_text("Only accept jpg, png, jpeg, gif file")`
- **File Size:** `self.file_size_error = page.get_by_text("File can't be larger than 5 MB")`

## Enhanced Assertions System
- **Purpose:** Automatic screenshot capture on assertion failures with timestamp
- **Usage:** `enhanced_assert_visible(page, locator, "Error message", "test_name")` 
- **Auto-detection:** Test name auto-detected from function name if not provided
- **Screenshot Location:** `screenshots/{feature}_screenshots/{test_name}_{timestamp}.png`
- **Timing:** Built-in 1-second wait for toast messages to appear before assertion

## Key Integration Points
- **Shared Test Data:** `@pytest.fixture(scope="module")` for agency names shared across test functions in same file
- **Login Management:** Helper functions handle different user types: `do_agency_login()`, `do_login()` with pre-configured credentials
- **Network Handling:** `wait_for_action_completion(page, action_type)` for reliable waits after save/update operations
- **Duplicate Element Handling:** Use `.first` for multiple elements with same text to avoid Playwright strict mode violations

## Test Development Patterns
- **Validation Tests:** Direct locator assertions - trigger validation → use specific locator → close modal
- **Success Messages:** Use specific success locators like `agency_created_successfully_message`
- **CRUD Operations:** Use helper functions (`do_create_agency`) → verify with pagination search → cleanup with deletion
- **File Upload Tests:** Use `agency_page.upload_file("images_for_test/file.pdf")` with files in `images_for_test/`
- **Timing Strategy:** Use `time.sleep()` for UI transitions, `enhanced_assert_visible()` for element waits, `wait_for_action_completion()` for network operations

## Helper Function Architecture
- **Centralized Workflows:** Complex operations abstracted in `utils/*_helper.py` (e.g., `do_create_agency_with_image_verification()`)
- **Assertion Helpers:** Feature-specific assertion functions using `enhanced_assert_visible()` internally
- **File Validation:** `assert_file_format_validation_message()` and `assert_file_size_validation_message()` for TC_15/TC_16
- **Generic Helpers:** Available but prefer specific locator assertions for reliability

## Test Data Management
- **Login Credentials:** Hardcoded in helpers for QA environment (`"50st3o@mepost.pw"`, `"gi7j8d@mepost.pw"`)
- **Dynamic Data:** Generated via `random_values_generator/` to ensure unique names/emails per test run
- **File Assets:** Test images stored in `images_for_test/` including validation files (`file-PDF_1MB.pdf`, `pexels-6MB.jpg`)
- **Mandatory vs Optional Fields:** Validation tests use only mandatory fields (agency name + industry), full tests use all fields

## Recent Architecture Evolution
- **Specific Locator Strategy:** Moved from generic validation detection to specific validation message locators
- **Direct Enhanced Assertions:** Tests now use `enhanced_assert_visible()` directly instead of helper wrapper functions
- **Cleaner Locator Definitions:** Removed duplicate and unused locators, kept only active ones
- **Simplified Test Structure:** Reduced helper function complexity, made tests more readable and maintainable

---
**Key File References:** 
- `conftest.py` (fixtures)
- `utils/enhanced_assertions.py` (screenshot system)
- `utils/config.py` (settings)
- `pytest.ini` (test runner config)
- `locators/loc_agency.py` (specific validation locators)
- `tests/test_agency.py` (current validation patterns TC_07-TC_12)
