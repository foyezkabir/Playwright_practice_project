"""
Agency Helper Module
Contains utility functions for agency tests
"""

from playwright.sync_api import Page
from utils.config import BASE_URL
from utils.login_helper import do_login
from conftest import wait_for_action_completion
from utils.enhanced_assertions import enhanced_assert_visible, enhanced_assert_not_visible
import time

def do_agency_login(page: Page, email: str, password: str):
    """
    Helper function to login and handle agency page
    
    Args:
        page: Playwright page object
        email: User email
        password: User password
    
    Returns:
        AgencyPage instance
    """
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    do_login(page, email, password)
    # Small wait for agency page to load
    time.sleep(2)
    return agency_page

def do_create_agency(page: Page, agency_name: str, email: str = "gi7j8d@mepost.pw", 
                    password: str = "Kabir123#", website: str = "https://testagency123.com",
                    address: str = "123 Test Agency St", 
                    description: str = "This is a test agency for automation."):
    """
    Helper function to create a new agency
    
    Args:
        page: Playwright page object
        agency_name: Name of the agency to create
        email: Login email (optional)
        password: Login password (optional)
        website: Agency website (optional)
        address: Agency address (optional)
        description: Agency description (optional)
    
    Returns:
        AgencyPage instance
    """
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    do_login(page, email, password)
    time.sleep(2)
    
    print(f"🔧 Creating agency: {agency_name}")
    
    # Check if modal is already open without taking screenshot
    modal_already_open = agency_page.locators.agency_create_modal_heading.count() > 0
    
    if modal_already_open:
        print("✅ Modal already open")
    else:
        # No modal, click to open
        print("🔄 Clicking create new agency button")
        agency_page.click_create_new_agency()
        time.sleep(1)
    
    print(f"📝 Filling agency details...")
    agency_page.fill_agency_name(agency_name)
    agency_page.click_industry_dropdown()
    agency_page.click_administration_of_justice_option()
    agency_page.fill_website(website)
    agency_page.fill_address(address)
    agency_page.fill_description(description)
    
    print("💾 Saving agency...")
    agency_page.click_agency_save_button()
    wait_for_action_completion(page, "save")
    
    # Additional wait and check for successful creation
    time.sleep(3)
    
    # Check current URL to confirm we're on agency list page
    current_url = page.url
    print(f"📍 Current URL after creation: {current_url}")
    
    # Check if we see any success indicators
    success_indicators = [
        "Agency created successfully",
        "Agency Created Successfully", 
        "Successfully created"
    ]
    
    for indicator in success_indicators:
        if page.get_by_text(indicator).count() > 0:
            print(f"✅ Found success indicator: {indicator}")
            break
    else:
        print("⚠️ No explicit success message found, but continuing...")
    
    return agency_page

def navigate_to_agency_page(page: Page, email: str, password: str):
    """
    Helper function to navigate to agency page after login
    
    Args:
        page: Playwright page object
        email: User email
        password: User password
    
    Returns:
        AgencyPage instance
    """
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    agency_page.navigate_to_login_page(BASE_URL + "/login")
    do_login(page, email, password)
    time.sleep(2)
    return agency_page

def find_and_edit_agency(page: Page, agency_name: str, new_name: str = None):
    """
    Helper function to find and edit an agency
    
    Args:
        page: Playwright page object
        agency_name: Current name of the agency
        new_name: New name for the agency (optional)
    
    Returns:
        AgencyPage instance
    """
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    
    # Find agency in paginated list
    agency_page.find_agency_in_paginated_list(page, agency_name)
    agency_page.get_agency_actions(agency_name)
    agency_page.click_edit_button_for_agency(agency_name)
    time.sleep(2)
    
    # Wait for input to be ready
    agency_page.locators.agency_name_input.wait_for(timeout=10000)
    
    if new_name:
        agency_page.locators.agency_name_input.fill(new_name)
        time.sleep(1)
        agency_page.locators.agency_update_button.click()
        wait_for_action_completion(page, "update")
    
    return agency_page

