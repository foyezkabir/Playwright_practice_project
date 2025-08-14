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
    
    # If modal appears, use it; otherwise click create new agency
    try:
        agency_page.expect_agency_modal_heading()
        # Modal is already open
    except:
        # No modal, click to open
        agency_page.click_create_new_agency()
        time.sleep(1)
    
    agency_page.fill_agency_name(agency_name)
    agency_page.click_industry_dropdown()
    agency_page.click_healthcare_option()
    agency_page.fill_website(website)
    agency_page.fill_address(address)
    agency_page.fill_description(description)
    agency_page.click_agency_save_button()
    wait_for_action_completion(page, "save")
    
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
    """Assert agency created successfully message is visible"""
    from pages.agency_page import AgencyPage
    agency_page = AgencyPage(page)
    enhanced_assert_visible(page, agency_page.locators.agency_created_successfully_message, 
                          "Agency created successfully message should be visible")

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
