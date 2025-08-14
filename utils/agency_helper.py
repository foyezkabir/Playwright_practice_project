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
    
    # If modal appears, use it; otherwise click create new agency
    try:
        agency_page.expect_agency_modal_heading()
        print("✅ Modal already open")
        # Modal is already open
    except:
        # No modal, click to open
        print("🔄 Clicking create new agency button")
        agency_page.click_create_new_agency()
        time.sleep(1)
    
    print(f"📝 Filling agency details...")
    agency_page.fill_agency_name(agency_name)
    agency_page.click_industry_dropdown()
    agency_page.click_healthcare_option()
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
    enhanced_assert_visible(page, agency_page.locators.agency_create_modal_heading, 
                          "Agency create modal heading should be visible")

def assert_create_modal_body(page: Page):
    """Assert create modal body is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.create_modal_body, 
                          "Create modal body should be visible")

def assert_agency_create_modal_not_visible(page: Page):
    """Assert agency create modal is not visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_not_visible(page, agency_page.locators.agency_create_modal_heading, 
                               "Agency create modal heading should not be visible")
    enhanced_assert_not_visible(page, agency_page.locators.create_modal_body, 
                               "Create modal body should not be visible")

def assert_update_confirm_message(page: Page):
    """Assert update confirmation message is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.update_confirm_message, 
                          "Update confirmation message should be visible")

def assert_all_agencies_message(page: Page):
    """Assert all agencies message is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.all_agencies_message, 
                          "All agencies message should be visible")

def assert_all_agencies_list(page: Page):
    """Assert all agencies list is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.all_agencies_list, 
                          "All agencies list should be visible")

def assert_agency_created_successfully_message(page: Page):
    """Assert agency created successfully message is visible or verify successful navigation"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    
    try:
        # First try to find the success message
        enhanced_assert_visible(page, agency_page.locators.agency_created_successfully_message, 
                              "Agency created successfully message should be visible", "agency_creation")
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
                enhanced_assert_visible(page, agency_list_elements.first, 
                                      "Should be on agency list page after creation", "agency_creation")
                print("✅ Verified we're on agency list page")
            except Exception as final_error:
                # If all methods fail, raise original error
                print(f"All verification methods failed. Original error: {e}")
                print(f"Final error: {final_error}")
                raise e

def assert_created_agency_appear(page: Page):
    """Assert created agency appears"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.created_agency_appear, 
                          "Created agency should appear")

def assert_update_agency_modal(page: Page):
    """Assert update agency modal is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.update_agency_modal, 
                          "Update agency modal should be visible")

def assert_delete_confirmation_modal(page: Page):
    """Assert delete confirmation modal is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.delete_confirmation_modal, 
                          "Delete confirmation modal should be visible")

def assert_agency_deleted_successfully_message(page: Page):
    """Assert agency deleted successfully message is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.agency_deleted_successfully_message, 
                          "Agency deleted successfully message should be visible")

def assert_main_content(page: Page):
    """Assert main content is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.main_content, 
                          "Main content should be visible")
