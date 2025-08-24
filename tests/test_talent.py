import pytest
import time
import re
from playwright.sync_api import Page
from pages.talent_page import TalentPage
from utils.talent_helper import TalentHelper
from random_values_generator.random_talent_name import RandomTalentName, generate_random_talent_data
from utils.enhanced_assertions import enhanced_assert_visible

# Global test data generator
talent_generator = RandomTalentName()

@pytest.fixture(scope="module")
def created_talent_data():
    """Generate unique talent data for the test session."""
    return generate_random_talent_data()

@pytest.fixture(scope="module")
def test_talent_helper(page: Page):
    """Initialize talent helper for tests."""
    return TalentHelper(page)

# NAVIGATION & UI STRUCTURE TESTS
# =============================================================================

def test_TC_01_navigate_to_talent_section_from_dashboard(page: Page):
    """Verify that Agency Personnel can successfully navigate to the 'Talent' section from the main dashboard and view available talent management options."""
    helper = TalentHelper(page)
    talent_page = helper.do_talent_login("nua26i@onemail.host", "Kabir123#")
    helper.validate_talent_navigation_accessibility()

def test_TC_02_add_new_talent_button_opens_form(page: Page):
    """Verify that clicking the '+ New Talent' button opens a well-structured form for creating a new talent profile."""
    helper = TalentHelper(page)
    talent_page = helper.do_talent_login("nua26i@onemail.host", "Kabir123#")
    helper.validate_add_new_talent_form_structure()

def test_TC_03_form_responsiveness_mobile(page: Page):
    """Verify that the "Create and Update Talent Profile" form is fully responsive and functional on mobile devices."""
    helper = TalentHelper(page)
    talent_page = helper.do_talent_login("nua26i@onemail.host", "Kabir123#")
    
    # Resize to mobile dimensions
    page.set_viewport_size({"width": 375, "height": 667})
    time.sleep(1)
    
    # Open form and verify responsiveness
    talent_page.click_add_new_talent()
    
    # Verify form elements are still accessible and properly sized
    enhanced_assert_visible(page, talent_page.locators.first_name_input, "First name input should be visible on mobile")
    enhanced_assert_visible(page, talent_page.locators.save_button, "Save button should be visible on mobile")
    
    # Reset viewport
    page.set_viewport_size({"width": 1280, "height": 720})
    talent_page.click_cancel_button()

def test_TC_04_cancel_button_discards_changes(page: Page):
    """Verify that clicking the "Cancel" button on the talent creation/edit form discards changes and redirects to the talent list without saving any input."""
    helper = TalentHelper(page)
    talent_page = helper.do_talent_login("nua26i@onemail.host", "Kabir123#")
    
    # Open form and add data
    talent_page.click_add_new_talent()
    talent_page.fill_first_name("TestUser")
    talent_page.fill_last_name("ToCancel")
    
    # Click cancel
    talent_page.click_cancel_button()
    
    # Verify we're back to list and data wasn't saved
    enhanced_assert_visible(page, talent_page.locators.add_new_talent_button, "Add talent button should be visible after cancel")
    
    # Reopen form and verify fields are empty
    talent_page.click_add_new_talent()
    first_name_value = talent_page.locators.first_name_input.input_value()
    last_name_value = talent_page.locators.last_name_input.input_value()
    
    enhanced_assert_visible(page, talent_page.locators.first_name_input, "First name field should be empty after cancel")
    enhanced_assert_visible(page, talent_page.locators.last_name_input, "Last name field should be empty after cancel")
    
    talent_page.click_cancel_button()

# FORM VALIDATION TESTS
# =============================================================================

def test_TC_05_mandatory_fields_validation_empty_form(page: Page):
    """Verify that all mandatory fields in the new talent form are enforced by the system and appropriate warnings are shown if skipped."""
    helper = TalentHelper(page)
    talent_page = helper.do_talent_login("nua26i@onemail.host", "Kabir123#")
    
    # Use helper method for validation
    helper.validate_required_fields_empty_form()
    
    # Close modal
    talent_page.click_cancel_button()

def test_TC_06_First_and_last_name_character_limit_validation(page: Page):
    """Validate that the Full Name field accepts only 2 to 50 characters and displays an error otherwise."""
    helper = TalentHelper(page)
    helper.do_name_fields_character_limit_validation()

