"""
Talent Helper Functions
Reusable helper functions for talent-related operations
"""

import time
from playwright.sync_api import Page
from pages.talent_page import TalentPage
from utils.login_helper import do_login
from utils.enhanced_assertions import enhanced_assert_visible

class TalentHelper:
    def __init__(self, page: Page):
        self.page = page
        self.talent_page = TalentPage(page)
    
    def do_talent_login(self, email: str, password: str):
        """Login and navigate to talent section."""
        # Use existing login helper
        do_login(self.page, email, password)
        time.sleep(3)
        
        # Click on "For Talent Only" agency card
        agency_card = self.page.get_by_role("heading", name="For Talent Only")
        agency_card.click()
        time.sleep(2)
        
        # Click on main Talent link first to expand dropdown
        self.talent_page.click_talent_main_link()
        time.sleep(1)
        
        # Then click on Talent list
        self.talent_page.click_talent_list_link()
        time.sleep(2)
        return self.talent_page
    
    def navigate_to_talent_list(self):
        """Navigate to talent list page."""
        # Click on main Talent link first to expand dropdown  
        self.talent_page.click_talent_main_link()
        time.sleep(1)
        
        # Then click on Talent list
        self.talent_page.click_talent_list_link()
        self.talent_page.wait_for_talent_list_load()
        return self.talent_page
    
    def do_create_talent(self, talent_data: dict):
        """Create a new talent with provided data."""
        # Open create talent modal
        self.talent_page.click_add_new_talent()
        
        # Fill required fields
        self.talent_page.fill_first_name(talent_data['first_name'])
        self.talent_page.fill_last_name(talent_data['last_name'])
        self.talent_page.select_gender(talent_data['gender'])
        self.talent_page.select_job_title(talent_data['job_title'])
        self.talent_page.fill_date_of_birth(talent_data['date_of_birth'])
        self.talent_page.select_japanese_level(talent_data['japanese_level'])
        self.talent_page.select_english_level(talent_data['english_level'])
        self.talent_page.select_location(talent_data['location'])
        self.talent_page.fill_cv_name(talent_data['cv_name'])
        self.talent_page.select_cv_language(talent_data['cv_language'])
        
        # Save talent
        self.talent_page.click_save_button()
        time.sleep(3)
        
        return self.talent_page
    
    def do_create_talent_minimal(self, first_name: str, last_name: str):
        """Create talent with minimal required fields."""
        talent_data = {
            'first_name': first_name,
            'last_name': last_name,
            'gender': 'Male',
            'job_title': 'Associate',
            'date_of_birth': '01/01/1990',
            'japanese_level': 'Basic',
            'english_level': 'Fluent',
            'location': 'United States',
            'cv_name': f'{first_name} CV',
            'cv_language': 'English'
        }
        return self.do_create_talent(talent_data)
    
    def do_edit_talent_section(self, section: str, field_data: dict):
        """Edit specific talent section with provided data."""
        if section == "personal_info":
            self.talent_page.click_personal_info_edit()
        elif section == "contact_info":
            self.talent_page.click_contact_info_edit()
        elif section == "employment_details":
            self.talent_page.click_employment_details_edit()
        elif section == "job_talent_details":
            self.talent_page.click_job_talent_details_edit()
        elif section == "skills_performance":
            self.talent_page.click_skills_performance_edit()
        elif section == "salary_compensation":
            self.talent_page.click_salary_compensation_edit()
        elif section == "communications":
            self.talent_page.click_communications_edit()
        
        time.sleep(2)
        
        # Fill fields based on field_data
        for field_name, field_value in field_data.items():
            field_input = self.page.get_by_role("textbox", name=field_name)
            if field_input.is_visible():
                field_input.fill(field_value)
        
        # Save changes
        self.talent_page.click_save_button()
        time.sleep(3)
    
    def search_and_select_talent(self, talent_name: str):
        """Search for talent and select first matching result."""
        self.talent_page.search_talent(talent_name)
        time.sleep(2)
        
        # Click on first talent with matching name
        talent_card = self.page.get_by_role("heading", name=talent_name).first()
        if talent_card.is_visible():
            talent_card.click()
            time.sleep(2)
            return True
        return False
    
    def do_bulk_delete_talents(self, talent_indices: list):
        """Bulk delete talents by selecting their indices."""
        # Select specified talents
        for index in talent_indices:
            self.talent_page.select_talent_checkbox(index)
        
        # Perform bulk delete
        self.talent_page.bulk_delete_talents()
        time.sleep(3)
    
    def do_single_talent_delete(self, talent_index: int = 0):
        """Delete a single talent by index."""
        self.talent_page.click_talent_delete_button(talent_index)
        # Confirm deletion if dialog appears
        confirm_button = self.page.get_by_role("button", name="Confirm")
        if confirm_button.is_visible():
            confirm_button.click()
            time.sleep(2)
    
    def verify_talent_in_list(self, talent_name: str):
        """Verify talent exists in talent list."""
        self.talent_page.search_talent(talent_name)
        time.sleep(2)
        talent_found = self.page.get_by_role("heading", name=talent_name).is_visible()
        return talent_found
    
    def upload_talent_file(self, file_type: str, file_path: str):
        """Upload file for talent profile."""
        if file_type == "profile_picture":
            self.talent_page.upload_profile_picture(file_path)
        elif file_type == "cv_file":
            self.talent_page.upload_cv_file(file_path)
        time.sleep(2)
    
    def validate_required_fields_empty_form(self):
        """Validate all required field errors appear on empty form."""
        self.talent_page.click_add_new_talent()
        
        # Upload a CV file to trigger CV name and CV language validation
        self.talent_page.upload_cv_file("images_for_test/file-PDF_1MB.pdf")
        time.sleep(2)
        
        self.talent_page.click_save_button()
        time.sleep(1)
        
        # Check all required field validations
        enhanced_assert_visible(self.page, self.talent_page.locators.first_name_required_error, 
                              "First name required error should be visible")
        enhanced_assert_visible(self.page, self.talent_page.locators.last_name_required_error, 
                              "Last name required error should be visible")
        enhanced_assert_visible(self.page, self.talent_page.locators.gender_required_error, 
                              "Gender required error should be visible")
        enhanced_assert_visible(self.page, self.talent_page.locators.job_title_required_error, 
                              "Job title required error should be visible")
        enhanced_assert_visible(self.page, self.talent_page.locators.japanese_level_required_error, 
                              "Japanese level required error should be visible")
        enhanced_assert_visible(self.page, self.talent_page.locators.english_level_required_error, 
                              "English level required error should be visible")
        enhanced_assert_visible(self.page, self.talent_page.locators.location_required_error, 
                              "Location required error should be visible")
        enhanced_assert_visible(self.page, self.talent_page.locators.cv_name_required_error, 
                              "CV name required error should be visible")
        enhanced_assert_visible(self.page, self.talent_page.locators.cv_language_required_error, 
                              "CV language required error should be visible")
    
    def validate_file_upload_error(self, error_type: str):
        """Validate file upload error messages."""
        if error_type == "format":
            enhanced_assert_visible(self.page, self.talent_page.locators.file_format_error, 
                                  "File format error should be visible")
        elif error_type == "size":
            enhanced_assert_visible(self.page, self.talent_page.locators.file_size_error, 
                                  "File size error should be visible")
    
    def assert_talent_navigation_breadcrumb(self):
        """Assert talent detail page breadcrumb navigation."""
        enhanced_assert_visible(self.page, self.talent_page.locators.breadcrumb_home, 
                              "Home breadcrumb should be visible")
        enhanced_assert_visible(self.page, self.talent_page.locators.breadcrumb_talent, 
                              "Talent breadcrumb should be visible")
        enhanced_assert_visible(self.page, self.talent_page.locators.breadcrumb_talent_details, 
                              "Talent Details should be visible")
    
    def assert_talent_detail_sections_visible(self):
        """Assert all talent detail sections are visible."""
        sections = [
            (self.talent_page.locators.personal_info_section, "Personal Info section"),
            (self.talent_page.locators.contact_info_section, "Contact Info section"),
            (self.talent_page.locators.employment_section, "Employment section"),
            (self.talent_page.locators.job_details_section, "Job Details section"),
            (self.talent_page.locators.skills_section, "Skills section"),
            (self.talent_page.locators.salary_section, "Salary section"),
            (self.talent_page.locators.communications_section, "Communications section")
        ]
        
        for section_locator, section_name in sections:
            enhanced_assert_visible(self.page, section_locator, f"{section_name} should be visible")
    
    def assert_talent_created_successfully(self):
        """Assert talent creation success."""
        enhanced_assert_visible(self.page, self.talent_page.locators.talent_created_successfully_message, 
                              "Talent created successfully message should be visible")
    
    def assert_talent_updated_successfully(self):
        """Assert talent update success."""
        enhanced_assert_visible(self.page, self.talent_page.locators.company_info_updated_message, 
                              "Talent info updated message should be visible")
    
    def do_export_talent_data(self, export_type: str):
        """Export talent data as PDF or CSV."""
        self.talent_page.click_profile_dropdown()
        
        if export_type.lower() == "pdf":
            self.talent_page.click_save_to_pdf()
        elif export_type.lower() == "csv":
            self.talent_page.click_save_to_csv()
        
        time.sleep(3)
    
    def navigate_to_talent_from_breadcrumb(self):
        """Navigate back to talent list using breadcrumb."""
        self.talent_page.locators.breadcrumb_talent.click()
        time.sleep(2)
        self.talent_page.wait_for_talent_list_load()
    
    def test_form_cancel_functionality(self):
        """Test cancel button functionality with unsaved changes."""
        self.talent_page.click_add_new_talent()
        
        # Add some data
        self.talent_page.fill_first_name("Test")
        self.talent_page.fill_last_name("User")
        
        # Click cancel
        self.talent_page.click_cancel_button()
        time.sleep(2)
        
        # Verify modal is closed
        assert not self.talent_page.is_modal_open(), "Modal should be closed after cancel"
    
    def verify_field_character_limits(self, field_name: str, max_length: int, test_string: str):
        """Verify field character limits."""
        field_locator = getattr(self.talent_page.locators, f"{field_name}_input")
        field_locator.fill(test_string)
        
        # Check if input was truncated to max length
        actual_value = field_locator.input_value()
        assert len(actual_value) <= max_length, f"{field_name} should not exceed {max_length} characters"
        
        return len(actual_value) == max_length
    
    def test_duplicate_talent_detection(self, existing_name: str):
        """Test duplicate talent name detection."""
        self.talent_page.click_add_new_talent()
        
        # Fill form with existing talent name
        self.talent_page.fill_first_name(existing_name.split()[0])
        self.talent_page.fill_last_name(existing_name.split()[1])
        
        # Fill minimal required fields
        self.talent_page.select_gender("Male")
        self.talent_page.select_job_title("Associate")
        self.talent_page.fill_date_of_birth("01/01/1990")
        self.talent_page.select_japanese_level("Basic")
        self.talent_page.select_english_level("Fluent")
        self.talent_page.select_location("United States")
        self.talent_page.fill_cv_name("Test CV")
        self.talent_page.select_cv_language("English")
        
        # Try to save
        self.talent_page.click_save_button()
        time.sleep(2)
        
        # Check for duplicate warning/confirmation dialog
        duplicate_warning = self.page.get_by_text("already exists")
        if duplicate_warning.is_visible():
            return True
        
        return False
