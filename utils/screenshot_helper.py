import os
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page
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

def create_screenshot_filename(test_name, timestamp=None):
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
        filename = f"test_{test_number}_{clean_name}_{timestamp}.png"
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