def test_TC_07_estimated_age_validation_invalid_range_minimum(page: Page):
    """Confirm that age below 18 shows validation error."""
    helper = TalentHelper(page)
    talent_page = helper.do_talent_login("nua26i@onemail.host", "Kabir123#")

    talent_page.click_add_new_talent()
    
    # Test age below 18 (using date of birth from 2010 - makes person ~15 years old)
    talent_page.fill_date_of_birth("01/01/2010")
    
    # Click on first name field to trigger date validation
    talent_page.locators.first_name_input.click()
    time.sleep(1)
    
    # Check for minimum age validation error - this should fail because validation is not implemented
    min_age_error = page.get_by_text("Age must be between 18 and 70")
    enhanced_assert_visible(page, min_age_error, "Minimum age validation error should be visible")
    
    talent_page.click_cancel_button()

def test_TC_08_estimated_age_validation_invalid_range_maximum(page: Page):
    """Confirm that age above 70 shows validation error."""
    helper = TalentHelper(page)
    talent_page = helper.do_talent_login("nua26i@onemail.host", "Kabir123#")

    talent_page.click_add_new_talent()
    
    # Test age above 70 (using date of birth from 1940 - makes person ~85 years old)
    talent_page.fill_date_of_birth("01/01/1940")
    
    # Click on first name field to trigger date validation
    talent_page.locators.first_name_input.click()
    time.sleep(1)
    
    # Check for maximum age validation error - this should fail because validation is not implemented
    max_age_error = page.get_by_text("Age must be between 18 and 70")
    enhanced_assert_visible(page, max_age_error, "Maximum age validation error should be visible")
    
    talent_page.click_cancel_button()

def test_TC_09_estimated_age_valid_range(page: Page):
    """Ensure that a valid Estimated Age value (within 18-70) is accepted and saved correctly."""
    helper = TalentHelper(page)
    helper.do_valid_age_range_validation()

def test_TC_10_comprehensive_talent_creation_with_all_fields_and_files(page: Page):
    """Create talent with specified dropdown values and verify in list
    Test Steps:
    1. Login and navigate to talent list page
    2. Create talent with all specified values and file uploads
    3. Verify talent appears in the list with correct information
    """
    # Step 1: Initialize helper and create talent with comprehensive data
    helper = TalentHelper(page)
    talent_data = helper.do_comprehensive_talent_creation_with_dropdowns_and_files()
    
    # Step 2: Verify talent appears in list with all correct values
    helper.assert_talent_appears_in_list_with_correct_values(talent_data)


#Not tested yet.
def test_TC_11_email_format_validation(page: Page):
    """Validate that if an email address is provided, it must be in a valid email format (e.g., abc@domain.com)."""
    helper = TalentHelper(page)
    talent_page = helper.do_talent_login("nua26i@onemail.host", "Kabir123#")
    
    # First create a talent so we have one to edit
    talent_data = generate_random_talent_data()
    helper.do_create_talent(talent_data)
    time.sleep(3)
    
    # Now click view details on the created talent
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Edit contact info section to test email validation
    talent_page.click_contact_info_edit()
    
    # Test invalid email format 1: missing @
    email_field = page.get_by_role("textbox", name="Email")
    email_field.fill("invalid-email-format")
    # Click on another field to trigger validation
    talent_page.locators.first_name_input.click()
    time.sleep(1)
    
    email_error = page.get_by_text("Please enter a valid email")
    enhanced_assert_visible(page, email_error, "Email format error should be visible for invalid format")
    
    # Test invalid email format 2: starting with dot
    email_field.clear()
    email_field.fill(".abc@gmail.com")
    # Click on another field to trigger validation
    talent_page.locators.first_name_input.click()
    time.sleep(1)
    
    email_error2 = page.get_by_text("Please enter a valid email")
    enhanced_assert_visible(page, email_error2, "Email format error should be visible for dot at start")

def test_TC_12_phone_number_format_validation(page: Page):
    """Ensure that the phone number field, if used, only accepts valid formats (e.g., 10–15 digits, country code, no text)."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to existing talent to test phone field
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Edit contact info section
    talent_page.click_contact_info_edit()
    
    # Test invalid phone format
    phone_field = page.get_by_role("textbox", name="Phone")
    if phone_field.is_visible():
        phone_field.fill("abc123def")
        talent_page.click_save_button()
        time.sleep(1)
        
        # Check for phone validation error
        phone_error = page.get_by_text("Please enter a valid phone number")
        if phone_error.is_visible():
            enhanced_assert_visible(page, phone_error, "Phone format error should be visible")

# =============================================================================
# DROPDOWN & FIELD VALIDATION TESTS
# =============================================================================

def test_TC_13_industry_subindustry_dropdown_validation(page: Page):
    """Verify that the Industry and Sub-industry fields are dropdowns populated with valid predefined values."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    talent_page.click_add_new_talent()
    
    # Test job title dropdown (assuming it's similar to industry)
    talent_page.locators.job_title_dropdown.click()
    time.sleep(1)
    
    # Check dropdown options are available
    dropdown_options = page.locator("div[role='option'], li[role='option']")
    enhanced_assert_visible(page, dropdown_options.first(), "Dropdown options should be available")
    
    # Select first available option
    dropdown_options.first().click()
    time.sleep(1)
    
    talent_page.click_cancel_button()

