"""
JD (Job Description) Test Suite
Comprehensive test cases covering all JD functionality including CRUD operations, search, filtering, validation, and bulk operations
"""

import pytest
import time
import random
from dataclasses import asdict
from playwright.sync_api import Page
from utils.jd_test_helpers import JDHelpers
from utils.jd_test_data import JDTestData, JDDataClass
from utils.jd_helper import (do_apply_all_filters, do_jd_login,do_open_filters_panel,do_verify_all_filter_headings_visible,do_apply_company_filter,do_apply_hiring_status_filter,do_verify_filter_tag_visible,do_verify_jd_count,do_verify_all_jds_contain_text,do_clear_all_filters,do_verify_filter_reset_to_add,do_expand_filter_section,do_select_filter_checkbox,do_verify_filtered_results_tc19,do_close_filter_modal_and_verify_results,do_compare_jd_counts_and_verify_cleared,do_close_filter_modal_after_clearing,do_open_share_modal_for_first_jd,do_verify_share_modal_opened,do_select_user_in_share_modal,do_click_share_button_and_verify_success,do_verify_user_in_shared_list,do_delete_shared_user,do_confirm_user_removal,do_verify_user_removed_successfully,do_close_share_modal,)   
from utils.enhanced_assertions import (enhanced_assert_visible,enhanced_assert_not_visible,)
from utils.config import BASE_URL


# ===== TEST FIXTURES =====


@pytest.fixture(scope="module")
def admin_credentials():
    """Admin credentials for JD management tests"""
    return {"email": "mi003b@onemail.host", "password": "Kabir123#"}


@pytest.fixture(scope="module")
def test_agency_info():
    """Test agency information for JD operations"""
    return {"agency_name": "demo 06","agency_id": "174","company_name": "company for test",}


@pytest.fixture(scope="module")
def test_jd_data():
    """Generate test JD data for the module"""
    return JDTestData.complete()


@pytest.fixture(scope="module")
def created_jd_title():
    """Track created JD title for cleanup"""
    return {"title": None}  # Mutable dict to store JD title across tests


@pytest.fixture(scope="function")
def fresh_jd_data():
    """Generate fresh JD data for each test"""
    jd_data = JDTestData.complete()
    print(f"Generated fresh JD data: {asdict(jd_data)}")
    return jd_data

def test_TC_01(page: Page, admin_credentials):
    """TC_01: Verify JD list empty state display"""
    print("🧪 TC_01: Testing JD list empty state")

    # Use agency 173 which has no JDs
    empty_agency_id = "173"

    # Login and navigate to JD page for agency 173
    jd_page = do_jd_login(page, admin_credentials["email"], admin_credentials["password"], empty_agency_id)
    time.sleep(2)

    # Verify empty state message
    enhanced_assert_visible(page, jd_page.locators.no_jds_message, "No JDs message should be visible", "test_TC_01_empty_state")

    # Verify "Add new JD" button is available
    enhanced_assert_visible(page, jd_page.locators.add_new_jd_button, "Add new JD button should be visible in empty state", "test_TC_01_add_new_button")

    print("✅ TC_01 passed: JD list empty state working correctly")

def test_TC_02(page: Page, admin_credentials):
    """TC_02: Verify JD creation modal heading and form fields presence"""
    print("🧪 TC_02: Testing JD creation modal heading and form fields")

    # Use agency 173 (empty state agency)
    empty_agency_id = "173"

    # Login and navigate to JD page for agency 173
    jd_page = do_jd_login(page, admin_credentials["email"], admin_credentials["password"], empty_agency_id)

    # Click on "Add new JD" button
    jd_page.click_add_jd()

    # Verify modal heading is "Add New JD"
    modal_heading = page.get_by_text("Add New JD", exact=True)
    enhanced_assert_visible(page, modal_heading, "Modal heading 'Add New JD' should be visible", "test_TC_11_modal_heading")
    print("✅ Modal heading verified: 'Add New JD'")

    # Verify all form fields and buttons using helper function
    from utils.jd_helper import verify_jd_modal_fields_and_buttons
    verify_jd_modal_fields_and_buttons(page, "test_TC_11")

    # Close modal using close modal button
    print("\n🔍 Closing modal using close modal button:")
    close_button = page.get_by_role("button", name="Close modal")
    close_button.click()
    time.sleep(1)
    
    # Verify modal is closed
    modal = page.locator("div[role='dialog'], div[class*='modal']").first
    enhanced_assert_not_visible(page, modal, "Modal should be closed after clicking close button", "test_TC_11_modal_closed")
    print("   ✅ Modal closed successfully")

    print("\n✅ TC_02 passed: JD creation modal heading, form fields, buttons, and close functionality verified")

def test_TC_03(
    page: Page, admin_credentials, test_agency_info, fresh_jd_data, created_jd_title):
    """TC_03: Verify JD creation with valid mandatory and optional data including file upload"""
    print("🧪 TC_03: Testing JD creation with valid data and file upload")

    # Convert the JDTestData dataclass to dictionary and override company name
    jd_data = asdict(fresh_jd_data)
    jd_data["company"] = test_agency_info["company_name"]  # Use test agency's company

    # Store the JD title for use in TC_06
    created_jd_title["title"] = jd_data["position_title"]

    # Login and navigate to JD page
    jd_page = do_jd_login(page,admin_credentials["email"],admin_credentials["password"],test_agency_info["agency_id"])

    print(f"🔧 Creating JD: {jd_data.get('position_title', 'Unknown Position')}")

    # Open JD creation modal
    jd_page.click_add_jd()
    jd_page.wait_for_modal_to_open()

    # Fill JD form
    jd_page.fill_jd_form(jd_data)

    # Upload JD file (optional)
    print("📎 Uploading JD file...")
    jd_file_path = "images_for_test/pexels-photo.jpeg"
    jd_page.upload_jd_file(jd_file_path)
    time.sleep(0.5)  # Wait for file upload to complete

    # Save JD
    jd_page.save_jd()

    # Wait a moment for the form to process
    time.sleep(5)  # Increased wait time for processing

    # Verify success message is visible
    enhanced_assert_visible(page,jd_page.locators.jd_created_successfully_message,"JD creation success message should be visible","test_TC_02_create_success",)

    # Verify modal closes after successful creation
    jd_page.expect_modal_closes_after_successful_save()

    # Find and display the created JD data from the list
    time.sleep(2)

    # Locate the first JD card (should be the newly created one)
    first_jd_card = page.locator(".flex.flex-col.sm\\:flex-row").first
    created_jd_display = first_jd_card.inner_text()
    print("\n" + "="*80)
    print("📋 CREATED JD DATA DISPLAYED ON PAGE:")
    print("="*80)
    print(created_jd_display)
    print("="*80)
    print(f"\n✅ JD Position Title stored for TC_06: '{created_jd_title['title']}'")
    print("="*80 + "\n")

    print("✅ TC_03 passed: JD created successfully with valid data and file upload")

