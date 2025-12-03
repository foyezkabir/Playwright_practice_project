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
        self.search_clients_input = page.get_by_placeholder("Search...")
        self.search_no_results_message = lambda query: page.locator("div").filter(has_text=re.compile(rf"^No clients found for \"{query}\"$")).nth(1)
        
        # Client card elements
        self.view_details_button = page.get_by_role("button", name="View Details")
        self.view_details_button_first = page.get_by_role("button", name="View Details").first
        self.open_action_menu_button = page.get_by_role("button", name="Open action menu")
        self.open_action_menu_button_first = page.get_by_role("button", name="Open action menu").first
        self.first_client_name = page.locator("h3.text-lg").first
        
        # ===== CLIENT CREATION MODAL ELEMENTS =====
        self.client_modal_body = page.locator(".modal-body")

        self.add_new_client_modal_heading = page.get_by_role("heading", name="Add New Client")
        self.close_modal_button = page.get_by_role("button", name="Close modal")
        
        # Basic information fields
        self.english_first_name_input = page.get_by_label("English First Name")
        self.english_last_name_input = page.get_by_label("English Last Name")
        self.japanese_first_name_input = page.get_by_label("Japanese First Name")
        self.japanese_last_name_input = page.get_by_label("Japanese Last Name")
        self.job_title_input = page.get_by_label("Job title")
        
        # Dropdown fields
        self.select_trigger_first = page.locator(".select-trigger").first
        self.gender_dropdown = page.get_by_text("Gender", exact=True)
        self.department_dropdown = page.get_by_text("Department", exact=True)
        self.department_select_trigger = page.locator("div:nth-child(5) > .searchable-select > .select-trigger")
        self.company_dropdown = page.get_by_text("Company", exact=True).first
        self.company_select_trigger = page.locator("label").filter(has_text="Company").locator("..").locator(".select-trigger")
        self.company_dropdown_with_error = page.locator("div").filter(has_text=re.compile(r"^Company \*Company is required\.$"))
        self.english_level_dropdown = page.get_by_text("English Level", exact=True)
        self.japanese_level_dropdown = page.get_by_text("Japanese Level", exact=True)
        
        # Contact fields - Phone
        self.phone_label_dropdown = page.get_by_text("Label").first
        self.phone_number_input = page.get_by_label("Number", exact=True)
        self.add_phone_number_button = page.get_by_role("button", name="+ Add Phone Number")
        
        # Contact fields - Email
        self.email_label_dropdown = page.get_by_text("Label").nth(1)
        self.email_input = page.get_by_label("Email")
        self.add_email_address_button = page.get_by_role("button", name="+ Add Email Address")
        
        # File upload
        self.upload_logo_label = page.get_by_text("Upload Logo")
        self.upload_logo_input = page.locator("input[type='file']")
        
        # Modal action buttons
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.create_button = page.get_by_role("button", name="Create")
        
        # ===== VALIDATION ERROR MESSAGES =====
        # Required field errors
        self.first_name_required_error = page.get_by_text("First name is required")
        self.last_name_required_error = page.get_by_text("Last name is required")
        self.company_required_error = page.get_by_text("Company is required.")
        self.email_address_required_error = page.get_by_text("At least one email address is required")
        self.invalid_email_address_error = page.get_by_text("Invalid email address")
        self.email_name_label_required_error = page.get_by_text("Email name/label is required when address is provided")
        
        # Min length validation errors
        self.first_name_min_length_error = page.get_by_text("First name must be at least 3 characters")
        self.last_name_min_length_error = page.get_by_text("Last name must be at least 3 characters")
        
        # Special character validation errors
        self.first_name_special_char_error = page.get_by_text("First name can't accept special characters")
        self.last_name_special_char_error = page.get_by_text("Last name can't accept special characters")
        
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
        self.note_saved_modal_heading = page.get_by_role("heading", name="Note Saved!")
        self.note_saved_modal_message = page.get_by_text("Successfully saved a note for this client.")
        self.note_saved_close_button = page.get_by_role("button", name="Close", exact=True)
        
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
        self.client_name_detail_heading = lambda name: page.locator("h3").filter(has_text=re.compile(rf"^{name}"))
        
        # ===== ADD NOTES FUNCTIONALITY =====
        self.add_notes_button = page.get_by_role("button", name="Add Notes").first
        self.add_note_modal_heading = page.get_by_role("heading", name="Add Note to Client")
        self.note_textbox = page.get_by_role("textbox").get_by_role("paragraph")
        self.note_textbox_general = page.get_by_role("textbox").nth(1)  # Second textbox is the note editor
        self.save_and_finish_button = page.get_by_role("button", name="Save & Finish")
        self.note_required_error = page.get_by_text("Please enter a note")
        self.close_button = page.get_by_role("button", name="Close", exact=True)
        
        # ===== FILTER PANEL ELEMENTS =====
        self.filters_button = page.locator("span").filter(has_text="Filters")
        self.filters_modal_heading = page.get_by_role("heading", name="Filters")
        self.filter_modal_close_button = page.locator("button.hover\\:bg-blue-100.rounded-full")
        self.all_clear_button = page.get_by_role("button", name="All clear")
        
        # Filter categories
        self.client_status_filter_heading = page.get_by_role("heading", name="Client Status")
        self.gender_filter_heading = page.get_by_role("heading", name="Gender")
        self.company_name_filter_heading = page.get_by_role("heading", name="Company Name")
        self.department_filter_heading = page.get_by_role("heading", name="Department")
        
        # Filter add buttons
        self.client_status_add_span = page.locator("div").filter(has_text=re.compile(r"^Client StatusAdd$")).locator("span")
        self.gender_add_span = page.locator("div").filter(has_text=re.compile(r"^GenderAdd$")).locator("span")
        self.company_add_span = page.locator("div").filter(has_text=re.compile(r"^Company NameAdd$")).locator("span")
        self.department_add_span = page.locator("div").filter(has_text=re.compile(r"^DepartmentAdd$")).locator("span")
        
        # Filter selections (checkboxes/options)
        self.client_status_passive = page.get_by_label("Passive")
        self.client_status_active = page.get_by_label("Active")
        self.gender_male = page.get_by_label("Male", exact=True)
        self.gender_female = page.get_by_label("Female")
        self.filter_company_input = page.get_by_placeholder("Company")
        self.filter_department_input = page.get_by_placeholder("Department")
        self.bulk_select_checkbox =  page.get_by_text("Select")
        
        # ===== BULK ACTION ELEMENTS =====
        # Bulk delete modal elements
        self.bulk_delete_modal_text = page.get_by_text("Are you sure you want to delete")
        self.bulk_delete_modal_cancel = page.get_by_role("button", name="Cancel", exact=True)
        self.bulk_delete_modal_confirm = page.get_by_role("button", name="Confirm", exact=True)
        
        # Bulk add notes modal elements
        self.bulk_add_notes_modal_cancel = page.get_by_role("button", name="Cancel", exact=True)
        self.bulk_add_notes_modal_save_next = page.get_by_role("button", name="Save & Next")
        
        # Filter pill close icon (X icon in applied filter tags)
        self.filter_pill_close_icon = page.locator("div").filter(has_text=re.compile(r"^All clear$")).get_by_role("img")
        
        # ===== PAGINATION ELEMENTS =====
        # Pagination uses SVG elements, not buttons
        # Structure: [SVG prev] [span "1 of 2"] [SVG next]
        self.page_number_display = page.locator("span").filter(has_text=re.compile(r"^\d+ of \d+$"))
        self.pagination_container = self.page_number_display.locator("..")
        # Use nth(0) for first SVG (previous), nth(1) for second SVG (next)
        self.previous_page_button = self.pagination_container.locator("svg").nth(0)
        self.next_page_button = self.pagination_container.locator("svg").nth(1)
    
    # ===== DYNAMIC LOCATORS =====
    def get_client_card_by_name(self, name: str):
        """Get client card by client name"""
        return self.page.locator(f"div:has-text('{name}')")
    
    def get_client_search_result(self, name: str):
        """Get client search result containing the client name"""
        return self.page.get_by_role("main").locator("div").filter(has_text=name)
    
    def get_page_button(self, page_number: int):
        """Get specific page number button - Note: This pagination uses SVG arrows, not page number buttons"""
        # This pagination style doesn't have clickable page numbers, only prev/next arrows
        return None
    
    def bulk_delete_button(self, count: int):
        """Get bulk delete button with specific count"""
        return self.page.get_by_role("button", name=f"Delete ({count})")
    
    def bulk_add_notes_button(self, count: int):
        """Get bulk add notes button with specific count"""
        return self.page.get_by_role("button", name=f"Add Notes ({count})")
    
    def bulk_add_notes_modal_heading(self, count: int):
        """Get bulk add notes modal heading with count"""
        return self.page.get_by_role("heading", name=f"Add Note to Clients ({count})")
    
    def note_nav(self, idx: int, count: int):
        """Get note navigation element for specific client index"""
        # The "1 of 10" text display, not clickable - navigation uses arrow buttons
        return self.page.get_by_text(f"{idx} of {count}")
