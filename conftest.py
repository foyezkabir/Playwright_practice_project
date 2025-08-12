import os
import pytest
import ast
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from playwright.sync_api import sync_playwright, Page
from utils.config import BROWSER_NAME, HEADLESS, DEFAULT_TIMEOUT, SLOW_MO, SCREENSHOT_DELAY
from utils.screenshot_helper import capture_failure_screenshot

# Global variables to store test results
test_results = {}
test_files_executed = set()

# REPORT GENERATION FUNCTIONALITY
# ============================================================================

def extract_test_descriptions(pyfile: str) -> dict:
    """
    Extracts docstrings from test functions and formats them with 'Verify' prefix.
    Returns dict: {test_function_name: description}
    """
    descriptions = {}
    try:
        with open(pyfile, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=pyfile)

        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                docstring = ast.get_docstring(node)
                if docstring:
                    # Ensure description starts with "Verify"
                    description = docstring.strip()
                    if not description.lower().startswith("verify"):
                        description = f"Verify {description}"
                    descriptions[node.name] = description
                else:
                    # Fallback to cleaned test name with "Verify" prefix
                    clean_name = clean_test_name(node.name)
                    descriptions[node.name] = f"Verify {clean_name}"
    except Exception as e:
        print(f"Error extracting descriptions from {pyfile}: {e}")
    return descriptions

def clean_test_name(name: str) -> str:
    """Cleans a Python test function name for reporting."""
    if name.startswith("test_"):
        name = name[5:]
    parts = [part for part in name.split('_') if not part.isdigit()]
    clean_name = " ".join(parts)
    return clean_name.capitalize() if clean_name else name

def get_dynamic_test_data(test_name: str, test_file: str) -> dict:
    """
    Returns dynamically generated test data based on test name patterns.
    """
    # Extract module name from test file
    module_name = os.path.basename(test_file).replace("test_", "").replace(".py", "").replace("_", " ").title()
    
    # Common patterns for different types of tests
    if "login" in test_name.lower():
        return get_login_test_data(test_name)
    elif "signup" in test_name.lower() or "register" in test_name.lower():
        return get_signup_test_data(test_name)
    elif "email" in test_name.lower() and "verif" in test_name.lower():
        return get_email_verification_test_data(test_name)
    elif "password" in test_name.lower() and ("reset" in test_name.lower() or "forgot" in test_name.lower()):
        return get_password_reset_test_data(test_name)
    elif "agency" in test_name.lower():
        return get_agency_test_data(test_name)
    else:
        return get_generic_test_data(test_name, module_name)

def get_login_test_data(test_name: str) -> dict:
    """Returns specific test data for login tests."""
    if "successful" in test_name.lower():
        return {
            "pre_conditions": "User is on the login page and has valid credentials",
            "test_data": "Valid email and password",
            "test_steps": "1. Navigate to login page\n2. Enter valid credentials\n3. Click Sign in button",
            "expected_result": "User should be logged in successfully",
            "actual_result": "User logged in successfully"
        }
    elif "email" in test_name.lower() and "required" in test_name.lower():
        return {
            "pre_conditions": "User is on the login page",
            "test_data": "Empty email field",
            "test_steps": "1. Navigate to login page\n2. Leave email field empty\n3. Enter password\n4. Click Sign in",
            "expected_result": "System should display 'Email is required' error",
            "actual_result": "'Email is required' error message displayed"
        }
    elif "password" in test_name.lower() and "required" in test_name.lower():
        return {
            "pre_conditions": "User is on the login page",
            "test_data": "Empty password field",
            "test_steps": "1. Navigate to login page\n2. Enter email\n3. Leave password empty\n4. Click Sign in",
            "expected_result": "System should display 'Password is required' error",
            "actual_result": "'Password is required' error message displayed"
        }
    elif "invalid" in test_name.lower() and "email" in test_name.lower():
        return {
            "pre_conditions": "User is on the login page",
            "test_data": "Invalid email format",
            "test_steps": "1. Navigate to login page\n2. Enter invalid email\n3. Enter password\n4. Click Sign in",
            "expected_result": "System should display email format error",
            "actual_result": "Invalid email format error displayed"
        }
    elif "invalid" in test_name.lower() and "credential" in test_name.lower():
        return {
            "pre_conditions": "User is on the login page",
            "test_data": "Wrong credentials",
            "test_steps": "1. Navigate to login page\n2. Enter wrong credentials\n3. Click Sign in",
            "expected_result": "System should display invalid credentials error",
            "actual_result": "Invalid credentials error displayed"
        }
    else:
        return get_generic_test_data(test_name, "Login")