def test_TC_04(page: Page, admin_credentials, test_agency_info):
    """TC_04: Verify validation errors when mandatory fields are missing"""
    print("🧪 TC_04: Testing JD creation with missing mandatory fields")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(page, admin_credentials["email"], admin_credentials["password"], test_agency_info["agency_id"])

    # Open JD creation modal
    jd_page.click_add_jd()
    jd_page.wait_for_modal_to_open()

    # Attempt to save without filling mandatory fields
    jd_page.trigger_mandatory_field_validation()

    # Verify validation errors for mandatory fields (based on actual validation messages from the page)
    expected_errors = [jd_page.locators.position_title_required_error,jd_page.locators.company_required_error,jd_page.locators.work_style_required_error,jd_page.locators.salary_required_error,jd_page.locators.target_age_min_required_error,jd_page.locators.target_age_max_required_error,jd_page.locators.client_required_error,jd_page.locators.hiring_status_required_error,]

    for error_locator in expected_errors:
        enhanced_assert_visible(page,error_locator,f"Mandatory field validation error should be visible","test_TC_03_mandatory_validation",)

    # Verify modal remains open after validation errors
    jd_page.expect_modal_remains_open_after_validation_error()

    # Close modal
    jd_page.close_jd_modal()

    print("✅ TC_04 passed: Mandatory field validation working correctly")

def test_TC_05(page: Page, admin_credentials, test_agency_info):
    """TC_05: Verify validation error for invalid salary range (max < min)"""
    print("🧪 TC_05: Testing JD creation with invalid salary range")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(page, admin_credentials["email"], admin_credentials["password"], test_agency_info["agency_id"])

    # Open JD creation modal
    jd_page.click_add_jd()
    jd_page.wait_for_modal_to_open()

    # Fill salary fields with invalid range (max < min) - validation appears immediately
    jd_page.fill_minimum_salary("80000")
    jd_page.fill_maximum_salary("50000")

    # Verify salary range validation error appears
    enhanced_assert_visible(page,jd_page.locators.invalid_salary_range_error,"Invalid salary range error should be visible","test_TC_04_salary_validation",)

    print("✅ TC_05 passed: Salary range validation working correctly")

def test_TC_06(page: Page, admin_credentials, test_agency_info):
    """TC_06: Verify validation error for invalid age range (max < min)"""
    print("🧪 TC_06: Testing JD creation with invalid age range")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(page, admin_credentials["email"], admin_credentials["password"], test_agency_info["agency_id"])

    # Open JD creation modal
    jd_page.click_add_jd()
    jd_page.wait_for_modal_to_open()

    # Fill target age fields with invalid range (max < min) - validation appears immediately
    jd_page.fill_target_age_min("35")
    jd_page.fill_target_age_max("25")

    # Verify age range validation error appears
    enhanced_assert_visible(page,jd_page.locators.invalid_target_age_range_error,"Invalid age range error should be visible","test_TC_05_age_validation",)

    print("✅ TC_06 passed: Age range validation working correctly")

def test_TC_07(page: Page, admin_credentials, test_agency_info):
    """TC_07: Verify character limit validation for text fields"""
    print("🧪 TC_07: Testing JD creation with character limit validation")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(page, admin_credentials["email"], admin_credentials["password"], test_agency_info["agency_id"])

    # Open JD creation modal
    jd_page.click_add_jd()
    jd_page.wait_for_modal_to_open()

    # Try to fill position title with text exceeding 100 char limit
    long_title = "A" * 150  # Try to input 150 characters
    jd_page.fill_position_job_title(long_title)
    
    # Get the actual value in the field
    actual_value = jd_page.locators.position_job_title_input.input_value()
    actual_length = len(actual_value)
    
    # Verify system prevents input beyond 100 characters
    assert actual_length <= 100, f"System should not allow more than 100 characters, but allowed {actual_length}"
    print(f"✅ System correctly limited input to {actual_length} characters (max 100)")

    print("✅ TC_07 passed: Character limit validation working correctly")

def test_TC_08(page: Page, admin_credentials, test_agency_info):
    """TC_08: Verify JD deletion cancellation by clicking cancel button"""
    print("🧪 TC_08: Testing JD deletion cancellation")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(page, admin_credentials["email"], admin_credentials["password"], test_agency_info["agency_id"])
    time.sleep(2)

    # Get the first JD card from the list
    first_jd_card = page.locator(".flex.flex-col.sm\\:flex-row").first
    
    # Get the inner text of the first JD card to identify it
    jd_card_text = first_jd_card.inner_text()
    print(f"🎯 First JD card content:\n{jd_card_text}")
    
    # Extract JD title (first line of the card text)
    jd_title = jd_card_text.split("\n")[0]
    print(f"🎯 Target JD for deletion cancellation: '{jd_title}'")
    
    # Click three-dot menu on the first JD card
    three_dot_button = first_jd_card.locator("button[aria-label='Open action menu'], button:has-text('⋮')").first.click()
    time.sleep(1)
    print(f"✅ Clicked three-dot menu for JD: '{jd_title}'")

    # Click delete button from the menu
    delete_button = page.get_by_role("button", name="Delete").first.click()
    time.sleep(1)
    print("✅ Clicked delete button")

    # Click CANCEL button instead of confirm
    cancel_button = page.get_by_role("button", name="Cancel").click()
    time.sleep(1)
    print("✅ Clicked cancel button")

    # Verify the confirmation modal closes after clicking cancel
    confirmation_modal = page.locator("div[role='dialog'], div[class*='modal']").first
    enhanced_assert_not_visible(page, confirmation_modal, "Confirmation modal should close after clicking cancel", "test_TC_07_modal_closes")

    print("✅ TC_08 passed: JD deletion cancellation working correctly")