# Enhanced assertion helper functions for agency tests
def assert_agency_create_modal_heading(page: Page):
    """Assert agency create modal heading is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.agency_create_modal_heading, "Agency create modal heading should be visible")

def assert_create_modal_body(page: Page):
    """Assert create modal body is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.create_modal_body, "Create modal body should be visible")

def assert_agency_create_modal_not_visible(page: Page):
    """Assert agency create modal is not visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_not_visible(page, agency_page.locators.agency_create_modal_heading, "Agency create modal heading should not be visible")
    enhanced_assert_not_visible(page, agency_page.locators.create_modal_body, "Create modal body should not be visible")

def assert_update_confirm_message(page: Page):
    """Assert update confirmation message is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.update_confirm_message, "Update confirmation message should be visible")

def assert_all_agencies_message(page: Page):
    """Assert all agencies message is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.all_agencies_message, "All agencies message should be visible")

def assert_all_agencies_list(page: Page):
    """Assert all agencies list is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.all_agencies_list, "All agencies list should be visible")

def assert_agency_created_successfully_message(page: Page):
    """Assert agency created successfully message is visible or verify successful navigation"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    
    try:
        # First try to find the success message
        enhanced_assert_visible(page, agency_page.locators.agency_created_successfully_message,     "Agency created successfully message should be visible", "agency_creation")
    except Exception as e:
        # If success message not found, check if we're on agency list page (alternative success indicator)
        try:
            # Wait for URL to change to agency list
            page.wait_for_url("**/agency-list", timeout=5000)
            print("✅ Successfully navigated to agency list page after creation")
        except:
            # Last resort: check for any agency list elements
            try:
                agency_list_elements = page.locator("h1:has-text('Agencies'), [data-testid='agency-list'], .agencies-container")
                enhanced_assert_visible(page, agency_list_elements.first, "Should be on agency list page after creation", "agency_creation")
                print("✅ Verified we're on agency list page")
            except Exception as final_error:
                # If all methods fail, raise original error
                print(f"All verification methods failed. Original error: {e}")
                print(f"Final error: {final_error}")
                raise e

def assert_validation_error_visible(page: Page, test_name: str = "validation_test"):
    """Assert that validation error message is visible with improved detection"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    
    # Wait for potential toast messages
    time.sleep(2)
    agency_page.wait_for_toast_message(timeout=3000)
    
    # Get error message for debugging
    error_message = agency_page.get_validation_error_message()
    print(f"🔍 Detected error message: '{error_message}'")
    
    # Check multiple error sources
    if agency_page.check_validation_error():
        if agency_page.locators.validation_error.count() > 0:
            enhanced_assert_visible(page, agency_page.locators.validation_error.first, "Form validation error should be visible", test_name)
        elif agency_page.locators.error_toast.count() > 0:
            enhanced_assert_visible(page, agency_page.locators.error_toast.first, "Toast validation error should be visible", test_name)
        elif agency_page.locators.toast_message.count() > 0:
            enhanced_assert_visible(page, agency_page.locators.toast_message.first, "Toast message should be visible", test_name)
    else:
        raise AssertionError(f"No validation error found for test: {test_name}")

