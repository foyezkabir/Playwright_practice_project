# Design Document

## Overview

The JD (Job Description) automation design follows the established Page Object Model (POM) architecture used throughout the Black Pigeon automation project. The design maintains consistency with existing patterns while providing comprehensive test coverage for all JD management functionalities including CRUD operations, search, filtering, pagination, and bulk operations.

## Architecture

### Page Object Model Structure

The JD automation follows the three-layer architecture:

1. **Locators Layer** (`locators/loc_jd.py`)
   - Centralized element selectors using Playwright's recommended locator strategies
   - Specific validation message locators for enhanced error handling
   - Dynamic locators for data-driven testing

2. **Page Object Layer** (`pages/jd_page.py`)
   - Business logic and user interactions
   - Method encapsulation for all JD operations
   - Integration with locators and helper functions

3. **Test Layer** (`tests/test_jd.py`)
   - Test cases following TC_## naming convention
   - Direct use of enhanced assertions
   - Minimal logic, maximum readability

### Helper Integration

- **JD Helper** (`utils/jd_helper.py`): Complex workflows and reusable operations
- **Enhanced Assertions** (`utils/enhanced_assertions.py`): Automatic screenshot capture on failures
- **Random Data Generator** (`random_values_generator/random_jd_data.py`): Dynamic test data generation

## Components and Interfaces

### JD Locators (`locators/loc_jd.py`)

```python
class JDLocators:
    def __init__(self, page: Page):
        # Navigation and main page elements
        self.jd_page_url = "https://bprp-qa.shadhinlab.xyz/agency/{agency_id}/jd"
        self.search_input = page.get_by_role("textbox", name="Search...")
        self.filters_button = page.locator("div").filter(has_text="Filters")
        self.add_jd_button = page.get_by_role("button", name="Add JD")
        self.upload_file_button = page.get_by_role("button", name="Upload File")
        
        # JD Creation Modal Elements
        self.jd_modal_heading = page.get_by_role("heading", name="Add New JD")
        self.position_job_title_input = page.get_by_role("textbox", name="Position Job Title")
        self.company_dropdown = page.locator("div").filter(has_text="Company")
        self.work_style_dropdown = page.locator("div").filter(has_text="Work Style")
        self.jd_workplace_input = page.get_by_role("textbox", name="JD Workplace")
        
        # Salary and compensation fields
        self.minimum_salary_input = page.get_by_role("textbox", name="Minimum Salary")
        self.maximum_salary_input = page.get_by_role("textbox", name="Maximum Salary")
        self.currency_dropdown = page.locator("div").filter(has_text="Currency")
        
        # Age and experience fields
        self.job_age_min_input = page.get_by_role("textbox", name="Job Age Min")
        self.job_age_max_input = page.get_by_role("textbox", name="Job Age Max")
        self.target_age_min_input = page.get_by_role("textbox", name="Target Age Min")
        self.target_age_max_input = page.get_by_role("textbox", name="Target Age Max")
        
        # Language and skills
        self.japanese_level_dropdown = page.locator("div").filter(has_text="Japanese Level")
        self.english_level_dropdown = page.locator("div").filter(has_text="English Level")
        
        # Additional fields
        self.priority_grade_dropdown = page.locator("div").filter(has_text="Priority Grade")
        self.client_dropdown = page.locator("div").filter(has_text="Client")
        self.hiring_status_dropdown = page.locator("div").filter(has_text="Hiring Status")
        self.employment_type_dropdown = page.locator("div").filter(has_text="Employment Type")
        self.department_input = page.get_by_role("textbox", name="Department")
        self.direct_report_input = page.get_by_role("textbox", name="Direct Report")
        self.job_function_input = page.get_by_role("textbox", name="Job Function")
        
        # File upload
        self.upload_jd_file_area = page.locator("div").filter(has_text="Upload JD file (optional)")
        
        # Modal actions
        self.save_button = page.get_by_role("button", name="Save")
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.close_modal_button = page.get_by_role("button", name="Close modal")
        
        # Validation error messages (specific locators)
        self.position_title_required_error = page.get_by_text("Position Job Title is required")
        self.company_required_error = page.get_by_text("Company is required")
        self.work_style_required_error = page.get_by_text("Work Style is required")
        self.workplace_required_error = page.get_by_text("JD Workplace is required")
        self.invalid_salary_range_error = page.get_by_text("Maximum salary must be greater than minimum salary")
        self.invalid_age_range_error = page.get_by_text("Maximum age must be greater than minimum age")
        
        # Success messages
        self.jd_created_successfully_message = page.get_by_text("JD created successfully")
        self.jd_updated_successfully_message = page.get_by_text("JD updated successfully")
        self.jd_deleted_successfully_message = page.get_by_text("JD deleted successfully")
        
        # JD List Elements
        self.no_jds_message = page.get_by_text("No companies found")
        self.add_new_jd_button = page.get_by_role("button", name="Add new JD")
        self.jd_card = lambda title: page.get_by_role("heading", name=title)
        
        # Filter panel elements
        self.filter_panel = page.locator(".filter-panel")
        self.company_name_filter = page.get_by_text("Company Name")
        self.position_title_filter = page.get_by_text("Open Position Job Title")
        self.hiring_status_filter = page.get_by_text("Hiring Status")
        self.work_style_filter = page.get_by_text("Work Style")
        self.all_clear_button = page.get_by_role("button", name="All clear")
        
        # Pagination elements
        self.pagination_container = page.locator(".pagination")
        self.next_page_button = page.get_by_role("button", name="Next")
        self.previous_page_button = page.get_by_role("button", name="Previous")
        self.page_number = lambda num: page.get_by_role("button", name=str(num))
```

