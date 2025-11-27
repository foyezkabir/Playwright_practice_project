"""
Client Page Object Model for BPRP Web Application
Contains all client management functions including login, navigation, CRUD operations, search, filter, and notes
"""
from playwright.sync_api import Page, expect
from locators.loc_client import ClientLocators
from utils.config import BASE_URL
import time
from functools import wraps


# write a decorator function to switch to modal context and back
def decorator_modal_context(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        assert self.page is not None, "Page object is not initialized."
        self.click_add_client_button()
        modal_body = self.get_client_modal_body()
        backup_page = self.page # Backup current page reference
        modal_body.wait_for() # Ensure modal is loaded
        self.page = modal_body # Switch context to modal body
        result = func(self, *args, **kwargs)
        self.page = backup_page # Restore original page reference
        return result
    return wrapper


class ClientPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = ClientLocators(page)

    # ===== LOGIN & NAVIGATION FUNCTIONS =====
    
    def login_and_navigate_to_agency_dashboard(self, email: str, password: str, agency_id: str = "173"):
        """
        Login to the application and navigate to specific agency dashboard.
        
        Args:
            email: User email for login
            password: User password for login
            agency_id: Agency ID (default: "173", alternative: "174")
        """
        # Navigate to login page
        login_url = f"{BASE_URL}/login/"
        self.page.goto(login_url)
        self.page.wait_for_load_state("networkidle")
        
        # Perform login
        self.page.get_by_role("textbox", name="Email").fill(email)
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()
        
        # Navigate to agency dashboard
        home_page_url = f"{BASE_URL}/agency"
        self.page.wait_for_url(home_page_url)
        dashboard_url = f"{BASE_URL}/agency/{agency_id}/dashboard"
        self.page.goto(dashboard_url)
    
    def navigate_to_client_page(self):
        """Navigate to client page from current location."""
        self.locators.client_link.click()
        self.page.wait_for_load_state("networkidle")
    
    def navigate_to_client_page_direct(self, agency_id: str = "173"):
        """
        Navigate directly to client page URL.
        
        Args:
            agency_id: Agency ID (default: "173", alternative: "174")
        """
        client_url = f"{BASE_URL}/agency/{agency_id}/client"
        self.page.goto(client_url)
        self.page.wait_for_load_state("networkidle")
        
    
    # ===== CLIENT LIST PAGE FUNCTIONS =====
    
    def click_client_link(self):
        """Click the Client link in navigation."""
        self.locators.client_link.click()
    
    def click_add_client_button(self):
        """Click Add Client button to open creation modal."""
        self.locators.add_client_button.click()
    
    def click_view_details_button(self):
        """Click View Details button for first client."""
        self.locators.view_details_button_first.click()
    
    def click_view_details_button_by_index(self, index: int = 0):
        """Click View Details button for specific client by index."""
        self.locators.view_details_button.nth(index).click()
    
    def click_open_action_menu(self):
        """Click Open action menu button for first client."""
        self.locators.open_action_menu_button_first.click()
    
    def click_open_action_menu_by_index(self, index: int = 0):
        """Click Open action menu button for specific client by index."""
        self.locators.open_action_menu_button.nth(index).click()
    
    # ===== SEARCH FUNCTIONALITY =====
    
    def fill_search_clients(self, search_text: str):
        """Fill the search clients input field."""
        self.locators.search_clients_input.fill(search_text)
    
    def clear_search_clients(self):
        """Clear the search clients input field."""
        self.locators.search_clients_input.clear()
    
    def click_search_clients_input(self):
        """Click the search clients input field."""
        self.locators.search_clients_input.click()
    
    # ===== CLIENT CREATION MODAL FUNCTIONS =====
    
    def click_close_modal_button(self):
        """Close the client modal."""
        self.locators.close_modal_button.click()
    
    def fill_english_name(self, first_name: str, last_name: str = ""):
        """Fill English first and last name fields."""
        self.locators.english_first_name_input.fill(first_name)
        if last_name:
            self.locators.english_last_name_input.fill(last_name)
    
    def fill_english_first_name(self, name: str):
        """Fill English first name field."""
        self.locators.english_first_name_input.fill(name)
    
    def fill_english_last_name(self, name: str):
        """Fill English last name field."""
        self.locators.english_last_name_input.fill(name)
    
    def clear_english_name(self):
        """Clear English name fields."""
        self.locators.english_first_name_input.clear()
        self.locators.english_last_name_input.clear()
    
    def fill_japanese_name(self, first_name: str, last_name: str = ""):
        """Fill Japanese first and last name fields."""
        self.locators.japanese_first_name_input.fill(first_name)
        if last_name:
            self.locators.japanese_last_name_input.fill(last_name)
    
    def fill_japanese_first_name(self, name: str):
        """Fill Japanese first name field."""
        self.locators.japanese_first_name_input.fill(name)
    
    def fill_japanese_last_name(self, name: str):
        """Fill Japanese last name field."""
        self.locators.japanese_last_name_input.fill(name)
    
    def clear_japanese_name(self):
        """Clear Japanese name fields."""
        self.locators.japanese_first_name_input.clear()
        self.locators.japanese_last_name_input.clear()
    
    def fill_job_title(self, title: str):
        """Fill job title field."""
        self.locators.job_title_input.fill(title)
    
    def clear_job_title(self):
        """Clear job title field."""
        self.locators.job_title_input.clear()
    
    def click_job_title_input(self):
        """Click job title input field."""
        self.locators.job_title_input.click()
    
    # ===== DROPDOWN FUNCTIONS =====
    
    def click_gender_dropdown(self):
        """Click Gender dropdown."""
        self.locators.gender_dropdown.click()
    
    def click_department_dropdown(self):
        """Click Department dropdown."""
        self.locators.department_dropdown.click()
    
    def click_company_dropdown(self):
        """Click Company dropdown."""
        self.locators.company_select_trigger.click()
    
    def click_english_level_dropdown(self):
        """Click English Level dropdown."""
        self.locators.english_level_dropdown.click()
    
    def click_japanese_level_dropdown(self):
        """Click Japanese Level dropdown."""
        self.locators.japanese_level_dropdown.click()
    
    def select_dropdown_option(self, option_text: str):
        """
        Select an option from any opened dropdown by text.
        
        Args:
            option_text: The exact text of the option to select
        """
        self.page.get_by_text(option_text, exact=True).click()
    
    # ===== CONTACT FIELDS - PHONE =====
    def fill_phone_label(self, label: str):
        """Select phone label from dropdown."""
        self.locators.phone_label_dropdown.click()
        self.select_dropdown_option(label)
    
    def fill_phone_number(self, number: str):
        """Fill phone number field."""
        self.locators.phone_number_input.fill(number)
    
    def click_add_phone_number_button(self):
        """Click Add Phone Number button."""
        self.locators.add_phone_number_button.click()
    
    # ===== CONTACT FIELDS - EMAIL =====
    
    def fill_email_label(self, label: str):
        """Select email label from dropdown."""
        self.locators.email_label_dropdown.click()
        self.select_dropdown_option(label)
    
    def fill_email(self, email: str):
        """Fill email address field."""
        self.locators.email_input.fill(email)
    
    def click_email_input(self):
        """Click email input field."""
        self.locators.email_input.click()
    
    def click_add_email_address_button(self):
        """Click Add Email Address button."""
        self.locators.add_email_address_button.click()
    
    # ===== MODAL ACTION BUTTONS =====
    
    def click_cancel_button(self):
        """Click Cancel button in modal."""
        self.locators.cancel_button.click()
    
    def click_create_button(self):
        """Click Create button to submit client creation."""
        self.locators.create_button.click()
        time.sleep(2)
    
    # ===== DELETE FUNCTIONALITY =====
        # ===== BULK ACTIONS =====
        def click_bulk_select_checkbox(self):
            """Click Bulk select checkbox to enable bulk actions."""
            self.locators.bulk_select_checkbox.click()

        def click_bulk_delete_button(self, count):
            """Click Bulk Delete button with count."""
            self.locators.bulk_delete_button(count).click()

        def click_bulk_add_notes_button(self, count):
            """Click Bulk Add Notes button with count."""
            self.locators.bulk_add_notes_button(count).click()

        def click_bulk_delete_modal_cancel(self):
            """Click Cancel in Bulk Delete modal."""
            self.locators.bulk_delete_modal_cancel.click()

        def click_bulk_delete_modal_confirm(self):
            """Click Confirm in Bulk Delete modal."""
            self.locators.bulk_delete_modal_confirm.click()

        def click_bulk_add_notes_modal_cancel(self):
            """Click Cancel in Bulk Add Notes modal."""
            self.locators.bulk_add_notes_modal_cancel.click()

        def click_bulk_add_notes_modal_save_next(self):
            """Click Save & Next in Bulk Add Notes modal."""
            self.locators.bulk_add_notes_modal_save_next.click()

        def click_note_nav(self, idx, count):
            """Click note navigation image for idx of count."""
            self.locators.note_nav(idx, count).click()

    def click_bulk_select_checkbox(self):
        """Click Bulk select checkbox to enable bulk actions."""
        self.locators.bulk_select_checkbox.click()
    
    def click_delete_button(self):
        """Click Delete button in action menu."""
        self.locators.delete_button_first.click()
    
    def click_confirm_delete_button(self):
        """Click Confirm button in delete confirmation modal."""
        self.locators.confirm_delete_button.click()

    def click_upload_logo_label(self, image_path: str):
        """Click Upload Logo label to upload image."""
        self.locators.upload_logo_input.set_input_files(image_path)

    # ===== NOTES FUNCTIONALITY =====
    
    def click_add_notes_button(self):
        """Click Add Notes button."""
        self.locators.add_notes_button.click()
    
    def fill_note_text(self, note_text: str):
        """Fill note text in the note textbox."""
        self.locators.note_textbox_general.fill(note_text)
    
    def click_note_textbox(self):
        """Click note textbox to focus."""
        try:
            self.locators.note_textbox.click()
        except:
            self.locators.note_textbox_general.click()
    
    def click_save_and_finish_button(self):
        """Click Save & Finish button to save note."""
        self.locators.save_and_finish_button.click()
        time.sleep(2)
    
    def click_close_button(self):
        """Click Close button."""
        self.locators.close_button.click()
    
    # ===== FILTER FUNCTIONALITY =====
    
    def click_filters_button(self):
        """Click Filters button to open filter panel."""
        self.page.get_by_text("Filters").first.click(force=True)
        time.sleep(1)  # Wait for modal animation
    
    def click_all_clear_button(self):
        """Click All clear button to reset filters."""
        self.locators.all_clear_button.wait_for(state="visible", timeout=5000)
        self.locators.all_clear_button.click()
    
    def click_client_status_add_span(self):
        """Click Client Status Add span."""
        self.locators.client_status_add_span.click()
    
    def click_gender_add_span(self):
        """Click Gender Add span."""
        self.locators.gender_add_span.click()
    
    # ===== ASSERTION/EXPECT FUNCTIONS =====
    
    def expect_client_page_heading(self):
        """Verify Client page heading is visible in breadcrumb."""
        expect(self.locators.client_page_heading).to_be_visible()
    
    def expect_client_breadcrumb(self):
        """Verify Client breadcrumb (Home > Client) is visible."""
        expect(self.locators.client_breadcrumb).to_be_visible()
    
    def expect_detail_view_breadcrumb(self, client_name: str):
        """Verify client detail view breadcrumb (Home>Client>[Client Name]) is visible."""
        expect(self.locators.breadcrumb(client_name)).to_be_visible()
    
    def expect_client_name_japanese_format(self, japanese_name: str):
        """Verify client name displays in Japanese format (LAST First) in detail view heading."""
        expect(self.locators.client_name_detail_heading(japanese_name)).to_be_visible()
    
    def convert_japanese_format_to_breadcrumb_format(self, japanese_format_name: str) -> str:
        """
        Convert client name from Japanese format (LAST First) to breadcrumb format (First Last).
        Args:
            japanese_format_name: Name in Japanese format (e.g., "TESTLAST TestFirst")
        Returns:
            Name in breadcrumb format (e.g., "TestFirst TestLast")
        """
        name_parts = japanese_format_name.split()
        last_name_caps = name_parts[0]  # e.g., "TESTLAST"
        first_name = name_parts[1] if len(name_parts) > 1 else ""  # e.g., "TestFirst"
        
        # Breadcrumb uses normal format: First Last (with proper capitalization)
        last_name_proper = last_name_caps[0] + last_name_caps[1:].lower()  # "TESTLAST" -> "TestLast"
        return f"{first_name} {last_name_proper}"
    
    def expect_main_content(self):
        """Verify main content area is visible."""
        expect(self.locators.main_content).to_be_visible()
    
    def expect_no_clients_found_message(self):
        """Verify 'No clients found' message is visible."""
        expect(self.locators.no_clients_found_message).to_be_visible()
    
    def expect_add_client_button(self):
        """Verify Add Client button is visible."""
        expect(self.locators.add_client_button).to_be_visible()
    
    def expect_add_new_client_modal_heading(self):
        """Verify Add New Client modal heading is visible."""
        expect(self.locators.add_new_client_modal_heading).to_be_visible()
    
    def click_add_new_client_modal_heading(self):
        """Click on Add New Client modal heading to trigger validation."""
        self.locators.add_new_client_modal_heading.click()
    
    def expect_english_name_input(self):
        """Verify English first and last name inputs are visible."""
        expect(self.locators.english_first_name_input).to_be_visible()
        expect(self.locators.english_last_name_input).to_be_visible()
    
    def expect_japanese_name_input(self):
        """Verify Japanese first and last name inputs are visible."""
        expect(self.locators.japanese_first_name_input).to_be_visible()
        expect(self.locators.japanese_last_name_input).to_be_visible()
    
    def expect_job_title_input(self):
        """Verify Job title input is visible."""
        expect(self.locators.job_title_input).to_be_visible()
    
    def expect_gender_dropdown(self):
        """Verify Gender dropdown is visible."""
        expect(self.locators.gender_dropdown).to_be_visible()
    
    def expect_department_dropdown(self):
        """Verify Department dropdown is visible."""
        expect(self.locators.department_dropdown).to_be_visible()
    
    def expect_company_dropdown(self):
        """Verify Company dropdown is visible."""
        expect(self.locators.company_dropdown).to_be_visible()
    
    def expect_english_level_dropdown(self):
        """Verify English Level dropdown is visible."""
        expect(self.locators.english_level_dropdown).to_be_visible()
    
    def expect_japanese_level_dropdown(self):
        """Verify Japanese Level dropdown is visible."""
        expect(self.locators.japanese_level_dropdown).to_be_visible()
    
    def expect_phone_contact_name_label(self):
        """Verify phone label dropdown is visible."""
        expect(self.locators.phone_label_dropdown).to_be_visible()
    
    def expect_phone_contact_number_label(self):
        """Verify phone number input is visible."""
        expect(self.locators.phone_number_input).to_be_visible()
    
    def expect_email_contact_name_label(self):
        """Verify email label dropdown is visible."""
        expect(self.locators.email_label_dropdown).to_be_visible()
    
    def expect_email_contact_email_label(self):
        """Verify email input is visible."""
        expect(self.locators.email_input).to_be_visible()
    
    def expect_email_input(self):
        """Verify email input is visible."""
        expect(self.locators.email_input).to_be_visible()
    
    def expect_email_name_input(self):
        """Verify email label dropdown is visible."""
        expect(self.locators.email_label_dropdown).to_be_visible()
    
    def expect_add_phone_number_button(self):
        """Verify Add Phone Number button is visible."""
        expect(self.locators.add_phone_number_button).to_be_visible()
    
    def expect_add_email_address_button(self):
        """Verify Add Email Address button is visible."""
        expect(self.locators.add_email_address_button).to_be_visible()
    
    def expect_upload_logo_label(self):
        """Verify Upload Logo label is visible."""
        expect(self.locators.upload_logo_label).to_be_visible()
    
    def expect_cancel_button(self):
        """Verify Cancel button is visible."""
        expect(self.locators.cancel_button).to_be_visible()
    
    def expect_create_button(self):
        """Verify Create button is visible."""
        expect(self.locators.create_button).to_be_visible()
    
    def expect_close_modal_button(self):
        """Verify Close modal button is visible."""
        expect(self.locators.close_modal_button).to_be_visible()
    
    # ===== VALIDATION ERROR EXPECTATIONS =====
    
    def expect_first_name_required_error(self):
        """Verify 'First name is required' error is visible."""
        expect(self.locators.first_name_required_error).to_be_visible()
    
    def expect_last_name_required_error(self):
        """Verify 'Last name is required' error is visible."""
        expect(self.locators.last_name_required_error).to_be_visible()
    
    def expect_first_name_min_length_error(self):
        """Verify 'First name must be at least 3 characters' error is visible."""
        expect(self.locators.first_name_min_length_error).to_be_visible()
    
    def expect_last_name_min_length_error(self):
        """Verify 'Last name must be at least 3 characters' error is visible."""
        expect(self.locators.last_name_min_length_error).to_be_visible()
    
    def expect_first_name_special_char_error(self):
        """Verify 'First name can't accept special characters' error is visible."""
        expect(self.locators.first_name_special_char_error).to_be_visible()
    
    def expect_last_name_special_char_error(self):
        """Verify 'Last name can't accept special characters' error is visible."""
        expect(self.locators.last_name_special_char_error).to_be_visible()
    
    def expect_client_name_required_error(self):
        """Verify 'Client name is required' error is visible (checks both first and last name)."""
        self.expect_first_name_required_error()
        self.expect_last_name_required_error()
    
    def expect_company_required_error(self):
        """Verify 'Company is required' error is visible."""
        expect(self.locators.company_required_error).to_be_visible()
    
    def expect_email_address_required_error(self):
        """Verify 'At least one email address is required' error is visible."""
        expect(self.locators.email_address_required_error).to_be_visible()
    
    def expect_invalid_email_address_error(self):
        """Verify 'Invalid email address' error is visible."""
        expect(self.locators.invalid_email_address_error).to_be_visible()

    def assert_email_address_and_name_label_errors(self):
        """Verify 'Invalid email address' error is visible."""
        self.fill_email("invalid-email")  # Trigger validation
        self.expect_invalid_email_address_error()
        self.expect_email_name_label_required_error()
        self.fill_email("heheh@gmail.com")
        self.expect_public_email_not_allowed_error()
        
    def expect_email_name_label_required_error(self):
        """Verify 'Email name/label is required' error is visible."""
        expect(self.locators.email_name_label_required_error).to_be_visible()
    
    def expect_public_email_not_allowed_error(self):
        """Verify 'Public email addresses are not allowed' error is visible."""
        expect(self.locators.public_email_not_allowed_error).to_be_visible()
    
    def expect_file_size_error(self):
        """Verify 'File can't be larger than 5 MB' error is visible."""
        expect(self.locators.file_size_error).to_be_visible()
    
    def expect_file_format_error(self):
        """Verify 'Only accept jpg, png, jpeg, gif file' error is visible."""
        expect(self.locators.file_format_error).to_be_visible()
    
    # ===== SUCCESS MESSAGE EXPECTATIONS =====
    
    def expect_client_created_successfully_message(self):
        """Verify 'Client created successfully' message is visible."""
        expect(self.locators.client_created_successfully_message).to_be_visible()
    
    def expect_client_deleted_successfully_message(self):
        """Verify 'Client deleted successfully' message is visible."""
        expect(self.locators.client_deleted_successfully_message).to_be_visible()
    
    def expect_note_saved_successfully_message(self):
        """Verify note saved successfully message is visible."""
        expect(self.locators.note_saved_successfully_message).to_be_visible()
    
    def expect_note_saved_modal_heading(self):
        """Verify Note Saved! modal heading is visible."""
        expect(self.locators.note_saved_modal_heading).to_be_visible()
    
    def expect_note_saved_modal_message(self):
        """Verify note saved modal message is visible."""
        expect(self.locators.note_saved_modal_message).to_be_visible()
    
    def expect_note_saved_close_button(self):
        """Verify note saved modal close button is visible."""
        expect(self.locators.note_saved_close_button).to_be_visible()
    
    def click_note_saved_close_button(self):
        """Click close button on note saved modal."""
        self.locators.note_saved_close_button.click()
    
    def expect_note_saved_toast(self):
        """Verify 'Note Saved! Successfully saved' toast is visible."""
        expect(self.locators.note_saved_toast).to_be_visible()
    
    # ===== DELETE CONFIRMATION EXPECTATIONS =====
    
    def expect_delete_confirmation_heading(self):
        """Verify delete confirmation heading is visible."""
        expect(self.locators.delete_confirmation_heading).to_be_visible()
    
    def expect_delete_confirmation_message(self):
        """Verify delete confirmation message is visible."""
        expect(self.locators.delete_confirmation_message).to_be_visible()
    
    def expect_confirm_delete_button(self):
        """Verify Confirm delete button is visible."""
        expect(self.locators.confirm_delete_button).to_be_visible()
    
    def expect_delete_button(self):
        """Verify Delete button is visible."""
        expect(self.locators.delete_button).to_be_visible()
    
    # ===== CLIENT DETAIL VIEW EXPECTATIONS =====
    
    def expect_breadcrumb(self, client_name: str):
        """Verify breadcrumb with client name is visible."""
        expect(self.locators.breadcrumb(client_name)).to_be_visible()
    
    def expect_client_name_in_modal(self, name: str):
        """Verify client name is visible in modal."""
        expect(self.locators.client_name_in_modal(name)).to_be_visible()
    
    # ===== NOTES EXPECTATIONS =====
    
    def expect_add_notes_button(self):
        """Verify Add Notes button is visible."""
        expect(self.locators.add_notes_button).to_be_visible()
    
    def expect_add_note_modal_heading(self):
        """Verify Add Note to Client modal heading is visible."""
        expect(self.locators.add_note_modal_heading).to_be_visible()
    
    def expect_note_required_error(self):
        """Verify note required error message is visible."""
        expect(self.locators.note_required_error).to_be_visible()
    
    def expect_save_and_finish_button(self):
        """Verify Save & Finish button is visible."""
        expect(self.locators.save_and_finish_button).to_be_visible()
    
    def expect_close_button(self):
        """Verify Close button is visible."""
        expect(self.locators.close_button).to_be_visible()
    
    # ===== FILTER EXPECTATIONS =====
    
    def expect_filters_modal_heading(self):
        """Verify Filters modal heading is visible."""
        expect(self.locators.filters_modal_heading).to_be_visible()
    
    def expect_all_clear_button(self):
        """Verify All clear button is visible."""
        expect(self.locators.all_clear_button).to_be_visible()
    
    def expect_client_status_filter_heading(self):
        """Verify Client Status filter heading is visible."""
        expect(self.locators.client_status_filter_heading).to_be_visible()
    
    def expect_gender_filter_heading(self):
        """Verify Gender filter heading is visible."""
        expect(self.locators.gender_filter_heading).to_be_visible()
    
    def expect_company_name_filter_heading(self):
        """Verify Company Name filter heading is visible."""
        expect(self.locators.company_name_filter_heading).to_be_visible()
    
    def expect_department_filter_heading(self):
        """Verify Department filter heading is visible."""
        expect(self.locators.department_filter_heading).to_be_visible()
    
    def expect_client_status_add_span(self):
        """Verify Client Status add span is visible."""
        expect(self.locators.client_status_add_span).to_be_visible()
    
    def expect_gender_add_span(self):
        """Verify Gender filter add span is visible."""
        expect(self.locators.gender_add_span).to_be_visible()
    
    def expect_company_add_span(self):
        """Verify Company Name filter add span is visible."""
        expect(self.locators.company_add_span).to_be_visible()
    
    def expect_department_add_span(self):
        """Verify Department filter add span is visible."""
        expect(self.locators.department_add_span).to_be_visible()
    
    # ===== FILTER ACTIONS =====
    
    def select_client_status_passive(self):
        """Select Passive status in filter (auto-applies immediately)."""
        self.click_client_status_add_span()
        time.sleep(0.5)
        self.locators.client_status_passive.click()
        time.sleep(0.5)  # Brief wait for auto-apply
        self.locators.client_status_filter_heading.click()  # Close dropdown
    
    def select_client_status_active(self):
        """Select Active status in filter (auto-applies immediately)."""
        self.click_client_status_add_span()
        time.sleep(0.5)
        self.locators.client_status_active.click()
        time.sleep(0.5)  # Brief wait for auto-apply
        self.locators.client_status_filter_heading.click()  # Close dropdown
    
    def select_gender_male(self):
        """Select Male gender in filter (auto-applies immediately)."""
        self.click_gender_add_span()
        time.sleep(0.5)
        self.locators.gender_male.click()
        time.sleep(0.5)  # Brief wait for auto-apply
        self.locators.gender_filter_heading.click()  # Close dropdown
    
    def select_gender_female(self):
        """Select Female gender in filter (auto-applies immediately)."""
        self.click_gender_add_span()
        time.sleep(0.5)
        self.locators.gender_female.click()
        time.sleep(0.5)  # Brief wait for auto-apply
        self.locators.gender_filter_heading.click()  # Close dropdown
    
    def fill_filter_company(self, company_name: str):
        """Fill company name in filter (auto-applies on Enter)."""
        self.locators.filter_company_input.fill(company_name)
        self.page.keyboard.press("Enter")
        time.sleep(0.5)  # Brief wait for auto-apply
        self.locators.company_name_filter_heading.click()  # Close dropdown
    
    def fill_filter_department(self, department_name: str):
        """Fill department name in filter (auto-applies on Enter)."""
        self.locators.filter_department_input.fill(department_name)
        self.page.keyboard.press("Enter")
        time.sleep(0.5)  # Brief wait for auto-apply
        self.locators.department_filter_heading.click()  # Close dropdown
    
    def click_apply_filter_button(self):
        """Click Apply button in filter modal."""
        self.locators.apply_filter_button.click()
    
    def click_all_clear_filter_button(self):
        """Click All clear button in filter modal."""
        # Verify modal is open first
        self.locators.filters_modal_heading.wait_for(state="visible", timeout=10000)
        time.sleep(0.5)
        self.locators.all_clear_button.click()
    
    def close_filter_modal(self):
        """Close filter modal by pressing Escape key."""
        self.page.keyboard.press("Escape")
        time.sleep(0.5)
    
    # ===== PAGINATION ACTIONS =====
    
    def click_next_page(self):
        """Click next page button."""
        self.locators.next_page_button.click()
    
    def click_previous_page(self):
        """Click previous page button."""
        self.locators.previous_page_button.click()
    
    def click_first_page(self):
        """Click first page button."""
        self.locators.first_page_button.click()
    
    def click_last_page(self):
        """Click last page button."""
        self.locators.last_page_button.click()
    
    def click_page_number(self, page_number: int):
        """Click specific page number button."""
        self.locators.get_page_button(page_number).click()
    
    def get_current_page_number(self) -> int:
        """Get current page number from display (e.g., '1 of 2' returns 1)."""
        text = self.locators.page_number_display.inner_text()
        # Extract first number from "1 of 2" format
        return int(text.split()[0])
    
    def expect_page_number(self, expected_page: int):
        """Verify current page number (checks for 'X of Y' format)."""
        expect(self.locators.page_number_display).to_contain_text(f"{expected_page} of")
    
    def expect_next_page_button_visible(self):
        """Verify next page button is visible."""
        expect(self.locators.next_page_button).to_be_visible()
    
    def expect_previous_page_button_visible(self):
        """Verify previous page button is visible."""
        expect(self.locators.previous_page_button).to_be_visible()
    
    def expect_next_page_button_disabled(self):
        """Verify next page button is disabled (not clickable)."""
        expect(self.locators.next_page_button).to_have_css("cursor", "not-allowed")
    
    def expect_previous_page_button_disabled(self):
        """Verify previous page button is disabled (not clickable)."""
        expect(self.locators.previous_page_button).to_have_css("cursor", "not-allowed")
    
    # ===== SEARCH EXPECTATIONS =====
    
    def expect_search_no_results_message(self, query: str):
        """Verify 'No clients found for <query>' message is visible."""
        expect(self.locators.search_no_results_message(query)).to_be_visible()
    
    def expect_view_details_button(self):
        """Verify View Details button is visible."""
        expect(self.locators.view_details_button_first).to_be_visible()
    
    def expect_open_action_menu_button(self):
        """Verify Open action menu button is visible."""
        expect(self.locators.open_action_menu_button_first).to_be_visible()
    
    # ===== FILTER RESULT EXPECTATIONS =====
    
    def expect_filter_result_contains_text(self, text: str):
        """Verify filter results contain specific text."""
        expect(self.page.get_by_text(text).first).to_be_visible(timeout=5000)
    
    def expect_passive_client_in_results(self):
        """Verify Passive client status appears in filter results."""
        expect(self.page.locator("text=Passive").first).to_be_visible(timeout=5000)
    
    def expect_active_client_in_results(self):
        """Verify Active client status appears in filter results."""
        expect(self.page.locator("text=Active").first).to_be_visible(timeout=5000)
    
    def expect_male_client_in_results(self):
        """Verify Male gender appears in filter results."""
        expect(self.page.locator("text=Male").first).to_be_visible(timeout=5000)
    
    def expect_female_client_in_results(self):
        """Verify Female gender appears in filter results."""
        expect(self.page.locator("text=Female").first).to_be_visible(timeout=5000)
    
    def expect_company_in_results(self, company_name: str):
        """Verify specific company name appears in filter results."""
        expect(self.page.get_by_text(company_name).first).to_be_visible(timeout=5000)
    
    def expect_department_in_results(self, department_name: str):
        """Verify specific department appears in filter results."""
        expect(self.page.get_by_text(department_name).first).to_be_visible(timeout=5000)
    
    # ===== HELPER FUNCTIONS =====

    def get_client_modal_body(self):
        """Get the client modal body locator."""
        return self.locators.client_modal_body
    
    
    @decorator_modal_context
    def create_client_with_mandatory_fields(self, english_first_name: str, english_last_name: str, company_name: str, email: str, email_label: str = "Work"):
        """
        Create a client with only mandatory fields.
        
        Args:
            english_first_name: Client English first name
            english_last_name: Client English last name
            company_name: Company name to select from dropdown
            email: Email address
            email_label: Email label (default: "Work")
        """
        self.fill_english_first_name(english_first_name)
        self.fill_english_last_name(english_last_name)
        self.click_company_dropdown()
        self.select_dropdown_option(company_name)
        self.fill_email_label(email_label)
        self.fill_email(email)
        self.click_create_button()
        time.sleep(2)


    @decorator_modal_context    
    def create_client_with_all_fields(
        self,
        # Mandatory fields
        english_first_name: str,
        english_last_name: str,
        company_name: str,
        email: str,
        email_label: str = "Work",
        # Optional fields
        japanese_first_name: str = None,
        japanese_last_name: str = None,
        job_title: str = None,
        gender: str = None,
        department: str = None,
        english_level: str = None,
        japanese_level: str = None,
        phone_label: str = None,
        phone_number: str = None,
        image: str = None,
        additional_email: str = None,
        additional_email_label: str = None
    ):
        """
        Create a client with all available fields (mandatory and optional).
        
        Args:
            # Mandatory fields:
            english_first_name: Client English first name (required)
            english_last_name: Client English last name (required)
            company_name: Company name to select from dropdown (required)
            email: Primary email address (required)
            email_label: Primary email label (default: "Work")
            
            # Optional fields:
            japanese_first_name: Client Japanese first name
            japanese_last_name: Client Japanese last name
            job_title: Client job title
            gender: Gender option to select from dropdown (e.g., "Male", "Female")
            department: Department to select from dropdown
            english_level: English proficiency level
            japanese_level: Japanese proficiency level
            phone_label: Phone contact label (e.g., "Mobile", "Work")
            phone_number: Phone contact number
            additional_email: Additional email address
            additional_email_label: Additional email label
        """
        # Fill mandatory fields
        self.fill_english_first_name(english_first_name)
        self.fill_english_last_name(english_last_name)
        
        # Fill optional basic information
        if japanese_first_name:
            self.fill_japanese_first_name(japanese_first_name)
        if japanese_last_name:
            self.fill_japanese_last_name(japanese_last_name)
        
        if job_title:
            self.fill_job_title(job_title)
        
        # Select gender if provided
        if gender:
            self.click_gender_dropdown()
            self.select_dropdown_option(gender)
        
        # Select department if provided
        if department:
            self.click_department_dropdown()
            self.select_dropdown_option(department)
        
        # Select company (mandatory)
        self.click_company_dropdown()
        self.select_dropdown_option(company_name)
        
        # Select language levels if provided
        if english_level:
            self.click_english_level_dropdown()
            self.select_dropdown_option(english_level)
        
        if japanese_level:
            self.click_japanese_level_dropdown()
            self.select_dropdown_option(japanese_level)
        
        # Fill phone contact if provided
        if phone_label and phone_number:
            self.fill_phone_label(phone_label)
            self.fill_phone_number(phone_number)
        
        # Fill primary email (mandatory)
        self.fill_email_label(email_label)
        self.fill_email(email)
        
        # Add additional email if provided
        if additional_email:
            self.click_add_email_address_button()
            # Fill additional email (you may need to add specific methods for second email)
            time.sleep(0.5)
            additional_email_label_dropdown = self.page.get_by_text("Label").nth(2)
            additional_email_label_dropdown.click()
            self.select_dropdown_option(additional_email_label)
            
            additional_email_input = self.page.get_by_placeholder("Email").nth(1)
            additional_email_input.fill(additional_email)

        self.scroll_to(self.locators.create_button)
        
        if image:
            # Upload logo/image if provided
            self.upload_client_image(image)
            
        # Submit the form
        self.click_create_button()
        time.sleep(2)

    def scroll_to(self, locator):
        """Scroll to a specific locator."""
        locator.scroll_into_view_if_needed()
        # time.sleep(1)

    def upload_client_image(self, image_path: str):
        """Upload a client image/logo."""
        self.locators.upload_logo_input.set_input_files(image_path)
        time.sleep(0.5)  # Wait for file to be uploaded

    def assert_client_creation_without_mandatory_fields(self):
        """
        Open client creation modal, click Create without filling mandatory fields,
        and assert all required validation error messages are displayed.
        
        This function tests the validation for:
        - Client name (English name) is required
        - Company is required
        - At least one email address is required
        - Invalid email address (for empty email)
        - Email name/label is required
        """
        # Open client creation modal
        self.click_add_client_button()
        
        # Verify modal is opened
        self.expect_add_new_client_modal_heading()
        
        # Click Create button without filling any fields
        self.click_create_button()
        time.sleep(2)
        
        # Assert all mandatory field validation errors
        print("🔍 Asserting mandatory field validation errors...")
        
        # Client name required error
        try:
            self.expect_client_name_required_error()
            print("✅ Client name required error is visible")
        except AssertionError:
            print("❌ Client name required error is NOT visible")
            raise
        
        # Company required error
        try:
            self.expect_company_required_error()
            print("✅ Company required error is visible")
        except AssertionError:
            print("❌ Company required error is NOT visible")
            raise
        
        # Email address required error
        try:
            self.expect_email_address_required_error()
            print("✅ Email address required error is visible")
        except AssertionError:
            print("❌ Email address required error is NOT visible")
            raise
        
        # Invalid email address error (when email field is empty)
        try:
            self.expect_invalid_email_address_error()
            print("✅ Invalid email address error is visible")
        except AssertionError:
            print("❌ Invalid email address error is NOT visible")
            raise
        
        # Email name/label required error
        try:
            self.expect_email_name_label_required_error()
            print("✅ Email name/label required error is visible")
        except AssertionError:
            print("❌ Email name/label required error is NOT visible")
            raise
        
        print("✅ All mandatory field validation errors are displayed correctly")
        
        # Close the modal after validation
        self.click_close_modal_button()
    
    def delete_client(self):
        """Delete a client (assumes client action menu is already open or you're on first client)."""
        self.click_open_action_menu()
        self.click_delete_button()
        self.expect_delete_confirmation_heading()
        self.expect_delete_confirmation_message()
        self.click_confirm_delete_button()
    
    def search_for_client(self, client_name: str):
        """Search for a client by name."""
        self.click_search_clients_input()
        self.fill_search_clients(client_name)
    
    def add_note_to_client(self, note_text: str):
        """
        Add a note to a client.
        
        Args:
            note_text: The note text to add
        """
        self.click_open_action_menu()
        self.click_add_notes_button()
        self.expect_add_note_modal_heading()
        self.click_note_textbox()
        self.fill_note_text(note_text)
        self.click_save_and_finish_button()
        self.expect_note_saved_successfully_message()
    
    def verify_client_created(self, wait_time: int = 2):
        """Verify client was created successfully with optional wait time."""
        time.sleep(wait_time)
        self.expect_client_created_successfully_message()
    
    def verify_client_deleted(self, wait_time: int = 2):
        """Verify client was deleted successfully with optional wait time."""
        time.sleep(wait_time)
        self.expect_client_deleted_successfully_message()
    
    def get_client_card_by_name(self, name: str):
        """Get client card locator by client name."""
        return self.locators.get_client_card_by_name(name)
    
    def get_client_search_result(self, name: str):
        """Get client search result locator by client name."""
        return self.locators.get_client_search_result(name)