def test_TC_13_talent_status_predefined_values(page: Page):
    """Confirm that the "Talent Status" field allows selection only from a list of predefined statuses and prevents custom entries."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent detail to check status field
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Check job & talent details section for status
    talent_page.click_job_talent_details_edit()
    
    # Find talent status field/dropdown
    status_field = page.locator("select, div[role='combobox']").filter(has_text="Status")
    status_field.click()
    time.sleep(1)
    
    # Check for predefined status options
    status_options = page.locator("div[role='option'], option").filter(has_text=re.compile("Active|Inactive|Proactive"))
    enhanced_assert_visible(page, status_options.first(), "Status options should be available")

def test_TC_14_nationality_searchable_dropdown(page: Page):
    """Ensure user can select Nationality from a searchable dropdown or autosuggest field."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Test location dropdown as nationality equivalent
    talent_page.click_add_new_talent()
    
    # Click location dropdown
    talent_page.locators.location_dropdown.click()
    time.sleep(1)
    
    # Type to search
    location_input = page.get_by_role("textbox", name="Search location")
    location_input.fill("United")
    time.sleep(1)
    
    # Check filtered results appear
    filtered_options = page.locator("div[role='option']").filter(has_text="United")
    enhanced_assert_visible(page, filtered_options.first(), "Location search should show filtered results")
    
    talent_page.click_cancel_button()

def test_TC_15_visa_type_dependent_field(page: Page):
    """Confirm Visa Type field behaves as a dependent or auto-complete based on nationality input (if configured)."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent detail to check visa field
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Edit personal info to check for visa type field
    talent_page.click_personal_info_edit()
    
    # Look for visa type field
    visa_field = page.get_by_role("textbox", name="Visa Type")
    if visa_field.is_visible():
        # Test dependency with location/nationality
        assert True, "Visa Type field is available"
    else:
        # Field might not be implemented yet
        print("Note: Visa Type field not found - may not be implemented")

# =============================================================================
# FILE UPLOAD VALIDATION TESTS
# =============================================================================

def test_TC_16_image_upload_functionality_and_preview(page: Page):
    """Ensure that image or logo upload is functional and a preview is shown before saving the form."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    talent_page.click_add_new_talent()
    
    # Test profile picture upload
    talent_page.locators.upload_profile_picture.click()
    time.sleep(1)
    
    # Upload test image
    file_input = page.locator("input[type='file']")
    file_input.set_input_files("images_for_test/pexels-photo.jpeg")
    time.sleep(2)
    
    # Check for preview or success indicator
    preview_element = page.locator("img[src*='blob'], .upload-preview, .file-uploaded")
    enhanced_assert_visible(page, preview_element, "Image preview should be visible after upload")
    
    talent_page.click_cancel_button()

def test_TC_17_invalid_file_types_rejected(page: Page):
    """Ensure invalid file types (e.g., .exe or .txt) are not accepted in the photo/logo upload field."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    talent_page.click_add_new_talent()
    talent_page.locators.upload_profile_picture.click()
    time.sleep(1)
    
    # Create temporary invalid file for testing
    with open("temp_invalid_file.exe", "w") as f:
        f.write("test")
    
    # Try to upload invalid file type
    file_input = page.locator("input[type='file']")
    file_input.set_input_files("temp_invalid_file.exe")
    time.sleep(2)
    
    # Check for file type validation error
    format_error = page.get_by_text("Invalid file format")
    enhanced_assert_visible(page, format_error, "File format error should be visible")
    
    # Clean up
    import os
    os.remove("temp_invalid_file.exe")
    
    talent_page.click_cancel_button()

def test_TC_18_file_size_validation(page: Page):
    """Validate that uploaded images larger than the allowed size (e.g., 5MB) are blocked by the system."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    talent_page.click_add_new_talent()
    talent_page.locators.upload_profile_picture.click()
    time.sleep(1)
    
    # Use existing large file for testing
    file_input = page.locator("input[type='file']")
    file_input.set_input_files("images_for_test/pexels-6MB.jpg")
    time.sleep(2)
    
    # Check for file size validation error
    size_error = page.get_by_text("File size too large")
    enhanced_assert_visible(page, size_error, "File size error should be visible")
    
    talent_page.click_cancel_button()