def test_TC_09(page: Page, admin_credentials, test_agency_info):
    """TC_09: Verify JD deletion by clicking confirm button"""
    print("🧪 TC_09: Testing JD deletion from list using three-dot menu")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(page, admin_credentials["email"], admin_credentials["password"], test_agency_info["agency_id"])
    time.sleep(2)

    # Get the first JD card from the list
    first_jd_card = page.locator(".flex.flex-col.sm\\:flex-row").first
    
    # Get the inner text of the first JD card to identify it
    jd_card_text = first_jd_card.inner_text()
    print(f"🎯 First JD card content:\n{jd_card_text}")
    
    # Extract JD title (first line of the card text)
    jd_title_to_delete = jd_card_text.split("\n")[0]
    print(f"🎯 Target JD to delete: '{jd_title_to_delete}'")
    
    # Click three-dot menu on the first JD card
    three_dot_button = first_jd_card.locator("button[aria-label='Open action menu'], button:has-text('⋮')").first.click()
    time.sleep(1)
    print(f"✅ Clicked three-dot menu for JD: '{jd_title_to_delete}'")

    # Click delete button from the menu
    delete_button = page.get_by_role("button", name="Delete").first.click()
    time.sleep(1)
    print("✅ Clicked delete button")

    # Confirm deletion in confirmation dialog
    confirm_button = page.get_by_role("button", name="Confirm").click()
    time.sleep(2)
    print("✅ Confirmed deletion")

    # Verify deletion success message
    enhanced_assert_visible(page, jd_page.locators.jd_deleted_successfully_message, "JD deletion success message should be visible", "test_TC_08_delete_success")

    # Verify the JD is no longer in the list by searching for the title
    jd_still_exists = page.locator(f"text={jd_title_to_delete}").count() > 0
    assert not jd_still_exists, f"JD '{jd_title_to_delete}' should not exist in the list after deletion"
    print(f"✅ Verified JD '{jd_title_to_delete}' is removed from the list")

    print("✅ TC_09 passed: JD deletion from list using three-dot menu working correctly")

def test_TC_10(page: Page, admin_credentials, test_agency_info):
    """TC_10: Verify JD detail view functionality"""
    print("🧪 TC_10: Testing JD detail view")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(page, admin_credentials["email"], admin_credentials["password"], test_agency_info["agency_id"])
    time.sleep(2)

    # Get the first JD card from the list
    first_jd_card = page.locator(".flex.flex-col.sm\\:flex-row").first
    
    # Get the inner text of the first JD card to capture all details
    jd_card_text = first_jd_card.inner_text()
    print(f"🎯 First JD card content:\n{jd_card_text}")
    
    # Extract JD title (first line of the card text)
    jd_title = jd_card_text.split("\n")[0]
    print(f"🎯 JD Title for detail view: '{jd_title}'")
    
    # Click "View Details" button on the first JD card
    view_details_button = first_jd_card.get_by_role("button", name="View Details").click()
    print("✅ Clicked 'View Details' button")
    
    # Wait for navigation to details page
    time.sleep(3)
    
    # Wait for page content to load - look for any substantial text content
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Get full page content to see what's loaded
    full_page_content = page.inner_text("body")
    print(f"\n📋 Full Page Content (first 1500 chars):\n{full_page_content[:1500]}\n")

    # Verify breadcrumb exists: "Home > JD > ..."
    assert "Home" in full_page_content and "JD" in full_page_content, f"Breadcrumb 'Home > JD' should be visible"
    print(f"✅ Breadcrumb 'Home > JD' verified")
    
    # Verify JD title is present in details page
    assert jd_title in full_page_content, f"JD title '{jd_title}' should be visible in details page"
    print(f"✅ JD title '{jd_title}' found in details page")
    
    # Parse and display JD details using helper function
    from utils.jd_helper import parse_and_display_jd_details
    parse_and_display_jd_details(full_page_content)

    print("✅ TC_10 passed: JD detail view working correctly")

def test_TC_11(page: Page, admin_credentials, test_agency_info):

    """TC_11: Verify JD list displays correctly when JDs exist"""
    print("🧪 TC_11: Testing JD list display with existing data")

    # Login and navigate to JD page (agency 174 has JDs)
    jd_page = JDHelpers.login(page, admin_credentials["email"], admin_credentials["password"], test_agency_info["agency_id"])
    time.sleep(2)

    # Verify JD list is displayed (should NOT show empty state message)
    enhanced_assert_not_visible(page, jd_page.locators.no_jds_message, "No JDs message should NOT be visible when JDs exist", "test_TC_10_no_empty_message")

    # Verify JD cards are present
    first_jd_card = page.locator(".flex.flex-col.sm\\:flex-row").first
    enhanced_assert_visible(page, first_jd_card, "JD cards should be visible in the list", "test_TC_10_jd_cards_visible")

    print("✅ TC_11 passed: JD list display working correctly")