def get_signup_test_data(test_name: str) -> dict:
    """Returns specific test data for signup tests."""
    return {
        "pre_conditions": "User is on the signup page",
        "test_data": "Signup form data",
        "test_steps": "1. Navigate to signup page\n2. Fill required fields\n3. Submit form",
        "expected_result": "Signup process should work as expected",
        "actual_result": "Signup functionality verified"
    }

def get_email_verification_test_data(test_name: str) -> dict:
    """Returns specific test data for email verification tests."""
    return {
        "pre_conditions": "User has received verification email",
        "test_data": "OTP or verification code",
        "test_steps": "1. Open verification page\n2. Enter verification code\n3. Submit verification",
        "expected_result": "Email should be verified successfully",
        "actual_result": "Email verification completed"
    }

def get_password_reset_test_data(test_name: str) -> dict:
    """Returns specific test data for password reset tests."""
    return {
        "pre_conditions": "User needs to reset password",
        "test_data": "Email address for reset",
        "test_steps": "1. Navigate to forgot password\n2. Enter email\n3. Submit reset request",
        "expected_result": "Password reset process should work",
        "actual_result": "Password reset functionality verified"
    }

def get_agency_test_data(test_name: str) -> dict:
    """Returns specific test data for agency tests."""
    return {
        "pre_conditions": "User is logged in and has agency permissions",
        "test_data": "Agency related data",
        "test_steps": "1. Navigate to agency section\n2. Perform agency operations\n3. Verify results",
        "expected_result": "Agency functionality should work as expected",
        "actual_result": "Agency operations completed successfully"
    }

def get_generic_test_data(test_name: str, module_name: str) -> dict:
    """Returns generic test data for any test."""
    return {
        "pre_conditions": f"User is on the {module_name.lower()} page",
        "test_data": f"{module_name} test data",
        "test_steps": f"1. Navigate to {module_name.lower()} page\n2. Perform required actions\n3. Verify expected behavior",
        "expected_result": f"{module_name} functionality should work as expected",
        "actual_result": f"{module_name} functionality verified"
    }

def generate_excel_report(test_file: str, test_descriptions: dict, results: dict) -> None:
    """
    Creates an Excel file with detailed test report.
    """
    # Generate report filename
    base_name = os.path.basename(test_file).replace(".py", "")
    report_filename = f"reports/{base_name}_report.xlsx"
    
    # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = f"{base_name.replace('_', ' ').title()} Test Report"

    # Define styles
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    center_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    thin_border = Border(
        left=Side(style="thin"), right=Side(style="thin"),
        top=Side(style="thin"), bottom=Side(style="thin")
    )

    # Header row
    headers = [
        "Serial No.", "Test Case Id.", "Test Objective", "Pre-Conditions",
        "Test Data", "Test Steps", "Expected Result", "Actual Result", "Test Status"
    ]
    ws.append(headers)
    
    # Apply header styling
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_alignment
        cell.border = thin_border

    # Data rows
    for idx, (test_name, desc) in enumerate(test_descriptions.items(), start=1):
        status = results.get(test_name, "Not Run")
        #tc_id = f"TC_{base_name.upper()}_{idx:03d}"
        tc_id = f"TC_{idx:03d}"
        test_data = get_dynamic_test_data(test_name, test_file)
        
        # Determine actual result based on test status
        if status == "PASSED":
            actual_result = test_data["actual_result"]
        elif status == "FAILED":
            actual_result = "Test failed - actual behavior did not match expected result"
        elif status == "SKIPPED":
            actual_result = "Test was skipped during execution"
        else:
            actual_result = "Test not executed"
        
        row_data = [
            f"{idx:02d}", tc_id, desc, test_data["pre_conditions"],
            test_data["test_data"], test_data["test_steps"], 
            test_data["expected_result"], actual_result, status
        ]
        
        ws.append(row_data)
        
        # Apply styling to data rows
        for col_num, value in enumerate(row_data, 1):
            cell = ws.cell(row=idx + 1, column=col_num)
            cell.border = thin_border
            if col_num == 1:  # Serial No.
                cell.alignment = center_alignment
            else:
                cell.alignment = left_alignment
            
            # Color code test status
            if col_num == 9:  # Test Status column
                if status == "PASSED":
                    cell.fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
                elif status == "FAILED":
                    cell.fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
                elif status == "SKIPPED":
                    cell.fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")

    # Adjust column widths
    column_widths = [10, 15, 40, 30, 30, 50, 40, 40, 12]
    for col_num, width in enumerate(column_widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=col_num).column_letter].width = width

    # Set row heights
    for row in range(2, len(test_descriptions) + 2):
        ws.row_dimensions[row].height = 80

    wb.save(report_filename)
    print(f"Test report generated: {report_filename}")