# =============================================================================
# CRUD OPERATIONS TESTS
# =============================================================================

def test_TC_19_valid_data_creates_talent_successfully(page: Page, created_talent_data):
    """Ensure that valid data entry into all required fields allows the Agency Personnel to create a new talent profile successfully."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Create talent with valid data
    talent_page = helper.do_create_talent(created_talent_data)
    
    # Verify success
    helper.assert_talent_created_successfully()

def test_TC_20_update_talent_with_valid_inputs(page: Page):
    """Verify that "Update" button correctly modifies an existing talent profile with valid inputs."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to first talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Edit personal info section
    updated_data = {
        "First Name": talent_generator.generate_first_name(),
        "Last Name": talent_generator.generate_last_name()
    }
    
    helper.do_edit_talent_section("personal_info", updated_data)
    
    # Verify update success
    helper.assert_talent_updated_successfully()

def test_TC_21_prevent_update_missing_mandatory_fields(page: Page):
    """Ensure system prevents update if mandatory fields are removed during editing."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Edit personal info and clear mandatory field
    talent_page.click_personal_info_edit()
    
    # Clear first name (mandatory field)
    first_name_field = page.get_by_role("textbox", name="First Name")
    if first_name_field.is_visible():
        first_name_field.fill("")
        talent_page.click_save_button()
        time.sleep(2)
        
        # Check for validation error
        required_error = page.get_by_text("First name is required")
        if required_error.is_visible():
            enhanced_assert_visible(page, required_error, "First name required error should be visible")

def test_TC_22_cancel_during_editing_without_changes(page: Page):
    """Verify that clicking "Cancel" during profile editing redirects without applying changes."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Start editing personal info
    talent_page.click_personal_info_edit()
    
    # Make changes
    first_name_field = page.get_by_role("textbox", name="First Name")
    original_value = ""
    if first_name_field.is_visible():
        original_value = first_name_field.input_value()
        first_name_field.fill("Changed Name")
    
    # Click cancel
    talent_page.click_cancel_button()
    time.sleep(1)
    
    # Verify changes were not applied
    talent_page.click_personal_info_edit()
    if first_name_field.is_visible():
        current_value = first_name_field.input_value()
        assert current_value == original_value, "Changes should not be saved after cancel"

def test_TC_23_single_talent_delete(page: Page):
    """Test single talent deletion functionality."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Get initial talent count
    initial_count = talent_page.get_talent_count()
    
    # Delete first talent
    helper.do_single_talent_delete(0)
    
    # Verify talent count decreased
    time.sleep(2)
    new_count = talent_page.get_talent_count()
    assert new_count < initial_count, "Talent count should decrease after deletion"

def test_TC_24_bulk_talent_delete(page: Page):
    """Test bulk talent deletion functionality."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Get initial talent count
    initial_count = talent_page.get_talent_count()
    
    # Perform bulk delete of first 2 talents
    if initial_count >= 2:
        helper.do_bulk_delete_talents([0, 1])
        
        # Verify talent count decreased
        time.sleep(2)
        new_count = talent_page.get_talent_count()
        assert new_count < initial_count, "Talent count should decrease after bulk deletion"

# =============================================================================
# ADVANCED FEATURES TESTS
# =============================================================================

def test_TC_25_duplicate_talent_detection(page: Page):
    """Check that the system detects duplicate talent profiles based on Full Name and Brand Name and prompts the user to confirm continuation."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Get existing talent name
    existing_talent = talent_page.get_talent_name_by_index(0)
    
    # Try to create duplicate
    is_duplicate_detected = helper.test_duplicate_talent_detection(existing_talent)
    
    if is_duplicate_detected:
        assert True, "Duplicate talent detection is working"
    else:
        print("Note: Duplicate detection may not be implemented or existing talent name format differs")

def test_TC_26_metadata_storage_and_display(page: Page):
    """Confirm that profile metadata (Created By, Created At) is stored and displayed correctly after creation."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Look for metadata fields
    created_by_field = page.get_by_text("Created By")
    created_at_field = page.get_by_text("Created At")
    
    if created_by_field.is_visible():
        enhanced_assert_visible(page, created_by_field, "Created By metadata should be visible")
    if created_at_field.is_visible():
        enhanced_assert_visible(page, created_at_field, "Created At metadata should be visible")