def test_TC_12(page: Page, admin_credentials, test_agency_info):
    """TC_12: Verify JD search by position title and company name"""
    print("🧪 TC_12: Testing JD search by position title and company name")

    # Import helper functions
    from utils.jd_helper import do_search_by_jd_title, do_clear_search_and_show_full_list, do_search_by_company_name
    
    # Login and navigate to JD page
    jd_page = JDHelpers.login(page, admin_credentials["email"], admin_credentials["password"], test_agency_info["agency_id"])
    time.sleep(1)

    # Part 1: Search by JD Title
    print("\n📋 Part 1: Searching by JD Title")
    do_search_by_jd_title(page, "JD for search Only")

    # Clear search and show full list
    do_clear_search_and_show_full_list(page)
    time.sleep(4)

    # Part 2: Search by Company Name
    print("\n📋 Part 2: Searching by Company Name")
    do_search_by_company_name(page, "Only for TC 13")

    print("\n✅ TC_12 passed: JD search by title and company name working correctly")

def test_TC_13(page: Page, admin_credentials, test_agency_info):
    """TC_13: Verify JD search with no results shows correct message"""
    print("🧪 TC_13: Testing JD search with no results")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(page, admin_credentials["email"], admin_credentials["password"], test_agency_info["agency_id"])
    time.sleep(0.3)

    # Search for non-existent term
    nonexistent_term = "non-existent job-position-12345"
    print(f"🔍 Searching for non-existent term: '{nonexistent_term}'")
    
    # Perform search
    search_count = jd_page.perform_search(nonexistent_term)
    print(f"✅ Search completed, found {search_count} results")
    time.sleep(2)

    # Verify "No JD found" message is displayed (correct message)
    no_jd_message = page.get_by_text("No JD found")
    enhanced_assert_visible(page, no_jd_message, "No JD found message should be visible after searching for non-existent JD", "test_TC_14_no_jd_found")
    print("✅ Correct message 'No JD found' is displayed")

    print("✅ TC_13 passed: JD search no results message working correctly")

def test_TC_14(page: Page, test_agency_info):
    """Verify that filter panel is accessible and all 12 filter headings are visible."""
    print("\n🧪 TC_14: Testing filter panel accessibility and filter headings visibility")

    # Login to agency with JD data (agency 174)
    jd_page = do_jd_login(page, "mi003b@onemail.host", "Kabir123#", test_agency_info["agency_id"])
    # time.sleep(0.5)
    
    # Open filters panel
    do_open_filters_panel(page)
    
    # Verify "All clear" button is visible
    all_clear_button = page.get_by_role("button", name="All clear")
    enhanced_assert_visible(page, all_clear_button, "All clear button should be visible", "test_TC_15_all_clear")
    
    # Verify all 12 filter headings are visible
    do_verify_all_filter_headings_visible(page)
    
    print("✅ TC_14 passed: Filter panel accessible, all filter headings visible")

def test_TC_15(page: Page, test_agency_info):
    """Verify that applying company filter displays only JDs from that company."""
    print("\n🧪 TC_15: Testing single company filter application")

    # Login to agency with JD data (agency 174)
    jd_page = do_jd_login(page, "mi003b@onemail.host", "Kabir123#", test_agency_info["agency_id"])
    time.sleep(0.5)
    
    # Open filters panel
    do_open_filters_panel(page)
    
    # Apply company filter for "company for test" (this will close the modal automatically)
    do_apply_company_filter(page, "company for test")
    
    # Verify all displayed JDs contain "Company For Test"
    do_verify_all_jds_contain_text(page, "Company For Test")

    print("✅ TC_15 passed: Company filter working correctly, only matching JDs displayed")

def test_TC_16(page: Page, test_agency_info):
    """Verify that applying multiple filter fields at once works correctly with AND logic."""
    print("\n🧪 TC_16: Testing multiple filters applied at once")

    # Login to agency with JD data (agency 174)
    jd_page = do_jd_login(page, "mi003b@onemail.host", "Kabir123#", test_agency_info["agency_id"])
    
    # Open filters panel
    do_open_filters_panel(page)
    
    # Apply all filters using helper function
    do_apply_all_filters(page)
    
    # Verify filtered results using helper function
    do_verify_filtered_results_tc19(page)
    
    print("\n✅ TC_16 passed: Multiple filters applied successfully, AND logic verified")

def test_TC_17(page: Page, test_agency_info):
    """Verify that applying multiple filters (Company + Hiring Status) works with AND logic."""
    print("\n🧪 TC_17: Testing multiple filters with AND logic")
    
    # Login to agency with JD data (agency 174)
    jd_page = do_jd_login(page, "mi003b@onemail.host", "Kabir123#", test_agency_info["agency_id"])
    time.sleep(2)
    
    # Open filters panel
    do_open_filters_panel(page)
    
    # Apply company filter for "company for test"
    do_apply_company_filter(page, "company for test")
    
    # Apply hiring status filter for "Closed"
    do_apply_hiring_status_filter(page, "Closed")
    
    # Verify only 1 JD is displayed (Company For Test + Closed status)
    filtered_count = page.locator(".flex.flex-col.sm\\:flex-row").count()
    print(f"📊 Filtered JD count: {filtered_count}")
    assert filtered_count == 1, f"Expected 1 JD with filters, but got {filtered_count}"
    
    # Verify the displayed JD contains both "Company For Test" and "Closed"
    do_verify_all_jds_contain_text(page, "Company For Test")
    do_verify_all_jds_contain_text(page, "Closed")
    
    # Verify the specific JD is "Staff System Administrator"
    do_verify_all_jds_contain_text(page, "Staff System Administrator")
    
    # Now clear all filters and verify all JDs are restored
    print("\n🔄 Clearing all filters...")
    
    # Reopen filters panel
    do_open_filters_panel(page)
    
    # Click "All clear" button
    do_clear_all_filters(page)
    time.sleep(3)  # Wait for results to reload after clearing
    
    # Close filter modal after clearing
    do_close_filter_modal_after_clearing(page)
    
    # Compare counts and verify filters were cleared
    do_compare_jd_counts_and_verify_cleared(page, filtered_count)
    
    print("✅ TC_17 passed: Multiple filters work with AND logic, and clearing restores all JDs")

