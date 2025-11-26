from email.mime import image
from http import client
from pydoc import cli
import time
import pytest
import allure
from playwright.sync_api import Page, expect
from utils.config import BASE_URL
from pages.client_page import ClientPage
from random_values_generator.random_email import RandomEmail
from random_values_generator.random_talent_name import RandomTalentName
from utils.client_helper import with_client_login, do_client_login_and_navigate

random_email = RandomEmail()
random_name = RandomTalentName()

# Example using decorator
@allure.title("TC_01 - Verify user can navigate to client page after login.")
@with_client_login()
def test_TC_01(page: Page):
    """Verify user can navigate to client page after login."""
    client_page: ClientPage = page._client_page
    client_page.expect_client_page_heading()

@allure.title("TC_02 - Verify 'No clients found' message and 'Add Client' button are visible on client page.")
@with_client_login()
def test_TC_02(page: Page):
    """Verify 'No clients found' message and 'Add Client' button are visible on client page."""
    client_page: ClientPage = page._client_page
    client_page.expect_no_clients_found_message()
    client_page.expect_add_client_button()

@allure.title("TC_03 - Verify all fields, labels and buttons are visible in client creation modal.")
@with_client_login()
def test_TC_03(page: Page):
    """Verify all fields, labels and buttons are visible in client creation modal."""
    client_page: ClientPage = page._client_page
    client_page.click_add_client_button()
    time.sleep(2)  # Wait for modal to load completely
    
    # Modal heading
    client_page.expect_add_new_client_modal_heading()
    
    # Text input fields - verify via locators
    expect(client_page.locators.english_first_name_input).to_be_visible()
    expect(client_page.locators.english_last_name_input).to_be_visible()
    expect(client_page.locators.japanese_first_name_input).to_be_visible()
    expect(client_page.locators.japanese_last_name_input).to_be_visible()
    expect(client_page.locators.job_title_input).to_be_visible()
    
    # Dropdown fields
    expect(client_page.locators.gender_dropdown).to_be_visible()
    expect(client_page.locators.department_dropdown).to_be_visible()
    expect(client_page.locators.company_dropdown).to_be_visible()
    expect(client_page.locators.english_level_dropdown).to_be_visible()
    expect(client_page.locators.japanese_level_dropdown).to_be_visible()
    
    # Contact fields
    expect(client_page.locators.phone_number_input).to_be_visible()
    expect(client_page.locators.email_input).to_be_visible()
    client_page.expect_add_phone_number_button()
    client_page.expect_add_email_address_button()
    
    # Upload and action buttons
    client_page.expect_upload_logo_label()
    client_page.expect_cancel_button()
    client_page.expect_create_button()
    client_page.expect_close_modal_button()
    client_page.click_close_modal_button()

@allure.title("TC_04 - Verify first name and last name validation errors (min length and special characters).")
@with_client_login(agency_id="173")
def test_TC_04(page: Page):
    """Verify first name and last name validation errors (min length and special characters)."""
    client_page: ClientPage = page._client_page
    client_page.click_add_client_button()
    time.sleep(1)
    
    # Test min length validation for first name (< 3 characters)
    client_page.fill_english_first_name("ab")
    client_page.click_add_new_client_modal_heading()
    time.sleep(0.5)
    client_page.expect_first_name_min_length_error()
    
    # Test special characters for first name
    client_page.fill_english_first_name("John@#$")
    client_page.click_add_new_client_modal_heading()
    time.sleep(0.5)
    client_page.expect_first_name_special_char_error()
    
    # Test min length validation for last name (< 3 characters)
    client_page.fill_english_first_name("John")  # Valid first name
    client_page.fill_english_last_name("ab")
    client_page.click_add_new_client_modal_heading()
    time.sleep(0.5)
    client_page.expect_last_name_min_length_error()
    
    # Test special characters for last name
    client_page.fill_english_last_name("Doe@#$")
    client_page.click_add_new_client_modal_heading()
    time.sleep(0.5)
    client_page.expect_last_name_special_char_error()
    
    client_page.click_close_modal_button()

@allure.title("TC_05 - Verify file upload validation for size and format.")
@with_client_login(agency_id="173")
def test_TC_05(page: Page):
    """Verify file upload validation for size and format."""
    client_page: ClientPage = page._client_page
    client_page.click_add_client_button()
    time.sleep(1)
    
    # Test file size validation (> 5MB)
    client_page.upload_client_image("images_for_test/pexels-6MB.jpg")
    time.sleep(2)
    client_page.expect_file_size_error()
    
    # Test file format validation (PDF not allowed)
    client_page.upload_client_image("images_for_test/file-PDF_1MB.pdf")
    time.sleep(2)
    client_page.expect_file_format_error()
    
    client_page.click_close_modal_button()

