import pytest
import time
from playwright.sync_api import Page, expect
from pages.agency_page import AgencyPage   
from utils.config import BASE_URL
from utils.agency_helper import (
    do_agency_login, do_create_agency, navigate_to_agency_page, find_and_edit_agency)

from random_values_generator.random_agency_name import generate_agency_name
from utils.enhanced_assertions import enhanced_assert_visible

@pytest.fixture(scope="module")
def created_agency_name():
    return generate_agency_name()

def test_TC_01(page: Page):
    """Verify agency modal appears on first time login."""
    agency_page = do_agency_login(page, "867da9@onemail.host", "Kabir123#")
    agency_page.expect_agency_modal_body()
    time.sleep(1)
    agency_page.click_cancel_button()
    time.sleep(1)
    agency_page.expect_all_agencies_message()

def test_TC_02(page: Page):
    """Verify agency create modal appears or not with existing agencies."""
    agency_page = do_agency_login(page, "50st3o@mepost.pw", "Kabir123#")
    agency_page.expect_no_agency_modal()
    agency_page.verify_agency_page_url()

def test_TC_03(page: Page):
    """Verify user can open create new agency modal."""
    agency_page = do_agency_login(page, "50st3o@mepost.pw", "Kabir123#")
    time.sleep(3)
    agency_page.click_create_new_agency()
    time.sleep(1)
    agency_page.expect_agency_modal_heading()
    time.sleep(1)
    agency_page.expect_agency_modal_body()
    time.sleep(1)
    agency_page.click_close_modal_button()

def test_TC_04(page: Page, created_agency_name):
    """Verify newly created agency appears in the all agency list."""
    agency_name = created_agency_name
    agency_page = do_create_agency(page, agency_name, email="gi7j8d@mepost.pw")
    
    expect(page.get_by_text("This is a protected route for authenticated users only.")).to_be_visible()
    page.go_back()
    time.sleep(4)
    agency_page.verify_created_agency_appears_in_list(agency_name)

def test_TC_05(page: Page, created_agency_name):
    """Verify user can delete the agency created previously."""
    agency_name = created_agency_name
    agency_page = navigate_to_agency_page(page, "gi7j8d@mepost.pw", "Kabir123#")
    page.go_back()
    agency_page.delete_agency_by_name(agency_name)

def test_TC_06(page: Page, created_agency_name):
    """Verify agency creation and appears in the list."""
    agency_name = created_agency_name
    agency_page = do_agency_login(page, "50st3o@mepost.pw", "Kabir123#")
    agency_page.click_create_new_agency()
    time.sleep(1)
    agency_page.fill_agency_name(agency_name)
    agency_page.click_industry_dropdown()
    agency_page.click_healthcare_option()
    agency_page.fill_website("https://testagency123.com")
    agency_page.fill_address("123 Test Agency St")
    agency_page.fill_description("This is a test agency for automation.")
    agency_page.click_agency_save_button()
    time.sleep(3)
    agency_page.verify_agency_created_successfully()
    time.sleep(12)
    agency_page.find_agency_in_paginated_list(page, agency_name)
    expect(page.get_by_text(agency_name, exact=True)).to_be_visible()

def test_TC_07(page: Page, created_agency_name):
    """Verify user can edit the agency user created."""
    agency_name = created_agency_name
    agency_page = do_create_agency(page, agency_name, email="gi7j8d@mepost.pw")
    time.sleep(5)
    
    updated_name = agency_name + " - Edited"
    find_and_edit_agency(page, agency_name, updated_name)
    
    # Use enhanced assertion for better screenshot timing
    enhanced_assert_visible(page, agency_page.locators.update_confirm_message, 
                           "Update confirmation message should be visible", "test_TC_07")
    agency_page.get_agency_by_name(updated_name)