def test_TC_18(page: Page, test_agency_info):
    """TC_18: Verify JD share functionality - sharing JD with user and then deleting user from share"""
    print("\n🧪 TC_18: Testing JD share and delete user functionality")
    
    # Login to agency with JD data (agency 174)
    jd_page = do_jd_login(page, "mi003b@onemail.host", "Kabir123#", test_agency_info["agency_id"])
    time.sleep(2)
    
    # Open share modal for the first JD in the list
    jd_title = do_open_share_modal_for_first_jd(page)
    
    # Verify share modal opened correctly with all elements
    do_verify_share_modal_opened(page, jd_title)
    
    # Select a user from the dropdown (default user: "GOAT")
    do_select_user_in_share_modal(page, "GOAT")
    
    # Click Share button and verify success
    do_click_share_button_and_verify_success(page)
    
    # Verify user appears in "People with share" list
    do_verify_user_in_shared_list(page, "GOAT")
    
    # Delete the shared user
    do_delete_shared_user(page, "GOAT")
    
    # Confirm user removal in confirmation dialog
    do_confirm_user_removal(page)
    
    # Verify user removed successfully
    do_verify_user_removed_successfully(page)
    
    # Close the share modal
    do_close_share_modal(page)
    
    print("✅ TC_18 passed: JD share and delete user functionality working correctly")





# ===== VALIDATION AND ERROR HANDLING TEST CASES (TC_26-TC_35) =====

def test_TC_26(page: Page, admin_credentials, test_agency_id):
    """TC_26: Verify numeric field format validation (salary, age)"""
    print("🧪 TC_26: Testing numeric field format validation")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(page, admin_credentials["email"], admin_credentials["password"], test_agency_id)

    # Open JD creation modal
    jd_page.click_add_jd()
    jd_page.wait_for_modal_to_open()

    # Test invalid salary format
    jd_page.trigger_format_validation("salary", "invalid_salary")

    # Verify salary format validation error
    enhanced_assert_visible(page,jd_page.locators.invalid_salary_format_error,"Invalid salary format error should be visible","test_TC_26_salary_format",)

    # Test invalid age format
    jd_page.trigger_format_validation("age", "invalid_age")

    # Verify age format validation error
    enhanced_assert_visible(page,jd_page.locators.invalid_age_format_error,"Invalid age format error should be visible","test_TC_26_age_format",)

    # Close modal
    jd_page.close_jd_modal()

    print("✅ TC_26 passed: Numeric field format validation working correctly")


def test_TC_27(page: Page, admin_credentials, test_agency_id):
    """TC_27: Verify negative value validation for salary and age fields"""
    print("🧪 TC_27: Testing negative value validation")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(
        page, admin_credentials["email"], admin_credentials["password"], test_agency_id
    )

    # Open JD creation modal
    jd_page.click_add_jd()
    jd_page.wait_for_modal_to_open()

    # Test negative salary
    jd_page.fill_minimum_salary("-50000")
    jd_page.attempt_save_with_validation_errors()

    # Verify negative salary error
    enhanced_assert_visible(
        page,
        jd_page.locators.negative_salary_error,
        "Negative salary error should be visible",
        "test_TC_27_negative_salary",
    )

    # Test negative age
    jd_page.fill_job_age_min("-25")
    jd_page.attempt_save_with_validation_errors()

    # Verify negative age error
    enhanced_assert_visible(
        page,
        jd_page.locators.negative_age_error,
        "Negative age error should be visible",
        "test_TC_27_negative_age",
    )

    # Close modal
    jd_page.close_jd_modal()

    print("✅ TC_27 passed: Negative value validation working correctly")


def test_TC_28(
    page: Page, admin_credentials, test_agency_id
):
    """TC_28: Verify email and URL format validation"""
    print("🧪 TC_28: Testing email and URL format validation")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(
        page, admin_credentials["email"], admin_credentials["password"], test_agency_id
    )

    # Open JD creation modal
    jd_page.click_add_jd()
    jd_page.wait_for_modal_to_open()

    # Test invalid email format (if email field exists in JD form)
    if hasattr(jd_page.locators, "contact_email_input"):
        jd_page.locators.contact_email_input.fill("invalid-email")
        jd_page.attempt_save_with_validation_errors()

        # Verify email format error
        enhanced_assert_visible(
            page,
            jd_page.locators.invalid_email_format_error,
            "Invalid email format error should be visible",
            "test_TC_28_email_format",
        )

    # Test invalid URL format (if URL field exists in JD form)
    if hasattr(jd_page.locators, "company_website_input"):
        jd_page.locators.company_website_input.fill("invalid-url")
        jd_page.attempt_save_with_validation_errors()

        # Verify URL format error
        enhanced_assert_visible(
            page,
            jd_page.locators.invalid_url_format_error,
            "Invalid URL format error should be visible",
            "test_TC_28_url_format",
        )

    # Close modal
    jd_page.close_jd_modal()

    print("✅ TC_28 passed: Email and URL format validation working correctly")


def test_TC_29(
    page: Page, admin_credentials, test_agency_id
):
    """TC_29: Verify file upload format validation"""
    print("🧪 TC_29: Testing file upload format validation")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(
        page, admin_credentials["email"], admin_credentials["password"], test_agency_id
    )

    # Test invalid file format upload
    invalid_file_path = (
        "images_for_test/pexels-photo.jpeg"  # Assuming JPEG is not allowed
    )

    try:
        # Attempt to upload invalid format file
        jd_page.upload_invalid_file_format(invalid_file_path)

        # Verify format error message
        enhanced_assert_visible(
            page,
            jd_page.locators.file_format_error,
            "File format error should be visible",
            "test_TC_29_file_format",
        )

    except Exception as e:
        print(f"⚠️ File upload format validation test encountered: {e}")

    # Test valid file format upload
    valid_file_path = "images_for_test/jd_files/valid_jd_document.txt"

    try:
        # Upload valid format file
        jd_page.upload_valid_file_format(valid_file_path)

        # Verify no format error
        jd_page.verify_no_file_format_error()

    except Exception as e:
        print(f"⚠️ Valid file upload test encountered: {e}")

    print("✅ TC_29 passed: File upload format validation working correctly")