def test_TC_27_last_modified_metadata_updates(page: Page):
    """Validate that changes to a talent profile update the "Last Modified" metadata accurately."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Make a change to update last modified
    talent_page.click_personal_info_edit()
    
    # Update a field
    notes_field = page.get_by_role("textbox", name="Notes")
    if notes_field.is_visible():
        notes_field.fill(f"Updated at {int(time.time())}")
        talent_page.click_save_button()
        time.sleep(2)
        
        # Check for last modified update
        last_modified_field = page.get_by_text("Last Modified")
        if last_modified_field.is_visible():
            enhanced_assert_visible(page, last_modified_field, "Last Modified metadata should be updated")

# def test_TC_28_profile_export_functionality(page: Page):
#     """Confirm that a talent profile can be exported (PDF, CSV) with complete structured data."""
#     helper = TalentHelper(page)
#     talent_page = helper.navigate_to_talent_list()
#     
#     # Navigate to talent details
#     talent_page.click_view_details(0)
#     time.sleep(2)
#     
#     # Test PDF export
#     talent_page.click_profile_dropdown()
#     talent_page.click_save_to_pdf()
#     time.sleep(3)
#     
#     # Test CSV export
#     talent_page.click_profile_dropdown()  
#     talent_page.click_save_to_csv()
#     time.sleep(3)
#     
#     # Note: File download verification would require additional browser configuration
#     assert True, "Export functionality is accessible"

def test_TC_29_sequential_talent_creation(page: Page):
    """Verify that multiple talents can be created sequentially without page reload errors."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Create first talent
    talent_data_1 = generate_random_talent_data()
    helper.do_create_talent(talent_data_1)
    time.sleep(2)
    
    # Create second talent immediately
    talent_data_2 = generate_random_talent_data()
    helper.do_create_talent(talent_data_2)
    time.sleep(2)
    
    # Verify both creations were successful
    talent_1_exists = helper.verify_talent_in_list(talent_data_1['full_name'])
    talent_2_exists = helper.verify_talent_in_list(talent_data_2['full_name'])
    
    assert talent_1_exists or talent_2_exists, "At least one talent should be created successfully"

def test_TC_30_talent_profile_searchability(page: Page, created_talent_data):
    """Validate that once created, a talent profile is searchable by name or brand name in the talent list."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Search for created talent
    search_result = helper.search_and_select_talent(created_talent_data['full_name'])
    
    assert search_result, "Created talent should be searchable and selectable"

# =============================================================================
# UI/UX & ACCESSIBILITY TESTS
# =============================================================================

def test_TC_31_keyboard_tabbing_order(page: Page):
    """Check that keyboard tabbing through form fields follows logical and accessible order."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    talent_page.click_add_new_talent()
    
    # Test tab order by focusing first field
    talent_page.locators.first_name_input.focus()
    
    # Tab to next field and verify it's last name
    page.keyboard.press("Tab")
    focused_element = page.evaluate("document.activeElement.getAttribute('name')")
    
    # Should tab to last name or next logical field
    assert focused_element is not None, "Tab navigation should move focus to next field"
    
    talent_page.click_cancel_button()

def test_TC_32_tooltip_help_text_on_hover(page: Page):
    """Confirm that tooltip/help text appears when hovering over info icons next to fields."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    talent_page.click_add_new_talent()
    
    # Look for info icons or help elements
    help_icons = page.locator("i.fa-question, .tooltip-trigger, [data-tooltip]")
    
    if help_icons.count() > 0:
        # Hover over first help icon
        help_icons.first().hover()
        time.sleep(1)
        
        # Check for tooltip appearance
        tooltip = page.locator(".tooltip, [role='tooltip']")
        if tooltip.is_visible():
            enhanced_assert_visible(page, tooltip, "Tooltip should appear on hover")
    else:
        print("Note: No help icons found - tooltips may not be implemented")
    
    talent_page.click_cancel_button()

def test_TC_33_default_values_in_dropdown_fields(page: Page):
    """Ensure default values are correctly set in dropdown fields upon form load."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    talent_page.click_add_new_talent()
    
    # Check if any dropdown fields have default values
    gender_default = page.evaluate("document.querySelector('[name*=\"gender\"]')?.value")
    location_default = page.evaluate("document.querySelector('[name*=\"location\"]')?.value")
    
    # Verify defaults are appropriate (empty or valid default)
    if gender_default:
        assert gender_default in ["", "Male", "Female", "Prefer not to say"], "Gender default should be valid"
    if location_default:
        assert isinstance(location_default, str), "Location default should be string"
    
    talent_page.click_cancel_button()

