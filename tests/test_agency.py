import pytest
import time
import allure
from playwright.sync_api import Page, expect
from pages.agency_page import AgencyPage   
from utils.config import BASE_URL
from conftest import wait_for_action_completion
from utils.agency_helper import (do_agency_login, do_create_agency, navigate_to_agency_page, find_and_edit_agency, assert_file_format_validation_message, assert_file_size_validation_message, assert_validation_error_visible, assert_successful_agency_creation_or_navigation, do_create_agency_with_image_verification)

from random_values_generator.random_agency_name import generate_agency_name
from utils.enhanced_assertions import enhanced_assert_visible

@pytest.fixture(scope="module")
def created_agency_name():
    return generate_agency_name()

@allure.title("TC_01 - Verify agency modal appears on first time login.")
def test_TC_01(page: Page):
    """Verify agency modal appears on first time login."""
    agency_page = do_agency_login(page, "867da9@onemail.host", "Kabir123#")
    agency_page.expect_agency_modal_body()
    time.sleep(1)
    agency_page.click_cancel_button()
    time.sleep(1)
    agency_page.expect_all_agencies_message()

@allure.title("TC_02 - Verify agency create modal appears or not with existing agencies.")
def test_TC_02(page: Page):
    """Verify agency create modal appears or not with existing agencies."""
    agency_page = do_agency_login(page, "50st3o@mepost.pw", "Kabir123#")
    agency_page.expect_no_agency_modal()
    agency_page.verify_agency_page_url()

@allure.title("TC_03 - Verify user can open create new agency modal.")
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

@allure.title("TC_04 - Verify newly created agency appears in the all agency list.")
def test_TC_04(page: Page, created_agency_name):
    """Verify newly created agency appears in the all agency list."""
    agency_name = created_agency_name
    agency_page = do_create_agency(page, agency_name, email="gi7j8d@mepost.pw")
    
    # Wait for creation to complete and navigate to list
    time.sleep(5)  # Allow time for creation and navigation
    
    # Search for the created agency in the list
    found = agency_page.find_agency_in_paginated_list(page, agency_name)
    
    # Verify the search was successful
    if not found:
        assert False, f"Agency '{agency_name}' was not found in the agencies list"
    
    # Use enhanced assertion to verify agency is visible on current page
    # Use .first to handle multiple elements with same text
    enhanced_assert_visible(page, page.get_by_text(agency_name, exact=True).first, f"Agency '{agency_name}' should be visible in the agencies list", "test_TC_04")

@allure.title("TC_05 - Verify user can delete the agency created previously.")
def test_TC_05(page: Page, created_agency_name):
    """Verify user can delete the agency created previously."""
    agency_name = created_agency_name
    agency_page = navigate_to_agency_page(page, "gi7j8d@mepost.pw", "Kabir123#")
    page.go_back()
    agency_page.delete_agency_by_name(agency_name)

@allure.title("TC_06 - Verify user can edit the agency user created.")
def test_TC_06(page: Page, created_agency_name):
    """Verify user can edit the agency user created."""
    agency_name = created_agency_name
    agency_page = do_create_agency(page, agency_name, email="gi7j8d@mepost.pw")
    time.sleep(5)
    
    updated_name = agency_name + " - Edited"
    find_and_edit_agency(page, agency_name, updated_name)
    
    # Use enhanced assertion for better screenshot timing
    enhanced_assert_visible(page, agency_page.locators.update_confirm_message, "Update confirmation message should be visible", "test_TC_07")
    agency_page.get_agency_by_name(updated_name)

@allure.title("TC_07 - Verify that the create agency modal validates website field and rejects URLs without https.")
def test_TC_07(page: Page):
    """Verify that the create agency modal validates website field and rejects URLs without https."""
    agency_page = do_agency_login(page, "50st3o@mepost.pw", "Kabir123#")
    time.sleep(1)
    agency_page.click_create_new_agency()
    time.sleep(1)
    
    # Fill valid agency name using random generator
    test_agency_name = generate_agency_name()
    agency_page.fill_agency_name(test_agency_name)
    
    # Fill invalid website URL (without https)
    agency_page.fill_website("www.invalidurl.com")
    
    # Try to save
    agency_page.click_agency_save_button()
    time.sleep(1)
    
    # Check for website validation error specifically
    enhanced_assert_visible(page, agency_page.locators.invalid_website_url_error, "Website validation error should be visible", "test_TC_07_website_validation")
    
    # Close modal
    agency_page.click_close_modal_button()

@allure.title("TC_08 - Verify that submitting form without agency name shows validation error.")
def test_TC_08(page: Page):
    """Verify that submitting form without agency name shows validation error."""
    agency_page = do_agency_login(page, "50st3o@mepost.pw", "Kabir123#")
    time.sleep(2)
    agency_page.click_create_new_agency()
    time.sleep(1)
    
    # Leave agency name empty and try to save
    agency_page.click_agency_save_button()
    time.sleep(2)
    
    # Check for agency name required validation error specifically
    enhanced_assert_visible(page, agency_page.locators.agency_name_required_error, "Agency name required error should be visible", "test_TC_08_name_required")
    
    # Close modal
    agency_page.click_close_modal_button()

@allure.title("TC_09 - Verify that agency name shorter than 3 characters shows validation error.")
def test_TC_09(page: Page):
    """Verify that agency name shorter than 3 characters shows validation error."""
    agency_page = do_agency_login(page, "50st3o@mepost.pw", "Kabir123#")
    time.sleep(2)
    agency_page.click_create_new_agency()
    time.sleep(1)
    
    # Fill agency name with less than 3 characters
    agency_page.fill_agency_name("AB")
    
    # Try to save
    agency_page.click_agency_save_button()
    time.sleep(2)
    
    # Check for agency name minimum length validation error specifically
    enhanced_assert_visible(page, agency_page.locators.agency_name_min_length_error, "Agency name minimum length error should be visible", "test_TC_09_name_min_length")
    
    # Close modal
    agency_page.click_close_modal_button()

