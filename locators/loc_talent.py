"""
Talent Module Locators
Centralized location for all talent-related element selectors
"""

from playwright.sync_api import Page

class TalentLocators:
    def __init__(self, page: Page):
        self.page = page
        
        # Navigation Elements
        self.talent_main_link = page.get_by_role("link", name="Talent", exact=True)
        self.talent_list_link = page.get_by_role("link", name="Talent list")
        self.group_list_link = page.get_by_role("link", name="Group list")
        
        # List Page Elements
        self.search_textbox = page.get_by_role("textbox", name="Search")
        self.filters_button = page.get_by_text("Filters")
        self.upload_file_button = page.get_by_role("button", name="Upload File")
        # Button text changes: "Add Candidate" when empty, "Add New Talent" when list has items
        self.add_new_talent_button = page.locator("button:has-text('Add Candidate'), button:has-text('Add New Talent')").first
        self.settings_button = page.get_by_role("button", name="Settings")
        
        # Talent Cards
        self.talent_card_checkboxes = page.locator("input[type='checkbox']")
        self.view_details_buttons = page.get_by_role("button", name="View Details")
        self.talent_names = page.locator("h3[class*='heading']")
        self.delete_buttons = page.get_by_role("button", name="Delete")
        
        # Modal Elements
        self.modal_title = page.get_by_text("Add New Talent")
        self.close_modal_button = page.get_by_role("button", name="Close modal")
        
        # Form Fields - Required (based on exact MCP exploration structure)
        self.first_name_input = page.get_by_role("textbox", name="First Name")
        self.last_name_input = page.get_by_role("textbox", name="Last Name")
        # Dropdown arrows - click these first to open the dropdowns
        self.gender_dropdown = page.locator("form div").filter(has_text="Gender").locator("img").first
        self.job_title_dropdown = page.locator("form div").filter(has_text="Job Title").locator("img").first
        self.date_of_birth_input = page.get_by_role("textbox", name="Date of Birth")
        self.japanese_level_dropdown = page.locator("form div").filter(has_text="Japanese Level").locator("img").first
        self.english_level_dropdown = page.locator("form div").filter(has_text="English Level").locator("img").first
        self.location_dropdown = page.locator("form div").filter(has_text="Location").locator("img").first
        
        # Dropdown Options
        # Gender options
        self.gender_male_option = page.get_by_text("Male", exact=True)
        self.gender_female_option = page.get_by_text("Female", exact=True)
        self.gender_other_option = page.get_by_text("Other", exact=True)
        self.gender_prefer_not_to_say_option = page.get_by_text("Prefer not to say", exact=True)
        
        # Job Title options (commonly used ones)
        self.job_title_student_option = page.get_by_text("Student", exact=True)
        self.job_title_assistant_option = page.get_by_text("Assistant", exact=True)
        self.job_title_associate_option = page.get_by_text("Associate", exact=True)
        
        # Japanese Level options
        self.japanese_level_basic_option = page.get_by_text("Basic", exact=True)
        self.japanese_level_conversational_option = page.get_by_text("Conversational", exact=True)
        self.japanese_level_fluent_option = page.get_by_text("Fluent", exact=True)
        self.japanese_level_native_option = page.get_by_text("Native", exact=True)
        
        # English Level options
        self.english_level_basic_option = page.get_by_text("Basic", exact=True)
        self.english_level_conversational_option = page.get_by_text("Conversational", exact=True)
        self.english_level_fluent_option = page.get_by_text("Fluent", exact=True)
        self.english_level_native_option = page.get_by_text("Native", exact=True)
        
        # Location options
        self.location_japan_option = page.get_by_text("Japan", exact=True)
        
        # CV Section
        self.cv_name_input = page.get_by_role("textbox", name="CV Name")
        self.cv_language_dropdown = page.locator("div").filter(has_text="Select CV Language").locator("div").nth(1)
        self.upload_profile_picture = page.get_by_text("Upload Profile Picture")
        self.upload_cv_file = page.get_by_text("Upload CV file (optional)")
        
        # Form Action Buttons
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.save_button = page.get_by_role("button", name="Save")
        
        # Validation Error Messages
        self.first_name_required_error = page.get_by_text("First name is required")
        self.last_name_required_error = page.get_by_text("Last name is required")
        self.gender_required_error = page.get_by_text("Gender is required")
        self.job_title_required_error = page.get_by_text("Job title is required.")
        self.date_of_birth_required_error = page.get_by_text("Date of birth is required")
        self.japanese_level_required_error = page.get_by_text("Japanese level is required.")
        self.english_level_required_error = page.get_by_text("English level is required.")
        self.location_required_error = page.get_by_text("Location is required.")
        self.cv_name_required_error = page.get_by_text("CV name is required")
        self.cv_language_required_error = page.get_by_text("CV language is required")
        
        # Success Messages
        self.talent_created_successfully_message = page.get_by_text("Talent Created Successfully")
        self.company_info_updated_message = page.get_by_text("Company info updated")
        
        # Detail Page Elements
        self.breadcrumb_home = page.get_by_role("link", name="Home")
        self.breadcrumb_talent = page.get_by_role("link", name="Talent")
        self.breadcrumb_talent_details = page.get_by_text("Talent Details")
        
        # Profile Actions
        self.profile_dropdown = page.locator("button").first
        self.save_to_jd_button = page.get_by_role("button", name="Save to JD")
        self.save_to_group_button = page.get_by_role("button", name="Save to Group")
        self.hide_button = page.get_by_role("button", name="Hide")
        self.add_to_note_button = page.get_by_role("button", name="Add to Note")
        self.message_button = page.get_by_role("button", name="Message")
        self.save_to_pdf_button = page.get_by_role("button", name="Save to PDF")
        self.save_to_csv_button = page.get_by_role("button", name="Save to CSV")
        self.delete_talent_button = page.get_by_role("button", name="Delete")
        
        # Tab Navigation
        self.profile_tab = page.get_by_role("button", name="Profile")
        self.add_note_tab = page.get_by_role("button", name="Add Note")
        
        # Detail Sections with Edit Buttons
        self.personal_info_edit = page.locator("div").filter(has_text="Personal Info").get_by_role("button", name="Edit")
        self.contact_info_edit = page.locator("div").filter(has_text="Contact Info").get_by_role("button", name="Edit")
        self.employment_details_edit = page.locator("div").filter(has_text="Employment & Company Details").get_by_role("button", name="Edit")
        self.job_talent_details_edit = page.locator("div").filter(has_text="Job & Talent Details").get_by_role("button", name="Edit")
        self.skills_performance_edit = page.locator("div").filter(has_text="Skills & Performance").get_by_role("button", name="Edit")
        self.salary_compensation_edit = page.locator("div").filter(has_text="Salary & Compensation").get_by_role("button", name="Edit")
        self.communications_edit = page.locator("div").filter(has_text="Communications").get_by_role("button", name="Edit")
        
        # Dropdown Options - Based on live application exploration
        # Gender options: Male, Female, Other, Prefer not to say
        self.male_option = page.get_by_text("Male", exact=True)
        self.female_option = page.get_by_text("Female", exact=True)
        self.other_option = page.get_by_text("Other", exact=True)
        self.prefer_not_to_say_option = page.get_by_text("Prefer not to say", exact=True)
        
        # Job Title options (extensive list, common ones included)
        self.student_job_option = page.get_by_text("Student", exact=True)
        self.assistant_job_option = page.get_by_text("Assistant", exact=True)
        self.associate_job_option = page.get_by_text("Associate", exact=True)
        
        # Language Level Options: Basic, Conversational, Fluent, Native
        self.basic_level = page.get_by_text("Basic", exact=True)
        self.conversational_level = page.get_by_text("Conversational", exact=True)
        self.fluent_level = page.get_by_text("Fluent", exact=True)
        self.native_level = page.get_by_text("Native", exact=True)
        
        # Location options (Japan confirmed available)
        self.japan_location = page.get_by_text("Japan", exact=True)
        
        # CV Language options (English is default)
        self.english_cv_language = page.get_by_text("English", exact=True)
        
        # Talent Status Options
        self.active_status = page.get_by_text("Active", exact=True)
        self.inactive_status = page.get_by_text("Inactive", exact=True)
        self.proactive_status = page.get_by_text("Proactive", exact=True)
        
        # Bulk Operations
        self.select_all_checkbox = page.locator("input[type='checkbox']").first
        self.bulk_actions_dropdown = page.locator("button[data-testid='bulk-actions']")
        
        # Pagination
        self.pagination_info = page.get_by_text("1 of 2")
        self.next_page_button = page.locator("img[alt='next']")
        self.previous_page_button = page.locator("img[alt='prev']")
        
        # File Upload Inputs
        self.profile_picture_input = page.locator("input[type='file'][accept*='image']")
        self.cv_file_input = page.locator("input[type='file'][accept*='pdf']")
        self.file_input = page.locator("input[type='file']")
        
        # Settings Panel
        self.settings_panel_checkboxes = page.locator("input[name*='column']")
        self.date_of_birth_checkbox = page.get_by_text("Date of birth").locator("../input")
        self.grade_checkbox = page.get_by_text("Grade").locator("../input")
        self.current_salary_checkbox = page.get_by_text("Current Salary").locator("../input")
        self.expected_salary_checkbox = page.get_by_text("Expected Salary").locator("../input")
        
        # Form Sections in Detail Page
        self.personal_info_section = page.get_by_text("Personal Info")
        self.contact_info_section = page.get_by_text("Contact Info")
        self.employment_section = page.get_by_text("Employment & Company Details")
        self.job_details_section = page.get_by_text("Job & Talent Details")
        self.skills_section = page.get_by_text("Skills & Performance")
        self.salary_section = page.get_by_text("Salary & Compensation")
        self.communications_section = page.get_by_text("Communications")
        
        # Field Values Display
        self.talent_name_display = page.locator("h3").first
        self.talent_status_display = page.get_by_text("Active").first
        self.talent_location_display = page.locator("text=United States")
        self.phone_number_display = page.locator("text=017833670578")
        self.email_display = page.locator("text=Kabir@gmail.com")