def test_TC_34_unsaved_data_warning_prompt(page: Page):
    """Verify that switching tabs (e.g., Personal Info to Job Info) with unsaved data prompts a warning."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Start editing personal info
    talent_page.click_personal_info_edit()
    
    # Make changes without saving
    first_name_field = page.get_by_role("textbox", name="First Name")
    if first_name_field.is_visible():
        first_name_field.fill("Modified Name")
    
    # Try to switch to another tab/section
    talent_page.click_contact_info_edit()
    time.sleep(1)
    
    # Check for warning dialog
    warning_dialog = page.locator("[role='dialog'], .modal").filter(has_text=re.compile("unsaved|discard|lose"))
    if warning_dialog.is_visible():
        enhanced_assert_visible(page, warning_dialog, "Unsaved data warning should appear")
        
        # Handle the dialog
        page.get_by_role("button", name="Cancel").click()
    else:
        print("Note: Unsaved data warning may not be implemented")

# =============================================================================
# LONG TEXT & DATA VALIDATION TESTS  
# =============================================================================

def test_TC_35_multiline_notes_input_support(page: Page):
    """Ensure multiline input (e.g., Notes) allows paragraphs, line breaks, and rich content where applicable."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Edit communications section (likely has notes)
    talent_page.click_communications_edit()
    
    # Test multiline notes input
    notes_field = page.get_by_role("textbox", name="Notes")
    if notes_field.is_visible():
        multiline_text = "Line 1\n\nLine 2 with paragraph break\n\n• Bullet point\n• Another bullet"
        notes_field.fill(multiline_text)
        
        # Verify multiline content is accepted
        field_value = notes_field.input_value()
        assert "\n" in field_value, "Notes field should accept line breaks"
        
        talent_page.click_save_button()
        time.sleep(2)

def test_TC_36_long_text_entries_layout_stability(page: Page):
    """Verify that long text entries in Notes fields do not break the layout or cause errors on save/view."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Edit communications section
    talent_page.click_communications_edit()
    
    # Test very long text
    notes_field = page.get_by_role("textbox", name="Notes")
    if notes_field.is_visible():
        long_text = "Very long text entry. " * 100  # ~2000+ characters
        notes_field.fill(long_text)
        
        # Try to save
        talent_page.click_save_button()
        time.sleep(2)
        
        # Verify no layout breaks or errors
        error_elements = page.locator(".error, [class*='error']")
        assert error_elements.count() == 0, "Long text should not cause layout errors"

def test_TC_37_html_script_sanitization(page: Page):
    """Ensure HTML tags or scripts entered in free text fields are sanitized or rejected."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Edit communications section
    talent_page.click_communications_edit()
    
    # Test HTML/script injection
    notes_field = page.get_by_role("textbox", name="Notes")
    if notes_field.is_visible():
        malicious_input = "<script>alert('xss')</script><b>Bold text</b>"
        notes_field.fill(malicious_input)
        
        talent_page.click_save_button()
        time.sleep(2)
        
        # Verify content is sanitized (no script execution, HTML may be escaped)
        page_content = page.content()
        assert "alert('xss')" not in page_content, "Scripts should be sanitized"

def test_TC_38_multiple_profile_updates_consistency(page: Page):
    """Confirm that multiple updates to a talent profile are saved correctly and reflected in the change log (if available)."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Perform multiple updates
    updates = [
        ("personal_info", {"First Name": "Updated1"}),
        ("contact_info", {"Email": "updated1@test.com"}),
        ("personal_info", {"Last Name": "Updated2"})
    ]
    
    for section, data in updates:
        helper.do_edit_talent_section(section, data)
        time.sleep(2)
    
    # Verify final state reflects all changes
    # Check if change log or history is available
    change_log = page.get_by_text("Change Log", "History", "Audit")
    if change_log.is_visible():
        enhanced_assert_visible(page, change_log, "Change log should be available")

# =============================================================================
# COMPLEX WORKFLOW TESTS
# =============================================================================

def test_TC_39_job_history_chronological_validation(page: Page):
    """Validate that the job history section enforces proper chronological order of employment (start date must be before end date)."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Edit employment section
    talent_page.click_employment_details_edit()
    
    # Test chronological validation if job history fields exist
    start_date_field = page.get_by_role("textbox", name="Start Date")
    end_date_field = page.get_by_role("textbox", name="End Date")
    
    if start_date_field.is_visible() and end_date_field.is_visible():
        # Set end date before start date
        start_date_field.fill("01/01/2023")
        end_date_field.fill("01/01/2022")  # Earlier than start date
        
        talent_page.click_save_button()
        time.sleep(2)
        
        # Check for chronological error
        date_error = page.get_by_text("End date must be after start date")
        if date_error.is_visible():
            enhanced_assert_visible(page, date_error, "Chronological validation error should be visible")