### JD Page Object (`pages/jd_page.py`)

```python
class JDPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = JDLocators(page)
    
    # Navigation methods
    def navigate_to_jd_page(self, agency_id: str):
        url = self.locators.jd_page_url.format(agency_id=agency_id)
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
    
    # JD Creation methods
    def click_add_jd(self):
        self.locators.add_jd_button.click()
    
    def fill_jd_form(self, jd_data: dict):
        # Fill mandatory fields
        self.locators.position_job_title_input.fill(jd_data["position_title"])
        self.select_company(jd_data["company"])
        self.select_work_style(jd_data["work_style"])
        self.locators.jd_workplace_input.fill(jd_data["workplace"])
        
        # Fill optional fields if provided
        if "min_salary" in jd_data:
            self.locators.minimum_salary_input.fill(str(jd_data["min_salary"]))
        if "max_salary" in jd_data:
            self.locators.maximum_salary_input.fill(str(jd_data["max_salary"]))
    
    def save_jd(self):
        self.locators.save_button.click()
    
    def cancel_jd_creation(self):
        self.locators.cancel_button.click()
    
    # Search and filter methods
    def search_jd(self, search_term: str):
        self.locators.search_input.fill(search_term)
        self.page.keyboard.press("Enter")
    
    def open_filters(self):
        self.locators.filters_button.click()
    
    def apply_company_filter(self, company_name: str):
        # Implementation for applying company filter
        pass
    
    # File upload methods
    def upload_jd_file(self, file_path: str):
        self.locators.upload_file_button.click()
        # Handle file upload dialog
        pass
```

### JD Helper Functions (`utils/jd_helper.py`)

```python
def do_jd_login(page: Page, email: str, password: str, agency_id: str) -> JDPage:
    """Login and navigate to JD page for specified agency."""
    
def do_create_jd(page: Page, jd_data: dict, agency_id: str) -> JDPage:
    """Complete JD creation workflow with validation."""
    
def do_search_and_verify_jd(page: Page, search_term: str, expected_results: list):
    """Search for JDs and verify results."""
    
def assert_jd_validation_errors(page: Page, expected_errors: list):
    """Assert specific validation error messages are visible."""
```

## Data Models