# BROWSER AND PAGE FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def browser():
    """Session-scoped browser fixture with configuration from config.py"""
    with sync_playwright() as p:
        if BROWSER_NAME == "chromium":
            browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        elif BROWSER_NAME == "firefox":
            browser = p.firefox.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        elif BROWSER_NAME == "webkit":
            browser = p.webkit.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        else:
            browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
            
        yield browser
        browser.close()

@pytest.fixture
def context(browser, request):
    """Browser context fixture with tracing support."""
    context = browser.new_context()
    tracing_enabled = request.config.getoption("--tracing") if hasattr(request.config, 'getoption') else False
    if tracing_enabled:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    if tracing_enabled:
        trace_dir = os.path.join(os.getcwd(), "traces")
        os.makedirs(trace_dir, exist_ok=True)
        trace_file = os.path.join(trace_dir, f"trace_{request.node.name}.zip")
        context.tracing.stop(path=trace_file)
    context.close()

@pytest.fixture
def page(context):
    """Page fixture using context, with configured timeout."""
    page = context.new_page()
    page.set_default_timeout(DEFAULT_TIMEOUT)
    yield page
    page.close()

# SCREENSHOT HOOKS AND FIXTURES
# ============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook to capture test execution results."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
    
    # Capture test results for report generation
    if rep.when == "call":  # Only capture the actual test execution result
        test_file = str(item.fspath)
        test_name = item.name
        
        # Store the test file being executed
        test_files_executed.add(test_file)
        
        # Store test result
        if test_file not in test_results:
            test_results[test_file] = {}
        
        if rep.passed:
            test_results[test_file][test_name] = "PASSED"
        elif rep.failed:
            test_results[test_file][test_name] = "FAILED"
        elif rep.skipped:
            test_results[test_file][test_name] = "SKIPPED"

def pytest_sessionfinish(session, exitstatus):
    """Generate reports after all tests complete."""
    for test_file in test_files_executed:
        if test_file in test_results and test_results[test_file]:
            # Extract test descriptions from the file
            test_descriptions = extract_test_descriptions(test_file)
            
            # Generate Excel report
            generate_excel_report(test_file, test_descriptions, test_results[test_file])
    
    # Clear the results for next run
    test_results.clear()
    test_files_executed.clear()

@pytest.fixture(autouse=True)
def auto_screenshot_on_failure(request, page: Page):
    """Automatic screenshot capture fixture for failed tests."""
    yield
    
    # Check if test failed
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        test_name = request.node.name
        test_file = request.node.fspath.strpath
        capture_failure_screenshot(page, test_name, test_file)

@pytest.fixture
def screenshot_on_failure(request, page: Page):
    """Manual screenshot fixture for tests marked with @pytest.mark.screenshot"""
    def _capture_screenshot():
        test_name = request.node.name
        test_file = request.node.fspath.strpath
        capture_failure_screenshot(page, test_name, test_file)
    
    yield _capture_screenshot
    
    # Auto-capture on failure if marked with @pytest.mark.screenshot
    if request.node.get_closest_marker("screenshot"):
        if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            test_name = request.node.name
            test_file = request.node.fspath.strpath
            capture_failure_screenshot(page, test_name, test_file)