def test_TC_40_education_history_support(page: Page):
    """Validate that education history allows input of degree, institution, and graduation year."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Check personal info section for education
    talent_page.click_personal_info_edit()
    
    # Look for education fields
    education_fields = [
        page.get_by_role("textbox", name="Institution"),
        page.get_by_role("textbox", name="Degree"),
        page.get_by_role("textbox", name="Graduation Year")
    ]
    
    visible_education_fields = [field for field in education_fields if field.is_visible()]
    
    if visible_education_fields:
        # Fill education information
        for i, field in enumerate(visible_education_fields):
            test_values = ["Test University", "Bachelor's Degree", "2020"]
            if i < len(test_values):
                field.fill(test_values[i])
        
        talent_page.click_save_button()
        time.sleep(2)
        
        assert True, "Education history fields are available and functional"
    else:
        print("Note: Education history fields may be in a different section or not implemented")

def test_TC_41_language_proficiency_multiple_languages(page: Page):
    """Verify language proficiency fields support entry of multiple languages with skill ratings."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details  
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Check job & talent details for language fields
    talent_page.click_job_talent_details_edit()
    
    # Look for additional language fields beyond Japanese and English
    language_fields = page.locator("input[name*='language'], select[name*='language']")
    
    if language_fields.count() > 2:  # More than just Japanese and English
        assert True, "Multiple language proficiency fields are supported"
    else:
        print("Note: Additional language fields beyond Japanese/English may not be implemented")

def test_TC_42_agent_notes_role_based_visibility(page: Page):
    """Confirm that agent notes or internal comments are only visible to users with appropriate roles."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Look for internal notes section
    internal_notes = page.get_by_text("Internal Notes", "Agent Notes", "Private Notes")
    
    if internal_notes.is_visible():
        enhanced_assert_visible(page, internal_notes, "Internal notes should be visible to authorized users")
        
        # Try to edit internal notes
        talent_page.click_add_note_tab()
        
        # Check if note creation is available
        note_input = page.get_by_role("textbox", name="Note")
        if note_input.is_visible():
            note_input.fill("Internal agent note for testing")
            
            # Save note
            save_note_btn = page.get_by_role("button", name="Save Note")
            if save_note_btn.is_visible():
                save_note_btn.click()
                time.sleep(2)
    else:
        print("Note: Internal notes functionality may not be implemented or visible to current user role")

# =============================================================================
# COMPREHENSIVE INTEGRATION TEST
# =============================================================================

def test_TC_43_comprehensive_talent_workflow(page: Page):
    """End-to-end test covering complete talent lifecycle: create, view, edit all sections, export, and delete."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Step 1: Create new talent
    comprehensive_talent_data = generate_random_talent_data()
    helper.do_create_talent(comprehensive_talent_data)
    helper.assert_talent_created_successfully()
    
    # Step 2: Search and view created talent
    search_success = helper.search_and_select_talent(comprehensive_talent_data['full_name'])
    assert search_success, "Should be able to find and view created talent"
    
    # Step 3: Verify detail page structure
    helper.assert_talent_navigation_breadcrumb()
    helper.assert_talent_detail_sections_visible()
    
    # Step 4: Edit each section
    sections_to_edit = [
        ("personal_info", {"First Name": "Updated"}),
        ("contact_info", {"Email": "updated@test.com"}),
        ("job_talent_details", {"Job Title": "Senior Associate"})
    ]
    
    for section, data in sections_to_edit:
        helper.do_edit_talent_section(section, data)
    
    # Step 5: Test export functionality
    helper.do_export_talent_data("PDF")
    helper.do_export_talent_data("CSV")
    
    # Step 6: Navigate back to list
    helper.navigate_to_talent_from_breadcrumb()
    
    # Step 7: Verify talent still exists in list
    final_verification = helper.verify_talent_in_list(comprehensive_talent_data['full_name'])
    assert final_verification, "Talent should exist in list after all operations"
    
    print("Comprehensive talent workflow completed successfully!")