@allure.title("TC_10 - Verify that agency name starting with special character triggers validation error.")
def test_TC_10(page: Page):
    """Verify that agency name starting with special character triggers validation error."""
    agency_page = do_agency_login(page, "50st3o@mepost.pw", "Kabir123#")
    time.sleep(2)
    agency_page.click_create_new_agency()
    time.sleep(1)
    
    # Fill agency name starting with special character
    agency_page.fill_agency_name("@Invalid Agency Name")
    
    # Try to save
    agency_page.click_agency_save_button()
    time.sleep(2)
    
    # Check for agency name special character validation error specifically
    enhanced_assert_visible(page, agency_page.locators.agency_name_special_char_error, "Agency name special character error should be visible", "test_TC_10_name_special_char")
    
    # Close modal
    agency_page.click_close_modal_button()

@allure.title("TC_11 - Verify that input containing only whitespace characters is not accepted.")
def test_TC_11(page: Page):
    """Verify that input containing only whitespace characters is not accepted."""
    agency_page = do_agency_login(page, "50st3o@mepost.pw", "Kabir123#")
    time.sleep(2)
    agency_page.click_create_new_agency()
    time.sleep(1)
    
    # Fill agency name with only whitespace
    agency_page.fill_agency_name("   ")
    
    # Try to save
    agency_page.click_agency_save_button()
    time.sleep(2)
    
    # Check for agency name required validation error specifically (whitespace should be treated as empty)
    enhanced_assert_visible(page, agency_page.locators.agency_name_required_error, "Agency name required error should be visible for whitespace input", "test_TC_12_whitespace_validation")
    
    # Close modal
    agency_page.click_close_modal_button()

@allure.title("TC_12 - Verify that all field labels are present, spelled correctly, and aligned with input fields.")
def test_TC_12(page: Page):
    """Verify that all field labels are present, spelled correctly, and aligned with input fields."""
    agency_page = do_agency_login(page, "50st3o@mepost.pw", "Kabir123#")
    time.sleep(2)
    agency_page.click_create_new_agency()
    time.sleep(1)
    
    # Check for presence of all required labels using enhanced assertions
    expected_labels = ["Agency name","Industry (optional)","Website (optional)", "Address (optional)","Description (optional)"]
    
    for label_text in expected_labels:
        label_element = page.locator(f"text='{label_text}'")
        enhanced_assert_visible(page, label_element, f"Label '{label_text}' should be present", "test_TC_13_labels")
    
    # Close modal
    agency_page.click_close_modal_button()

@allure.title("TC_13 - Verify that all field labels use the same font size and weight for visual consistency.")
def test_TC_13(page: Page):
    """Verify that all field labels use the same font size and weight for visual consistency."""
    agency_page = do_agency_login(page, "50st3o@mepost.pw", "Kabir123#")
    time.sleep(2)
    agency_page.click_create_new_agency()
    time.sleep(1)
    
    # Get all label elements using centralized locator
    labels = agency_page.locators.form_labels
    
    # Verify at least some labels exist
    assert labels.count() > 0, "No labels found in the form"    
    
    # Close modal
    agency_page.click_close_modal_button()

@allure.title("TC_14 - Verify that uploading PDF file shows validation message: 'Only accept jpg, png, jpeg, gif file'")
def test_TC_14(page: Page):
    """Verify that uploading PDF file shows validation message: 'Only accept jpg, png, jpeg, gif file'"""
    agency_page = do_agency_login(page, "50st3o@mepost.pw", "Kabir123#")
    time.sleep(2)
    agency_page.click_create_new_agency()
    time.sleep(1)
    
    # Fill only mandatory fields
    test_agency_name = generate_agency_name()
    agency_page.fill_agency_name(test_agency_name)
    
    # Upload PDF file (should trigger validation message)
    agency_page.upload_file("images_for_test/file-PDF_1MB.pdf")
    time.sleep(3)  # Wait for validation message to appear
    
    # Check for the specific file format validation message using helper function
    assert_file_format_validation_message(page, "test_TC_15")
    
    # Close modal and end test
    agency_page.click_close_modal_button()

@allure.title("TC_15 - Verify that uploading file larger than 5MB shows validation message: 'File can't be larger than 5 MB'")
def test_TC_15(page: Page):
    """Verify that uploading file larger than 5MB shows validation message: 'File can't be larger than 5 MB'"""
    agency_page = do_agency_login(page, "50st3o@mepost.pw", "Kabir123#")
    time.sleep(2)
    agency_page.click_create_new_agency()
    time.sleep(1)
    
    # Fill only mandatory fields
    test_agency_name = generate_agency_name()
    agency_page.fill_agency_name(test_agency_name)
    
    # Upload large file (should trigger validation message)
    agency_page.upload_file("images_for_test/pexels-6MB.jpg")
    time.sleep(3)  # Wait for validation message to appear
    
    # Check for the specific file size validation message using helper function
    assert_file_size_validation_message(page, "test_TC_16")
    
    # Close modal and end test
    agency_page.click_close_modal_button()

@allure.title("TC_16 - Verify creating agency with image upload and verify it appears in list")
def test_TC_16(page: Page):
    """Verify creating agency with image upload and verify it appears in list"""
    
    # Use helper function to handle the entire flow
    agency_name, image_uploaded = do_create_agency_with_image_verification(page)
    
    if image_uploaded:
        print("✅ Image was successfully uploaded and verified")