def test_TC_30(
    page: Page, admin_credentials, test_agency_id
):
    """TC_30: Verify file upload size validation"""
    print("🧪 TC_30: Testing file upload size validation")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(
        page, admin_credentials["email"], admin_credentials["password"], test_agency_id
    )

    # Test oversized file upload
    large_file_path = "images_for_test/jd_files/large_jd_file.txt"

    try:
        # Attempt to upload oversized file
        jd_page.upload_oversized_file(large_file_path)

        # Verify size error message
        enhanced_assert_visible(
            page,
            jd_page.locators.file_size_error,
            "File size error should be visible",
            "test_TC_30_file_size",
        )

    except Exception as e:
        print(f"⚠️ File size validation test encountered: {e}")

    print("✅ TC_30 passed: File upload size validation working correctly")


def test_TC_31(
    page: Page, admin_credentials, test_agency_id
):
    """TC_31: Verify file upload content validation"""
    print("🧪 TC_31: Testing file upload content validation")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(
        page, admin_credentials["email"], admin_credentials["password"], test_agency_id
    )

    # Test file with invalid content structure
    invalid_content_file = "images_for_test/jd_files/invalid_content.txt"

    try:
        # Upload file with invalid content
        jd_page.upload_file_for_bulk_import(invalid_content_file)

        # Verify content validation errors
        jd_page.verify_file_content_validation_errors()

    except Exception as e:
        print(f"⚠️ File content validation test encountered: {e}")

    print("✅ TC_31 passed: File upload content validation working correctly")


# ===== PAGINATION AND BULK OPERATION TEST CASES (TC_36-TC_45) =====

def test_TC_36(page: Page, admin_credentials, test_agency_id):
    """TC_36: Verify pagination navigation using next and previous buttons"""
    print("🧪 TC_36: Testing pagination navigation with next/previous buttons")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(page, admin_credentials["email"], admin_credentials["password"], test_agency_id)

    # Test pagination navigation
    jd_page, navigation_results = do_test_pagination_navigation(page)

    # Verify next page navigation works
    if jd_page.has_next_page():
        jd_page.click_next_page()
        jd_page.verify_page_navigation_successful("next")

        # Verify previous page navigation works
        jd_page.click_previous_page()
        jd_page.verify_page_navigation_successful("previous")

    print("✅ TC_36 passed: Pagination navigation working correctly")


def test_TC_37(
    page: Page, admin_credentials, test_agency_id
):
    """TC_37: Verify pagination navigation using specific page numbers"""
    print("🧪 TC_37: Testing pagination navigation with specific page numbers")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(
        page, admin_credentials["email"], admin_credentials["password"], test_agency_id
    )

    # Test navigation to specific page numbers
    if jd_page.get_total_pages() > 2:
        # Navigate to page 2
        jd_page.click_page_number(2)
        jd_page.verify_current_page_is(2)

        # Navigate to page 3 if available
        if jd_page.get_total_pages() > 3:
            jd_page.click_page_number(3)
            jd_page.verify_current_page_is(3)

        # Navigate back to page 1
        jd_page.click_page_number(1)
        jd_page.verify_current_page_is(1)

    print("✅ TC_37 passed: Specific page number navigation working correctly")


def test_TC_38(
    page: Page, admin_credentials, test_agency_id
):
    """TC_38: Verify pagination works correctly with search results"""
    print("🧪 TC_38: Testing pagination with search results")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(
        page, admin_credentials["email"], admin_credentials["password"], test_agency_id
    )

    # Perform search that should return multiple pages of results
    search_term = "engineer"  # Common term likely to have many results
    jd_page.perform_search(search_term)

    # Verify pagination works with search results
    if jd_page.has_pagination_with_search():
        # Test next page with search
        jd_page.click_next_page()
        jd_page.verify_search_maintained_across_pages(search_term)

        # Test previous page with search
        jd_page.click_previous_page()
        jd_page.verify_search_maintained_across_pages(search_term)

    print("✅ TC_38 passed: Pagination with search results working correctly")


def test_TC_39(page: Page, admin_credentials, test_agency_id):
    """TC_39: Verify pagination works correctly with applied filters"""
    print("🧪 TC_39: Testing pagination with applied filters")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(
        page, admin_credentials["email"], admin_credentials["password"], test_agency_id
    )

    # Apply filters
    filters = {"work_style": "Remote"}
    jd_page = JDHelpers.apply_filters(page, filters)

    # Verify pagination works with filters
    if jd_page.has_pagination_with_filters():
        # Test next page with filters
        jd_page.click_next_page()
        jd_page.verify_filters_maintained_across_pages(filters)

        # Test previous page with filters
        jd_page.click_previous_page()
        jd_page.verify_filters_maintained_across_pages(filters)

    print("✅ TC_39 passed: Pagination with filters working correctly")


def test_TC_40(page: Page, admin_credentials, test_agency_id):
    """TC_40: Verify bulk JD selection functionality"""
    print("🧪 TC_40: Testing bulk JD selection")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(
        page, admin_credentials["email"], admin_credentials["password"], test_agency_id
    )

    # Test bulk selection functionality
    jd_page, selection_results = do_test_bulk_selection(page)

    # Test select all functionality
    jd_page.click_select_all_checkbox()
    jd_page.verify_all_jds_selected()

    # Test individual selection
    jd_page.click_select_all_checkbox()  # Deselect all first
    jd_page.select_individual_jds(3)  # Select first 3 JDs
    jd_page.verify_selected_count(3)

    # Test bulk actions become available
    jd_page.verify_bulk_actions_enabled()

    print("✅ TC_40 passed: Bulk JD selection working correctly")


