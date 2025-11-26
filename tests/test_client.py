from email.mime import image
from http import client
from pydoc import cli
import time
import pytest
from playwright.sync_api import Page, expect
from utils.config import BASE_URL
from pages.client_page import ClientPage
from random_values_generator.random_email import RandomEmail
from utils.client_helper import with_client_login, do_client_login_and_navigate

random_email = RandomEmail()

# Example using decorator
@with_client_login()
def test_TC_01(page: Page):
    """Verify user can navigate to client page after login."""
    client_page = page._client_page
    client_page.expect_client_page_heading()

# Example using decorator
@with_client_login()
def test_TC_02(page: Page):
    """Verify 'No clients found' message and 'Add Client' button are visible on client page."""
    client_page = page._client_page
    client_page.expect_no_clients_found_message()
    client_page.expect_add_client_button()

# Example using decorator
@with_client_login()
def test_TC_03(page: Page):
    """Verify all fields, labels and buttons are visible in client creation modal."""
    client_page: ClientPage = page._client_page
    client_page.click_add_client_button()
    
    # Modal heading
    client_page.expect_add_new_client_modal_heading()
    
    # Basic information fields
    client_page.expect_english_name_input()
    client_page.expect_japanese_name_input()
    client_page.expect_gender_dropdown()
    client_page.expect_job_title_input()
    client_page.expect_department_dropdown()
    client_page.expect_company_dropdown()
    client_page.expect_english_level_dropdown()
    client_page.expect_japanese_level_dropdown()
    
    # Contact fields - Phone and Email
    client_page.expect_phone_contact_name_label()
    client_page.expect_phone_contact_number_label()
    client_page.expect_email_contact_name_label()
    client_page.expect_email_contact_email_label()
    client_page.expect_add_phone_number_button()
    client_page.expect_add_email_address_button()
    
    # Upload and action buttons
    client_page.expect_upload_logo_label()
    client_page.expect_cancel_button()
    client_page.expect_create_button()
    client_page.expect_close_modal_button()
    client_page.click_close_modal_button()

def test_TC_04(page: Page):
    """Verify validation errors appear when creating client without mandatory fields."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.click_add_client_button()
    client_page.click_create_button()
    client_page.expect_client_name_required_error()
    client_page.expect_company_required_error()
    client_page.expect_email_address_required_error()

def test_TC_05(page: Page):
    """Verify 'Invalid email address' error appears when email is empty."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.click_add_client_button()
    client_page.click_create_button()
    client_page.assert_email_address_and_name_label_errors()
    client_page.click_close_modal_button()

def test_TC_06(page: Page):
    """Verify user can create a client with only mandatory fields."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "174")
    client_page.navigate_to_client_page()
    
    email = random_email.generate_email()
    client_page.create_client_with_mandatory_fields(english_first_name="Test", english_last_name="Client", company_name="Only for TC 13", email=email, email_label="Work")
    client_page.verify_client_created()

@with_client_login(agency_id="174")
def test_TC_07(page: Page):
    """Verify user can create a client with all fields (mandatory and optional) and file upload validation."""
    client_page: ClientPage = page._client_page    
    
    # Create client with all fields using new first/last name structure
    email = random_email.generate_email()
    client_page.create_client_with_all_fields(
        english_first_name="Complete",
        english_last_name="Client Test",
        company_name="Only for TC 13",
        email=email,
        email_label="Office",
        japanese_first_name="テスト",
        japanese_last_name="クライアント",
        job_title="Senior Manager",
        gender="Male",
        phone_label="Mobile",
        phone_number="+819012345678",
        english_level="Elementary",
        japanese_level="Limited Working",
        department="Sales",
        image="images_for_test\\pexels-photo.jpeg"
    )

    client_page.verify_client_created()

@with_client_login(agency_id="174")
def test_TC_08(page: Page):
    """Verify 'View Details' button is visible for existing clients."""
    client_page = page._client_page
    client_page.navigate_to_client_page()
    client_page.expect_view_details_button()

@with_client_login(agency_id="174")
def test_TC_09(page: Page):
    """Verify 'Open action menu' button is visible for existing clients."""
    client_page = page._client_page
    client_page.navigate_to_client_page()
    client_page.expect_open_action_menu_button()

def test_TC_15(page: Page):
    """Verify delete confirmation modal appears when deleting a client."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.click_open_action_menu()
    client_page.click_delete_button()
    client_page.expect_delete_confirmation_heading()
    client_page.expect_delete_confirmation_message()
    client_page.expect_confirm_delete_button()


def test_TC_16(page: Page):
    """Verify user can successfully delete a client."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.click_open_action_menu()
    client_page.click_delete_button()
    client_page.click_confirm_delete_button()
    client_page.verify_client_deleted()


def test_TC_17(page: Page):
    """Verify search functionality works for finding clients."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.search_for_client("OG IS")
    time.sleep(1)
    # Verify search results appear


def test_TC_18(page: Page):
    """Verify 'No clients found' message appears for non-existent search query."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.fill_search_clients("NonExistentClient12345")
    time.sleep(1)
    client_page.expect_search_no_results_message("NonExistentClient12345")


def test_TC_19(page: Page):
    """Verify 'Add Notes' button is visible in action menu."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.click_open_action_menu()
    client_page.expect_add_notes_button()


def test_TC_20(page: Page):
    """Verify 'Add Note to Client' modal opens when 'Add Notes' is clicked."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.click_open_action_menu()
    client_page.click_add_notes_button()
    client_page.expect_add_note_modal_heading()
    client_page.expect_save_and_finish_button()
    client_page.click_close_modal_button()


def test_TC_21(page: Page):
    """Verify user can successfully add a note to a client."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.add_note_to_client("This is a test note for the client.")
    client_page.expect_note_saved_successfully_message()


def test_TC_22(page: Page):
    """Verify 'Filters' button is visible on client page."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.click_filters_button()
    client_page.expect_filters_modal_heading()


def test_TC_23(page: Page):
    """Verify all filter categories are visible in filters modal."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.click_filters_button()
    client_page.expect_all_clear_button()
    client_page.expect_client_status_filter_heading()
    client_page.expect_gender_filter_heading()
    client_page.expect_company_name_filter_heading()
    client_page.expect_department_filter_heading()


def test_TC_24(page: Page):
    """Verify 'Client Status' filter add button is visible."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.click_filters_button()
    client_page.expect_client_status_add_span()


def test_TC_25(page: Page):
    """Verify 'Gender' filter add button is visible."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.click_filters_button()
    client_page.expect_gender_add_span()


def test_TC_26(page: Page):
    """Verify client detail view opens when 'View Details' is clicked."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.click_view_details_button()
    time.sleep(2)
    # Verify breadcrumb or detail view elements