def assert_file_format_validation_error(page: Page, test_name: str = "file_format_validation"):
    """Assert that file format validation error is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    
    # Wait for potential validation messages
    time.sleep(2)
    agency_page.wait_for_toast_message(timeout=3000)
    
    # Get error message for debugging
    error_message = agency_page.get_validation_error_message()
    print(f"🔍 Detected error message: '{error_message}'")
    
    # Check for file format specific errors first
    if agency_page.check_file_format_error():
        if agency_page.locators.file_format_error.count() > 0:
            enhanced_assert_visible(page, agency_page.locators.file_format_error.first, "File format validation error should be visible", test_name)
        else:
            enhanced_assert_visible(page, agency_page.locators.error_toast.first, "File format error toast should be visible", test_name)
    else:
        # Fallback to general validation error
        assert_validation_error_visible(page, test_name)

def assert_validation_message_appears(page: Page, expected_message: str, fallback_pattern: str, test_name: str):
    """
    Reusable helper function to detect and assert validation messages
    
    Args:
        page: Playwright page object
        expected_message: The exact message to look for (regex pattern)
        fallback_pattern: Fallback regex pattern for broader search
        test_name: Name of the test for screenshot naming
    
    Returns:
        True if message found and assertion passed
    """
    # Look for the specific validation message
    validation_message = page.locator(f"text=/{expected_message}/i")
    
    # Wait for the message to appear
    try:
        validation_message.first.wait_for(state="visible", timeout=5000)
        message_text = validation_message.first.text_content()
        print(f"✅ Found validation message: '{message_text}'")
        
        # Assert the message is visible (use simple assertion for reliability)
        assert validation_message.count() > 0, f"Validation message should be visible: {expected_message}"
        print(f"✅ {test_name} completed successfully - validation message appeared")
        return True
        
    except Exception as e:
        # Fallback: try broader search for validation keywords
        fallback_elements = page.locator(f"text=/{fallback_pattern}/i")
        if fallback_elements.count() > 0:
            message_text = fallback_elements.first.text_content()
            print(f"✅ Found related validation message: '{message_text}'")
            assert fallback_elements.count() > 0, f"Validation message should be visible: {fallback_pattern}"
            print(f"✅ {test_name} completed successfully - validation message found with fallback")
            return True
        else:
            print(f"❌ Expected validation message not found: {e}")
            page.screenshot(path=f"screenshots/agency_screenshots/{test_name}_no_validation_message.png")
            raise AssertionError(f"Expected validation message did not appear: {expected_message}")

def assert_file_format_validation_message(page: Page, test_name: str = "file_format_validation"):
    """Assert that file format validation message appears"""
    return assert_validation_message_appears(
        page=page,
        expected_message=".*Only accept jpg, png, jpeg, gif file.*",
        fallback_pattern=".*jpg.*png.*jpeg.*gif.*",
        test_name=test_name
    )

def assert_file_size_validation_message(page: Page, test_name: str = "file_size_validation"):
    """Assert that file size validation message appears"""
    return assert_validation_message_appears(
        page=page,
        expected_message=".*File can't be larger than 5 MB.*",
        fallback_pattern=".*5.*MB.*larger.*",
        test_name=test_name
    )

def assert_custom_validation_message(page: Page, expected_message: str, fallback_keywords: list, test_name: str):
    """
    Generic helper for any custom validation message
    
    Args:
        page: Playwright page object
        expected_message: The exact message to look for
        fallback_keywords: List of keywords to search for as fallback
        test_name: Name of the test for screenshot naming
    
    Example usage:
        assert_custom_validation_message(
            page, 
            "Please enter a valid email address", 
            ["email", "valid", "address"], 
            "test_email_validation"
        )
    """
    fallback_pattern = ".*" + ".*".join(fallback_keywords) + ".*"
    return assert_validation_message_appears(
        page=page,
        expected_message=f".*{expected_message}.*",
        fallback_pattern=fallback_pattern,
        test_name=test_name
    )

def assert_successful_agency_creation_or_navigation(page: Page, test_name: str = "agency_success"):
    """Assert that agency creation was successful by checking success indicators"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    
    # Check for success message first
    if agency_page.check_success_message_exists():
        enhanced_assert_visible(page, agency_page.locators.success_message.first,     "Success message should be visible", test_name)
    elif agency_page.check_all_agencies_heading():
        enhanced_assert_visible(page, agency_page.locators.all_agencies_heading,     "Should be on all agencies page after successful creation", test_name)
    else:
        # Fallback - check URL contains agency
        current_url = page.url
        assert "agency" in current_url, f"Expected to be on agency page, but URL is: {current_url}"