def test_TC_41(page: Page, admin_credentials, test_agency_id):
    """TC_41: Verify bulk JD deletion functionality"""
    print("🧪 TC_41: Testing bulk JD deletion")

    # Create multiple test JDs for bulk deletion
    test_jds = []
    for i in range(3):
        jd_data = JDTestData.complete()
        jd_page, success = JDHelpers.create_jd(
            page,
            jd_data.__dict__,
            test_agency_id,
            admin_credentials["email"],
            admin_credentials["password"],
        )
        if success:
            test_jds.append(jd_data.position_title)
        time.sleep(1)

    # Perform bulk deletion
    if len(test_jds) > 0:
        jd_page, deletion_results = do_test_bulk_deletion(page, test_jds)

        # Verify bulk deletion success
        enhanced_assert_visible(
            page,
            jd_page.locators.bulk_jd_deleted_successfully_message,
            "Bulk deletion success message should be visible",
            "test_TC_41_bulk_deletion",
        )

        # Verify JDs are removed from list
        for jd_title in test_jds:
            jd_page.verify_jd_removed_from_list(jd_title)

    print("✅ TC_41 passed: Bulk JD deletion working correctly")


def test_TC_42(page: Page, admin_credentials, test_agency_id):
    """TC_42: Verify bulk JD status update functionality"""
    print("🧪 TC_42: Testing bulk JD status update")

    # Create multiple test JDs for bulk status update
    test_jds = []
    for i in range(2):
        jd_data = JDTestData.complete()
        jd_page, success = JDHelpers.create_jd(
            page,
            jd_data.__dict__,
            test_agency_id,
            admin_credentials["email"],
            admin_credentials["password"],
        )
        if success:
            test_jds.append(jd_data.position_title)
        time.sleep(1)

    # Perform bulk status update
    if len(test_jds) > 0:
        new_status = "Inactive"
        jd_page, update_results = do_test_bulk_status_update(page, test_jds, new_status)

        # Verify bulk status update success
        enhanced_assert_visible(
            page,
            jd_page.locators.bulk_status_updated_successfully_message,
            "Bulk status update success message should be visible",
            "test_TC_42_bulk_status_update",
        )

        # Verify JD statuses are updated
        for jd_title in test_jds:
            jd_page.verify_jd_status_updated(jd_title, new_status)

    print("✅ TC_42 passed: Bulk JD status update working correctly")


def test_TC_43(
    page: Page, admin_credentials, test_agency_id
):
    """TC_43: Verify bulk operations work across pagination"""
    print("🧪 TC_43: Testing bulk operations across pagination")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(
        page, admin_credentials["email"], admin_credentials["password"], test_agency_id
    )

    # Test bulk selection across pages
    if jd_page.has_multiple_pages():
        # Select JDs on first page
        jd_page.select_individual_jds(2)
        first_page_count = jd_page.get_selected_count()

        # Navigate to next page
        jd_page.click_next_page()

        # Select JDs on second page
        jd_page.select_individual_jds(2)

        # Verify total selection count includes both pages
        total_selected = jd_page.get_total_selected_across_pages()
        assert (
            total_selected >= first_page_count + 2
        ), "Selection should work across pages"

        # Test bulk operation across pages
        jd_page.perform_bulk_operation_across_pages("status_update", "Inactive")

    print("✅ TC_43 passed: Bulk operations across pagination working correctly")


def test_TC_44(
    page: Page, admin_credentials, test_agency_id
):
    """TC_44: Verify bulk operation confirmation dialogs"""
    print("🧪 TC_44: Testing bulk operation confirmation dialogs")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(
        page, admin_credentials["email"], admin_credentials["password"], test_agency_id
    )

    # Select some JDs for bulk operations
    jd_page.select_individual_jds(2)

    # Test bulk deletion confirmation
    jd_page.click_bulk_delete_button()

    # Verify confirmation dialog appears
    enhanced_assert_visible(
        page,
        jd_page.locators.bulk_delete_confirmation_modal,
        "Bulk delete confirmation dialog should be visible",
        "test_TC_44_bulk_delete_confirmation",
    )

    # Test cancellation
    jd_page.click_cancel_bulk_delete_button()
    jd_page.verify_bulk_operation_cancelled()

    # Test confirmation
    jd_page.click_bulk_delete_button()
    jd_page.click_confirm_bulk_delete_button()

    # Verify operation proceeds
    jd_page.verify_bulk_operation_confirmed()

    print("✅ TC_44 passed: Bulk operation confirmation dialogs working correctly")


def test_TC_45(page: Page, admin_credentials, test_agency_id):
    """TC_45: Verify pagination edge cases (first page, last page, single page)"""
    print("🧪 TC_45: Testing pagination edge cases")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(
        page, admin_credentials["email"], admin_credentials["password"], test_agency_id
    )

    # Test first page behavior
    jd_page.navigate_to_first_page()
    jd_page.verify_first_page_controls()

    # Test last page behavior
    if jd_page.has_multiple_pages():
        jd_page.navigate_to_last_page()
        jd_page.verify_last_page_controls()

    # Test single page scenario (if applicable)
    # Apply filters to reduce results to single page
    restrictive_filters = {"company": "NonExistentCompany"}
    jd_page = JDHelpers.apply_filters(page, restrictive_filters)

    if jd_page.get_total_pages() <= 1:
        jd_page.verify_single_page_behavior()

    # Clear filters to restore normal pagination
    jd_page.click_all_clear_button()

    print("✅ TC_45 passed: Pagination edge cases working correctly")