@allure.title("TC_06 - Verify validation errors appear when creating client without mandatory fields.")
@with_client_login(agency_id="173")
def test_TC_06(page: Page):
    """Verify validation errors appear when creating client without mandatory fields."""
    client_page: ClientPage = page._client_page
    client_page.click_add_client_button()
    time.sleep(1)
    client_page.click_create_button()
    time.sleep(1)
    client_page.expect_first_name_required_error()
    client_page.expect_last_name_required_error()
    client_page.expect_company_required_error()
    client_page.expect_email_address_required_error()
    time.sleep(1)
    # Fill email to trigger email name label required error
    client_page.fill_email("aaa@example.com")
    client_page.expect_email_name_label_required_error()

@allure.title("TC_07 - Verify 'Invalid email address' error appears with invalid email format.")
@with_client_login(agency_id="173")
def test_TC_07(page: Page):
    """Verify 'Invalid email address' error appears with invalid email format."""
    client_page: ClientPage = page._client_page
    client_page.click_add_client_button()
    time.sleep(1)
    
    # Fill with invalid email to trigger validation
    client_page.fill_email("invalid-email")
    client_page.click_create_button()
    time.sleep(1)
    
    # Verify invalid email error
    client_page.expect_invalid_email_address_error()
    
    client_page.click_close_modal_button()

@allure.title("TC_08 - Verify user can create a client with only mandatory fields.")
@with_client_login(agency_id="174")
def test_TC_08(page: Page):
    """Verify user can create a client with only mandatory fields."""
    client_page: ClientPage = page._client_page
    
    email = random_email.generate_email()
    first_name = random_name.generate_first_name()
    last_name = random_name.generate_last_name()
    client_page.create_client_with_mandatory_fields(english_first_name=first_name, english_last_name=last_name, company_name="Only for TC 13", email=email, email_label="Work")
    client_page.verify_client_created()

@allure.title("TC_09 - Verify user can create a client with all fields (mandatory and optional) and file upload validation.")
@with_client_login(agency_id="174")
def test_TC_09(page: Page):
    """Verify user can create a client with all fields (mandatory and optional) and file upload validation."""
    client_page: ClientPage = page._client_page    
    
    # Create client with all fields using new first/last name structure
    email = random_email.generate_email()
    english_first = random_name.generate_first_name()
    english_last = random_name.generate_last_name()
    japanese_first = "テスト"
    japanese_last = "クライアント"
    
    client_page.create_client_with_all_fields(
        english_first_name=english_first,
        english_last_name=english_last,
        company_name="Only for TC 13",
        email=email,
        email_label="Work",
        japanese_first_name=japanese_first,
        japanese_last_name=japanese_last,
        job_title="Senior Manager",
        gender="Male",
        phone_label="Home",
        phone_number="+819012345678",
        english_level="Elementary",
        japanese_level="Limited Working",
        department="Sales",
        image="images_for_test\\pexels-photo.jpeg"
    )

    client_page.verify_client_created()

@allure.title("TC_10 - Verify 'View Details' button is visible for existing clients.")
@with_client_login(agency_id="174")
def test_TC_10(page: Page):
    """Verify 'View Details' button is visible for existing clients."""
    client_page: ClientPage = page._client_page
    client_page.navigate_to_client_page()
    client_page.expect_view_details_button()

@allure.title("TC_11 - Verify 'Open action menu' button is visible for existing clients.")
@with_client_login(agency_id="174")
def test_TC_11(page: Page):
    """Verify 'Open action menu' button is visible for existing clients."""
    client_page: ClientPage = page._client_page
    client_page.navigate_to_client_page()
    client_page.expect_open_action_menu_button()

@allure.title("TC_12 - Verify delete confirmation modal appears when deleting a client.")
@with_client_login(agency_id="174")
def test_TC_12(page: Page):
    """Verify delete confirmation modal appears when deleting a client."""
    client_page: ClientPage = page._client_page
    client_page.click_open_action_menu()
    client_page.click_delete_button()
    client_page.expect_delete_confirmation_heading()
    client_page.expect_delete_confirmation_message()
    client_page.expect_confirm_delete_button()

@allure.title("TC_13 - Verify user can successfully delete a client.")
@with_client_login(agency_id="174")
def test_TC_13(page: Page):
    """Verify user can successfully delete a client."""
    client_page: ClientPage = page._client_page
    client_page.click_open_action_menu()
    client_page.click_delete_button()
    client_page.click_confirm_delete_button()
    client_page.verify_client_deleted()

