import os
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError, expect
from utils.config import (
    SCREENSHOT_DATE_FORMAT,
    SCREENSHOT_TIME_FORMAT, 
    SCREENSHOT_BASE_DIR,
    INCLUDE_TEST_FILE_PREFIX,
    INCLUDE_VERIFY_WORD,
    FULL_PAGE_SCREENSHOT
)

def get_screenshot_directory(test_file_name):
    """Generate screenshot directory path using config."""
    base_name = test_file_name.replace('test_', '').replace('.py', '')
    dir_name = f"{base_name}_screenshots"
    screenshot_dir = os.path.join(SCREENSHOT_BASE_DIR, dir_name)
    return screenshot_dir

def create_screenshot_filename(test_name, timestamp=None, error_type=None):
    """Create screenshot filename using config settings."""
    if timestamp is None:
        now = datetime.now()
        date_str = now.strftime(SCREENSHOT_DATE_FORMAT)
        time_str = now.strftime(SCREENSHOT_TIME_FORMAT)
        timestamp = f"{date_str}_{time_str}"
    
    # Clean test name based on config settings
    clean_test_name = test_name.replace('test_', '')
    
    if not INCLUDE_VERIFY_WORD:
        clean_test_name = clean_test_name.replace('verify_', '')
    
    if not INCLUDE_TEST_FILE_PREFIX:
        clean_test_name = clean_test_name.replace('reset_pass_', '')
        clean_test_name = clean_test_name.replace('demo_login_', '')
        clean_test_name = clean_test_name.replace('login_', '')
        clean_test_name = clean_test_name.replace('signup_', '')
    
    # Extract test number if present (e.g., "01", "02")
    parts = clean_test_name.split('_')
    if len(parts) > 0 and parts[0].isdigit():
        test_number = parts[0]
        remaining_parts = parts[1:]
        clean_name = '_'.join(remaining_parts)
        if error_type:
            filename = f"test_{test_number}_{clean_name}_{error_type}_{timestamp}.png"
        else:
            filename = f"test_{test_number}_{clean_name}_{timestamp}.png"
    else:
        if error_type:
            filename = f"test_{clean_test_name}_{error_type}_{timestamp}.png"
        else:
            filename = f"test_{clean_test_name}_{timestamp}.png"
    
    return filename

def ensure_unique_filename(directory, base_filename):
    """Ensure filename is unique by adding counter if file exists."""
    filepath = os.path.join(directory, base_filename)
    
    if not os.path.exists(filepath):
        return base_filename
    
    # Extract name and extension
    name, ext = os.path.splitext(base_filename)
    counter = 1
    
    while True:
        new_filename = f"{name}_{counter:02d}{ext}"
        new_filepath = os.path.join(directory, new_filename)
        
        if not os.path.exists(new_filepath):
            return new_filename
        
        counter += 1

def capture_failure_screenshot(page: Page, test_name: str, test_file: str):
    """Capture screenshot for failed test case using config settings."""
    try:
        test_file_name = os.path.basename(test_file)
        screenshot_dir = get_screenshot_directory(test_file_name)
        Path(screenshot_dir).mkdir(parents=True, exist_ok=True)
        
        base_filename = create_screenshot_filename(test_name)
        unique_filename = ensure_unique_filename(screenshot_dir, base_filename)
        screenshot_path = os.path.join(screenshot_dir, unique_filename)
        
        page.screenshot(path=screenshot_path, full_page=FULL_PAGE_SCREENSHOT)
        print(f"📸 Screenshot saved: {screenshot_path}")
        
    except Exception as e:
        print(f"❌ Failed to capture screenshot: {str(e)}")

def capture_error_screenshot(page: Page, test_name: str, error_type: str, test_file: str = None):
    """
    Capture screenshot immediately when error appears (before it disappears).
    This is specifically for error toasts/messages that appear and disappear quickly.
    
    Args:
        page: Playwright page object
        test_name: Name of the test function
        error_type: Type of error (e.g., "invalid_credentials", "email_required")
        test_file: Test file name (optional, will try to extract from stack if not provided)
    """
    try:
        # Try to get test file from current context if not provided
        if test_file is None:
            import inspect
            frame = inspect.currentframe()
            try:
                # Go up the stack to find the test file
                while frame:
                    filename = frame.f_code.co_filename
                    if 'test_' in os.path.basename(filename) and filename.endswith('.py'):
                        test_file = filename
                        break
                    frame = frame.f_back
            finally:
                del frame
        
        if test_file:
            test_file_name = os.path.basename(test_file)
            screenshot_dir = get_screenshot_directory(test_file_name)
        else:
            # Fallback to a general error screenshots directory
            screenshot_dir = os.path.join(SCREENSHOT_BASE_DIR, "error_screenshots")
        
        Path(screenshot_dir).mkdir(parents=True, exist_ok=True)
        
        base_filename = create_screenshot_filename(test_name, error_type=error_type)
        unique_filename = ensure_unique_filename(screenshot_dir, base_filename)
        screenshot_path = os.path.join(screenshot_dir, unique_filename)
        
        page.screenshot(path=screenshot_path, full_page=FULL_PAGE_SCREENSHOT)
        print(f"🔍 Error screenshot captured: {screenshot_path}")
        
        return screenshot_path
        
    except Exception as e:
        print(f"❌ Failed to capture error screenshot: {str(e)}")
        return None

def expect_with_immediate_screenshot(locator: Locator, page: Page, test_name: str, error_type: str, timeout: int = 5000):
    """
    Enhanced expect function that captures screenshot immediately when error element appears,
    before performing the actual expectation that might fail.
    
    Args:
        locator: Playwright Locator object to check
        page: Playwright Page object for screenshot
        test_name: Name of the test function
        error_type: Type of error for screenshot naming
        timeout: Timeout in milliseconds
    """
    try:
        # First, wait for the element to appear with a very short timeout to check if it exists
        locator.wait_for(state="visible", timeout=2000)
        
        # If element appears, capture screenshot immediately
        capture_error_screenshot(page, test_name, error_type)
        
        # Small delay to ensure message is fully rendered and visible
        page.wait_for_timeout(1000)
        
        # Now perform the actual expectation (this should pass since element is visible)
        expect(locator).to_be_visible(timeout=timeout)
        
    except PlaywrightTimeoutError:
        # Element didn't appear in 2 seconds, perform normal expectation
        # This will fail and trigger the pytest hook screenshot as backup
        expect(locator).to_be_visible(timeout=timeout)