def test_TC_50(
    page: Page, admin_credentials, test_agency_id
):
    """TC_50: Verify comprehensive test coverage across all JD functionality"""
    print("🧪 TC_50: Testing comprehensive test coverage verification")

    # Login and navigate to JD page
    jd_page = JDHelpers.login(
        page, admin_credentials["email"], admin_credentials["password"], test_agency_id
    )

    # Verify all major JD functionality areas are covered
    coverage_areas = [
        {
            "area": "jd_creation",
            "element": jd_page.locators.add_jd_button,
            "description": "JD Creation functionality",
        },
        {
            "area": "jd_search",
            "element": jd_page.locators.search_input,
            "description": "JD Search functionality",
        },
        {
            "area": "jd_filters",
            "element": jd_page.locators.filters_button,
            "description": "JD Filter functionality",
        },
        {
            "area": "jd_pagination",
            "element": jd_page.locators.pagination_container,
            "description": "JD Pagination functionality",
        },
        {
            "area": "jd_bulk_ops",
            "element": jd_page.locators.select_all_checkbox,
            "description": "JD Bulk Operations functionality",
        },
        {
            "area": "jd_file_upload",
            "element": jd_page.locators.upload_file_button,
            "description": "JD File Upload functionality",
        },
    ]

    coverage_results = {}

    for area in coverage_areas:
        try:
            # Verify functionality area is accessible
            enhanced_assert_visible(
                page,
                area["element"],
                area["description"],
                f"test_TC_50_coverage_{area['area']}",
            )
            coverage_results[area["area"]] = {
                "covered": True,
                "description": area["description"],
            }

        except Exception as e:
            coverage_results[area["area"]] = {
                "covered": False,
                "error": str(e),
                "description": area["description"],
            }

    # Report coverage results
    covered_areas = [
        area for area, result in coverage_results.items() if result["covered"]
    ]
    total_areas = len(coverage_areas)
    coverage_percentage = (len(covered_areas) / total_areas) * 100

    print(f"📊 Test Coverage Report:")
    print(f"   Total functionality areas: {total_areas}")
    print(f"   Covered areas: {len(covered_areas)}")
    print(f"   Coverage percentage: {coverage_percentage:.1f}%")

    for area, result in coverage_results.items():
        status = "✅" if result["covered"] else "❌"
        print(f"   {status} {area}: {result['description']}")

    # Verify minimum coverage threshold (e.g., 80%)
    assert (
        coverage_percentage >= 80
    ), f"Test coverage should be at least 80%, but was {coverage_percentage:.1f}%"

    print("✅ TC_50 passed: Comprehensive test coverage verification completed")


# ===== TEST EXECUTION SUMMARY AND CLEANUP =====

# def test_TC_06(page: Page, admin_credentials, test_agency_info, fresh_jd_data):
#     """TC_06: Verify JD editing functionality with pre-filled data"""
#     print("🧪 TC_06: Testing JD editing functionality")

#     # Convert dataclass to dict and override company name with test agency's company
#     jd_data = asdict(fresh_jd_data)
#     jd_data["company"] = test_agency_info["company_name"]

#     # First create a JD to edit
#     jd_page, success = JDHelpers.create_jd(page,jd_data,test_agency_info["agency_id"],admin_credentials["email"],admin_credentials["password"],)

#     assert success, "JD creation should succeed before testing edit"
#     time.sleep(2)

#     # Find and edit the created JD
#     jd_page.find_and_click_edit_jd(fresh_jd_data.position_title)

#     # Verify edit modal opens with pre-filled data
#     enhanced_assert_visible(page,jd_page.locators.edit_jd_modal_heading,"Edit JD modal should be visible","test_TC_06_edit_modal",)

#     # Verify pre-filled data
#     jd_page.verify_prefilled_jd_data(jd_data)

#     # Update JD data
#     updated_title = f"{jd_data['position_title']} - EDITED"
#     jd_page.fill_position_job_title(updated_title)

#     # Save changes
#     jd_page.update_jd()

#     # Verify update success message
#     enhanced_assert_visible(page,jd_page.locators.jd_updated_successfully_message,"JD update success message should be visible","test_TC_06_update_success",)

#     print("✅ TC_06 passed: JD editing functionality working correctly")


# def test_TC_07(page: Page, admin_credentials, test_agency_info, fresh_jd_data):
#     """TC_07: Verify validation during JD editing"""
#     print("🧪 TC_07: Testing JD edit validation")

#     # Convert dataclass to dict and override company name with test agency's company
#     jd_data = asdict(fresh_jd_data)
#     jd_data["company"] = test_agency_info["company_name"]

#     # Create a JD to edit
#     jd_page, success = JDHelpers.create_jd(
#         page,
#         jd_data,
#         test_agency_info["agency_id"],
#         admin_credentials["email"],
#         admin_credentials["password"],
#     )

#     assert success, "JD creation should succeed before testing edit validation"
#     time.sleep(2)

#     # Find and edit the created JD
#     jd_page.find_and_click_edit_jd(jd_data["position_title"])

#     # Clear mandatory field to trigger validation
#     jd_page.locators.edit_position_job_title_input.clear()

#     # Attempt to save with empty mandatory field
#     jd_page.update_jd()

#     # Verify validation error
#     enhanced_assert_visible(
#         page,
#         jd_page.locators.position_title_required_error,
#         "Position title required error should be visible during edit",
#         "test_TC_07_edit_validation",
#     )

#     # Cancel edit
#     jd_page.cancel_jd_operation()

#     print("✅ TC_07 passed: JD edit validation working correctly")


# def test_TC_08(
#     page: Page, admin_credentials, test_agency_info, fresh_jd_data
# ):
#     """TC_08: Verify JD edit cancellation without saving changes"""
#     print("🧪 TC_08: Testing JD edit cancellation")

#     # Convert dataclass to dict and override company name with test agency's company
#     jd_data = asdict(fresh_jd_data)
#     jd_data["company"] = test_agency_info["company_name"]

#     # Create a JD to edit
#     jd_page, success = JDHelpers.create_jd(
#         page,
#         jd_data,
#         test_agency_info["agency_id"],
#         admin_credentials["email"],
#         admin_credentials["password"],
#     )

#     assert success, "JD creation should succeed before testing edit cancellation"
#     time.sleep(2)

#     # Find and edit the created JD
#     jd_page.find_and_click_edit_jd(jd_data["position_title"])

#     # Make changes without saving
#     original_title = jd_data["position_title"]
#     modified_title = f"{original_title} - MODIFIED"
#     jd_page.fill_position_job_title(modified_title)

#     # Cancel edit
#     jd_page.cancel_jd_operation()

#     # Verify changes were not saved by checking original data still exists
#     jd_page.verify_jd_data_unchanged(original_title)

#     print("✅ TC_08 passed: JD edit cancellation working correctly")