@allure.title("TC_14 - Verify search functionality works for finding clients and no results message for non-existent query.")
@with_client_login(agency_id="174")
def test_TC_14(page: Page):
    """Verify search functionality works for finding clients and no results message for non-existent query."""
    client_page: ClientPage = page._client_page
    
    # Test with valid search
    client_page.search_for_client("OG IS")
    time.sleep(3)
    # Verify search results appear (client card contains the searched name)
    expect(page.get_by_text("OG IS").first).to_be_visible()
    time.sleep(1.5)
    
    # Test with non-existent search query
    client_page.fill_search_clients("NonExistentClient12345")
    time.sleep(3)
    client_page.expect_search_no_results_message("NonExistentClient12345")
    time.sleep(0.5)

@allure.title("TC_15 - Verify 'Add Notes' button is visible in action menu and modal opens correctly.")
@with_client_login(agency_id="174")
def test_TC_15(page: Page):
    """Verify 'Add Notes' button is visible in action menu and modal opens correctly."""
    client_page: ClientPage = page._client_page
    client_page.click_open_action_menu()
    client_page.expect_add_notes_button()
    
    # Click Add Notes and verify modal opens
    client_page.click_add_notes_button()
    client_page.expect_add_note_modal_heading()
    client_page.expect_save_and_finish_button()
    client_page.click_close_modal_button()

@allure.title("TC_16 - Verify user can successfully add a note, success modal appears with heading, message, and close button, then modal closes and user stays on client page.")
@with_client_login(agency_id="174")
def test_TC_16(page: Page):
    """Verify user can successfully add a note, success modal appears with heading, message, and close button, then modal closes and user stays on client page."""
    client_page: ClientPage = page._client_page
    client_page.add_note_to_client("This is a test note for the client.")
    time.sleep(2)
    
    # Verify success modal elements
    client_page.expect_note_saved_modal_heading()
    client_page.expect_note_saved_modal_message()
    client_page.expect_note_saved_close_button()
    
    # Click close button
    client_page.click_note_saved_close_button()
    time.sleep(1)
    
    # Verify modal disappears and user stays on client page
    client_page.expect_client_page_heading()

@allure.title("TC_17 - Verify that add notes field does not accept blank spaces only.")
@with_client_login(agency_id="174")
def test_TC_17(page: Page):
    """Verify that add notes field does not accept blank spaces only."""
    client_page: ClientPage = page._client_page
    
    # Fill note with only blank spaces
    client_page.add_note_to_client("                        ")
    client_page.click_save_and_finish_button()
    time.sleep(0.5)
    
    # Verify error message appears
    client_page.expect_note_required_error()

@allure.title("TC_18 - Verify filter feature is present and after clicking it filters modal opens and all filter fields are present.")
@with_client_login(agency_id="174")
def test_TC_18(page: Page):
    """Verify filter feature is present and after clicking it filters modal opens and all filter fields are present."""
    client_page: ClientPage = page._client_page
    client_page.click_filters_button()
    time.sleep(1)
    
    # Verify modal heading
    client_page.expect_filters_modal_heading()
    
    # Verify all filter category headings
    client_page.expect_client_status_filter_heading()
    client_page.expect_gender_filter_heading()
    client_page.expect_company_name_filter_heading()
    client_page.expect_department_filter_heading()
    
    # Verify filter add buttons
    client_page.expect_client_status_add_span()
    client_page.expect_gender_add_span()
    client_page.expect_company_add_span()
    client_page.expect_department_add_span()
    
    # Verify All clear button
    client_page.expect_all_clear_button()

@allure.title("TC_19 - Verify client detail view breadcrumb and name display in Japanese format (Last First).")
@with_client_login(agency_id="174")
def test_TC_19(page: Page):
    """Verify client detail view breadcrumb and name display in Japanese format (Last First)."""
    client_page: ClientPage = page._client_page
    
    # Get the first client's name from the list (displayed in Japanese format: "LAST First")
    first_client_heading = client_page.locators.first_client_name
    japanese_format_name = first_client_heading.inner_text()
    
    # Convert Japanese format to breadcrumb format
    breadcrumb_name = client_page.convert_japanese_format_to_breadcrumb_format(japanese_format_name)
    
    # Click View Details button
    client_page.click_view_details_button()
    time.sleep(2)
    
    # Verify breadcrumb shows: Home>Client>TestFirst TestLast (normal format)
    client_page.expect_detail_view_breadcrumb(breadcrumb_name)
    
    # Verify detail view heading shows: TESTLAST TestFirst (Japanese format - same as card)
    client_page.expect_client_name_japanese_format(japanese_format_name)

