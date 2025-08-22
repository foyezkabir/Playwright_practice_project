"""
Enhanced Assertions Utility
Provides assertion methods that capture immediate screenshots on failure
"""

import inspect
import os
from datetime import datetime
from playwright.sync_api import Page

def enhanced_assert_visible(page: Page, locator, error_message: str, test_name: str = None, timeout: int = 3000):
    """
    Enhanced assert that captures screenshot immediately if assertion fails.
    
    Args:
        page: Playwright page object
        locator: The locator to check for visibility
        error_message: Error message to display
        test_name: Name of the test (auto-detected if not provided)
        timeout: Timeout in milliseconds (default: 3000)
    """
    # Auto-detect test name if not provided
    if test_name is None:
        frame = inspect.currentframe()
        while frame:
            frame_info = inspect.getframeinfo(frame)
            if 'test_' in frame_info.function:
                test_name = frame_info.function
                break
            frame = frame.f_back
        test_name = test_name or "unknown_test"
    
    # Give a moment for any toast/error messages to appear after the action
    page.wait_for_timeout(1000)  # Wait 1 second for messages to appear
    
    try:
        # Check if the expected element is visible
        locator.wait_for(state="visible", timeout=timeout)  # Use provided timeout
        # Success - element appeared
        assert True
    except:
        # Element didn't appear - take screenshot NOW to capture current state
        capture_failure_screenshot(page, test_name, "assertion_failure")
        # Then fail the assertion
        assert False, error_message

def enhanced_assert_not_visible(page: Page, locator, error_message: str, test_name: str = None):
    """
    Enhanced assert that captures screenshot immediately if assertion fails.
    Checks that element is NOT visible.
    """
    try:
        if locator.is_visible():
            # Capture screenshot immediately before raising assertion error
            if test_name is None:
                frame = inspect.currentframe()
                while frame:
                    frame_info = inspect.getframeinfo(frame)
                    if 'test_' in frame_info.function:
                        test_name = frame_info.function
                        break
                    frame = frame.f_back
                test_name = test_name or "unknown_test"
            
            capture_failure_screenshot(page, test_name, "assertion_failure")
            assert False, error_message
        else:
            # Success - locator is not visible
            assert True
            
    except Exception as e:
        if test_name is None:
            frame = inspect.currentframe()
            while frame:
                frame_info = inspect.getframeinfo(frame)
                if 'test_' in frame_info.function:
                    test_name = frame_info.function
                    break
                frame = frame.f_back
            test_name = test_name or "unknown_test"
        
        capture_failure_screenshot(page, test_name, "exception")
        raise e

def capture_failure_screenshot(page: Page, test_name: str, failure_type: str = "failure"):
    """
    Capture screenshot immediately when assertion fails.
    """
    try:
        timestamp = datetime.now().strftime("%d-%m-%Y_%H.%M.%S")
        
        # Get the test file from the call stack to determine correct folder
        frame = inspect.currentframe()
        test_file = ""
        while frame:
            frame_info = inspect.getframeinfo(frame)
            if frame_info.filename and 'test_' in frame_info.filename:
                test_file = frame_info.filename
                break
            frame = frame.f_back
        
        # Determine screenshot folder based on test file name
        if "test_login.py" in test_file:
            folder = "login_screenshots"
        elif "test_signup.py" in test_file:
            folder = "signup_screenshots"
        elif "test_agency.py" in test_file:
            folder = "agency_screenshots"
        elif "test_email" in test_file:
            folder = "email_verify_screenshots"
        elif "test_reset" in test_file:
            folder = "reset_pass_screenshots"
        else:
            folder = "general_screenshots"
        
        # Create directory
        screenshot_dir = os.path.join("screenshots", folder)
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # Generate filename in format: TC_XX_DD-MM-YYYY_HH.MM.SS.png
        clean_test_name = test_name.replace("test_", "")
        filename = f"{clean_test_name}_{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)
        
        # Take screenshot immediately
        page.screenshot(path=filepath)
        print(f"📸 Immediate assertion failure screenshot: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"⚠️  Failed to capture immediate screenshot: {e}")
        return None
