"""
Talent Page Object Model
Handles all talent-related page interactions
"""

import time
from playwright.sync_api import Page
from locators.loc_talent import TalentLocators
from utils.enhanced_assertions import enhanced_assert_visible

class TalentPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = TalentLocators(page)
    
    # Navigation Methods
    def click_talent_main_link(self):
        """Click main Talent link in sidebar."""
        self.locators.talent_main_link.click()
        time.sleep(2)
    
    def click_talent_list_link(self):
        """Click Talent list submenu link."""
        self.locators.talent_list_link.click()
        time.sleep(2)
    
    def click_group_list_link(self):
        """Click Group list submenu link."""
        self.locators.group_list_link.click()
        time.sleep(2)
    
    # List Page Actions
    def click_add_new_talent(self):
        """Click Add New Talent button."""
        self.locators.add_new_talent_button.click()
        time.sleep(2)
    
    def search_talent(self, search_term: str):
        """Search for talent using search box."""
        self.locators.search_textbox.fill(search_term)
        time.sleep(1)
    
    def click_filters(self):
        """Click Filters button."""
        self.locators.filters_button.click()
        time.sleep(1)
    
    def click_upload_file(self):
        """Click Upload File button."""
        self.locators.upload_file_button.click()
        time.sleep(1)
    
    def click_settings(self):
        """Click Settings button."""
        self.locators.settings_button.click()
        time.sleep(1)
    
    def click_view_details(self, index: int = 0):
        """Click View Details button for talent at given index."""
        self.locators.view_details_buttons.nth(index).click()
        time.sleep(2)
    
    def click_talent_delete_button(self, index: int = 0):
        """Click delete button for talent at given index."""
        self.locators.delete_buttons.nth(index).click()
        time.sleep(1)
    
    def select_talent_checkbox(self, index: int = 0):
        """Select talent checkbox at given index."""
        self.locators.talent_card_checkboxes.nth(index).check()
        time.sleep(1)
    
    # Form Interaction Methods
    def fill_first_name(self, first_name: str):
        """Fill first name field."""
        self.locators.first_name_input.fill(first_name)
    
    def fill_last_name(self, last_name: str):
        """Fill last name field."""
        self.locators.last_name_input.fill(last_name)
    
    def select_gender(self, gender: str):
        """Select gender from dropdown."""
        # Try different approaches to click the dropdown
        try:
            self.locators.gender_dropdown.click()
        except:
            # If normal click fails, try force click
            self.locators.gender_dropdown.click(force=True)
        time.sleep(2)
        
        # Wait for options to appear and click the specified gender option
        if gender.lower() == "male":
            self.locators.gender_male_option.click()
        elif gender.lower() == "female":
            self.locators.gender_female_option.click()
        elif gender.lower() == "other":
            self.locators.gender_other_option.click()
        elif gender.lower() == "prefer not to say":
            self.locators.gender_prefer_not_to_say_option.click()
        time.sleep(1)
    
    def select_job_title(self, job_title: str):
        """Select job title from dropdown."""
        self.locators.job_title_dropdown.click()
        time.sleep(1)
        # Wait for options to appear and select the specified job title
        if job_title.lower() == "student":
            self.locators.job_title_student_option.click()
        elif job_title.lower() == "assistant":
            self.locators.job_title_assistant_option.click()
        elif job_title.lower() == "associate":
            self.locators.job_title_associate_option.click()
        else:
            # Fallback for other job titles
            self.page.get_by_text(job_title, exact=True).click()
        time.sleep(1)
    
    def fill_date_of_birth(self, date: str):
        """Fill date of birth field."""
        self.locators.date_of_birth_input.fill(date)
        time.sleep(1)
    
    def select_japanese_level(self, level: str):
        """Select Japanese language level."""
        self.locators.japanese_level_dropdown.click()
        time.sleep(1)
        if level.lower() == "basic":
            self.locators.japanese_level_basic_option.click()
        elif level.lower() == "conversational":
            self.locators.japanese_level_conversational_option.click()
        elif level.lower() == "fluent":
            self.locators.japanese_level_fluent_option.click()
        elif level.lower() == "native":
            self.locators.japanese_level_native_option.click()
        time.sleep(1)
    
    def select_english_level(self, level: str):
        """Select English language level."""
        self.locators.english_level_dropdown.click()
        time.sleep(1)
        if level.lower() == "basic":
            self.locators.english_level_basic_option.click()
        elif level.lower() == "conversational":
            self.locators.english_level_conversational_option.click()
        elif level.lower() == "fluent":
            self.locators.english_level_fluent_option.click()
        elif level.lower() == "native":
            self.locators.english_level_native_option.click()
        time.sleep(1)
    
    def select_location(self, location: str):
        """Select location from dropdown."""
        self.locators.location_dropdown.click()
        time.sleep(1)
        # Wait for options to appear and select the specified location
        if location.lower() == "japan":
            self.locators.location_japan_option.click()
        else:
            # Fallback for other locations
            self.page.get_by_text(location, exact=True).click()
        time.sleep(1)
    
    def fill_cv_name(self, cv_name: str):
        """Fill CV name field."""
        self.locators.cv_name_input.fill(cv_name)
    
    def select_cv_language(self, language: str):
        """Select CV language from dropdown."""
        self.locators.cv_language_dropdown.click()
        time.sleep(1)
        self.page.get_by_text(language, exact=True).click()
        time.sleep(1)
    
    def upload_profile_picture(self, file_path: str):
        """Upload profile picture file."""
        # Click the upload profile picture area to trigger file input
        self.locators.upload_profile_picture.click()
        time.sleep(1)
        # Find and use the file input element for profile picture
        file_input = self.page.locator("input[type='file']").first
        file_input.set_input_files(file_path)
        time.sleep(2)
    
    def upload_cv_file(self, file_path: str):
        """Upload CV file."""
        # Click the upload CV file area to trigger file input  
        self.locators.upload_cv_file.click()
        time.sleep(1)
        # Find and use the file input element for CV (usually the second file input)
        file_input = self.page.locator("input[type='file']").nth(1)
        file_input.set_input_files(file_path)
        time.sleep(2)
    
    def click_save_button(self):
        """Click Save button."""
        self.locators.save_button.click()
        time.sleep(2)
    
    def click_cancel_button(self):
        """Click Cancel button."""
        self.locators.cancel_button.click()
        time.sleep(1)
    
    def click_close_modal(self):
        """Click Close modal button."""
        self.locators.close_modal_button.click()
        time.sleep(1)
    
    # Detail Page Actions
    def click_personal_info_edit(self):
        """Click Edit button for Personal Info section."""
        self.locators.personal_info_edit.click()
        time.sleep(2)
    
    def click_contact_info_edit(self):
        """Click Edit button for Contact Info section."""
        self.locators.contact_info_edit.click()
        time.sleep(2)
    
    def click_employment_details_edit(self):
        """Click Edit button for Employment & Company Details section."""
        self.locators.employment_details_edit.click()
        time.sleep(2)
    
    def click_job_talent_details_edit(self):
        """Click Edit button for Job & Talent Details section."""
        self.locators.job_talent_details_edit.click()
        time.sleep(2)
    
    def click_skills_performance_edit(self):
        """Click Edit button for Skills & Performance section."""
        self.locators.skills_performance_edit.click()
        time.sleep(2)
    
    def click_salary_compensation_edit(self):
        """Click Edit button for Salary & Compensation section."""
        self.locators.salary_compensation_edit.click()
        time.sleep(2)
    
    def click_communications_edit(self):
        """Click Edit button for Communications section."""
        self.locators.communications_edit.click()
        time.sleep(2)
    
    # Profile Actions
    def click_profile_dropdown(self):
        """Click profile actions dropdown."""
        self.locators.profile_dropdown.click()
        time.sleep(1)
    
    def click_save_to_jd(self):
        """Click Save to JD button."""
        self.locators.save_to_jd_button.click()
        time.sleep(1)
    
    def click_save_to_group(self):
        """Click Save to Group button."""
        self.locators.save_to_group_button.click()
        time.sleep(1)
    
    def click_hide_talent(self):
        """Click Hide button."""
        self.locators.hide_button.click()
        time.sleep(1)
    
    def click_add_to_note(self):
        """Click Add to Note button."""
        self.locators.add_to_note_button.click()
        time.sleep(1)
    
    def click_message(self):
        """Click Message button."""
        self.locators.message_button.click()
        time.sleep(1)
    
    def click_save_to_pdf(self):
        """Click Save to PDF button."""
        self.locators.save_to_pdf_button.click()
        time.sleep(1)
    
    def click_save_to_csv(self):
        """Click Save to CSV button."""
        self.locators.save_to_csv_button.click()
        time.sleep(1)
    
    def click_delete_talent_detail(self):
        """Click Delete button in detail page."""
        self.locators.delete_talent_button.click()
        time.sleep(1)
    
    # Tab Navigation
    def click_profile_tab(self):
        """Click Profile tab."""
        self.locators.profile_tab.click()
        time.sleep(1)
    
    def click_add_note_tab(self):
        """Click Add Note tab."""
        self.locators.add_note_tab.click()
        time.sleep(1)
    
    # Bulk Operations
    def select_all_talents(self):
        """Select all talents using select all checkbox."""
        self.locators.select_all_checkbox.check()
        time.sleep(1)
    
    def bulk_delete_talents(self):
        """Perform bulk delete operation."""
        # First select talents
        self.select_all_talents()
        # Then trigger bulk action
        self.locators.bulk_actions_dropdown.click()
        time.sleep(1)
        self.page.get_by_text("Delete Selected").click()
        time.sleep(2)
    
    # Utility Methods
    def get_talent_count(self):
        """Get total number of talents displayed."""
        return self.locators.talent_names.count()
    
    def get_talent_name_by_index(self, index: int):
        """Get talent name at specific index."""
        return self.locators.talent_names.nth(index).inner_text()
    
    def is_modal_open(self):
        """Check if Add New Talent modal is open."""
        return self.locators.modal_title.is_visible()
    
    def wait_for_talent_list_load(self):
        """Wait for talent list to load completely."""
        self.page.wait_for_selector("h3[class*='heading']", timeout=10000)
        time.sleep(2)
    
    # Assertion Helper Methods
    def expect_modal_title(self):
        """Assert modal title is visible."""
        enhanced_assert_visible(self.page, self.locators.modal_title, "Add New Talent modal should be visible")
    
    def expect_breadcrumb_navigation(self):
        """Assert breadcrumb navigation is visible."""
        enhanced_assert_visible(self.page, self.locators.breadcrumb_home, "Home breadcrumb should be visible")
        enhanced_assert_visible(self.page, self.locators.breadcrumb_talent, "Talent breadcrumb should be visible")
        enhanced_assert_visible(self.page, self.locators.breadcrumb_talent_details, "Talent Details should be visible")
    
    def expect_personal_info_section(self):
        """Assert personal info section is visible."""
        enhanced_assert_visible(self.page, self.locators.personal_info_section, "Personal Info section should be visible")
    
    def expect_talent_created_success(self):
        """Assert talent created success message."""
        enhanced_assert_visible(self.page, self.locators.talent_created_successfully_message, "Talent created successfully message should be visible")
    
    def expect_talent_updated_success(self):
        """Assert talent updated success message."""
        enhanced_assert_visible(self.page, self.locators.company_info_updated_message, "Talent info updated successfully message should be visible")
