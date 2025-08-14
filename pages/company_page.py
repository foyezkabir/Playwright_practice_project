from playwright.sync_api import Page, expect
from locators.loc_company import CompanyLocators
from utils.config import BASE_URL
from utils.enhanced_assertions import enhanced_assert_visible, enhanced_assert_not_visible
import time

class CompanyPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = CompanyLocators(page)

    # ===== NAVIGATION METHODS =====
    def navigate_to_login_page(self, url: str):
        """Navigate to login page and wait for elements to load."""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        self.locators.email_input.wait_for()
        self.locators.password_input.wait_for()

    def click_company_tab(self):
        """Click on the Company tab. Try multiple locator strategies."""
        try:
            if self.locators.company_tab.count() > 0:
                self.locators.company_tab.click()
            else:
                self.locators.company_tab_alt.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error clicking company tab: {e}")
            # Final fallback
            company_element = self.page.locator("text=Company").first
            company_element.click()
            time.sleep(2)

    def click_agency_card(self, agency_name: str = "Test this agency"):
        """Click on an agency card to navigate to agency details."""
        try:
            if agency_name == "Test this agency":
                self.locators.test_agency_card.click()
            else:
                agency_card = self.locators.agency_card(agency_name)
                agency_card.click()
            time.sleep(3)
        except Exception as e:
            print(f"Error clicking agency card '{agency_name}': {e}")
            first_agency = self.page.locator("[data-testid='agency-card'], .agency-card").first
            first_agency.click()
            time.sleep(3)

    # ===== LOGIN METHODS =====
    def click_email_input(self):
        """Click email input field."""
        self.locators.email_input.click()

    def expect_email_input(self):
        """Expect email input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.email_input, "Email input should be visible")

    def fill_email_input(self, email: str):
        """Fill email input field."""
        self.locators.email_input.fill(email)

    def click_password_input(self):
        """Click password input field."""
        self.locators.password_input.click()

    def expect_password_input(self):
        """Expect password input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.password_input, "Password input should be visible")

    def fill_password_input(self, password: str):
        """Fill password input field."""
        self.locators.password_input.fill(password)

    def click_sign_in_button(self):
        """Click sign in button."""
        self.locators.sign_in_button.click()

    # ===== COMPANY NAME METHODS =====
    def click_company_name_input(self):
        """Click company name input field."""
        if self.locators.company_name_input.count() > 0:
            self.locators.company_name_input.click()
        else:
            self.locators.company_name_field.first.click()

    def expect_company_name_input(self):
        """Expect company name input field to be visible."""
        if self.locators.company_name_input.count() > 0:
            enhanced_assert_visible(self.page, self.locators.company_name_input, "Company name input should be visible")
        else:
            enhanced_assert_visible(self.page, self.locators.company_name_field.first, "Company name field should be visible")

    def fill_company_name_input(self, company_name: str):
        """Fill company name input field."""
        try:
            if self.locators.company_name_input.count() > 0:
                self.locators.company_name_input.fill(company_name)
            else:
                self.locators.company_name_field.first.fill(company_name)
        except Exception as e:
            print(f"Error filling company name: {e}")
            name_input = self.page.locator("input[placeholder*='Company'], input[name*='company']").first
            name_input.fill(company_name)

    # ===== WEBSITE INPUT METHODS =====
    def click_website_input(self):
        """Click website input field."""
        self.locators.website_input.click()

    def expect_website_input(self):
        """Expect website input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.website_input, "Website input should be visible")

    def fill_website_input(self, website: str):
        """Fill website input field."""
        self.locators.website_input.fill(website)

    # ===== TOTAL EMPLOYEES INPUT METHODS =====
    def click_total_employees_input(self):
        """Click total employees input field."""
        self.locators.total_employees_input.click()

    def expect_total_employees_input(self):
        """Expect total employees input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.total_employees_input, "Total employees input should be visible")

    def fill_total_employees_input(self, total_employees: str):
        """Fill total employees input field."""
        self.locators.total_employees_input.fill(total_employees)

    # ===== ADDRESS INPUT METHODS =====
    def click_address_input(self):
        """Click address input field."""
        self.locators.address_input.click()

    def expect_address_input(self):
        """Expect address input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.address_input, "Address input should be visible")

    def fill_address_input(self, address: str):
        """Fill address input field."""
        self.locators.address_input.fill(address)

    # ===== MAIN TEL INPUT METHODS =====
    def click_main_tel_input(self):
        """Click main tel input field."""
        self.locators.main_tel_input.click()

    def expect_main_tel_input(self):
        """Expect main tel input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.main_tel_input, "Main tel input should be visible")

    def fill_main_tel_input(self, main_tel: str):
        """Fill main tel input field."""
        self.locators.main_tel_input.fill(main_tel)

    # ===== HR TEL INPUT METHODS =====
    def click_hr_tel_input(self):
        """Click HR tel input field."""
        self.locators.hr_tel_input.click()

    def expect_hr_tel_input(self):
        """Expect HR tel input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.hr_tel_input, "HR tel input should be visible")

    # ===== INDUSTRY DROPDOWN METHODS =====
    def click_industry_dropdown(self):
        """Click industry dropdown."""
        self.locators.industry_dropdown.click()
        time.sleep(1)

    def expect_industry_dropdown(self):
        """Expect industry dropdown to be visible."""
        enhanced_assert_visible(self.page, self.locators.industry_dropdown, "Industry dropdown should be visible")

    def select_industry_option(self, industry: str):
        """Select industry from dropdown options."""
        self.click_industry_dropdown()
        if industry.lower() == "finance":
            self.locators.finance_option.click()
        elif industry.lower() == "healthcare":
            self.locators.healthcare_option.click()
        elif industry.lower() == "technology":
            self.locators.technology_option.click()
        elif industry.lower() == "education":
            self.locators.education_option.click()
        elif industry.lower() == "retail":
            self.locators.retail_option.click()
        elif industry.lower() == "information technology":
            self.locators.information_technology_option.click()
        else:
            self.page.get_by_text(industry, exact=True).click()
        time.sleep(1)

    # ===== HIRING STATUS DROPDOWN METHODS =====
    def click_hiring_status_dropdown(self):
        """Click hiring status dropdown."""
        self.locators.hiring_status_dropdown.click()
        time.sleep(1)

    def expect_hiring_status_dropdown(self):
        """Expect hiring status dropdown to be visible."""
        enhanced_assert_visible(self.page, self.locators.hiring_status_dropdown, "Hiring status dropdown should be visible")

    def select_hiring_status_option(self, status: str):
        """Select hiring status from dropdown options."""
        self.click_hiring_status_dropdown()
        if status.lower() == "active":
            self.locators.hiring_active_option.click()
        elif status.lower() == "inactive":
            self.locators.hiring_inactive_option.click()
        elif status.lower() == "on hold":
            self.locators.hiring_on_hold_option.click()
        elif status.lower() == "recruiting":
            self.locators.hiring_recruiting_option.click()
        else:
            self.page.get_by_text(status).click()
        time.sleep(1)

    # ===== COMPANY GRADE DROPDOWN METHODS =====
    def click_company_grade_dropdown(self):
        """Click company grade dropdown."""
        self.locators.company_grade_dropdown.click()
        time.sleep(1)

    def expect_company_grade_dropdown(self):
        """Expect company grade dropdown to be visible."""
        enhanced_assert_visible(self.page, self.locators.company_grade_dropdown, "Company grade dropdown should be visible")

    def select_company_grade_option(self, grade: str):
        """Select company grade from dropdown options."""
        self.click_company_grade_dropdown()
        if grade.upper() == "AAA":
            self.locators.grade_aaa_option.click()
        elif grade.upper() == "AA":
            self.locators.grade_aa_option.click()
        elif grade.upper() == "BBB":
            self.locators.grade_bbb_option.click()
        else:
            self.page.get_by_text(grade).click()
        time.sleep(1)

    # ===== HQ IN JAPAN DROPDOWN METHODS =====
    def click_hq_in_japan_dropdown(self):
        """Click HQ in Japan dropdown."""
        self.locators.hq_in_japan_dropdown.click()
        time.sleep(1)

    def expect_hq_in_japan_dropdown(self):
        """Expect HQ in Japan dropdown to be visible."""
        enhanced_assert_visible(self.page, self.locators.hq_in_japan_dropdown, "HQ in Japan dropdown should be visible")

    def select_hq_in_japan_option(self, option: str):
        """Select HQ in Japan option from dropdown."""
        self.click_hq_in_japan_dropdown()
        if option.lower() == "yes":
            self.locators.hq_yes_option.click()
        elif option.lower() == "no":
            self.locators.hq_no_option.click()
        else:
            self.page.get_by_text(option).click()
        time.sleep(1)

    # ===== JOB OPENING DROPDOWN METHODS =====
    def click_job_opening_dropdown(self):
        """Click job opening dropdown."""
        self.locators.job_opening_dropdown.click()
        time.sleep(1)

    def expect_job_opening_dropdown(self):
        """Expect job opening dropdown to be visible."""
        enhanced_assert_visible(self.page, self.locators.job_opening_dropdown, "Job opening dropdown should be visible")

    def select_job_opening_option(self, option: str):
        """Select job opening option from dropdown."""
        self.click_job_opening_dropdown()
        if option.lower() == "yes":
            self.locators.job_opening_yes_option.click()
        elif option.lower() == "no":
            self.locators.job_opening_no_option.click()
        else:
            self.page.get_by_text(option).click()
        time.sleep(1)

    # ===== OWNER DROPDOWN METHODS =====
    def click_owner_dropdown(self):
        """Click owner dropdown."""
        self.locators.owner_dropdown.click()
        time.sleep(1)

    def expect_owner_dropdown(self):
        """Expect owner dropdown to be visible."""
        enhanced_assert_visible(self.page, self.locators.owner_dropdown, "Owner dropdown should be visible")

    def select_owner_option(self, owner: str = "test"):
        """Select owner option from dropdown."""
        self.click_owner_dropdown()
        if owner.lower() == "test":
            self.locators.owner_option.click()
        else:
            self.page.get_by_text(owner).click()
        time.sleep(1)

    # ===== FILE UPLOAD METHODS =====
    def click_upload_logo(self):
        """Click upload logo area."""
        self.locators.upload_logo_text.click()

    def expect_upload_logo(self):
        """Expect upload logo area to be visible."""
        enhanced_assert_visible(self.page, self.locators.upload_logo_text, "Upload logo area should be visible")

    def upload_company_logo(self, file_path: str):
        """Upload company logo file."""
        try:
            # Try file input method
            file_input = self.page.locator("input[type='file']")
            if file_input.count() > 0:
                file_input.set_input_files(file_path)
            else:
                # Alternative method
                self.page.set_input_files("body", file_path)
        except Exception as e:
            print(f"Error uploading file: {e}")

    def upload_file(self, file_path: str):
        """Upload file - alias for upload_company_logo."""
        self.upload_company_logo(file_path)

    # ===== ACTION BUTTON METHODS =====
    def click_add_new_company_button(self):
        """Click Add new company button."""
        try:
            if self.locators.add_new_company_button.count() > 0:
                self.locators.add_new_company_button.click()
            elif self.locators.create_new_company_button.count() > 0:
                self.locators.create_new_company_button.click()
            else:
                self.locators.add_company_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error clicking add new company button: {e}")

    def click_create_button(self):
        """Click Create button."""
        self.locators.create_button.click()
        time.sleep(3)

    def click_save_button(self):
        """Click Save button."""
        self.locators.save_button.click()
        time.sleep(3)

    def click_update_button(self):
        """Click Update button."""
        self.locators.update_button.click()
        time.sleep(3)

    def click_cancel_button(self):
        """Click Cancel button."""
        self.locators.cancel_button.click()

    def click_close_modal_button(self):
        """Click Close modal button."""
        self.locators.close_modal_button.click()

    # ===== COMPANY ACTIONS METHODS =====
    def click_view_details_button(self):
        """Click View Details button."""
        self.locators.view_details_button.click()
        time.sleep(2)

    def click_three_dot_menu(self):
        """Click three dot menu."""
        self.locators.three_dot_menu.click()
        time.sleep(1)

    def click_edit_company_button(self):
        """Click Edit company button."""
        self.locators.edit_company_button.click()
        time.sleep(2)

    def click_delete_company_button(self):
        """Click Delete company button."""
        self.locators.delete_company_button.click()
        time.sleep(2)

    # ===== COMPANY PROFILE TAB METHODS =====
    def click_summary_tab(self):
        """Click Summary tab."""
        self.locators.summary_tab.click()
        time.sleep(2)

    def click_basic_company_info_tab(self):
        """Click Basic company info tab."""
        self.locators.basic_company_info_tab.click()
        time.sleep(2)

    def click_web_contact_info_tab(self):
        """Click Web & Contact info tab."""
        self.locators.web_contact_info_tab.click()
        time.sleep(2)

    def click_location_details_tab(self):
        """Click Location details tab."""
        self.locators.location_details_tab.click()
        time.sleep(2)

    def click_employees_business_info_tab(self):
        """Click Employees & Business info tab."""
        self.locators.employees_business_info_tab.click()
        time.sleep(2)

    # ===== CLIENT TAB METHODS =====
    def click_client_tab(self):
        """Click Client tab."""
        self.locators.client_tab.click()
        time.sleep(2)

    def click_add_new_client_button(self):
        """Click Add new client button."""
        self.locators.add_new_client_button.click()
        time.sleep(2)

    def click_add_client_button(self):
        """Click Add Client button."""
        self.locators.add_client_button.click()
        time.sleep(2)

    def click_create_client_button(self):
        """Click Create client button."""
        self.locators.create_client_button.click()
        time.sleep(3)

    # ===== CLIENT FORM INPUT METHODS =====
    def click_client_english_name_input(self):
        """Click client English name input field."""
        self.locators.client_english_name_input.click()

    def expect_client_english_name_input(self):
        """Expect client English name input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.client_english_name_input, "Client English name input should be visible")

    def fill_client_english_name_input(self, english_name: str):
        """Fill client English name input field."""
        self.locators.client_english_name_input.fill(english_name)

    def click_client_japanese_name_input(self):
        """Click client Japanese name input field."""
        self.locators.client_japanese_name_input.click()

    def expect_client_japanese_name_input(self):
        """Expect client Japanese name input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.client_japanese_name_input, "Client Japanese name input should be visible")

    def fill_client_japanese_name_input(self, japanese_name: str):
        """Fill client Japanese name input field."""
        self.locators.client_japanese_name_input.fill(japanese_name)

    def click_client_job_title_input(self):
        """Click client job title input field."""
        self.locators.client_job_title_input.click()

    def expect_client_job_title_input(self):
        """Expect client job title input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.client_job_title_input, "Client job title input should be visible")

    def fill_client_job_title_input(self, job_title: str):
        """Fill client job title input field."""
        self.locators.client_job_title_input.fill(job_title)

    def click_client_department_input(self):
        """Click client department input field."""
        self.locators.client_department_input.click()

    def expect_client_department_input(self):
        """Expect client department input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.client_department_input, "Client department input should be visible")

    def fill_client_department_input(self, department: str):
        """Fill client department input field."""
        self.locators.client_department_input.fill(department)

    def click_client_phone_name_input(self):
        """Click client phone name input field."""
        self.locators.client_phone_name_input.click()

    def expect_client_phone_name_input(self):
        """Expect client phone name input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.client_phone_name_input, "Client phone name input should be visible")

    def fill_client_phone_name_input(self, phone_name: str):
        """Fill client phone name input field."""
        self.locators.client_phone_name_input.fill(phone_name)

    def click_client_phone_number_input(self):
        """Click client phone number input field."""
        self.locators.client_phone_number_input.click()

    def expect_client_phone_number_input(self):
        """Expect client phone number input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.client_phone_number_input, "Client phone number input should be visible")

    def fill_client_phone_number_input(self, phone_number: str):
        """Fill client phone number input field."""
        self.locators.client_phone_number_input.fill(phone_number)

    def click_client_email_name_input(self):
        """Click client email name input field."""
        self.locators.client_email_name_input.click()

    def expect_client_email_name_input(self):
        """Expect client email name input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.client_email_name_input, "Client email name input should be visible")

    def fill_client_email_name_input(self, email_name: str):
        """Fill client email name input field."""
        self.locators.client_email_name_input.fill(email_name)

    def click_client_email_input(self):
        """Click client email input field."""
        self.locators.client_email_input.click()

    def expect_client_email_input(self):
        """Expect client email input field to be visible."""
        enhanced_assert_visible(self.page, self.locators.client_email_input, "Client email input should be visible")

    def fill_client_email_input(self, email: str):
        """Fill client email input field."""
        self.locators.client_email_input.fill(email)

    # ===== CLIENT DROPDOWN METHODS =====
    def click_client_gender_dropdown(self):
        """Click client gender dropdown."""
        self.locators.client_gender_dropdown.click()
        time.sleep(1)

    def expect_client_gender_dropdown(self):
        """Expect client gender dropdown to be visible."""
        enhanced_assert_visible(self.page, self.locators.client_gender_dropdown, "Client gender dropdown should be visible")

    def select_client_gender_option(self, gender: str):
        """Select client gender from dropdown options."""
        self.click_client_gender_dropdown()
        if gender.lower() == "male":
            self.locators.client_male_option.click()
        elif gender.lower() == "female":
            self.locators.client_female_option.click()
        else:
            self.page.get_by_text(gender).click()
        time.sleep(1)

    def click_client_english_skill_dropdown(self):
        """Click client English skill dropdown."""
        self.locators.client_english_skill_dropdown.click()
        time.sleep(1)

    def expect_client_english_skill_dropdown(self):
        """Expect client English skill dropdown to be visible."""
        enhanced_assert_visible(self.page, self.locators.client_english_skill_dropdown, "Client English skill dropdown should be visible")

    def select_client_english_skill_option(self, skill: str):
        """Select client English skill from dropdown options."""
        self.click_client_english_skill_dropdown()
        if skill.lower() == "basic":
            self.locators.client_basic_option.click()
        else:
            self.page.get_by_text(skill).click()
        time.sleep(1)

    def click_client_japanese_skill_dropdown(self):
        """Click client Japanese skill dropdown."""
        self.locators.client_japanese_skill_dropdown.click()
        time.sleep(1)

    def expect_client_japanese_skill_dropdown(self):
        """Expect client Japanese skill dropdown to be visible."""
        enhanced_assert_visible(self.page, self.locators.client_japanese_skill_dropdown, "Client Japanese skill dropdown should be visible")

    def select_client_japanese_skill_option(self, skill: str):
        """Select client Japanese skill from dropdown options."""
        self.click_client_japanese_skill_dropdown()
        if skill.lower() == "conversational":
            self.locators.client_conversational_option.click()
        else:
            self.page.get_by_text(skill).click()
        time.sleep(1)

    def click_add_email_button(self):
        """Click Add Email Address button."""
        self.locators.add_email_button.click()
        time.sleep(1)

    # ===== VALIDATION EXPECTATION METHODS =====
    def expect_company_name_required_validation_error(self, test_name: str = None):
        """Expect company name required validation error to be visible."""
        enhanced_assert_visible(self.page, self.locators.company_name_required_error, 
                              "Company name required error should be visible", test_name)

    def expect_company_name_already_exists_validation_error(self, test_name: str = None):
        """Expect company name already exists validation error to be visible."""
        enhanced_assert_visible(self.page, self.locators.company_name_already_exists_error, 
                              "Company name already exists error should be visible", test_name)

    def expect_company_name_min_length_validation_error(self, test_name: str = None):
        """Expect company name minimum length validation error to be visible."""
        enhanced_assert_visible(self.page, self.locators.company_name_min_length_error, 
                              "Company name minimum length error should be visible", test_name)

    def expect_company_name_max_length_validation_error(self, test_name: str = None):
        """Expect company name maximum length validation error to be visible."""
        enhanced_assert_visible(self.page, self.locators.company_name_max_length_error, 
                              "Company name maximum length error should be visible", test_name)

    def expect_company_name_special_char_validation_error(self, test_name: str = None):
        """Expect company name special character validation error to be visible."""
        enhanced_assert_visible(self.page, self.locators.company_name_special_char_error, 
                              "Company name special character error should be visible", test_name)

    def expect_industry_required_validation_error(self, test_name: str = None):
        """Expect industry required validation error to be visible."""
        enhanced_assert_visible(self.page, self.locators.industry_required_error, 
                              "Industry required error should be visible", test_name)

    def expect_website_required_validation_error(self, test_name: str = None):
        """Expect website required validation error to be visible."""
        enhanced_assert_visible(self.page, self.locators.website_required_error, 
                              "Website required error should be visible", test_name)

    def expect_address_required_validation_error(self, test_name: str = None):
        """Expect address required validation error to be visible."""
        enhanced_assert_visible(self.page, self.locators.address_required_error, 
                              "Address required error should be visible", test_name)

    def expect_owner_required_validation_error(self, test_name: str = None):
        """Expect owner required validation error to be visible."""
        enhanced_assert_visible(self.page, self.locators.owner_required_error, 
                              "Owner required error should be visible", test_name)

    def expect_file_size_validation_error(self, test_name: str = None):
        """Expect file size validation error to be visible."""
        enhanced_assert_visible(self.page, self.locators.file_size_error, 
                              "File size error should be visible", test_name)

    def expect_file_type_validation_error(self, test_name: str = None):
        """Expect file type validation error to be visible."""
        enhanced_assert_visible(self.page, self.locators.file_type_error, 
                              "File type error should be visible", test_name)

    # ===== CLIENT VALIDATION EXPECTATION METHODS =====
    def expect_client_name_required_validation_error(self, test_name: str = None):
        """Expect client name required validation error to be visible."""
        enhanced_assert_visible(self.page, self.locators.client_name_required_error, 
                              "Client name required error should be visible", test_name)

    def expect_client_email_required_validation_error(self, test_name: str = None):
        """Expect client email required validation error to be visible."""
        enhanced_assert_visible(self.page, self.locators.client_email_required_error, 
                              "Client email required error should be visible", test_name)

    # ===== SUCCESS MESSAGE EXPECTATION METHODS =====
    def expect_company_created_successfully_message(self, test_name: str = None):
        """Expect company created successfully message to be visible."""
        enhanced_assert_visible(self.page, self.locators.company_created_successfully_message, 
                              "Company created successfully message should be visible", test_name)

    def expect_company_added_successfully_message(self, test_name: str = None):
        """Expect company added successfully message to be visible."""
        enhanced_assert_visible(self.page, self.locators.company_added_successfully_message, 
                              "Company added successfully message should be visible", test_name)

    def expect_company_updated_successfully_message(self, test_name: str = None):
        """Expect company updated successfully message to be visible."""
        enhanced_assert_visible(self.page, self.locators.company_updated_successfully_message, 
                              "Company updated successfully message should be visible", test_name)

    def expect_company_deleted_successfully_message(self, test_name: str = None):
        """Expect company deleted successfully message to be visible."""
        enhanced_assert_visible(self.page, self.locators.company_deleted_successfully_message, 
                              "Company deleted successfully message should be visible", test_name)

    def expect_client_created_successfully_message(self, test_name: str = None):
        """Expect client created successfully message to be visible."""
        enhanced_assert_visible(self.page, self.locators.client_created_successfully_message, 
                              "Client created successfully message should be visible", test_name)

    # ===== PAGE ELEMENT EXPECTATION METHODS =====
    def expect_home_company_heading(self, test_name: str = None):
        """Expect Home>Company breadcrumb heading to be visible."""
        enhanced_assert_visible(self.page, self.locators.home_company_heading, 
                              "Home>Company heading should be visible", test_name)

    def expect_no_companies_found_message(self, test_name: str = None):
        """Expect no companies found message to be visible."""
        enhanced_assert_visible(self.page, self.locators.no_companies_found_message, 
                              "No companies found message should be visible", test_name)

    def expect_no_clients_found_message(self, test_name: str = None):
        """Expect no clients found message to be visible."""
        enhanced_assert_visible(self.page, self.locators.no_clients_found_message, 
                              "No clients found message should be visible", test_name)

    def expect_delete_confirmation_modal(self, test_name: str = None):
        """Expect delete confirmation modal to be visible."""
        enhanced_assert_visible(self.page, self.locators.delete_confirm_modal, 
                              "Delete confirmation modal should be visible", test_name)

    def expect_add_new_client_modal_heading(self, test_name: str = None):
        """Expect Add New Client modal heading to be visible."""
        enhanced_assert_visible(self.page, self.locators.add_new_client_modal_heading, 
                              "Add New Client modal heading should be visible", test_name)

    def expect_selected_delete_text(self, test_name: str = None):
        """Expect selected delete text to be visible."""
        enhanced_assert_visible(self.page, self.locators.selected_delete_text, 
                              "Selected delete text should be visible", test_name)

    def expect_created_company_heading(self, company_name: str, test_name: str = None):
        """Expect created company heading to be visible."""
        company_heading = self.locators.created_company_heading(company_name)
        enhanced_assert_visible(self.page, company_heading, 
                              f"Created company heading '{company_name}' should be visible", test_name)

    def expect_created_client_heading(self, client_name: str, test_name: str = None):
        """Expect created client heading to be visible."""
        client_heading = self.locators.created_client_heading(client_name)
        enhanced_assert_visible(self.page, client_heading, 
                              f"Created client heading '{client_name}' should be visible", test_name)

    # ===== UTILITY METHODS =====
    def wait_for_page_load(self, timeout: int = 10000):
        """Wait for page to load completely."""
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        time.sleep(2)

    def clear_company_name_input(self):
        """Clear company name input field."""
        if self.locators.company_name_input.count() > 0:
            self.locators.company_name_input.fill("")
        else:
            self.locators.company_name_field.first.fill("")

    def verify_breadcrumb_heading(self):
        """Verify that 'Home>Company' breadcrumb is visible."""
        try:
            return self.locators.home_company_heading.is_visible(timeout=5000)
        except:
            return (self.locators.breadcrumb_home.is_visible() and 
                    self.locators.breadcrumb_company.is_visible())

    def find_company_in_list(self, company_name: str):
        """Find a company in the companies list."""
        try:
            company_element = self.page.get_by_text(company_name, exact=True)
            return company_element.count() > 0
        except:
            return False

    def wait_for_navigation(self, expected_path: str = None, timeout: int = 10000):
        """Wait for navigation to complete."""
        try:
            if expected_path:
                self.page.wait_for_url(f"**/{expected_path}**", timeout=timeout)
            else:
                self.page.wait_for_load_state("networkidle", timeout=timeout)
            time.sleep(2)
        except:
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=5000)
                time.sleep(2)
            except:
                time.sleep(3)

    def click_add_new_company_button(self):
        """Click the Add new company button."""
        try:
            if self.locators.add_new_company_button.count() > 0:
                self.locators.add_new_company_button.click()
            elif self.locators.create_new_company_button.count() > 0:
                self.locators.create_new_company_button.click()
            else:
                self.locators.add_company_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error clicking add new company button: {e}")
            # Fallback
            add_button = self.page.locator("text='Add new company', text='Create new company'").first
            add_button.click()
            time.sleep(2)

    def verify_breadcrumb_heading(self):
        """Verify that 'Home>Company' breadcrumb is visible."""
        try:
            return self.locators.home_company_heading.is_visible(timeout=5000)
        except:
            # Alternative verification
            return (self.locators.breadcrumb_home.is_visible() and 
                    self.locators.breadcrumb_company.is_visible())

    def fill_company_name(self, company_name: str):
        """Fill the company name field."""
        try:
            if self.locators.company_name_input.count() > 0:
                self.locators.company_name_input.fill(company_name)
            else:
                self.locators.company_name_field.first.fill(company_name)
        except Exception as e:
            print(f"Error filling company name: {e}")
            # Fallback to any input that might be the company name field
            name_input = self.page.locator("input[placeholder*='Company'], input[name*='company']").first
            name_input.fill(company_name)

    def select_industry(self, industry: str = "Finance"):
        """Select industry from dropdown."""
        try:
            # Click dropdown
            self.locators.industry_dropdown.click()
            time.sleep(1)
            
            # Select industry
            if industry.lower() == "finance":
                self.locators.finance_option.click()
            elif industry.lower() == "healthcare":
                self.locators.healthcare_option.click()
            elif industry.lower() == "technology":
                self.locators.technology_option.click()
            elif industry.lower() == "education":
                self.locators.education_option.click()
            else:
                # Fallback - select any option with the given text
                self.page.get_by_text(industry, exact=True).click()
                
            time.sleep(1)
        except Exception as e:
            print(f"Error selecting industry '{industry}': {e}")

    def fill_optional_fields(self, website: str = None, address: str = None, owner: str = None, division: str = None):
        """Fill optional form fields if provided."""
        if website:
            try:
                self.locators.website_input.fill(website)
            except:
                pass
                
        if address:
            try:
                self.locators.address_input.fill(address)
            except:
                pass
                
        if owner:
            try:
                self.locators.owner_input.fill(owner)
            except:
                pass
                
        if division:
            try:
                self.locators.division_dropdown.click()
                time.sleep(1)
                if division.lower() == "dhaka":
                    self.locators.dhaka_division.click()
                else:
                    self.page.get_by_text(division, exact=True).click()
                time.sleep(1)
            except:
                pass

    def click_create_button(self):
        """Click the Create button."""
        try:
            if self.locators.create_button.count() > 0:
                self.locators.create_button.click()
            elif self.locators.save_button.count() > 0:
                self.locators.save_button.click()
            else:
                # Fallback
                submit_btn = self.page.locator("button[type='submit'], .btn-primary").first
                submit_btn.click()
            time.sleep(3)  # Wait for processing
        except Exception as e:
            print(f"Error clicking create button: {e}")

    def verify_success_message(self, message_type: str = "created"):
        """Verify success message appears."""
        try:
            if message_type == "created":
                return (self.locators.company_created_successfully_message.is_visible(timeout=10000) or
                        self.locators.company_added_successfully_message.is_visible(timeout=10000))
            elif message_type == "updated":
                return self.locators.company_updated_successfully_message.is_visible(timeout=10000)
            elif message_type == "deleted":
                return self.locators.company_deleted_successfully_message.is_visible(timeout=10000)
        except:
            return False

    def verify_company_profile_page(self, company_name: str):
        """Verify that we're on the company profile page with the correct company name."""
        try:
            # Check if company name appears as heading
            company_heading = self.locators.company_profile_heading(company_name)
            return company_heading.is_visible(timeout=10000)
        except:
            # Fallback - check if company name appears anywhere on page
            return self.page.get_by_text(company_name).count() > 0

    def verify_validation_error(self, error_type: str):
        """Verify specific validation error appears."""
        try:
            if error_type == "company_name_required":
                return self.locators.company_name_required_error.is_visible(timeout=5000)
            elif error_type == "company_name_already_exists":
                return self.locators.company_name_already_exists_error.is_visible(timeout=5000)
            elif error_type == "company_name_min_length":
                return self.locators.company_name_min_length_error.is_visible(timeout=5000)
            elif error_type == "company_name_max_length":
                return self.locators.company_name_max_length_error.is_visible(timeout=5000)
            elif error_type == "company_name_special_char":
                return self.locators.company_name_special_char_error.is_visible(timeout=5000)
            elif error_type == "industry_required":
                return self.locators.industry_required_error.is_visible(timeout=5000)
            else:
                return False
        except:
            return False

    def clear_form(self):
        """Clear all form fields."""
        try:
            if self.locators.company_name_input.count() > 0:
                self.locators.company_name_input.fill("")
            else:
                self.locators.company_name_field.first.fill("")
        except:
            pass

    def navigate_back_to_company_form(self):
        """Navigate back to add new company form."""
        try:
            # If we're on company profile page, look for Add Company button
            add_button = self.page.locator("text='Add Company', text='Add new company'").first
            if add_button.is_visible():
                add_button.click()
            else:
                # Navigate via breadcrumb or back button
                self.page.go_back()
                time.sleep(2)
                self.click_add_new_company_button()
        except Exception as e:
            print(f"Error navigating back to company form: {e}")

    def find_company_in_list(self, company_name: str):
        """Find a company in the companies list."""
        try:
            company_element = self.page.get_by_text(company_name, exact=True)
            return company_element.count() > 0
        except:
            return False

    def click_view_details_button(self, company_name: str):
        """Click View Details button for a specific company."""
        try:
            # First find the company
            company_element = self.page.get_by_text(company_name, exact=True)
            if company_element.count() > 0:
                # Look for View Details button near the company name
                parent = company_element.locator('xpath=..')
                view_details_btn = parent.locator("button", has_text="View Details")
                if view_details_btn.count() > 0:
                    view_details_btn.click()
                else:
                    # Fallback to any View Details button
                    self.locators.view_details_button.click()
                time.sleep(2)
        except Exception as e:
            print(f"Error clicking view details for company '{company_name}': {e}")

    def click_three_dot_menu(self, company_name: str):
        """Click three dot menu for a specific company."""
        try:
            company_element = self.page.get_by_text(company_name, exact=True)
            if company_element.count() > 0:
                parent = company_element.locator('xpath=..')
                menu_btn = parent.locator(".p-1, [data-testid='menu']").first
                menu_btn.click()
                time.sleep(1)
        except Exception as e:
            print(f"Error clicking three dot menu for company '{company_name}': {e}")

    def click_edit_company_button(self):
        """Click edit button from three dot menu."""
        try:
            self.locators.edit_company_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error clicking edit company button: {e}")

    def click_delete_company_button(self):
        """Click delete button from three dot menu."""
        try:
            self.locators.delete_company_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error clicking delete company button: {e}")

    def click_update_button(self):
        """Click the Update button."""
        try:
            self.locators.update_button.click()
            time.sleep(3)
        except Exception as e:
            print(f"Error clicking update button: {e}")

    def click_client_tab(self):
        """Click on the Client tab."""
        try:
            if self.locators.client_tab.count() > 0:
                self.locators.client_tab.click()
            else:
                self.locators.clients_tab.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error clicking client tab: {e}")

    def click_add_new_client_button(self):
        """Click Add new client button."""
        try:
            self.locators.add_new_client_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error clicking add new client button: {e}")

    def fill_client_form(self, client_name: str, email: str = None, phone: str = None):
        """Fill client creation form."""
        try:
            self.locators.client_name_input.fill(client_name)
            
            if email:
                self.locators.client_email_input.fill(email)
                
            if phone:
                self.locators.client_phone_input.fill(phone)
                
        except Exception as e:
            print(f"Error filling client form: {e}")

    def click_create_client_button(self):
        """Click Create Client button."""
        try:
            if self.locators.create_client_button.count() > 0:
                self.locators.create_client_button.click()
            else:
                self.locators.create_button.click()
            time.sleep(3)
        except Exception as e:
            print(f"Error clicking create client button: {e}")

    def wait_for_navigation(self, expected_path: str = None, timeout: int = 10000):
        """Wait for navigation to complete."""
        try:
            if expected_path:
                self.page.wait_for_url(f"**/{expected_path}**", timeout=timeout)
            else:
                self.page.wait_for_load_state("networkidle", timeout=timeout)
            time.sleep(2)
        except:
            # Fallback - just wait for load state
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=5000)
                time.sleep(2)
            except:
                time.sleep(3)  # Final fallback