### JD Test Data Structure

```python
@dataclass
class JDTestData:
    position_title: str
    company: str
    work_style: str
    workplace: str
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    currency: Optional[str] = None
    job_age_min: Optional[int] = None
    job_age_max: Optional[int] = None
    target_age_min: Optional[int] = None
    target_age_max: Optional[int] = None
    japanese_level: Optional[str] = None
    english_level: Optional[str] = None
    priority_grade: Optional[str] = None
    hiring_status: Optional[str] = None
    employment_type: Optional[str] = None
    department: Optional[str] = None
    direct_report: Optional[str] = None
    job_function: Optional[str] = None
```

### Random Data Generator (`random_values_generator/random_jd_data.py`)

```python
def generate_jd_data() -> JDTestData:
    """Generate random JD data for testing."""
    
def generate_position_title() -> str:
    """Generate random position titles."""
    
def generate_workplace_location() -> str:
    """Generate random workplace locations."""
```

## Error Handling

### Validation Strategy

1. **Field-Level Validation**: Each input field has specific validation rules and error messages
2. **Form-Level Validation**: Cross-field validation (e.g., salary ranges, age ranges)
3. **Business Logic Validation**: Company-client relationships, hiring status constraints

### Error Message Patterns

- **Required Field Errors**: "{Field Name} is required"
- **Format Errors**: "Please enter a valid {field type}"
- **Range Errors**: "{Max Field} must be greater than {Min Field}"
- **File Errors**: "Only accept {formats} file" / "File can't be larger than {size}"

### Enhanced Assertion Integration

```python
# Direct assertion usage in tests
enhanced_assert_visible(page, jd_page.locators.position_title_required_error, 
                       "Position title required error should be visible", "test_TC_01_position_title_required")
```

## Testing Strategy

### Test Categories

1. **CRUD Operations** (TC_01-TC_10)
   - JD creation with valid/invalid data
   - JD editing and updates
   - JD deletion with confirmation
   - JD viewing and details

2. **Search and Filter** (TC_11-TC_20)
   - Text search functionality
   - Filter combinations
   - Search result validation
   - Filter clearing

3. **Validation Testing** (TC_21-TC_30)
   - Required field validation
   - Format validation
   - Range validation
   - File upload validation

4. **Pagination and Navigation** (TC_31-TC_35)
   - Page navigation
   - Items per page
   - URL parameter handling

5. **Bulk Operations** (TC_36-TC_40)
   - Multi-select functionality
   - Bulk delete operations
   - Bulk status updates

### Test Data Management

- **Fixtures**: Shared test data using `@pytest.fixture(scope="module")`
- **Cleanup**: Automatic cleanup of created test data
- **Isolation**: Each test creates its own data to avoid conflicts

### Screenshot Strategy

- **Automatic Capture**: Enhanced assertions capture screenshots on failures
- **Organized Storage**: Screenshots stored in `screenshots/jd_screenshots/`
- **Timestamped Files**: Unique filenames with test name and timestamp

## Integration Points

### Existing System Integration

1. **Login System**: Reuse existing login helpers and credentials
2. **Agency Context**: JD operations within specific agency context
3. **Navigation**: Integration with existing navigation patterns
4. **Assertions**: Use established enhanced assertion system

### File Structure Integration

```
├── locators/
│   └── loc_jd.py                 # JD-specific locators
├── pages/
│   └── jd_page.py               # JD page object
├── tests/
│   └── test_jd.py               # JD test cases
├── utils/
│   └── jd_helper.py             # JD helper functions
├── random_values_generator/
│   └── random_jd_data.py        # JD test data generation
├── screenshots/
│   └── jd_screenshots/          # JD test screenshots
└── images_for_test/
    └── jd_files/                # Test files for upload
```

### Configuration Integration

- **Base URL**: Use existing `utils/config.py` configuration
- **Timeouts**: Follow existing timing strategies
- **Browser Settings**: Inherit from `pytest.ini` configuration