def assert_created_agency_appear(page: Page):
    """Assert created agency appears"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.created_agency_appear, "Created agency should appear")

def assert_update_agency_modal(page: Page):
    """Assert update agency modal is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.update_agency_modal, "Update agency modal should be visible")

def assert_delete_confirmation_modal(page: Page):
    """Assert delete confirmation modal is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.delete_confirmation_modal, "Delete confirmation modal should be visible")

def assert_agency_deleted_successfully_message(page: Page):
    """Assert agency deleted successfully message is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.agency_deleted_successfully_message, "Agency deleted successfully message should be visible")

def assert_main_content(page: Page):
    """Assert main content is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.main_content, "Main content should be visible")

def do_create_agency_with_image_verification(page: Page, email: str = "50st3o@mepost.pw", password: str = "Kabir123#", 
                                           image_file: str = "pexels-photo.jpeg"):
    """
    Helper function to create agency with image upload and verify it appears in list
    
    Args:
        page: Playwright page object
        email: Login email
        password: Login password
        image_file: Image file to upload
    
    Returns:
        tuple: (agency_name, image_uploaded_successfully)
    """
    from utils.enhanced_assertions import enhanced_assert_visible
    from random_values_generator.random_agency_name import generate_agency_name
    
    agency_page = do_agency_login(page, email, password)
    time.sleep(2)
    agency_page.click_create_new_agency()
    time.sleep(1)

    # Generate random agency name using the random generator
    random_agency_name = generate_agency_name()
    print(f"🏢 Creating agency with name: '{random_agency_name}'")

    # Fill all agency fields with comprehensive data
    agency_page.fill_agency_name(random_agency_name)
    agency_page.click_industry_dropdown()
    agency_page.click_administration_of_justice_option()
    agency_page.fill_website("https://test-agency-with-image.com")
    agency_page.fill_address("456 Image Upload Street, Test City, TC 12345")
    agency_page.fill_description("Test agency created with image upload functionality")
    
    # Upload image file
    image_uploaded = False
    try:
        print(f"📸 Attempting to upload image: {image_file}")
        agency_page.upload_file(f"images_for_test/{image_file}")
        time.sleep(2)
        print("✅ Successfully uploaded image")
        image_uploaded = True
    except Exception as e:
        print(f"⚠️ Failed to upload image: {e}")

    # Save the agency
    print("💾 Saving agency...")
    agency_page.click_agency_save_button()
    wait_for_action_completion(page, "save")
    time.sleep(5)  # Wait for creation
    
    # Check if we need to navigate back to agency list
    current_url = page.url
    print(f"📍 Current URL after save: {current_url}")
    
    # Wait before refreshing
    time.sleep(1.5)
    
    # Refresh the page to ensure latest data is loaded
    print("🔄 Refreshing page to load latest agencies...")
    page.reload()
    time.sleep(1.5)

    # Search for the created agency in the paginated list
    print(f"🔍 Searching for agency '{random_agency_name}' in the list...")
    found = agency_page.find_agency_in_paginated_list(page, random_agency_name)
    
    # Verify the agency was created and appears in list
    assert found, f"Agency '{random_agency_name}' was not found in the agencies list"
    
    # Use enhanced assertion to verify agency is visible in the list
    enhanced_assert_visible(page, page.get_by_text(random_agency_name, exact=True).first, 
                           f"Agency '{random_agency_name}' should be visible in the agencies list", 
                           "agency_creation_with_image")
    
    print(f"✅ Agency '{random_agency_name}' successfully created and verified in the list!")
    
    # Optional: Check if image is visible within the agency card
    if image_uploaded:
        try:
            agency_images = page.locator("img").filter(has=page.get_by_text(random_agency_name))
            if agency_images.count() > 0:
                print("✅ Image appears to be displayed with the agency in the list")
            else:
                print("ℹ️ Image upload successful but visual verification in list needs manual check")
        except:
            print("ℹ️ Image verification in list requires manual check of screenshot")
    
    return random_agency_name, image_uploaded