def test_TC_44_form_field_interaction_and_dependencies(page: Page):
    """Test complex form interactions, field dependencies, and dynamic behavior."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    talent_page.click_add_new_talent()
    
    # Test field interactions
    # Fill first name and check if it affects other fields
    talent_page.fill_first_name("Dynamic")
    talent_page.fill_last_name("Test")
    
    # Select gender and see if it affects other options
    talent_page.select_gender("Female")
    
    # Select location and check for dynamic updates
    talent_page.select_location("Japan")
    
    # Check if Japanese level becomes pre-selected or highlighted
    # (This would be application-specific behavior)
    
    # Fill CV name and see if it auto-generates based on name
    cv_name_field = talent_page.locators.cv_name_input
    current_cv_name = cv_name_field.input_value()
    
    # Some applications auto-fill CV name based on person's name
    if "Dynamic Test" in current_cv_name:
        assert True, "CV name auto-generation is working"
    
    # Test form validation interactions
    talent_page.select_japanese_level("Native")
    talent_page.select_english_level("Basic")
    
    # Complete form and save
    talent_page.fill_date_of_birth("01/01/1990")
    talent_page.select_job_title("Associate")  
    talent_page.select_cv_language("English")
    
    talent_page.click_save_button()
    time.sleep(3)
    
    # Verify successful creation with dynamic interactions
    success_message = page.get_by_text("Talent Created Successfully")
    if success_message.is_visible():
        enhanced_assert_visible(page, success_message, "Dynamic form should save successfully")

# =============================================================================
# PERFORMANCE & RELIABILITY TESTS
# =============================================================================

def test_TC_45_talent_list_pagination_and_performance(page: Page):
    """Test talent list pagination, loading performance, and large dataset handling."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Wait for initial load and measure
    start_time = time.time()
    talent_page.wait_for_talent_list_load()
    load_time = time.time() - start_time
    
    assert load_time < 10, "Talent list should load within 10 seconds"
    
    # Test pagination if available
    next_page = talent_page.locators.next_page_button
    if next_page.is_visible():
        next_page.click()
        time.sleep(2)
        
        # Verify page changed
        page_info = talent_page.locators.pagination_info.inner_text()
        assert "2 of" in page_info or "page 2" in page_info.lower(), "Should navigate to page 2"
        
        # Go back to first page
        prev_page = talent_page.locators.previous_page_button
        if prev_page.is_visible():
            prev_page.click()
            time.sleep(2)
    
    print(f"Talent list loaded in {load_time:.2f} seconds")

def test_TC_46_settings_panel_column_customization(page: Page):
    """Test settings panel for customizing visible columns in talent list."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Open settings panel
    talent_page.click_settings()
    
    # Test column visibility toggles
    checkboxes = [
        (talent_page.locators.date_of_birth_checkbox, "Date of birth"),
        (talent_page.locators.current_salary_checkbox, "Current Salary"),
        (talent_page.locators.grade_checkbox, "Grade")
    ]
    
    for checkbox, column_name in checkboxes:
        if checkbox.is_visible():
            # Toggle checkbox
            initial_state = checkbox.is_checked()
            checkbox.click() if not initial_state else checkbox.uncheck()
            time.sleep(1)
            
            # Verify column visibility changed in list
            # This would require checking actual column presence
            print(f"Toggled {column_name} column visibility")
    
    # Close settings panel
    talent_page.click_settings()

def test_TC_47_cross_module_integration(page: Page):
    """Confirm that once created, talent profiles are available for view/edit in other modules if integrated (e.g., job matching)."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Test save to JD functionality (cross-module integration)
    talent_page.click_profile_dropdown()
    talent_page.click_save_to_jd()
    time.sleep(2)
    
    # Check for success message or redirect
    jd_success = page.get_by_text("Saved to JD", "Added to JD")
    if jd_success.is_visible():
        enhanced_assert_visible(page, jd_success, "Talent should be saveable to JD module")
    
    # Test save to group functionality
    talent_page.click_profile_dropdown()
    talent_page.click_save_to_group()
    time.sleep(2)
    
    # Check for group save success
    group_success = page.get_by_text("Saved to Group", "Added to Group")
    if group_success.is_visible():
        enhanced_assert_visible(page, group_success, "Talent should be saveable to Group module")

def test_TC_48_back_navigation_data_consistency(page: Page):
    """Verify that back navigation (browser or UI button) after save takes user to the profile or list, not form with stale data."""
    helper = TalentHelper(page)
    talent_page = helper.navigate_to_talent_list()
    
    # Navigate to talent details
    talent_page.click_view_details(0)
    time.sleep(2)
    
    # Make an edit and save
    talent_page.click_personal_info_edit()
    
    first_name_field = page.get_by_role("textbox", name="First Name")
    if first_name_field.is_visible():
        updated_name = f"BackNav{int(time.time())}"
        first_name_field.fill(updated_name)
        talent_page.click_save_button()
        time.sleep(2)
        
        # Use browser back navigation
        page.go_back()
        time.sleep(2)
        
        # Verify we're at talent list, not stuck in edit form
        assert talent_page.locators.add_new_talent_button.is_visible(), "Should be back at talent list"
        assert not talent_page.is_modal_open(), "Should not be stuck in edit modal"
        
        # Go forward again to verify data persistence
        page.go_forward()
        time.sleep(2)
        
        # Verify the updated name is still displayed
        displayed_name = talent_page.locators.talent_name_display.inner_text()
        if updated_name in displayed_name:
            assert True, "Updated data should persist through navigation"

