"""
Client Locators for BPRP Web Application
Contains all locators for Client management features including creation, editing, listing, search, filtering, and notes
"""
from playwright.sync_api import Page, Locator
import re

class ClientLocators:
    def __init__(self, page: Page):
        self.page = page

        # ===== NAVIGATION & MAIN PAGE ELEMENTS =====
        self.client_link = page.get_by_role("link", name="Client")
        self.client_page_heading = page.get_by_text("Home>Client")
        self.client_breadcrumb = page.locator("nav.flex.items-center").filter(has_text="Home")
        self.main_content = page.get_by_role("main")
        
        # ===== CLIENT LIST ELEMENTS =====
        self.no_clients_found_message = page.get_by_text("No clients found")
        self.add_client_button = page.get_by_role("button", name="Add Client")
        
        # Search functionality
        self.search_clients_input = page.get_by_role("textbox", name="Search clients...")
        self.search_no_results_message = lambda query: page.locator("div").filter(has_text=re.compile(rf"^No clients found for \"{query}\"$")).nth(1)
        
        # Client card elements
        self.view_details_button = page.get_by_role("button", name="View Details")
        self.view_details_button_first = page.get_by_role("button", name="View Details").first
        self.open_action_menu_button = page.get_by_role("button", name="Open action menu")
        self.open_action_menu_button_first = page.get_by_role("button", name="Open action menu").first
        
        # ===== CLIENT CREATION MODAL ELEMENTS =====
        self.client_modal_body = page.locator(".modal-body")

        self.add_new_client_modal_heading = page.get_by_role("heading", name="Add New Client")
        self.close_modal_button = page.get_by_role("button", name="Close modal")
        
        # Basic information fields
        self.english_name_input = page.get_by_role("textbox", name="English name")
        self.japanese_name_input = page.get_by_role("textbox", name="Japanese name")
        self.job_title_input = page.get_by_role("textbox", name="Job title")
        
        # Dropdown fields
        self.select_trigger_first = page.locator(".select-trigger").first
        self.gender_dropdown = page.get_by_text("Gender", exact=True)
        self.department_dropdown = page.get_by_text("Department", exact=True)
        self.department_select_trigger = page.locator("div:nth-child(5) > .searchable-select > .select-trigger")
        self.company_dropdown = page.get_by_text("Company *", exact=True)
        self.company_dropdown_with_error = page.locator("div").filter(has_text=re.compile(r"^Company \*Company is required\.$"))
        self.english_level_dropdown = page.get_by_text("English Level", exact=True)
        self.japanese_level_dropdown = page.get_by_text("Japanese Level", exact=True)
        
        # Contact fields - Phone
        # The input for phone contact name was removed; use the label locator to interact
        # (clicking the label focuses the input in the UI). Keep the label locator.
        self.phone_contact_name_label = page.get_by_text("Name").nth(2)
        self.phone_contact_number_label = page.get_by_text("Number", exact=True)
        self.add_phone_number_button = page.get_by_role("button", name="+ Add Phone Number")
        
        # Contact fields - Email
        self.email_contact_name_label = page.get_by_text("Name").nth(3)
        self.email_contact_email_label = page.get_by_text("Email", exact=True)
        self.add_email_address_button = page.get_by_role("button", name="+ Add Email Address")
        
        # File upload
        self.upload_logo_label = page.get_by_text("Upload Logo")
        self.upload_logo_input = page.locator("input[type='file']")
        
        # Modal action buttons
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.create_button = page.get_by_role("button", name="Create")
        
        # ===== VALIDATION ERROR MESSAGES =====
        # Required field errors
        self.client_name_required_error = page.get_by_text("Client name is required")
        self.company_required_error = page.get_by_text("Company is required.")
        self.email_address_required_error = page.get_by_text("At least one email address is")
        self.invalid_email_address_error = page.get_by_text("Invalid email address")
        self.email_name_label_required_error = page.get_by_text("Email name/label is required when address is provided")
        
        # Email validation errors
        self.public_email_not_allowed_error = page.get_by_text("Public email addresses are")
        
        # File upload validation errors
        self.file_size_error = page.get_by_text("File can't be larger than 5 MB")
        self.file_format_error = page.get_by_text("Only accept jpg, png, jpeg, gif")
        
        # ===== SUCCESS MESSAGES =====
        self.client_created_successfully_message = page.get_by_text("Client created successfully")
        self.client_deleted_successfully_message = page.get_by_text("Client deleted successfully")
        self.note_saved_successfully_message = page.get_by_text("Note saved successfully")
        self.note_saved_toast = page.get_by_text("Note Saved!Successfully saved")
        
        # ===== DELETE CONFIRMATION MODAL =====
        self.delete_confirmation_heading = page.get_by_role("heading", name="Are you sure you want to")
        self.delete_confirmation_message = page.get_by_text("This action cannot be undone")
        self.confirm_delete_button = page.get_by_role("button", name="Confirm")
        
        # Delete button in action menu
        self.delete_button = page.get_by_role("button", name="Delete")
        self.delete_button_first = page.get_by_role("button", name="Delete").first
        
        # ===== CLIENT DETAIL VIEW =====
        self.breadcrumb = lambda client_name: page.get_by_text(f"Home>Client>{client_name}")
        self.client_name_in_modal = lambda name: page.locator("div").filter(has_text=re.compile(rf"^{name}$")).nth(1)
        
        # ===== ADD NOTES FUNCTIONALITY =====
        self.add_notes_button = page.get_by_role("button", name="Add Notes")
        self.add_note_modal_heading = page.get_by_role("heading", name="Add Note to Client")
        self.note_textbox = page.get_by_role("textbox").get_by_role("paragraph")
        self.note_textbox_general = page.get_by_role("textbox")
        self.save_and_finish_button = page.get_by_role("button", name="Save & Finish")
        self.close_button = page.get_by_role("button", name="Close", exact=True)
        
        # ===== FILTER PANEL ELEMENTS =====
        self.filters_button = page.get_by_text("Filters")
        self.filters_modal_heading = page.get_by_role("heading", name="Filters")
        self.all_clear_button = page.get_by_role("button", name="All clear")
        
        # Filter categories
        self.client_status_filter_heading = page.get_by_role("heading", name="Client Status")
        self.gender_filter_heading = page.get_by_role("heading", name="Gender")
        self.company_name_filter_heading = page.get_by_role("heading", name="Company Name")
        self.department_filter_heading = page.get_by_role("heading", name="Department")
        
        # Filter add buttons
        self.client_status_add_span = page.locator("div").filter(has_text=re.compile(r"^Client StatusAdd$")).locator("span")
        self.gender_add_span = page.locator("div").filter(has_text=re.compile(r"^GenderAdd$")).locator("span")
        
        # ===== DYNAMIC LOCATORS =====
        def get_client_card_by_name(self, name: str):
            """Get client card by client name"""
            return self.page.locator(f"div:has-text('{name}')")
        
        def get_client_search_result(self, name: str):
            """Get client search result containing the client name"""
            return self.page.get_by_role("main").locator("div").filter(has_text=name)
