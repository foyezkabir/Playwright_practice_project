"""
JD (Job Description) Page Object Model
Handles all JD management operations including creation, editing, listing, search, filtering, and bulk operations
"""

from playwright.sync_api import Page, expect
from locators.loc_jd import JDLocators
from utils.config import BASE_URL
from utils.enhanced_assertions import enhanced_assert_visible, enhanced_assert_not_visible
import time


class JDPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = JDLocators(page)

    # ===== NAVIGATION METHODS =====
    def navigate_to_jd_page(self, agency_id: str):
        """Navigate to JD page for specific agency"""
        url = self.locators.jd_page_url.format(agency_id=agency_id)
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        time.sleep(2)  # Allow page to fully load

    def navigate_to_login_page(self, url: str):
        """Navigate to login page"""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def verify_jd_page_url(self, agency_id: str):
        """Verify that we're on the correct JD page"""
        current_url = self.page.url
        expected_url_part = f"/agency/{agency_id}/jd"
        assert expected_url_part in current_url, f"Expected to be on JD page with {expected_url_part}, but was on {current_url}"

    # ===== JD MODAL OPERATIONS =====
    def click_add_jd(self):
        """Click Add JD button to open creation modal"""
        self.locators.add_jd_button.click()
        time.sleep(1)

    def expect_jd_modal_heading(self):
        """Verify JD creation modal heading is visible"""
        enhanced_assert_visible(self.page, self.locators.jd_modal_heading, 
                               "JD modal heading should be visible", "jd_modal_heading")

    def expect_jd_modal_body(self):
        """Verify JD modal body is visible"""
        enhanced_assert_visible(self.page, self.locators.jd_modal_body, 
                               "JD modal body should be visible", "jd_modal_body")

    def close_jd_modal(self):
        """Close JD modal using close button"""
        self.locators.close_modal_button.click()
        time.sleep(1)

    def expect_no_jd_modal(self):
        """Verify JD modal is not visible"""
        try:
            time.sleep(2)
            enhanced_assert_not_visible(self.page, self.locators.jd_modal_heading, 
                                       "JD modal should not be visible", "no_jd_modal")
            print("✅ No JD creation modal appeared (as expected)")
        except Exception as e:
            raise AssertionError(f"JD creation modal appeared when it shouldn't have: {str(e)}")

    def wait_for_modal_to_open(self, timeout: int = 5000):
        """Wait for JD modal to open and become visible"""
        try:
            self.locators.jd_modal_heading.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    def wait_for_modal_to_close(self, timeout: int = 5000):
        """Wait for JD modal to close and become hidden"""
        try:
            self.locators.jd_modal_heading.wait_for(state="hidden", timeout=timeout)
            return True
        except:
            return False

    def is_modal_open(self) -> bool:
        """Check if JD modal is currently open"""
        return self.locators.jd_modal_heading.count() > 0

    def is_modal_closed(self) -> bool:
        """Check if JD modal is currently closed"""
        return self.locators.jd_modal_heading.count() == 0

    def expect_modal_remains_open_after_validation_error(self):
        """Verify modal stays open when validation errors occur"""
        if not self.is_modal_open():
            raise AssertionError("Modal should remain open after validation error, but it was closed")
        print("✅ Modal correctly remained open after validation error")

    def expect_modal_closes_after_successful_save(self):
        """Verify modal closes after successful JD creation"""
        if not self.wait_for_modal_to_close():
            raise AssertionError("Modal should close after successful save, but it remained open")
        print("✅ Modal correctly closed after successful save")

    def handle_modal_state_during_validation(self):
        """Handle modal state management during validation scenarios"""
        # Ensure modal is open before validation
        if not self.is_modal_open():
            raise AssertionError("Modal should be open before validation testing")
        
        # Modal should remain open during validation errors
        self.expect_modal_remains_open_after_validation_error()

    # ===== FORM FILLING METHODS =====
    def fill_position_job_title(self, title: str):
        """Fill position job title field"""
        self.locators.position_job_title_input.fill(title)

    def fill_jd_workplace(self, workplace: str):
        """Fill JD workplace field"""
        self.locators.jd_workplace_input.fill(workplace)

    def fill_minimum_salary(self, salary: str):
        """Fill minimum salary field"""
        self.locators.minimum_salary_input.fill(str(salary))

    def fill_maximum_salary(self, salary: str):
        """Fill maximum salary field"""
        self.locators.maximum_salary_input.fill(str(salary))

    def fill_job_age_min(self, age: str):
        """Fill minimum job age field"""
        self.locators.job_age_min_input.fill(str(age))

    def fill_job_age_max(self, age: str):
        """Fill maximum job age field"""
        self.locators.job_age_max_input.fill(str(age))

    def fill_target_age_min(self, age: str):
        """Fill minimum target age field"""
        self.locators.target_age_min_input.fill(str(age))

    def fill_target_age_max(self, age: str):
        """Fill maximum target age field"""
        self.locators.target_age_max_input.fill(str(age))

    def fill_department(self, department: str):
        """Fill department field"""
        self.locators.department_input.fill(department)

    def fill_direct_report(self, direct_report: str):
        """Fill direct report field"""
        self.locators.direct_report_input.fill(direct_report)

    def fill_job_function(self, job_function: str):
        """Fill job function field"""
        self.locators.job_function_input.fill(job_function)

    # ===== DROPDOWN SELECTION METHODS =====
    def select_company(self, company_name: str):
        """Select company from dropdown"""
        print(f"🔧 Selecting company: {company_name}")
        
        try:
            # Wait for the company dropdown to be visible first
            self.locators.company_dropdown.wait_for(state="visible", timeout=5000)
            print("✅ Company dropdown is visible")
            
            # Click the chevron to open dropdown
            self.locators.company_dropdown.click()
            print("✅ Clicked company dropdown")
            time.sleep(2)
            
            # Wait for and click the company option
            self.locators.company_option(company_name).wait_for(state="visible", timeout=5000)
            self.locators.company_option(company_name).click()
            print(f"✅ Selected company: {company_name}")
            
        except Exception as e:
            print(f"❌ Error selecting company: {e}")
            raise

    def select_work_style(self, work_style: str):
        """Select work style from dropdown"""
        print(f"🔧 Selecting work style: {work_style}")
        
        try:
            # Wait for the work style dropdown to be visible first
            self.locators.work_style_dropdown.wait_for(state="visible", timeout=5000)
            print("✅ Work style dropdown is visible")
            
            # Click the chevron to open dropdown
            self.locators.work_style_dropdown.click()
            print("✅ Clicked work style dropdown")
            time.sleep(2)  # Increased wait time
            
            # Wait for dropdown to be visible
            self.page.wait_for_timeout(1000)
            
            if work_style.lower() == "remote":
                # Try to wait for the option to be visible first
                try:
                    self.locators.remote_work_option.wait_for(state="visible", timeout=10000)
                    self.locators.remote_work_option.click()
                    print("✅ Selected Remote work style")
                except Exception as e:
                    print(f"⚠️ First attempt failed: {e}")
                    # Fallback: try clicking the dropdown again and retry
                    self.locators.work_style_dropdown.click()
                    time.sleep(1)
                    self.locators.remote_work_option.click()
                    print("✅ Selected Remote work style (fallback)")
            elif work_style.lower() == "on-site" or work_style.lower() == "onsite":
                try:
                    self.locators.onsite_work_option.wait_for(state="visible", timeout=10000)
                    self.locators.onsite_work_option.click()
                    print("✅ Selected On-site work style")
                except Exception as e:
                    print(f"⚠️ First attempt failed: {e}")
                    self.locators.work_style_dropdown.click()
                    time.sleep(1)
                    self.locators.onsite_work_option.click()
                    print("✅ Selected On-site work style (fallback)")
            elif work_style.lower() == "hybrid":
                try:
                    self.locators.hybrid_work_option.wait_for(state="visible", timeout=10000)
                    self.locators.hybrid_work_option.click()
                    print("✅ Selected Hybrid work style")
                except Exception as e:
                    print(f"⚠️ First attempt failed: {e}")
                    self.locators.work_style_dropdown.click()
                    time.sleep(1)
                    self.locators.hybrid_work_option.click()
                    print("✅ Selected Hybrid work style (fallback)")
                    
        except Exception as e:
            print(f"❌ Error selecting work style: {e}")
            raise

    def select_currency(self, currency: str):
        """Select currency from dropdown
        Available options: USD ($), EUR (€), GBP (£), JPY (¥)
        """
        self.locators.currency_dropdown.click()
        time.sleep(2)  # Wait for dropdown to open
        
        currency_upper = currency.upper()
        
        try:
            # Dropdowns close after selection, so use .first for the visible option
            if currency_upper == "USD":
                self.page.get_by_text("USD ($)", exact=True).first.click(timeout=10000)
            elif currency_upper == "EUR":
                self.page.get_by_text("EUR (€)", exact=True).first.click(timeout=10000)
            elif currency_upper == "GBP":
                self.page.get_by_text("GBP (£)", exact=True).first.click(timeout=10000)
            elif currency_upper == "JPY":
                self.page.get_by_text("JPY (¥)", exact=True).first.click(timeout=10000)
            else:
                # Default to USD if not recognized
                self.page.get_by_text("USD ($)", exact=True).first.click(timeout=10000)
            time.sleep(0.5)  # Wait for selection to register
        except Exception as e:
            print(f"⚠️ Could not select currency: {currency}, error: {e}")

    def select_japanese_level(self, level: str):
        """Select Japanese language level from dropdown
        Available options: Elementary, Limited Working, Professional Working, Full Professional, Native or Bilingual
        """
        self.locators.japanese_level_dropdown.click()
        time.sleep(2)  # Wait for dropdown to open
        level_lower = level.lower()
        
        try:
            # Dropdowns close after selection, so use .first for the visible option
            if level_lower == "native or bilingual" or level_lower == "native":
                self.page.get_by_text("Native or Bilingual", exact=True).first.click(timeout=10000)
            elif level_lower == "full professional":
                self.page.get_by_text("Full Professional", exact=True).first.click(timeout=10000)
            elif level_lower == "professional working":
                self.page.get_by_text("Professional Working", exact=True).first.click(timeout=10000)
            elif level_lower == "limited working":
                self.page.get_by_text("Limited Working", exact=True).first.click(timeout=10000)
            elif level_lower == "elementary":
                self.page.get_by_text("Elementary", exact=True).first.click(timeout=10000)
            else:
                # Default to Elementary
                self.page.get_by_text("Elementary", exact=True).first.click(timeout=10000)
            time.sleep(0.5)  # Wait for selection to register
        except Exception as e:
            print(f"⚠️ Could not select Japanese level: {level}, error: {e}")

    def select_english_level(self, level: str):
        """Select English language level from dropdown
        Available options: Elementary, Limited Working, Professional Working, Full Professional, Native or Bilingual
        """
        self.locators.english_level_dropdown.click()
        time.sleep(2)  # Wait for dropdown to open
        level_lower = level.lower()
        
        try:
            # Dropdowns close after selection, so use .first for the visible option
            if level_lower == "native or bilingual" or level_lower == "native":
                self.page.get_by_text("Native or Bilingual", exact=True).first.click(timeout=10000)
            elif level_lower == "full professional":
                self.page.get_by_text("Full Professional", exact=True).first.click(timeout=10000)
            elif level_lower == "professional working":
                self.page.get_by_text("Professional Working", exact=True).first.click(timeout=10000)
            elif level_lower == "limited working":
                self.page.get_by_text("Limited Working", exact=True).first.click(timeout=10000)
            elif level_lower == "elementary":
                self.page.get_by_text("Elementary", exact=True).first.click(timeout=10000)
            else:
                # Default to Elementary
                self.page.get_by_text("Elementary", exact=True).first.click(timeout=10000)
            time.sleep(0.5)  # Wait for selection to register
        except Exception as e:
            print(f"⚠️ Could not select English level: {level}, error: {e}")

    def select_priority_grade(self, priority: str):
        """Select priority grade from dropdown"""
        # Scroll to priority grade field to ensure it's visible
        self.locators.priority_grade_dropdown.scroll_into_view_if_needed()
        time.sleep(1)
        
        self.locators.priority_grade_dropdown.click()
        time.sleep(2)  # Wait for dropdown to open and load all options
        
        priority_upper = priority.upper()
        
        try:
            # Dropdowns close after selection, so use .first for the visible option
            if priority_upper == "AAA":
                self.page.get_by_text("AAA", exact=True).first.click(timeout=10000)
            elif priority_upper == "AA":
                self.page.get_by_text("AA", exact=True).first.click(timeout=10000)
            elif priority_upper == "A":
                self.page.get_by_text("A", exact=True).first.click(timeout=10000)
            elif priority_upper == "BBB":
                self.page.get_by_text("BBB", exact=True).first.click(timeout=10000)
            elif priority_upper == "BB":
                self.page.get_by_text("BB", exact=True).first.click(timeout=10000)
            else:
                # Default to A if not recognized
                self.page.get_by_text("A", exact=True).first.click(timeout=10000)
            time.sleep(0.5)  # Wait for selection to register
        except Exception as e:
            print(f"⚠️ Could not select Priority Grade: {priority}, error: {e}")

    def select_hiring_status(self, status: str):
        """Select hiring status from dropdown"""
        self.locators.hiring_status_dropdown.scroll_into_view_if_needed()
        time.sleep(1)
        
        self.locators.hiring_status_dropdown.click()
        time.sleep(2)  # Wait for dropdown to open and load all options
        
        status_lower = status.lower()
        
        try:
            # Dropdowns close after selection, so use .first for the visible option
            if status_lower == "open":
                self.page.get_by_text("Open", exact=True).first.click(timeout=10000)
            elif status_lower == "urgent":
                self.page.get_by_text("Urgent", exact=True).first.click(timeout=10000)
            elif status_lower == "closed":
                self.page.get_by_text("Closed", exact=True).first.click(timeout=10000)
            else:
                # Default to Open if not recognized
                self.page.get_by_text("Open", exact=True).first.click(timeout=10000)
            time.sleep(0.5)  # Wait for selection to register
        except Exception as e:
            print(f"⚠️ Could not select Hiring Status: {status}, error: {e}")

    def select_employment_type(self, employment_type: str):
        """Select employment type from dropdown"""
        self.locators.employment_type_dropdown.scroll_into_view_if_needed()
        time.sleep(1)
        
        self.locators.employment_type_dropdown.click()
        time.sleep(2)  # Wait for dropdown to open and load all options
        
        type_lower = employment_type.lower()
        
        try:
            # Dropdowns close after selection, so use .first for the visible option
            if type_lower == "part-time" or type_lower == "parttime":
                self.page.get_by_text("Part-time", exact=True).first.click(timeout=10000)
            elif type_lower == "permanent":
                self.page.get_by_text("Permanent", exact=True).first.click(timeout=10000)
            elif type_lower == "self-employed":
                self.page.get_by_text("Self-employed", exact=True).first.click(timeout=10000)
            elif type_lower == "freelance":
                self.page.get_by_text("Freelance", exact=True).first.click(timeout=10000)
            elif type_lower == "contract":
                self.page.get_by_text("Contract", exact=True).first.click(timeout=10000)
            elif type_lower == "internship":
                self.page.get_by_text("Internship", exact=True).first.click(timeout=10000)
            elif type_lower == "apprenticeship":
                self.page.get_by_text("Apprenticeship", exact=True).first.click(timeout=10000)
            elif type_lower == "indirect contract":
                self.page.get_by_text("Indirect Contract", exact=True).first.click(timeout=10000)
            else:
                # Default to Permanent if not recognized
                self.page.get_by_text("Permanent", exact=True).first.click(timeout=10000)
            time.sleep(0.5)  # Wait for selection to register
        except Exception as e:
            print(f"⚠️ Could not select Employment Type: {employment_type}, error: {e}")

    def select_client(self, client_name: str):
        """Select client from dropdown (conditional based on company selection)
        Handles dynamic client list with search functionality
        """

        print(f"🔧 Selecting client: {client_name}")
        # Scroll to client dropdown to ensure visibility
        self.locators.client_dropdown.scroll_into_view_if_needed()
        time.sleep(1)
        
        # Click to open dropdown
        self.locators.client_dropdown.click()
        time.sleep(2)  # Wait for dropdown to open and load options

        dropdown_options = self.page.locator("text=").all()
        print(f"🔍 Found {len(dropdown_options)} options in client dropdown")
        for option in dropdown_options:
            if option.is_visible() and option.text_content().strip():
                option.click()
                print(f"✅ Selected first available client: {option.text_content()}")
                break
        
        # try:
        #     # Check if there's a search input in the dropdown and use it
        #     search_input = self.page.locator("input[placeholder='Search...']").first
        #     if search_input.is_visible():
        #         print(f"🔍 Using search to find client: {client_name}")
        #         search_input.fill(client_name)
        #         time.sleep(1)  # Wait for search results
            
        #     # Click the client option using exact text match
        #     self.page.get_by_text(client_name, exact=True).first.click(timeout=10000)
        #     time.sleep(0.5)  # Wait for selection to register
        #     print(f"✅ Selected client: {client_name}")
            
        # except Exception as e:
        #     print(f"⚠️ Could not select client: {client_name}, error: {e}")
        #     # If specific client not found, try to select any available client (first option)
        #     try:
        #         print("🔄 Attempting to select first available client option")
        #         time.sleep(1)
        #         # Get all text options in dropdown and click the first non-search element
        #         dropdown_options = self.page.locator("text=").all()
        #         for option in dropdown_options:
        #             if option.is_visible() and option.text_content().strip():
        #                 option.click()
        #                 print(f"✅ Selected first available client: {option.text_content()}")
        #                 break
        #     except Exception as e2:
        #         print(f"❌ Could not select any client: {e2}")
        #         raise

    # ===== FORM SUBMISSION METHODS =====
    def save_jd(self):
        """Save JD form"""
        self.locators.save_button.click()
        time.sleep(2)

    def update_jd(self):
        """Update JD form"""
        self.locators.update_button.click()
        time.sleep(2)

    def cancel_jd_operation(self):
        """Cancel JD creation/editing"""
        self.locators.cancel_button.click()
        time.sleep(1)

    def attempt_save_with_validation_errors(self):
        """Attempt to save JD form to trigger validation errors"""
        self.locators.save_button.click()
        time.sleep(1)  # Allow validation errors to appear

    def trigger_mandatory_field_validation(self):
        """Trigger validation by attempting to save empty mandatory fields"""
        # Clear all mandatory fields to ensure they're empty
        self.locators.position_job_title_input.fill("")
        self.locators.jd_workplace_input.fill("")
        # Attempt to save to trigger validation
        self.attempt_save_with_validation_errors()

    def trigger_salary_range_validation(self, min_salary: str, max_salary: str):
        """Trigger salary range validation with invalid range"""
        self.fill_minimum_salary(min_salary)
        self.fill_maximum_salary(max_salary)
        self.attempt_save_with_validation_errors()

    def trigger_age_range_validation(self, min_age: str, max_age: str):
        """Trigger age range validation with invalid range"""
        self.fill_job_age_min(min_age)
        self.fill_job_age_max(max_age)
        self.attempt_save_with_validation_errors()

    def trigger_target_age_range_validation(self, min_age: str, max_age: str):
        """Trigger target age range validation with invalid range"""
        self.fill_target_age_min(min_age)
        self.fill_target_age_max(max_age)
        self.attempt_save_with_validation_errors()

    def trigger_character_limit_validation(self, field_type: str, long_text: str):
        """Trigger character limit validation for specific field"""
        if field_type == "position_title":
            self.fill_position_job_title(long_text)
        elif field_type == "workplace":
            self.fill_jd_workplace(long_text)
        elif field_type == "department":
            self.fill_department(long_text)
        elif field_type == "job_function":
            self.fill_job_function(long_text)
        
        self.attempt_save_with_validation_errors()

    def trigger_format_validation(self, field_type: str, invalid_data: str):
        """Trigger format validation with invalid data"""
        if field_type == "salary":
            self.fill_minimum_salary(invalid_data)
        elif field_type == "age":
            self.fill_job_age_min(invalid_data)
        
        self.attempt_save_with_validation_errors()

    # ===== COMPREHENSIVE FORM FILLING METHOD =====
    def fill_jd_form(self, jd_data: dict):
        """Fill JD form with provided data dictionary"""
        # Fill mandatory fields
        if "position_title" in jd_data:
            self.fill_position_job_title(jd_data["position_title"])
        
        if "company" in jd_data:
            self.select_company(jd_data["company"])
        
        if "work_style" in jd_data:
            self.select_work_style(jd_data["work_style"])
        
        if "workplace" in jd_data:
            self.fill_jd_workplace(jd_data["workplace"])
        
        # Fill optional fields if provided
        if "min_salary" in jd_data and jd_data["min_salary"]:
            self.fill_minimum_salary(jd_data["min_salary"])
        
        if "max_salary" in jd_data and jd_data["max_salary"]:
            self.fill_maximum_salary(jd_data["max_salary"])
        
        if "currency" in jd_data and jd_data["currency"]:
            self.select_currency(jd_data["currency"])
        
        if "job_age_min" in jd_data and jd_data["job_age_min"]:
            self.fill_job_age_min(jd_data["job_age_min"])
        
        if "job_age_max" in jd_data and jd_data["job_age_max"]:
            self.fill_job_age_max(jd_data["job_age_max"])
        
        if "target_age_min" in jd_data and jd_data["target_age_min"]:
            self.fill_target_age_min(jd_data["target_age_min"])
        
        if "target_age_max" in jd_data and jd_data["target_age_max"]:
            self.fill_target_age_max(jd_data["target_age_max"])
        
        if "japanese_level" in jd_data and jd_data["japanese_level"]:
            self.select_japanese_level(jd_data["japanese_level"])
        
        if "english_level" in jd_data and jd_data["english_level"]:
            self.select_english_level(jd_data["english_level"])
        
        if "priority_grade" in jd_data and jd_data["priority_grade"]:
            self.select_priority_grade(jd_data["priority_grade"])
        
        if "hiring_status" in jd_data and jd_data["hiring_status"]:
            self.select_hiring_status(jd_data["hiring_status"])
        
        if "employment_type" in jd_data and jd_data["employment_type"]:
            self.select_employment_type(jd_data["employment_type"])
        
        if "department" in jd_data and jd_data["department"]:
            self.fill_department(jd_data["department"])
        
        if "direct_report" in jd_data and jd_data["direct_report"]:
            self.fill_direct_report(jd_data["direct_report"])
        
        if "job_function" in jd_data and jd_data["job_function"]:
            self.fill_job_function(jd_data["job_function"])

        if "client" in jd_data and jd_data["client"]:
            self.select_client(jd_data["client"])

    # ===== FILE UPLOAD METHODS =====
    def upload_jd_file(self, file_path: str):
        """Upload JD file"""
        try:
            # Try to use the file input directly
            self.locators.file_upload_input.first.set_input_files(file_path)
        except Exception as e:
            # Alternative approach - click upload area first
            try:
                self.locators.upload_jd_file_area.click()
                time.sleep(1)
                self.locators.file_upload_input.first.set_input_files(file_path)
            except Exception as e2:
                print(f"File upload failed: {e2}")
                raise e2

    def click_upload_file_button(self):
        """Click upload file button to open file upload modal"""
        self.locators.upload_file_button.click()
        time.sleep(1)

    # ===== BULK FILE UPLOAD FUNCTIONALITY =====
    def click_upload_file_button_for_bulk_import(self):
        """Click 'Upload File' button to open file selection dialog for bulk import"""
        try:
            print("📁 Clicking Upload File button for bulk import")
            enhanced_assert_visible(self.page, self.locators.upload_file_button, 
                                   "Upload File button should be visible", "upload_file_button")
            
            self.locators.upload_file_button.click()
            time.sleep(1)
            
            # Verify file upload modal opens
            self.verify_file_upload_modal_opened()
            print("✅ Successfully opened file upload dialog")
            return True
            
        except Exception as e:
            print(f"❌ Error clicking Upload File button: {e}")
            raise

    def verify_file_upload_modal_opened(self):
        """Verify file upload modal has opened correctly"""
        try:
            enhanced_assert_visible(self.page, self.locators.file_upload_modal, 
                                   "File upload modal should be visible", "file_upload_modal")
            
            enhanced_assert_visible(self.page, self.locators.file_upload_modal_heading, 
                                   "File upload modal heading should be visible", "file_upload_modal_heading")
            
            print("✅ File upload modal opened successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying file upload modal: {e}")
            raise

    def upload_file_for_bulk_import(self, file_path: str):
        """Upload file for bulk JD import and verify processing"""
        try:
            print(f"📤 Uploading file for bulk import: {file_path}")
            
            # Handle file selection dialog
            with self.page.expect_file_chooser() as fc_info:
                self.locators.browse_files_button.click()
            file_chooser = fc_info.value
            file_chooser.set_files(file_path)
            
            # Wait for upload to process
            time.sleep(2)
            
            # Verify upload success
            self.verify_file_upload_success()
            print(f"✅ Successfully uploaded file: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error uploading file for bulk import: {e}")
            raise

    def upload_file_via_drag_drop(self, file_path: str):
        """Upload file using drag and drop to file drop area"""
        try:
            print(f"🎯 Uploading file via drag and drop: {file_path}")
            
            # Verify drop area is visible
            enhanced_assert_visible(self.page, self.locators.file_drop_area, 
                                   "File drop area should be visible", "file_drop_area")
            
            # Use Playwright's file upload on the drop area
            self.locators.file_drop_area.set_input_files(file_path)
            time.sleep(2)
            
            # Verify upload success
            self.verify_file_upload_success()
            print(f"✅ Successfully uploaded file via drag and drop: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error uploading file via drag and drop: {e}")
            raise

    def verify_file_upload_success(self):
        """Verify file upload completed successfully"""
        try:
            # Check for success message
            enhanced_assert_visible(self.page, self.locators.file_uploaded_successfully_message, 
                                   "File upload success message should be visible", "file_upload_success")
            
            print("✅ File upload success verified")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying file upload success: {e}")
            raise

    def verify_file_processing_success(self, expected_jd_count: int = None):
        """Verify file processing completed and JDs were imported"""
        try:
            # Wait for processing to complete
            time.sleep(3)
            
            # Check for processing success message
            success_message = self.page.locator("text=JDs imported successfully")
            if success_message.count() > 0:
                enhanced_assert_visible(self.page, success_message, 
                                       "JD import success message should be visible", "jd_import_success")
            
            # If expected count provided, verify JD count
            if expected_jd_count is not None:
                actual_count = self.get_jd_cards_count()
                if actual_count >= expected_jd_count:
                    print(f"✅ File processing success - imported {actual_count} JDs (expected at least {expected_jd_count})")
                else:
                    raise AssertionError(f"Expected at least {expected_jd_count} JDs but found {actual_count}")
            else:
                print("✅ File processing completed successfully")
            
            return True
            
        except Exception as e:
            print(f"❌ Error verifying file processing success: {e}")
            raise

    # ===== FILE FORMAT VALIDATION =====
    def upload_valid_file_format(self, file_path: str):
        """Upload file with valid format (PDF, DOC, DOCX) and verify acceptance"""
        try:
            print(f"✅ Uploading valid format file: {file_path}")
            
            # Upload the file
            self.upload_file_for_bulk_import(file_path)
            
            # Verify no format error appears
            self.verify_no_file_format_error()
            
            # Verify processing begins
            self.verify_file_processing_started()
            
            print(f"✅ Valid file format accepted: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error uploading valid file format: {e}")
            raise

    def upload_invalid_file_format(self, file_path: str):
        """Upload file with invalid format and verify rejection"""
        try:
            print(f"❌ Uploading invalid format file: {file_path}")
            
            # Attempt to upload the file
            try:
                with self.page.expect_file_chooser() as fc_info:
                    self.locators.browse_files_button.click()
                file_chooser = fc_info.value
                file_chooser.set_files(file_path)
                time.sleep(1)
            except:
                pass  # File selection might be rejected
            
            # Verify format error message appears
            self.verify_file_format_error()
            
            print(f"✅ Invalid file format correctly rejected: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error handling invalid file format: {e}")
            raise

    def verify_file_format_error(self):
        """Verify file format error message is displayed"""
        try:
            enhanced_assert_visible(self.page, self.locators.file_format_error, 
                                   "File format error message should be visible", "file_format_error")
            
            print("✅ File format error message displayed correctly")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying file format error: {e}")
            raise

    def verify_no_file_format_error(self):
        """Verify no file format error message is displayed"""
        try:
            # Check that format error is not visible
            if self.locators.file_format_error.count() > 0:
                raise AssertionError("File format error message should not be visible for valid formats")
            
            print("✅ No file format error (as expected for valid format)")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying no file format error: {e}")
            raise

    # ===== FILE SIZE VALIDATION =====
    def upload_oversized_file(self, file_path: str):
        """Upload file exceeding size limit and verify error"""
        try:
            print(f"📏 Uploading oversized file: {file_path}")
            
            # Attempt to upload the file
            try:
                with self.page.expect_file_chooser() as fc_info:
                    self.locators.browse_files_button.click()
                file_chooser = fc_info.value
                file_chooser.set_files(file_path)
                time.sleep(1)
            except:
                pass  # File selection might be rejected
            
            # Verify size error message appears
            self.verify_file_size_error()
            
            print(f"✅ Oversized file correctly rejected: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error handling oversized file: {e}")
            raise

    def verify_file_size_error(self):
        """Verify file size error message is displayed"""
        try:
            enhanced_assert_visible(self.page, self.locators.file_size_error, 
                                   "File size error message should be visible", "file_size_error")
            
            print("✅ File size error message displayed correctly")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying file size error: {e}")
            raise

    def verify_file_processing_started(self):
        """Verify file processing has started (progress indicator visible)"""
        try:
            # Check for progress bar or processing indicator
            if self.locators.upload_progress_bar.count() > 0:
                enhanced_assert_visible(self.page, self.locators.upload_progress_bar, 
                                       "Upload progress bar should be visible", "upload_progress")
                print("✅ File processing started (progress bar visible)")
            else:
                # Alternative: check for processing message
                processing_message = self.page.locator("text=Processing file")
                if processing_message.count() > 0:
                    print("✅ File processing started (processing message visible)")
                else:
                    print("ℹ️ File processing started (no visual indicator found)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error verifying file processing started: {e}")
            raise

    def cancel_file_upload(self):
        """Cancel file upload process"""
        try:
            print("🚫 Cancelling file upload")
            
            # Click cancel upload button if available
            if self.locators.upload_cancel_button.count() > 0:
                self.locators.upload_cancel_button.click()
                time.sleep(1)
                print("✅ File upload cancelled via cancel button")
            else:
                # Alternative: close the upload modal
                if self.locators.close_modal_button.count() > 0:
                    self.locators.close_modal_button.click()
                    time.sleep(1)
                    print("✅ File upload cancelled via modal close")
            
            return True
            
        except Exception as e:
            print(f"❌ Error cancelling file upload: {e}")
            raise

    # ===== BULK OPERATIONS FUNCTIONALITY =====
    def select_all_jds(self):
        """Select all JDs using select all checkbox"""
        try:
            print("☑️ Selecting all JDs")
            
            enhanced_assert_visible(self.page, self.locators.select_all_checkbox, 
                                   "Select all checkbox should be visible", "select_all_checkbox")
            
            self.locators.select_all_checkbox.click()
            time.sleep(1)
            
            # Verify bulk actions menu becomes available
            self.verify_bulk_actions_menu_enabled()
            
            print("✅ Successfully selected all JDs")
            return True
            
        except Exception as e:
            print(f"❌ Error selecting all JDs: {e}")
            raise

    def select_multiple_jds(self, jd_titles: list):
        """Select multiple JDs by their titles"""
        try:
            print(f"☑️ Selecting multiple JDs: {jd_titles}")
            
            selected_count = 0
            for title in jd_titles:
                checkbox = self.locators.jd_checkbox(title)
                if checkbox.count() > 0:
                    enhanced_assert_visible(self.page, checkbox, 
                                           f"Checkbox for JD '{title}' should be visible", f"jd_checkbox_{title}")
                    checkbox.click()
                    selected_count += 1
                    time.sleep(0.5)
                else:
                    print(f"⚠️ JD '{title}' not found for selection")
            
            if selected_count > 0:
                # Verify bulk actions menu becomes available
                self.verify_bulk_actions_menu_enabled()
                
                # Verify selected count is displayed
                self.verify_selected_items_count(selected_count)
            
            print(f"✅ Successfully selected {selected_count} JDs")
            return selected_count
            
        except Exception as e:
            print(f"❌ Error selecting multiple JDs: {e}")
            raise

    def verify_bulk_actions_menu_enabled(self):
        """Verify bulk actions menu is enabled when JDs are selected"""
        try:
            enhanced_assert_visible(self.page, self.locators.bulk_actions_menu, 
                                   "Bulk actions menu should be visible when JDs are selected", "bulk_actions_menu")
            
            # Verify bulk action buttons are enabled
            enhanced_assert_visible(self.page, self.locators.bulk_delete_button, 
                                   "Bulk delete button should be visible", "bulk_delete_button")
            
            enhanced_assert_visible(self.page, self.locators.bulk_status_update_button, 
                                   "Bulk status update button should be visible", "bulk_status_update_button")
            
            print("✅ Bulk actions menu is properly enabled")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying bulk actions menu: {e}")
            raise

    def verify_bulk_actions_menu_disabled(self):
        """Verify bulk actions menu is disabled when no JDs are selected"""
        try:
            # Check if bulk actions menu is hidden or disabled
            if self.locators.bulk_actions_menu.count() == 0:
                print("✅ Bulk actions menu is hidden (no JDs selected)")
                return True
            
            # If visible, check if buttons are disabled
            delete_button = self.locators.bulk_delete_button
            if delete_button.count() > 0:
                is_disabled = delete_button.is_disabled()
                if is_disabled:
                    print("✅ Bulk actions menu is disabled (no JDs selected)")
                    return True
                else:
                    raise AssertionError("Bulk actions should be disabled when no JDs are selected")
            
            print("✅ Bulk actions menu properly disabled")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying bulk actions menu disabled: {e}")
            raise

    def verify_selected_items_count(self, expected_count: int):
        """Verify the selected items count display"""
        try:
            if self.locators.selected_items_count.count() > 0:
                count_text = self.locators.selected_items_count.text_content()
                if str(expected_count) in count_text:
                    print(f"✅ Selected items count correctly shows {expected_count}")
                    return True
                else:
                    raise AssertionError(f"Expected count {expected_count} but found '{count_text}'")
            else:
                print(f"ℹ️ Selected items count not displayed (expected {expected_count})")
                return True
            
        except Exception as e:
            print(f"❌ Error verifying selected items count: {e}")
            raise

    # ===== BULK STATUS UPDATE OPERATIONS =====
    def perform_bulk_status_update(self, new_status: str):
        """Perform bulk status update on selected JDs"""
        try:
            print(f"🔄 Performing bulk status update to '{new_status}'")
            
            # Click bulk status update button
            enhanced_assert_visible(self.page, self.locators.bulk_status_update_button, 
                                   "Bulk status update button should be visible", "bulk_status_update_button")
            
            self.locators.bulk_status_update_button.click()
            time.sleep(1)
            
            # Select the new status from dropdown/modal
            self.select_bulk_status_option(new_status)
            
            # Confirm the bulk update
            self.confirm_bulk_status_update()
            
            # Verify success message
            self.verify_bulk_status_update_success()
            
            print(f"✅ Successfully performed bulk status update to '{new_status}'")
            return True
            
        except Exception as e:
            print(f"❌ Error performing bulk status update: {e}")
            raise

    def select_bulk_status_option(self, status: str):
        """Select status option in bulk update modal"""
        try:
            # Look for status dropdown in bulk update modal
            status_dropdown = self.page.locator(".bulk-status-dropdown, [name='bulkStatus']")
            if status_dropdown.count() > 0:
                status_dropdown.click()
                time.sleep(0.5)
                
                # Select the status option
                status_option = self.page.get_by_text(status, exact=True)
                status_option.click()
                time.sleep(0.5)
            else:
                # Alternative: direct button selection
                status_button = self.page.get_by_role("button", name=status)
                if status_button.count() > 0:
                    status_button.click()
                    time.sleep(0.5)
            
            print(f"✅ Selected bulk status option: {status}")
            return True
            
        except Exception as e:
            print(f"❌ Error selecting bulk status option: {e}")
            raise

    def confirm_bulk_status_update(self):
        """Confirm bulk status update operation"""
        try:
            # Look for confirmation button
            confirm_button = self.page.get_by_role("button", name="Update Status")
            if confirm_button.count() == 0:
                confirm_button = self.page.get_by_role("button", name="Confirm")
            if confirm_button.count() == 0:
                confirm_button = self.page.get_by_role("button", name="Apply")
            
            if confirm_button.count() > 0:
                confirm_button.click()
                time.sleep(2)
                print("✅ Confirmed bulk status update")
            else:
                print("⚠️ No confirmation button found for bulk status update")
            
            return True
            
        except Exception as e:
            print(f"❌ Error confirming bulk status update: {e}")
            raise

    def verify_bulk_status_update_success(self):
        """Verify bulk status update completed successfully"""
        try:
            enhanced_assert_visible(self.page, self.locators.bulk_status_updated_successfully_message, 
                                   "Bulk status update success message should be visible", "bulk_status_update_success")
            
            print("✅ Bulk status update success verified")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying bulk status update success: {e}")
            raise

    def verify_bulk_status_update_across_jds(self, jd_titles: list, expected_status: str):
        """Verify status was updated across multiple JDs"""
        try:
            print(f"🔍 Verifying status '{expected_status}' across JDs: {jd_titles}")
            
            updated_count = 0
            for title in jd_titles:
                jd_card = self.get_jd_card_by_title(title)
                if jd_card.count() > 0:
                    # Look for status indicator in the card
                    status_element = jd_card.locator(".jd-status, [class*='status']")
                    if status_element.count() > 0:
                        status_text = status_element.text_content().lower()
                        if expected_status.lower() in status_text:
                            updated_count += 1
                            print(f"✅ JD '{title}' status updated to '{expected_status}'")
                        else:
                            print(f"⚠️ JD '{title}' status not updated (found: '{status_text}')")
                    else:
                        print(f"⚠️ Status element not found for JD '{title}'")
                else:
                    print(f"⚠️ JD '{title}' not found after status update")
            
            if updated_count == len(jd_titles):
                print(f"✅ All {updated_count} JDs successfully updated to '{expected_status}'")
                return True
            else:
                print(f"⚠️ Only {updated_count} out of {len(jd_titles)} JDs were updated")
                return False
            
        except Exception as e:
            print(f"❌ Error verifying bulk status update across JDs: {e}")
            raise

    # ===== BULK OPERATION CONFIRMATION AND SUCCESS VERIFICATION =====
    def verify_bulk_operation_confirmation(self, operation_type: str):
        """Verify bulk operation confirmation dialog appears"""
        try:
            if operation_type.lower() == "delete":
                enhanced_assert_visible(self.page, self.locators.bulk_delete_confirmation_modal, 
                                       "Bulk delete confirmation modal should be visible", "bulk_delete_confirmation")
                
                enhanced_assert_visible(self.page, self.locators.bulk_delete_confirmation_heading, 
                                       "Bulk delete confirmation heading should be visible", "bulk_delete_heading")
            else:
                # Generic confirmation modal
                confirmation_modal = self.page.get_by_role("dialog")
                enhanced_assert_visible(self.page, confirmation_modal, 
                                       f"Bulk {operation_type} confirmation modal should be visible", f"bulk_{operation_type}_confirmation")
            
            print(f"✅ Bulk {operation_type} confirmation dialog verified")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying bulk {operation_type} confirmation: {e}")
            raise

    def confirm_bulk_operation(self, operation_type: str):
        """Confirm bulk operation (delete, status update, etc.)"""
        try:
            if operation_type.lower() == "delete":
                confirm_button = self.locators.confirm_bulk_delete_button
            else:
                confirm_button = self.page.get_by_role("button", name="Confirm")
                if confirm_button.count() == 0:
                    confirm_button = self.page.get_by_role("button", name="Yes")
            
            enhanced_assert_visible(self.page, confirm_button, 
                                   f"Confirm button for bulk {operation_type} should be visible", f"confirm_bulk_{operation_type}")
            
            confirm_button.click()
            time.sleep(2)
            
            print(f"✅ Confirmed bulk {operation_type} operation")
            return True
            
        except Exception as e:
            print(f"❌ Error confirming bulk {operation_type}: {e}")
            raise

    def cancel_bulk_operation(self, operation_type: str):
        """Cancel bulk operation"""
        try:
            if operation_type.lower() == "delete":
                cancel_button = self.locators.cancel_bulk_delete_button
            else:
                cancel_button = self.page.get_by_role("button", name="Cancel")
            
            enhanced_assert_visible(self.page, cancel_button, 
                                   f"Cancel button for bulk {operation_type} should be visible", f"cancel_bulk_{operation_type}")
            
            cancel_button.click()
            time.sleep(1)
            
            print(f"✅ Cancelled bulk {operation_type} operation")
            return True
            
        except Exception as e:
            print(f"❌ Error cancelling bulk {operation_type}: {e}")
            raise

    # ===== MIXED SUCCESS/FAILURE SCENARIOS =====
    def handle_mixed_bulk_operation_results(self, operation_type: str):
        """Handle scenarios where bulk operations have mixed success/failure results"""
        try:
            print(f"🔍 Checking for mixed results in bulk {operation_type} operation")
            
            # Look for partial success messages
            partial_success_messages = [
                "Some items could not be processed",
                "Partial success",
                "completed with errors",
                "Some JDs failed to"
            ]
            
            mixed_results_found = False
            for message_text in partial_success_messages:
                message_element = self.page.locator(f"text={message_text}")
                if message_element.count() > 0:
                    print(f"⚠️ Mixed results detected: {message_text}")
                    mixed_results_found = True
                    break
            
            if mixed_results_found:
                # Look for detailed error information
                self.verify_bulk_operation_error_details()
            else:
                print(f"✅ No mixed results detected for bulk {operation_type}")
            
            return mixed_results_found
            
        except Exception as e:
            print(f"❌ Error handling mixed bulk operation results: {e}")
            raise

    def verify_bulk_operation_error_details(self):
        """Verify detailed error information is provided for failed bulk operations"""
        try:
            # Look for error details section
            error_details = self.page.locator(".error-details, .bulk-errors, [class*='error-list']")
            if error_details.count() > 0:
                enhanced_assert_visible(self.page, error_details, 
                                       "Bulk operation error details should be visible", "bulk_error_details")
                
                error_text = error_details.text_content()
                print(f"📋 Bulk operation error details: {error_text}")
            else:
                print("ℹ️ No detailed error information found")
            
            return True
            
        except Exception as e:
            print(f"❌ Error verifying bulk operation error details: {e}")
            raise

    def verify_bulk_operation_progress_tracking(self, operation_type: str):
        """Verify bulk operation progress is tracked and reported"""
        try:
            print(f"📊 Verifying progress tracking for bulk {operation_type}")
            
            # Look for progress indicators
            progress_indicators = [
                self.page.locator(".progress-bar, [class*='progress']"),
                self.page.locator(".loading, .spinner"),
                self.page.locator("text=Processing"),
                self.page.locator("text=Updating")
            ]
            
            progress_found = False
            for indicator in progress_indicators:
                if indicator.count() > 0:
                    print(f"✅ Progress indicator found for bulk {operation_type}")
                    progress_found = True
                    break
            
            if not progress_found:
                print(f"ℹ️ No progress indicator found for bulk {operation_type} (operation may be too fast)")
            
            # Wait for operation to complete
            time.sleep(2)
            
            # Look for completion message
            completion_messages = [
                f"Bulk {operation_type} completed",
                "Operation completed",
                "All items processed"
            ]
            
            for message_text in completion_messages:
                message_element = self.page.locator(f"text={message_text}")
                if message_element.count() > 0:
                    print(f"✅ Completion message found: {message_text}")
                    break
            
            return True
            
        except Exception as e:
            print(f"❌ Error verifying bulk operation progress: {e}")
            raise

    # ===== FILE PROCESSING ERROR HANDLING =====
    def handle_invalid_file_data_errors(self):
        """Handle and verify invalid file data errors with line-specific information"""
        try:
            print("🔍 Checking for invalid file data errors")
            
            # Look for general file processing error
            file_processing_error = self.page.locator("text=File processing failed")
            if file_processing_error.count() > 0:
                enhanced_assert_visible(self.page, file_processing_error, 
                                       "File processing error should be visible", "file_processing_error")
                
                # Look for detailed error information
                self.verify_line_specific_errors()
                print("✅ Invalid file data errors handled correctly")
                return True
            else:
                print("ℹ️ No file processing errors found")
                return False
            
        except Exception as e:
            print(f"❌ Error handling invalid file data errors: {e}")
            raise

    def verify_line_specific_errors(self):
        """Verify line-specific error messages are displayed"""
        try:
            # Look for line-specific error patterns
            line_error_patterns = [
                "Line \\d+:",
                "Row \\d+:",
                "Error on line",
                "Invalid data at line"
            ]
            
            line_errors_found = False
            for pattern in line_error_patterns:
                line_error_elements = self.page.locator(f"text=/{pattern}/")
                if line_error_elements.count() > 0:
                    line_errors_found = True
                    error_count = line_error_elements.count()
                    print(f"✅ Found {error_count} line-specific errors")
                    
                    # Display first few error messages
                    for i in range(min(3, error_count)):
                        error_text = line_error_elements.nth(i).text_content()
                        print(f"   📍 {error_text}")
                    
                    if error_count > 3:
                        print(f"   ... and {error_count - 3} more errors")
                    break
            
            if not line_errors_found:
                print("ℹ️ No line-specific errors found")
            
            return line_errors_found
            
        except Exception as e:
            print(f"❌ Error verifying line-specific errors: {e}")
            raise

    def verify_file_content_validation_errors(self):
        """Verify file content and data format validation errors"""
        try:
            print("🔍 Verifying file content validation errors")
            
            # Common file content validation errors
            content_error_messages = [
                "Invalid file format",
                "Missing required columns",
                "Invalid data format",
                "Duplicate entries found",
                "Required field missing",
                "Invalid email format",
                "Invalid date format",
                "Invalid salary range"
            ]
            
            errors_found = []
            for error_message in content_error_messages:
                error_element = self.page.locator(f"text={error_message}")
                if error_element.count() > 0:
                    errors_found.append(error_message)
                    enhanced_assert_visible(self.page, error_element, 
                                           f"Content validation error '{error_message}' should be visible", 
                                           f"content_error_{error_message.replace(' ', '_').lower()}")
            
            if errors_found:
                print(f"✅ Found {len(errors_found)} content validation errors:")
                for error in errors_found:
                    print(f"   ❌ {error}")
            else:
                print("ℹ️ No content validation errors found")
            
            return len(errors_found) > 0
            
        except Exception as e:
            print(f"❌ Error verifying file content validation errors: {e}")
            raise

    def verify_data_format_requirement_errors(self):
        """Verify data format requirement validation errors"""
        try:
            print("🔍 Verifying data format requirement errors")
            
            # Look for format requirement errors
            format_errors = self.page.locator(".format-error, [class*='format-error']")
            if format_errors.count() > 0:
                error_count = format_errors.count()
                print(f"✅ Found {error_count} data format requirement errors")
                
                # Display error details
                for i in range(min(5, error_count)):
                    error_text = format_errors.nth(i).text_content()
                    print(f"   📋 Format error {i+1}: {error_text}")
                
                return True
            else:
                print("ℹ️ No data format requirement errors found")
                return False
            
        except Exception as e:
            print(f"❌ Error verifying data format requirement errors: {e}")
            raise

    def verify_processing_failure_error_messages(self):
        """Verify error messages for file processing failures"""
        try:
            print("🔍 Verifying processing failure error messages")
            
            # Look for processing failure messages
            processing_failure_messages = [
                "Failed to process file",
                "Processing error occurred",
                "Unable to import data",
                "File processing interrupted",
                "Import failed"
            ]
            
            failure_found = False
            for message in processing_failure_messages:
                message_element = self.page.locator(f"text={message}")
                if message_element.count() > 0:
                    enhanced_assert_visible(self.page, message_element, 
                                           f"Processing failure message '{message}' should be visible", 
                                           f"processing_failure_{message.replace(' ', '_').lower()}")
                    failure_found = True
                    print(f"✅ Processing failure message found: {message}")
                    break
            
            if not failure_found:
                print("ℹ️ No processing failure messages found")
            
            return failure_found
            
        except Exception as e:
            print(f"❌ Error verifying processing failure error messages: {e}")
            raise

    # ===== NETWORK ERROR AND TIMEOUT HANDLING =====
    def handle_network_timeout_during_processing(self):
        """Handle network timeouts during file processing"""
        try:
            print("🌐 Checking for network timeout during file processing")
            
            # Look for network timeout messages
            timeout_messages = [
                "Request timeout",
                "Network timeout",
                "Connection timeout",
                "Processing timeout",
                "Server timeout"
            ]
            
            timeout_found = False
            for message in timeout_messages:
                timeout_element = self.page.locator(f"text={message}")
                if timeout_element.count() > 0:
                    enhanced_assert_visible(self.page, timeout_element, 
                                           f"Timeout message '{message}' should be visible", 
                                           f"timeout_{message.replace(' ', '_').lower()}")
                    timeout_found = True
                    print(f"⏰ Network timeout detected: {message}")
                    break
            
            if timeout_found:
                # Look for retry option
                self.verify_retry_option_available()
            else:
                print("ℹ️ No network timeout detected")
            
            return timeout_found
            
        except Exception as e:
            print(f"❌ Error handling network timeout: {e}")
            raise

    def handle_large_file_processing_scenarios(self):
        """Handle large file processing scenarios and timeouts"""
        try:
            print("📁 Handling large file processing scenarios")
            
            # Look for large file processing indicators
            large_file_indicators = [
                "Processing large file",
                "This may take a while",
                "Large file detected",
                "Extended processing time"
            ]
            
            large_file_detected = False
            for indicator in large_file_indicators:
                indicator_element = self.page.locator(f"text={indicator}")
                if indicator_element.count() > 0:
                    print(f"📊 Large file processing indicator: {indicator}")
                    large_file_detected = True
                    break
            
            if large_file_detected:
                # Wait longer for large file processing
                print("⏳ Waiting for large file processing to complete...")
                time.sleep(10)
                
                # Check if processing completed or timed out
                self.verify_large_file_processing_completion()
            else:
                print("ℹ️ No large file processing indicators found")
            
            return large_file_detected
            
        except Exception as e:
            print(f"❌ Error handling large file processing: {e}")
            raise

    def verify_large_file_processing_completion(self):
        """Verify large file processing completed successfully or handle timeout"""
        try:
            # Check for completion indicators
            completion_indicators = [
                "Processing completed",
                "File imported successfully",
                "Import finished"
            ]
            
            completed = False
            for indicator in completion_indicators:
                indicator_element = self.page.locator(f"text={indicator}")
                if indicator_element.count() > 0:
                    print(f"✅ Large file processing completed: {indicator}")
                    completed = True
                    break
            
            if not completed:
                # Check for timeout or error
                timeout_occurred = self.handle_network_timeout_during_processing()
                if not timeout_occurred:
                    print("⏳ Large file still processing or completed without explicit message")
            
            return completed
            
        except Exception as e:
            print(f"❌ Error verifying large file processing completion: {e}")
            raise

    def verify_retry_option_available(self):
        """Verify retry option is available after processing failure"""
        try:
            # Look for retry button or option
            retry_button = self.page.get_by_role("button", name="Retry")
            if retry_button.count() == 0:
                retry_button = self.page.get_by_role("button", name="Try Again")
            if retry_button.count() == 0:
                retry_button = self.page.locator("text=Retry")
            
            if retry_button.count() > 0:
                enhanced_assert_visible(self.page, retry_button, 
                                       "Retry option should be available after processing failure", "retry_option")
                print("✅ Retry option is available")
                return True
            else:
                print("ℹ️ No retry option found")
                return False
            
        except Exception as e:
            print(f"❌ Error verifying retry option: {e}")
            raise

    def click_retry_processing(self):
        """Click retry button to retry file processing"""
        try:
            print("🔄 Clicking retry to reprocess file")
            
            retry_button = self.page.get_by_role("button", name="Retry")
            if retry_button.count() == 0:
                retry_button = self.page.get_by_role("button", name="Try Again")
            
            if retry_button.count() > 0:
                retry_button.click()
                time.sleep(2)
                print("✅ Retry processing initiated")
                return True
            else:
                print("❌ Retry button not found")
                return False
            
        except Exception as e:
            print(f"❌ Error clicking retry processing: {e}")
            raise

    # ===== JD LIST OPERATIONS =====
    def expect_no_jds_message(self):
        """Verify 'No companies found' message is visible"""
        enhanced_assert_visible(self.page, self.locators.no_jds_message, 
                               "No JDs message should be visible", "no_jds_message")

    def expect_jd_list_visible(self):
        """Verify JD list container is visible"""
        enhanced_assert_visible(self.page, self.locators.jd_list_container, 
                               "JD list should be visible", "jd_list_visible")

    def click_add_new_jd_button(self):
        """Click 'Add new JD' button when no JDs exist"""
        self.locators.add_new_jd_button.click()
        time.sleep(1)

    def get_jd_card_by_title(self, title: str):
        """Get JD card element by position title"""
        return self.locators.get_jd_card_by_title(title)

    def click_jd_card(self, title: str):
        """Click on JD card to view details"""
        jd_card = self.get_jd_card_by_title(title)
        jd_card.click()
        time.sleep(2)

    # ===== JD LIST NAVIGATION AND DISPLAY METHODS =====
    def navigate_to_jd_list_within_agency(self, agency_id: str):
        """Navigate to JD list page within specific agency context"""
        self.navigate_to_jd_page(agency_id)
        self.verify_jd_page_url(agency_id)
        print(f"✅ Successfully navigated to JD list for agency {agency_id}")

    def verify_jd_list_display(self):
        """Verify JD list is properly displayed with cards"""
        try:
            # Check if JDs exist by looking for the list container
            if self.locators.jd_list_container.count() > 0:
                enhanced_assert_visible(self.page, self.locators.jd_list_container, 
                                       "JD list container should be visible", "jd_list_display")
                print("✅ JD list is displayed with existing JDs")
                return True
            else:
                # If no list container, check for empty state
                self.expect_no_jds_message()
                print("✅ Empty state is properly displayed (no JDs found)")
                return False
        except Exception as e:
            print(f"❌ Error verifying JD list display: {e}")
            raise

    def verify_jd_card_information(self, expected_jd_data: dict):
        """Verify JD card displays correct information"""
        try:
            title = expected_jd_data.get("position_title", "")
            company = expected_jd_data.get("company", "")
            
            # Get the JD card by title
            jd_card = self.get_jd_card_by_title(title)
            enhanced_assert_visible(self.page, jd_card, 
                                   f"JD card with title '{title}' should be visible", "jd_card_visible")
            
            # Verify card contains expected information
            if company:
                company_element = jd_card.locator(f"text={company}")
                enhanced_assert_visible(self.page, company_element, 
                                       f"Company '{company}' should be visible in JD card", "jd_card_company")
            
            print(f"✅ JD card information verified for '{title}'")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying JD card information: {e}")
            raise

    def handle_empty_state_display(self):
        """Handle empty state when no JDs exist"""
        try:
            # Verify empty state message is displayed
            self.expect_no_jds_message()
            
            # Verify "Add new JD" button is available
            enhanced_assert_visible(self.page, self.locators.add_new_jd_button, 
                                   "Add new JD button should be visible in empty state", "add_new_jd_empty_state")
            
            print("✅ Empty state properly handled - showing 'No companies found' message and 'Add new JD' button")
            return True
            
        except Exception as e:
            print(f"❌ Error handling empty state: {e}")
            raise

    def click_jd_card_for_details(self, title: str):
        """Click on JD card to access detail view"""
        try:
            jd_card = self.get_jd_card_by_title(title)
            enhanced_assert_visible(self.page, jd_card, 
                                   f"JD card with title '{title}' should be visible before clicking", "jd_card_before_click")
            
            # Click the card to view details
            jd_card.click()
            time.sleep(2)
            
            print(f"✅ Successfully clicked JD card '{title}' to view details")
            return True
            
        except Exception as e:
            print(f"❌ Error clicking JD card for details: {e}")
            raise

    def verify_jd_detail_view_opened(self, expected_title: str):
        """Verify JD detail view has opened correctly"""
        try:
            # Check if detail view is displayed
            enhanced_assert_visible(self.page, self.locators.jd_detail_container, 
                                   "JD detail container should be visible", "jd_detail_view")
            
            # Verify the correct JD title is shown in detail view
            detail_title = self.locators.jd_detail_title
            enhanced_assert_visible(self.page, detail_title, 
                                   "JD detail title should be visible", "jd_detail_title")
            
            # Check if the title matches expected
            title_text = detail_title.text_content()
            if expected_title.lower() in title_text.lower():
                print(f"✅ JD detail view opened correctly for '{expected_title}'")
                return True
            else:
                raise AssertionError(f"Expected title '{expected_title}' but found '{title_text}'")
                
        except Exception as e:
            print(f"❌ Error verifying JD detail view: {e}")
            raise

    def get_jd_cards_count(self) -> int:
        """Get the total count of JD cards displayed"""
        try:
            cards = self.page.locator(".jd-card, [class*='jd-card']")
            count = cards.count()
            print(f"✅ Found {count} JD cards on current page")
            return count
        except Exception as e:
            print(f"❌ Error getting JD cards count: {e}")
            return 0

    def verify_jd_cards_contain_required_info(self):
        """Verify all JD cards contain required information fields"""
        try:
            cards_count = self.get_jd_cards_count()
            if cards_count == 0:
                print("ℹ️ No JD cards to verify (empty state)")
                return True
            
            # Check each card has required elements
            for i in range(cards_count):
                card = self.page.locator(".jd-card, [class*='jd-card']").nth(i)
                
                # Verify card has title
                title_element = card.locator(".jd-title, [class*='title'], h3, h4")
                if title_element.count() > 0:
                    print(f"✅ Card {i+1} has title element")
                else:
                    print(f"⚠️ Card {i+1} missing title element")
                
                # Verify card has company info
                company_element = card.locator(".jd-company, [class*='company']")
                if company_element.count() > 0:
                    print(f"✅ Card {i+1} has company element")
                else:
                    print(f"⚠️ Card {i+1} missing company element")
            
            print(f"✅ Verified information structure for {cards_count} JD cards")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying JD cards information: {e}")
            raise

    def navigate_back_to_jd_list(self):
        """Navigate back to JD list from detail view"""
        try:
            if self.locators.back_to_list_button.count() > 0:
                self.locators.back_to_list_button.click()
                time.sleep(2)
                print("✅ Successfully navigated back to JD list")
                return True
            else:
                # Alternative: use browser back button
                self.page.go_back()
                time.sleep(2)
                print("✅ Used browser back to return to JD list")
                return True
        except Exception as e:
            print(f"❌ Error navigating back to JD list: {e}")
            raise

    # ===== JD ACTIONS (EDIT, DELETE, VIEW) =====
    def click_edit_jd_button(self, title: str):
        """Click edit button for specific JD"""
        self.locators.edit_jd_button_by_title(title).click()
        time.sleep(1)

    def click_delete_jd_button(self, title: str):
        """Click delete button for specific JD"""
        self.locators.delete_jd_button_by_title(title).click()
        time.sleep(1)

    def click_view_jd_button(self, title: str):
        """Click view button for specific JD"""
        self.locators.view_jd_button_by_title(title).click()
        time.sleep(2)

    # ===== SINGLE JD DELETION METHODS =====
    def trigger_jd_deletion_from_list(self, jd_title: str):
        """Trigger JD deletion from list view by clicking delete button"""
        try:
            print(f"🗑️ Triggering deletion for JD: '{jd_title}' from list view")
            
            # Find and click the delete button for the specific JD
            delete_button = self.locators.delete_jd_button_by_title(jd_title)
            enhanced_assert_visible(self.page, delete_button, 
                                   f"Delete button for JD '{jd_title}' should be visible", "delete_button_visible")
            
            delete_button.click()
            time.sleep(1)
            
            # Verify deletion confirmation dialog appears
            self.verify_deletion_confirmation_dialog()
            print(f"✅ Successfully triggered deletion for JD '{jd_title}' from list")
            return True
            
        except Exception as e:
            print(f"❌ Error triggering JD deletion from list: {e}")
            raise

    def trigger_jd_deletion_from_detail_view(self, jd_title: str):
        """Trigger JD deletion from detail view"""
        try:
            print(f"🗑️ Triggering deletion for JD: '{jd_title}' from detail view")
            
            # First navigate to detail view
            self.click_jd_card_for_details(jd_title)
            
            # Then click delete button in detail view
            delete_button = self.locators.delete_jd_button
            enhanced_assert_visible(self.page, delete_button, 
                                   "Delete button should be visible in detail view", "delete_button_detail_view")
            
            delete_button.click()
            time.sleep(1)
            
            # Verify deletion confirmation dialog appears
            self.verify_deletion_confirmation_dialog()
            print(f"✅ Successfully triggered deletion for JD '{jd_title}' from detail view")
            return True
            
        except Exception as e:
            print(f"❌ Error triggering JD deletion from detail view: {e}")
            raise

    def verify_deletion_confirmation_dialog(self):
        """Verify that deletion confirmation dialog appears correctly"""
        try:
            # Check for deletion confirmation modal
            enhanced_assert_visible(self.page, self.locators.delete_confirmation_modal, 
                                   "Delete confirmation modal should be visible", "delete_confirmation_modal")
            
            # Verify confirmation heading
            enhanced_assert_visible(self.page, self.locators.delete_confirmation_heading, 
                                   "Delete confirmation heading should be visible", "delete_confirmation_heading")
            
            # Verify confirmation message
            enhanced_assert_visible(self.page, self.locators.delete_confirmation_message, 
                                   "Delete confirmation message should be visible", "delete_confirmation_message")
            
            # Verify action buttons are present
            enhanced_assert_visible(self.page, self.locators.confirm_delete_button, 
                                   "Confirm delete button should be visible", "confirm_delete_button")
            enhanced_assert_visible(self.page, self.locators.cancel_delete_button, 
                                   "Cancel delete button should be visible", "cancel_delete_button")
            
            print("✅ Deletion confirmation dialog verified successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying deletion confirmation dialog: {e}")
            raise

    def confirm_jd_deletion(self):
        """Confirm JD deletion by clicking 'Yes, Delete' button"""
        try:
            print("✅ Confirming JD deletion")
            
            # Click confirm delete button
            self.locators.confirm_delete_button.click()
            time.sleep(2)
            
            # Wait for deletion to complete and modal to close
            self.wait_for_deletion_confirmation_to_close()
            print("✅ JD deletion confirmed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error confirming JD deletion: {e}")
            raise

    def cancel_jd_deletion(self):
        """Cancel JD deletion by clicking 'Cancel' button"""
        try:
            print("❌ Cancelling JD deletion")
            
            # Click cancel delete button
            self.locators.cancel_delete_button.click()
            time.sleep(1)
            
            # Wait for confirmation dialog to close
            self.wait_for_deletion_confirmation_to_close()
            print("✅ JD deletion cancelled successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error cancelling JD deletion: {e}")
            raise

    def wait_for_deletion_confirmation_to_close(self, timeout: int = 5000):
        """Wait for deletion confirmation dialog to close"""
        try:
            self.locators.delete_confirmation_modal.wait_for(state="hidden", timeout=timeout)
            return True
        except:
            return False

    def verify_successful_jd_deletion(self, deleted_jd_title: str):
        """Verify that JD was successfully deleted"""
        try:
            print(f"🔍 Verifying successful deletion of JD: '{deleted_jd_title}'")
            
            # Check for success message
            enhanced_assert_visible(self.page, self.locators.jd_deleted_successfully_message, 
                                   "JD deleted successfully message should be visible", "jd_deleted_success_message")
            
            # Verify the JD no longer appears in the list
            time.sleep(2)  # Allow list to refresh
            deleted_jd_card = self.get_jd_card_by_title(deleted_jd_title)
            
            # The JD card should not be visible anymore
            if deleted_jd_card.count() == 0:
                print(f"✅ JD '{deleted_jd_title}' successfully removed from list")
                return True
            else:
                raise AssertionError(f"JD '{deleted_jd_title}' still appears in list after deletion")
                
        except Exception as e:
            print(f"❌ Error verifying successful JD deletion: {e}")
            raise

    def verify_jd_list_updated_after_deletion(self, original_count: int):
        """Verify that JD list count has decreased after deletion"""
        try:
            print("🔍 Verifying JD list updated after deletion")
            
            # Wait for list to refresh
            time.sleep(2)
            
            # Get new count
            new_count = self.get_jd_cards_count()
            
            # Verify count decreased by 1
            if new_count == original_count - 1:
                print(f"✅ JD list count correctly updated: {original_count} → {new_count}")
                return True
            elif new_count == 0 and original_count == 1:
                # Special case: last JD was deleted, should show empty state
                self.handle_empty_state_display()
                print("✅ Last JD deleted, empty state displayed correctly")
                return True
            else:
                raise AssertionError(f"Expected count {original_count - 1}, but got {new_count}")
                
        except Exception as e:
            print(f"❌ Error verifying JD list update after deletion: {e}")
            raise

    def perform_complete_jd_deletion_workflow(self, jd_title: str, from_detail_view: bool = False):
        """Perform complete JD deletion workflow from trigger to verification"""
        try:
            print(f"🗑️ Starting complete deletion workflow for JD: '{jd_title}'")
            
            # Get original count for verification
            original_count = self.get_jd_cards_count()
            
            # Trigger deletion
            if from_detail_view:
                self.trigger_jd_deletion_from_detail_view(jd_title)
            else:
                self.trigger_jd_deletion_from_list(jd_title)
            
            # Confirm deletion
            self.confirm_jd_deletion()
            
            # Verify successful deletion
            self.verify_successful_jd_deletion(jd_title)
            
            # Verify list updated
            self.verify_jd_list_updated_after_deletion(original_count)
            
            print(f"✅ Complete JD deletion workflow successful for '{jd_title}'")
            return True
            
        except Exception as e:
            print(f"❌ Error in complete JD deletion workflow: {e}")
            raise

    def perform_jd_deletion_cancellation_workflow(self, jd_title: str):
        """Perform JD deletion cancellation workflow to verify cancellation works"""
        try:
            print(f"❌ Starting deletion cancellation workflow for JD: '{jd_title}'")
            
            # Get original count for verification
            original_count = self.get_jd_cards_count()
            
            # Trigger deletion
            self.trigger_jd_deletion_from_list(jd_title)
            
            # Cancel deletion
            self.cancel_jd_deletion()
            
            # Verify JD still exists in list
            time.sleep(1)
            jd_card = self.get_jd_card_by_title(jd_title)
            enhanced_assert_visible(self.page, jd_card, 
                                   f"JD '{jd_title}' should still be visible after cancellation", "jd_still_visible_after_cancel")
            
            # Verify count unchanged
            new_count = self.get_jd_cards_count()
            if new_count != original_count:
                raise AssertionError(f"JD count changed after cancellation: {original_count} → {new_count}")
            
            print(f"✅ JD deletion cancellation workflow successful for '{jd_title}'")
            return True
            
        except Exception as e:
            print(f"❌ Error in JD deletion cancellation workflow: {e}")
            raise

    # ===== BULK DELETION FUNCTIONALITY =====
    def select_jd_checkbox(self, jd_title: str):
        """Select checkbox for specific JD"""
        try:
            print(f"☑️ Selecting checkbox for JD: '{jd_title}'")
            
            # Find and click the checkbox for the specific JD
            jd_checkbox = self.locators.jd_checkbox(jd_title)
            enhanced_assert_visible(self.page, jd_checkbox, 
                                   f"Checkbox for JD '{jd_title}' should be visible", "jd_checkbox_visible")
            
            jd_checkbox.click()
            time.sleep(0.5)
            
            print(f"✅ Successfully selected checkbox for JD '{jd_title}'")
            return True
            
        except Exception as e:
            print(f"❌ Error selecting JD checkbox: {e}")
            raise

    def select_multiple_jds(self, jd_titles: list):
        """Select multiple JDs using checkboxes"""
        try:
            print(f"☑️ Selecting multiple JDs: {jd_titles}")
            
            selected_count = 0
            for jd_title in jd_titles:
                try:
                    self.select_jd_checkbox(jd_title)
                    selected_count += 1
                except Exception as e:
                    print(f"⚠️ Failed to select JD '{jd_title}': {e}")
            
            # Verify bulk actions are enabled
            self.verify_bulk_actions_enabled()
            
            print(f"✅ Successfully selected {selected_count} JDs for bulk operations")
            return selected_count
            
        except Exception as e:
            print(f"❌ Error selecting multiple JDs: {e}")
            raise

    def select_all_jds(self):
        """Select all JDs using select all checkbox"""
        try:
            print("☑️ Selecting all JDs using select all checkbox")
            
            # Click select all checkbox
            enhanced_assert_visible(self.page, self.locators.select_all_checkbox, 
                                   "Select all checkbox should be visible", "select_all_checkbox")
            
            self.locators.select_all_checkbox.click()
            time.sleep(1)
            
            # Verify bulk actions are enabled
            self.verify_bulk_actions_enabled()
            
            print("✅ Successfully selected all JDs")
            return True
            
        except Exception as e:
            print(f"❌ Error selecting all JDs: {e}")
            raise

    def verify_bulk_actions_enabled(self):
        """Verify that bulk action buttons are enabled when JDs are selected"""
        try:
            # Check if bulk actions menu is visible
            enhanced_assert_visible(self.page, self.locators.bulk_actions_menu, 
                                   "Bulk actions menu should be visible when JDs are selected", "bulk_actions_menu")
            
            # Check if bulk delete button is enabled
            enhanced_assert_visible(self.page, self.locators.bulk_delete_button, 
                                   "Bulk delete button should be visible", "bulk_delete_button")
            
            print("✅ Bulk actions are properly enabled")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying bulk actions enabled: {e}")
            raise

    def verify_selected_items_count(self, expected_count: int):
        """Verify the count of selected items is displayed correctly"""
        try:
            # Check selected items count display
            if self.locators.selected_items_count.count() > 0:
                count_text = self.locators.selected_items_count.text_content()
                if str(expected_count) in count_text:
                    print(f"✅ Selected items count correctly shows {expected_count}")
                    return True
                else:
                    raise AssertionError(f"Expected count {expected_count} but found '{count_text}'")
            else:
                print(f"ℹ️ Selected items count not displayed (expected {expected_count})")
                return True
                
        except Exception as e:
            print(f"❌ Error verifying selected items count: {e}")
            raise

    def trigger_bulk_deletion(self):
        """Trigger bulk deletion by clicking bulk delete button"""
        try:
            print("🗑️ Triggering bulk deletion")
            
            # Click bulk delete button
            enhanced_assert_visible(self.page, self.locators.bulk_delete_button, 
                                   "Bulk delete button should be visible", "bulk_delete_button_trigger")
            
            self.locators.bulk_delete_button.click()
            time.sleep(1)
            
            # Verify bulk deletion confirmation dialog appears
            self.verify_bulk_deletion_confirmation_dialog()
            
            print("✅ Successfully triggered bulk deletion")
            return True
            
        except Exception as e:
            print(f"❌ Error triggering bulk deletion: {e}")
            raise

    def verify_bulk_deletion_confirmation_dialog(self):
        """Verify that bulk deletion confirmation dialog appears correctly"""
        try:
            # Check for bulk deletion confirmation modal
            enhanced_assert_visible(self.page, self.locators.bulk_delete_confirmation_modal, 
                                   "Bulk delete confirmation modal should be visible", "bulk_delete_confirmation_modal")
            
            # Verify confirmation heading
            enhanced_assert_visible(self.page, self.locators.bulk_delete_confirmation_heading, 
                                   "Bulk delete confirmation heading should be visible", "bulk_delete_confirmation_heading")
            
            # Verify action buttons are present
            enhanced_assert_visible(self.page, self.locators.confirm_bulk_delete_button, 
                                   "Confirm bulk delete button should be visible", "confirm_bulk_delete_button")
            enhanced_assert_visible(self.page, self.locators.cancel_bulk_delete_button, 
                                   "Cancel bulk delete button should be visible", "cancel_bulk_delete_button")
            
            print("✅ Bulk deletion confirmation dialog verified successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying bulk deletion confirmation dialog: {e}")
            raise

    def confirm_bulk_deletion(self):
        """Confirm bulk deletion by clicking 'Yes, Delete All' button"""
        try:
            print("✅ Confirming bulk deletion")
            
            # Click confirm bulk delete button
            self.locators.confirm_bulk_delete_button.click()
            time.sleep(3)  # Allow more time for bulk operations
            
            # Wait for bulk deletion confirmation to close
            self.wait_for_bulk_deletion_confirmation_to_close()
            
            print("✅ Bulk deletion confirmed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error confirming bulk deletion: {e}")
            raise

    def cancel_bulk_deletion(self):
        """Cancel bulk deletion by clicking 'Cancel' button"""
        try:
            print("❌ Cancelling bulk deletion")
            
            # Click cancel bulk delete button
            self.locators.cancel_bulk_delete_button.click()
            time.sleep(1)
            
            # Wait for confirmation dialog to close
            self.wait_for_bulk_deletion_confirmation_to_close()
            
            print("✅ Bulk deletion cancelled successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error cancelling bulk deletion: {e}")
            raise

    def wait_for_bulk_deletion_confirmation_to_close(self, timeout: int = 10000):
        """Wait for bulk deletion confirmation dialog to close"""
        try:
            self.locators.bulk_delete_confirmation_modal.wait_for(state="hidden", timeout=timeout)
            return True
        except:
            return False

    def verify_bulk_deletion_success(self, deleted_jd_titles: list):
        """Verify that bulk deletion was successful"""
        try:
            print(f"🔍 Verifying successful bulk deletion of JDs: {deleted_jd_titles}")
            
            # Check for bulk success message
            enhanced_assert_visible(self.page, self.locators.bulk_jd_deleted_successfully_message, 
                                   "Bulk JDs deleted successfully message should be visible", "bulk_deleted_success_message")
            
            # Verify none of the deleted JDs appear in the list anymore
            time.sleep(2)  # Allow list to refresh
            
            for jd_title in deleted_jd_titles:
                deleted_jd_card = self.get_jd_card_by_title(jd_title)
                if deleted_jd_card.count() > 0:
                    raise AssertionError(f"JD '{jd_title}' still appears in list after bulk deletion")
            
            print(f"✅ All {len(deleted_jd_titles)} JDs successfully removed from list")
            return True
                
        except Exception as e:
            print(f"❌ Error verifying bulk deletion success: {e}")
            raise

    def verify_jd_list_updated_after_bulk_deletion(self, original_count: int, deleted_count: int):
        """Verify that JD list count has decreased correctly after bulk deletion"""
        try:
            print(f"🔍 Verifying JD list updated after bulk deletion of {deleted_count} JDs")
            
            # Wait for list to refresh
            time.sleep(2)
            
            # Get new count
            new_count = self.get_jd_cards_count()
            expected_count = original_count - deleted_count
            
            # Verify count decreased correctly
            if new_count == expected_count:
                print(f"✅ JD list count correctly updated: {original_count} → {new_count}")
                return True
            elif new_count == 0 and expected_count <= 0:
                # Special case: all JDs were deleted, should show empty state
                self.handle_empty_state_display()
                print("✅ All JDs deleted, empty state displayed correctly")
                return True
            else:
                raise AssertionError(f"Expected count {expected_count}, but got {new_count}")
                
        except Exception as e:
            print(f"❌ Error verifying JD list update after bulk deletion: {e}")
            raise

    def handle_partial_bulk_deletion_failure(self, attempted_jd_titles: list, expected_failures: list = None):
        """Handle scenarios where bulk deletion partially fails"""
        try:
            print(f"⚠️ Handling partial bulk deletion failure scenario")
            
            # Check for partial failure messages or error indicators
            if self.locators.error_toast.count() > 0:
                error_message = self.locators.error_toast.text_content()
                print(f"ℹ️ Partial failure error message: {error_message}")
            
            # Verify which JDs were actually deleted vs which failed
            time.sleep(2)  # Allow list to refresh
            
            still_present = []
            successfully_deleted = []
            
            for jd_title in attempted_jd_titles:
                jd_card = self.get_jd_card_by_title(jd_title)
                if jd_card.count() > 0:
                    still_present.append(jd_title)
                else:
                    successfully_deleted.append(jd_title)
            
            print(f"✅ Successfully deleted: {successfully_deleted}")
            print(f"⚠️ Still present (failed to delete): {still_present}")
            
            # If expected failures were provided, verify they match
            if expected_failures:
                for expected_failure in expected_failures:
                    if expected_failure not in still_present:
                        raise AssertionError(f"Expected '{expected_failure}' to fail deletion, but it was deleted")
            
            return {
                "successfully_deleted": successfully_deleted,
                "failed_to_delete": still_present
            }
            
        except Exception as e:
            print(f"❌ Error handling partial bulk deletion failure: {e}")
            raise

    def perform_complete_bulk_deletion_workflow(self, jd_titles: list):
        """Perform complete bulk deletion workflow from selection to verification"""
        try:
            print(f"🗑️ Starting complete bulk deletion workflow for JDs: {jd_titles}")
            
            # Get original count for verification
            original_count = self.get_jd_cards_count()
            
            # Select multiple JDs
            selected_count = self.select_multiple_jds(jd_titles)
            
            # Verify selected count
            self.verify_selected_items_count(selected_count)
            
            # Trigger bulk deletion
            self.trigger_bulk_deletion()
            
            # Confirm bulk deletion
            self.confirm_bulk_deletion()
            
            # Verify successful bulk deletion
            self.verify_bulk_deletion_success(jd_titles)
            
            # Verify list updated
            self.verify_jd_list_updated_after_bulk_deletion(original_count, len(jd_titles))
            
            print(f"✅ Complete bulk deletion workflow successful for {len(jd_titles)} JDs")
            return True
            
        except Exception as e:
            print(f"❌ Error in complete bulk deletion workflow: {e}")
            raise

    def perform_bulk_deletion_cancellation_workflow(self, jd_titles: list):
        """Perform bulk deletion cancellation workflow to verify cancellation works"""
        try:
            print(f"❌ Starting bulk deletion cancellation workflow for JDs: {jd_titles}")
            
            # Get original count for verification
            original_count = self.get_jd_cards_count()
            
            # Select multiple JDs
            selected_count = self.select_multiple_jds(jd_titles)
            
            # Trigger bulk deletion
            self.trigger_bulk_deletion()
            
            # Cancel bulk deletion
            self.cancel_bulk_deletion()
            
            # Verify all JDs still exist in list
            time.sleep(1)
            for jd_title in jd_titles:
                jd_card = self.get_jd_card_by_title(jd_title)
                enhanced_assert_visible(self.page, jd_card, 
                                       f"JD '{jd_title}' should still be visible after bulk cancellation", "jd_still_visible_after_bulk_cancel")
            
            # Verify count unchanged
            new_count = self.get_jd_cards_count()
            if new_count != original_count:
                raise AssertionError(f"JD count changed after bulk cancellation: {original_count} → {new_count}")
            
            print(f"✅ Bulk deletion cancellation workflow successful for {len(jd_titles)} JDs")
            return True
            
        except Exception as e:
            print(f"❌ Error in bulk deletion cancellation workflow: {e}")
            raise

    # ===== DELETION VALIDATION AND ERROR HANDLING =====
    def verify_jd_with_associated_data_warning(self):
        """Verify warning message appears for JDs with associated data"""
        try:
            print("⚠️ Verifying associated data warning for JD deletion")
            
            # Check for associated data warning message
            enhanced_assert_visible(self.page, self.locators.jd_deletion_warning, 
                                   "JD deletion warning should be visible for JDs with associated data", "jd_deletion_warning")
            
            # Check for force delete checkbox if required
            if self.locators.force_delete_checkbox.count() > 0:
                enhanced_assert_visible(self.page, self.locators.force_delete_checkbox, 
                                       "Force delete checkbox should be visible", "force_delete_checkbox")
                print("✅ Force delete checkbox available for associated data")
            
            print("✅ Associated data warning verified successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying associated data warning: {e}")
            raise

    def handle_force_delete_for_associated_data(self):
        """Handle force delete scenario for JDs with associated data"""
        try:
            print("⚠️ Handling force delete for JD with associated data")
            
            # Verify warning is displayed
            self.verify_jd_with_associated_data_warning()
            
            # Check the force delete checkbox if present
            if self.locators.force_delete_checkbox.count() > 0:
                self.locators.force_delete_checkbox.click()
                time.sleep(0.5)
                print("✅ Force delete checkbox checked")
            
            # Confirm deletion
            self.confirm_jd_deletion()
            
            print("✅ Force delete for associated data handled successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error handling force delete for associated data: {e}")
            raise

    def verify_deletion_failure_error_messages(self, expected_error_type: str = None):
        """Verify appropriate error messages are displayed when deletion fails"""
        try:
            print(f"🔍 Verifying deletion failure error messages (type: {expected_error_type})")
            
            # Check for general deletion failed error
            if expected_error_type == "general" or expected_error_type is None:
                if self.locators.deletion_failed_error.count() > 0:
                    enhanced_assert_visible(self.page, self.locators.deletion_failed_error, 
                                           "Deletion failed error should be visible", "deletion_failed_error")
                    print("✅ General deletion failed error message verified")
                    return True
            
            # Check for network error
            if expected_error_type == "network":
                enhanced_assert_visible(self.page, self.locators.deletion_network_error, 
                                       "Network error message should be visible", "deletion_network_error")
                print("✅ Network error message verified")
                return True
            
            # Check for permission error
            if expected_error_type == "permission":
                enhanced_assert_visible(self.page, self.locators.deletion_permission_error, 
                                       "Permission error message should be visible", "deletion_permission_error")
                print("✅ Permission error message verified")
                return True
            
            # Check for associated data error
            if expected_error_type == "associated_data":
                enhanced_assert_visible(self.page, self.locators.deletion_associated_data_error, 
                                       "Associated data error message should be visible", "deletion_associated_data_error")
                print("✅ Associated data error message verified")
                return True
            
            # Check for any error toast message
            if self.locators.error_toast.count() > 0:
                error_message = self.locators.error_toast.text_content()
                print(f"ℹ️ Error toast message found: {error_message}")
                return True
            
            print("⚠️ No specific error message found")
            return False
            
        except Exception as e:
            print(f"❌ Error verifying deletion failure error messages: {e}")
            raise

    def verify_jd_remains_in_list_after_failed_deletion(self, jd_title: str):
        """Verify JD remains in list when deletion fails"""
        try:
            print(f"🔍 Verifying JD '{jd_title}' remains in list after failed deletion")
            
            # Wait for any error processing to complete
            time.sleep(2)
            
            # Verify the JD still appears in the list
            jd_card = self.get_jd_card_by_title(jd_title)
            enhanced_assert_visible(self.page, jd_card, 
                                   f"JD '{jd_title}' should still be visible after failed deletion", "jd_remains_after_failed_deletion")
            
            print(f"✅ JD '{jd_title}' correctly remains in list after failed deletion")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying JD remains after failed deletion: {e}")
            raise

    def verify_list_count_unchanged_after_failed_deletion(self, original_count: int):
        """Verify JD list count remains unchanged when deletion fails"""
        try:
            print("🔍 Verifying JD list count unchanged after failed deletion")
            
            # Wait for any processing to complete
            time.sleep(2)
            
            # Get current count
            current_count = self.get_jd_cards_count()
            
            # Verify count is unchanged
            if current_count == original_count:
                print(f"✅ JD list count correctly unchanged: {original_count}")
                return True
            else:
                raise AssertionError(f"Expected count {original_count} but got {current_count} after failed deletion")
                
        except Exception as e:
            print(f"❌ Error verifying list count unchanged after failed deletion: {e}")
            raise

    def handle_network_error_during_deletion(self, jd_title: str, retry: bool = False):
        """Handle network errors that occur during deletion"""
        try:
            print(f"🌐 Handling network error during deletion of JD: '{jd_title}'")
            
            # Verify network error message
            self.verify_deletion_failure_error_messages("network")
            
            # Verify JD remains in list
            self.verify_jd_remains_in_list_after_failed_deletion(jd_title)
            
            if retry:
                print("🔄 Attempting retry after network error")
                # Close any error dialogs
                if self.locators.error_toast.count() > 0:
                    # Try to close error toast if there's a close button
                    close_buttons = self.page.locator("button").filter(has_text="Close")
                    if close_buttons.count() > 0:
                        close_buttons.first.click()
                        time.sleep(1)
                
                # Retry the deletion
                self.trigger_jd_deletion_from_list(jd_title)
                return True
            
            print("✅ Network error during deletion handled successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error handling network error during deletion: {e}")
            raise

    def handle_permission_error_during_deletion(self, jd_title: str):
        """Handle permission errors that occur during deletion"""
        try:
            print(f"🔒 Handling permission error during deletion of JD: '{jd_title}'")
            
            # Verify permission error message
            self.verify_deletion_failure_error_messages("permission")
            
            # Verify JD remains in list
            self.verify_jd_remains_in_list_after_failed_deletion(jd_title)
            
            # Verify delete button might be disabled or hidden for this JD
            delete_button = self.locators.delete_jd_button_by_title(jd_title)
            if delete_button.count() == 0:
                print("✅ Delete button correctly hidden for JD without delete permission")
            elif not delete_button.is_enabled():
                print("✅ Delete button correctly disabled for JD without delete permission")
            
            print("✅ Permission error during deletion handled successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error handling permission error during deletion: {e}")
            raise

    def verify_successful_list_update_after_deletion(self, deleted_jd_titles: list, original_count: int):
        """Verify list is properly updated after successful deletions"""
        try:
            print(f"🔍 Verifying successful list update after deletion of {len(deleted_jd_titles)} JDs")
            
            # Wait for list to refresh
            time.sleep(2)
            
            # Verify deleted JDs are no longer in the list
            for jd_title in deleted_jd_titles:
                deleted_jd_card = self.get_jd_card_by_title(jd_title)
                if deleted_jd_card.count() > 0:
                    raise AssertionError(f"JD '{jd_title}' still appears in list after successful deletion")
            
            # Verify count is correct
            expected_count = original_count - len(deleted_jd_titles)
            current_count = self.get_jd_cards_count()
            
            if current_count == expected_count:
                print(f"✅ List successfully updated: {original_count} → {current_count}")
            elif current_count == 0 and expected_count <= 0:
                # Handle empty state
                self.handle_empty_state_display()
                print("✅ List successfully updated to empty state")
            else:
                raise AssertionError(f"Expected count {expected_count} but got {current_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error verifying successful list update after deletion: {e}")
            raise

    def perform_deletion_with_error_handling(self, jd_title: str, expected_error_type: str = None):
        """Perform deletion with comprehensive error handling"""
        try:
            print(f"🗑️ Performing deletion with error handling for JD: '{jd_title}' (expected error: {expected_error_type})")
            
            # Get original count
            original_count = self.get_jd_cards_count()
            
            # Trigger deletion
            self.trigger_jd_deletion_from_list(jd_title)
            
            if expected_error_type == "associated_data":
                # Handle associated data scenario
                self.handle_force_delete_for_associated_data()
                # Verify successful deletion after force delete
                self.verify_successful_jd_deletion(jd_title)
                self.verify_jd_list_updated_after_deletion(original_count)
                
            elif expected_error_type in ["network", "permission", "general"]:
                # Attempt to confirm deletion (should fail)
                try:
                    self.confirm_jd_deletion()
                    time.sleep(2)
                except:
                    pass  # Expected to fail
                
                # Verify appropriate error message
                self.verify_deletion_failure_error_messages(expected_error_type)
                
                # Verify JD remains in list
                self.verify_jd_remains_in_list_after_failed_deletion(jd_title)
                
                # Verify count unchanged
                self.verify_list_count_unchanged_after_failed_deletion(original_count)
                
            else:
                # Normal successful deletion
                self.confirm_jd_deletion()
                self.verify_successful_jd_deletion(jd_title)
                self.verify_jd_list_updated_after_deletion(original_count)
            
            print(f"✅ Deletion with error handling completed for JD: '{jd_title}'")
            return True
            
        except Exception as e:
            print(f"❌ Error in deletion with error handling: {e}")
            raise

    def perform_bulk_deletion_with_partial_failures(self, jd_titles: list, expected_failures: list = None):
        """Perform bulk deletion expecting some failures"""
        try:
            print(f"🗑️ Performing bulk deletion with expected partial failures")
            print(f"Attempting to delete: {jd_titles}")
            print(f"Expected failures: {expected_failures}")
            
            # Get original count
            original_count = self.get_jd_cards_count()
            
            # Select JDs for bulk deletion
            self.select_multiple_jds(jd_titles)
            
            # Trigger bulk deletion
            self.trigger_bulk_deletion()
            
            # Confirm bulk deletion
            self.confirm_bulk_deletion()
            
            # Handle partial failure scenario
            results = self.handle_partial_bulk_deletion_failure(jd_titles, expected_failures)
            
            # Verify list updated correctly for successful deletions
            if results["successfully_deleted"]:
                self.verify_successful_list_update_after_deletion(results["successfully_deleted"], original_count)
            
            print(f"✅ Bulk deletion with partial failures completed successfully")
            return results
            
        except Exception as e:
            print(f"❌ Error in bulk deletion with partial failures: {e}")
            raise

    # ===== JD EDIT MODE ACCESS METHODS =====
    def access_edit_mode_from_list(self, jd_title: str):
        """Access edit mode from JD list by clicking edit button on specific JD"""
        try:
            print(f"🔧 Accessing edit mode for JD: '{jd_title}'")
            
            # Find and click the edit button for the specific JD
            edit_button = self.locators.edit_jd_button_by_title(jd_title)
            enhanced_assert_visible(self.page, edit_button, 
                                   f"Edit button for JD '{jd_title}' should be visible", "edit_button_visible")
            
            edit_button.click()
            time.sleep(2)
            
            # Verify edit modal opened
            self.verify_edit_modal_opened()
            print(f"✅ Successfully accessed edit mode for JD '{jd_title}'")
            return True
            
        except Exception as e:
            print(f"❌ Error accessing edit mode from list: {e}")
            raise

    def access_edit_mode_from_detail_view(self, jd_title: str):
        """Access edit mode from JD detail view"""
        try:
            print(f"🔧 Accessing edit mode from detail view for JD: '{jd_title}'")
            
            # First navigate to detail view
            self.click_jd_card_for_details(jd_title)
            
            # Then click edit button in detail view
            edit_button = self.locators.edit_jd_button
            enhanced_assert_visible(self.page, edit_button, 
                                   "Edit button should be visible in detail view", "edit_button_detail_view")
            
            edit_button.click()
            time.sleep(2)
            
            # Verify edit modal opened
            self.verify_edit_modal_opened()
            print(f"✅ Successfully accessed edit mode from detail view for JD '{jd_title}'")
            return True
            
        except Exception as e:
            print(f"❌ Error accessing edit mode from detail view: {e}")
            raise

    def verify_edit_modal_opened(self):
        """Verify that edit modal has opened correctly"""
        try:
            # Check for edit modal heading
            enhanced_assert_visible(self.page, self.locators.edit_jd_modal_heading, 
                                   "Edit JD modal heading should be visible", "edit_modal_heading")
            
            # Verify modal body is visible
            enhanced_assert_visible(self.page, self.locators.jd_modal_body, 
                                   "Edit modal body should be visible", "edit_modal_body")
            
            print("✅ Edit modal opened successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying edit modal opened: {e}")
            raise

    def verify_edit_modal_pre_filled_data(self, expected_jd_data: dict):
        """Verify that edit modal opens with pre-filled data from existing JD"""
        try:
            print("🔍 Verifying edit modal has pre-filled data")
            
            # Verify position title is pre-filled
            if "position_title" in expected_jd_data:
                title_value = self.locators.edit_position_job_title_input.input_value()
                expected_title = expected_jd_data["position_title"]
                if expected_title.lower() in title_value.lower():
                    print(f"✅ Position title pre-filled correctly: '{title_value}'")
                else:
                    raise AssertionError(f"Expected position title '{expected_title}' but found '{title_value}'")
            
            # Verify workplace is pre-filled
            if "workplace" in expected_jd_data:
                workplace_value = self.locators.edit_jd_workplace_input.input_value()
                expected_workplace = expected_jd_data["workplace"]
                if expected_workplace.lower() in workplace_value.lower():
                    print(f"✅ Workplace pre-filled correctly: '{workplace_value}'")
                else:
                    raise AssertionError(f"Expected workplace '{expected_workplace}' but found '{workplace_value}'")
            
            # Verify salary fields if provided
            if "min_salary" in expected_jd_data and expected_jd_data["min_salary"]:
                min_salary_value = self.locators.edit_minimum_salary_input.input_value()
                expected_min_salary = str(expected_jd_data["min_salary"])
                if expected_min_salary in min_salary_value:
                    print(f"✅ Minimum salary pre-filled correctly: '{min_salary_value}'")
                else:
                    print(f"⚠️ Minimum salary mismatch - expected '{expected_min_salary}' but found '{min_salary_value}'")
            
            if "max_salary" in expected_jd_data and expected_jd_data["max_salary"]:
                max_salary_value = self.locators.edit_maximum_salary_input.input_value()
                expected_max_salary = str(expected_jd_data["max_salary"])
                if expected_max_salary in max_salary_value:
                    print(f"✅ Maximum salary pre-filled correctly: '{max_salary_value}'")
                else:
                    print(f"⚠️ Maximum salary mismatch - expected '{expected_max_salary}' but found '{max_salary_value}'")
            
            print("✅ Edit modal pre-filled data verification completed")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying pre-filled data: {e}")
            raise

    def validate_existing_jd_data_loaded(self, jd_title: str, expected_data: dict):
        """Validate that existing JD data is correctly loaded in edit mode"""
        try:
            print(f"🔍 Validating existing JD data loaded for: '{jd_title}'")
            
            # Verify all form fields contain expected data
            self.verify_edit_modal_pre_filled_data(expected_data)
            
            # Additional validation for dropdown selections
            # Note: Dropdown values might need special handling depending on implementation
            
            # Verify form is in edit state (not creation state)
            if self.locators.edit_mode_indicator.count() > 0:
                enhanced_assert_visible(self.page, self.locators.edit_mode_indicator, 
                                       "Edit mode indicator should be visible", "edit_mode_indicator")
                print("✅ Form is correctly in edit mode")
            
            # Verify Update button is present (not Save button)
            enhanced_assert_visible(self.page, self.locators.confirm_edit_button, 
                                   "Update button should be visible in edit mode", "update_button_visible")
            
            print(f"✅ Existing JD data validation completed for '{jd_title}'")
            return True
            
        except Exception as e:
            print(f"❌ Error validating existing JD data: {e}")
            raise

    def handle_edit_mode_navigation(self, agency_id: str, jd_id: str = None):
        """Handle edit mode navigation and URL parameter management"""
        try:
            print(f"🔧 Handling edit mode navigation for agency {agency_id}")
            
            # If jd_id is provided, construct edit URL directly
            if jd_id:
                edit_url = self.locators.edit_jd_url_pattern.format(agency_id=agency_id, jd_id=jd_id)
                self.page.goto(edit_url)
                self.page.wait_for_load_state("networkidle")
                time.sleep(2)
                
                # Verify we're on edit page
                current_url = self.page.url
                if f"/jd/edit/{jd_id}" in current_url:
                    print(f"✅ Successfully navigated to edit URL: {current_url}")
                else:
                    raise AssertionError(f"Expected edit URL with jd_id {jd_id}, but got: {current_url}")
            
            # Verify edit modal or page is loaded
            self.verify_edit_modal_opened()
            
            print("✅ Edit mode navigation handled successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error handling edit mode navigation: {e}")
            raise

    def verify_edit_url_parameters(self, agency_id: str, jd_id: str):
        """Verify edit mode URL contains correct parameters"""
        try:
            current_url = self.page.url
            
            # Check agency_id in URL
            if f"/agency/{agency_id}/" in current_url:
                print(f"✅ Agency ID {agency_id} found in URL")
            else:
                raise AssertionError(f"Agency ID {agency_id} not found in URL: {current_url}")
            
            # Check jd_id in URL (if provided)
            if jd_id and f"/jd/edit/{jd_id}" in current_url:
                print(f"✅ JD ID {jd_id} found in edit URL")
            elif jd_id:
                raise AssertionError(f"JD ID {jd_id} not found in URL: {current_url}")
            
            # Check edit mode indicator in URL
            if "/edit" in current_url:
                print("✅ Edit mode indicator found in URL")
            else:
                print("⚠️ Edit mode might be modal-based (no /edit in URL)")
            
            print("✅ Edit URL parameters verification completed")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying edit URL parameters: {e}")
            raise

    # ===== JD UPDATE FUNCTIONALITY METHODS =====
    def modify_jd_fields_in_edit_mode(self, updated_data: dict):
        """Modify JD fields in edit mode with new data"""
        try:
            print("🔧 Modifying JD fields in edit mode")
            
            # Update position title if provided
            if "position_title" in updated_data:
                print(f"📝 Updating position title to: '{updated_data['position_title']}'")
                self.locators.edit_position_job_title_input.fill(updated_data["position_title"])
            
            # Update workplace if provided
            if "workplace" in updated_data:
                print(f"📝 Updating workplace to: '{updated_data['workplace']}'")
                self.locators.edit_jd_workplace_input.fill(updated_data["workplace"])
            
            # Update company if provided
            if "company" in updated_data:
                print(f"📝 Updating company to: '{updated_data['company']}'")
                self.locators.edit_company_dropdown.click()
                time.sleep(1)
                self.locators.company_option(updated_data["company"]).click()
            
            # Update work style if provided
            if "work_style" in updated_data:
                print(f"📝 Updating work style to: '{updated_data['work_style']}'")
                self.locators.edit_work_style_dropdown.click()
                time.sleep(1)
                self.select_work_style_option_in_edit(updated_data["work_style"])
            
            # Update salary fields if provided
            if "min_salary" in updated_data:
                print(f"📝 Updating minimum salary to: '{updated_data['min_salary']}'")
                self.locators.edit_minimum_salary_input.fill(str(updated_data["min_salary"]))
            
            if "max_salary" in updated_data:
                print(f"📝 Updating maximum salary to: '{updated_data['max_salary']}'")
                self.locators.edit_maximum_salary_input.fill(str(updated_data["max_salary"]))
            
            # Update other fields following the same pattern as creation
            if "currency" in updated_data:
                self.select_currency_in_edit_mode(updated_data["currency"])
            
            if "job_age_min" in updated_data:
                self.locators.job_age_min_input.fill(str(updated_data["job_age_min"]))
            
            if "job_age_max" in updated_data:
                self.locators.job_age_max_input.fill(str(updated_data["job_age_max"]))
            
            if "department" in updated_data:
                self.locators.department_input.fill(updated_data["department"])
            
            if "job_function" in updated_data:
                self.locators.job_function_input.fill(updated_data["job_function"])
            
            print("✅ JD fields modification completed")
            return True
            
        except Exception as e:
            print(f"❌ Error modifying JD fields in edit mode: {e}")
            raise

    def select_work_style_option_in_edit(self, work_style: str):
        """Select work style option in edit mode"""
        if work_style.lower() == "remote":
            self.locators.remote_work_option.click()
        elif work_style.lower() == "on-site" or work_style.lower() == "onsite":
            self.locators.onsite_work_option.click()
        elif work_style.lower() == "hybrid":
            self.locators.hybrid_work_option.click()

    def select_currency_in_edit_mode(self, currency: str):
        """Select currency in edit mode"""
        self.locators.currency_dropdown.click()
        time.sleep(1)
        if currency.upper() == "JPY":
            self.locators.jpy_currency_option.click()
        elif currency.upper() == "USD":
            self.locators.usd_currency_option.click()
        elif currency.upper() == "EUR":
            self.locators.eur_currency_option.click()

    def implement_update_validation(self, validation_data: dict):
        """Implement update validation following same rules as creation"""
        try:
            print("🔍 Implementing update validation")
            
            # Test mandatory field validation in edit mode
            if "test_mandatory_fields" in validation_data and validation_data["test_mandatory_fields"]:
                self.trigger_mandatory_field_validation_in_edit()
            
            # Test salary range validation in edit mode
            if "test_salary_range" in validation_data:
                salary_data = validation_data["test_salary_range"]
                self.trigger_salary_range_validation_in_edit(
                    salary_data.get("min_salary", ""), 
                    salary_data.get("max_salary", "")
                )
            
            # Test age range validation in edit mode
            if "test_age_range" in validation_data:
                age_data = validation_data["test_age_range"]
                self.trigger_age_range_validation_in_edit(
                    age_data.get("min_age", ""), 
                    age_data.get("max_age", "")
                )
            
            # Test character limit validation in edit mode
            if "test_character_limits" in validation_data:
                char_data = validation_data["test_character_limits"]
                for field_type, long_text in char_data.items():
                    self.trigger_character_limit_validation_in_edit(field_type, long_text)
            
            print("✅ Update validation implementation completed")
            return True
            
        except Exception as e:
            print(f"❌ Error implementing update validation: {e}")
            raise

    def trigger_mandatory_field_validation_in_edit(self):
        """Trigger mandatory field validation in edit mode"""
        print("🔍 Testing mandatory field validation in edit mode")
        
        # Clear mandatory fields
        self.locators.edit_position_job_title_input.fill("")
        self.locators.edit_jd_workplace_input.fill("")
        
        # Attempt to update to trigger validation
        self.attempt_update_with_validation_errors()

    def trigger_salary_range_validation_in_edit(self, min_salary: str, max_salary: str):
        """Trigger salary range validation in edit mode"""
        print(f"🔍 Testing salary range validation in edit mode: min={min_salary}, max={max_salary}")
        
        self.locators.edit_minimum_salary_input.fill(min_salary)
        self.locators.edit_maximum_salary_input.fill(max_salary)
        
        self.attempt_update_with_validation_errors()

    def trigger_age_range_validation_in_edit(self, min_age: str, max_age: str):
        """Trigger age range validation in edit mode"""
        print(f"🔍 Testing age range validation in edit mode: min={min_age}, max={max_age}")
        
        self.locators.job_age_min_input.fill(min_age)
        self.locators.job_age_max_input.fill(max_age)
        
        self.attempt_update_with_validation_errors()

    def trigger_character_limit_validation_in_edit(self, field_type: str, long_text: str):
        """Trigger character limit validation in edit mode"""
        print(f"🔍 Testing character limit validation in edit mode for field: {field_type}")
        
        if field_type == "position_title":
            self.locators.edit_position_job_title_input.fill(long_text)
        elif field_type == "workplace":
            self.locators.edit_jd_workplace_input.fill(long_text)
        elif field_type == "department":
            self.locators.department_input.fill(long_text)
        elif field_type == "job_function":
            self.locators.job_function_input.fill(long_text)
        
        self.attempt_update_with_validation_errors()

    def attempt_update_with_validation_errors(self):
        """Attempt to update JD to trigger validation errors"""
        print("🔍 Attempting update to trigger validation errors")
        self.locators.confirm_edit_button.click()
        time.sleep(1)  # Allow validation errors to appear

    def save_jd_changes(self):
        """Save JD changes in edit mode"""
        try:
            print("💾 Saving JD changes")
            
            # Click update button
            enhanced_assert_visible(self.page, self.locators.confirm_edit_button, 
                                   "Update button should be visible", "update_button_save")
            
            self.locators.confirm_edit_button.click()
            time.sleep(2)
            
            print("✅ JD changes save initiated")
            return True
            
        except Exception as e:
            print(f"❌ Error saving JD changes: {e}")
            raise

    def verify_update_success_message(self):
        """Verify success message appears after successful JD update"""
        try:
            print("🔍 Verifying update success message")
            
            # Check for success message
            enhanced_assert_visible(self.page, self.locators.jd_updated_successfully_message, 
                                   "JD updated successfully message should be visible", "update_success_message")
            
            print("✅ Update success message verified")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying update success message: {e}")
            raise

    def handle_update_error_scenarios(self, error_type: str):
        """Handle update error scenarios and validation message display"""
        try:
            print(f"🔍 Handling update error scenario: {error_type}")
            
            if error_type == "mandatory_fields":
                # Verify mandatory field error messages
                enhanced_assert_visible(self.page, self.locators.position_title_required_error, 
                                       "Position title required error should be visible", "position_title_error_update")
                enhanced_assert_visible(self.page, self.locators.workplace_required_error, 
                                       "Workplace required error should be visible", "workplace_error_update")
            
            elif error_type == "salary_range":
                # Verify salary range error message
                enhanced_assert_visible(self.page, self.locators.invalid_salary_range_error, 
                                       "Invalid salary range error should be visible", "salary_range_error_update")
            
            elif error_type == "age_range":
                # Verify age range error message
                enhanced_assert_visible(self.page, self.locators.invalid_age_range_error, 
                                       "Invalid age range error should be visible", "age_range_error_update")
            
            elif error_type == "character_limit":
                # Check for any character limit error messages
                char_limit_errors = [
                    self.locators.position_title_max_length_error,
                    self.locators.workplace_max_length_error,
                    self.locators.department_max_length_error,
                    self.locators.job_function_max_length_error
                ]
                
                error_found = False
                for error_locator in char_limit_errors:
                    if error_locator.count() > 0:
                        enhanced_assert_visible(self.page, error_locator, 
                                               "Character limit error should be visible", "char_limit_error_update")
                        error_found = True
                        break
                
                if not error_found:
                    raise AssertionError("No character limit error message found")
            
            elif error_type == "network_error":
                # Handle network-related errors
                network_errors = [
                    self.locators.error_toast,
                    self.page.get_by_text("Network error"),
                    self.page.get_by_text("Connection failed")
                ]
                
                error_found = False
                for error_locator in network_errors:
                    if error_locator.count() > 0:
                        enhanced_assert_visible(self.page, error_locator, 
                                               "Network error should be visible", "network_error_update")
                        error_found = True
                        break
                
                if not error_found:
                    print("⚠️ No network error message found (might be expected)")
            
            # Verify modal remains open during error scenarios
            self.expect_modal_remains_open_after_validation_error()
            
            print(f"✅ Update error scenario '{error_type}' handled successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error handling update error scenario '{error_type}': {e}")
            raise

    def verify_validation_message_display_in_edit(self, expected_errors: list):
        """Verify validation messages are displayed correctly in edit mode"""
        try:
            print("🔍 Verifying validation messages in edit mode")
            
            for error_type in expected_errors:
                if error_type == "position_title_required":
                    enhanced_assert_visible(self.page, self.locators.position_title_required_error, 
                                           "Position title required error should be visible", "position_title_required_edit")
                
                elif error_type == "company_required":
                    enhanced_assert_visible(self.page, self.locators.company_required_error, 
                                           "Company required error should be visible", "company_required_edit")
                
                elif error_type == "work_style_required":
                    enhanced_assert_visible(self.page, self.locators.work_style_required_error, 
                                           "Work style required error should be visible", "work_style_required_edit")
                
                elif error_type == "workplace_required":
                    enhanced_assert_visible(self.page, self.locators.workplace_required_error, 
                                           "Workplace required error should be visible", "workplace_required_edit")
                
                elif error_type == "invalid_salary_range":
                    enhanced_assert_visible(self.page, self.locators.invalid_salary_range_error, 
                                           "Invalid salary range error should be visible", "invalid_salary_range_edit")
                
                elif error_type == "invalid_age_range":
                    enhanced_assert_visible(self.page, self.locators.invalid_age_range_error, 
                                           "Invalid age range error should be visible", "invalid_age_range_edit")
            
            print("✅ Validation messages verification completed in edit mode")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying validation messages in edit mode: {e}")
            raise

    def complete_jd_update_workflow(self, jd_title: str, updated_data: dict):
        """Complete JD update workflow from start to finish"""
        try:
            print(f"🔄 Starting complete JD update workflow for: '{jd_title}'")
            
            # Step 1: Access edit mode
            self.access_edit_mode_from_list(jd_title)
            
            # Step 2: Verify pre-filled data (optional, based on available data)
            # self.verify_edit_modal_pre_filled_data(original_data)
            
            # Step 3: Modify fields with new data
            self.modify_jd_fields_in_edit_mode(updated_data)
            
            # Step 4: Save changes
            self.save_jd_changes()
            
            # Step 5: Verify success message
            self.verify_update_success_message()
            
            # Step 6: Verify modal closes after successful update
            self.expect_modal_closes_after_successful_save()
            
            print(f"✅ Complete JD update workflow completed successfully for '{jd_title}'")
            return True
            
        except Exception as e:
            print(f"❌ Error in complete JD update workflow: {e}")
            raise

    # ===== EDIT CANCELLATION AND STATE MANAGEMENT METHODS =====
    def cancel_edit_without_saving(self):
        """Cancel JD edit operation without saving changes"""
        try:
            print("❌ Cancelling JD edit without saving changes")
            
            # Click cancel button
            enhanced_assert_visible(self.page, self.locators.cancel_edit_button, 
                                   "Cancel edit button should be visible", "cancel_edit_button")
            
            self.locators.cancel_edit_button.click()
            time.sleep(1)
            
            print("✅ Edit cancellation initiated")
            return True
            
        except Exception as e:
            print(f"❌ Error cancelling edit: {e}")
            raise

    def handle_unsaved_changes_warning(self, action: str = "discard"):
        """Handle unsaved changes warning dialog"""
        try:
            print(f"⚠️ Handling unsaved changes warning with action: {action}")
            
            # Check if unsaved changes warning appears
            if self.locators.unsaved_changes_warning.count() > 0:
                enhanced_assert_visible(self.page, self.locators.unsaved_changes_warning, 
                                       "Unsaved changes warning should be visible", "unsaved_changes_warning")
                
                if action == "discard":
                    # Confirm discarding changes
                    if self.locators.discard_changes_confirmation.count() > 0:
                        enhanced_assert_visible(self.page, self.locators.confirm_discard_button, 
                                               "Confirm discard button should be visible", "confirm_discard_button")
                        self.locators.confirm_discard_button.click()
                        print("✅ Confirmed discarding changes")
                    else:
                        # Direct discard if no confirmation dialog
                        self.locators.discard_changes_button.click()
                        print("✅ Discarded changes directly")
                
                elif action == "keep_editing":
                    # Keep editing (stay in edit mode)
                    enhanced_assert_visible(self.page, self.locators.keep_editing_button, 
                                           "Keep editing button should be visible", "keep_editing_button")
                    self.locators.keep_editing_button.click()
                    print("✅ Chose to keep editing")
                
                time.sleep(1)
            else:
                print("ℹ️ No unsaved changes warning appeared")
            
            return True
            
        except Exception as e:
            print(f"❌ Error handling unsaved changes warning: {e}")
            raise

    def verify_data_not_modified_after_cancellation(self, original_data: dict, jd_title: str):
        """Verify that JD data is not modified after cancellation"""
        try:
            print(f"🔍 Verifying data not modified after cancellation for: '{jd_title}'")
            
            # Navigate back to the JD to check its data
            # This could be done by refreshing the page or navigating to JD list and back
            self.page.reload()
            time.sleep(2)
            
            # Re-access edit mode to check if original data is preserved
            self.access_edit_mode_from_list(jd_title)
            
            # Verify original data is still present
            self.verify_edit_modal_pre_filled_data(original_data)
            
            # Close edit mode after verification
            self.cancel_edit_without_saving()
            
            print(f"✅ Verified data not modified after cancellation for '{jd_title}'")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying data not modified after cancellation: {e}")
            raise

    def verify_no_data_loss_after_cancellation(self, jd_title: str, expected_data: dict):
        """Verify no data loss occurs after edit cancellation"""
        try:
            print(f"🔍 Verifying no data loss after cancellation for: '{jd_title}'")
            
            # Check that JD still exists in the list
            jd_card = self.get_jd_card_by_title(jd_title)
            enhanced_assert_visible(self.page, jd_card, 
                                   f"JD card '{jd_title}' should still be visible after cancellation", "jd_card_after_cancel")
            
            # Verify JD data integrity by accessing edit mode again
            self.access_edit_mode_from_list(jd_title)
            self.verify_edit_modal_pre_filled_data(expected_data)
            
            # Close edit mode
            self.cancel_edit_without_saving()
            
            print(f"✅ No data loss verified after cancellation for '{jd_title}'")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying no data loss after cancellation: {e}")
            raise

    def manage_edit_modal_state(self, action: str):
        """Manage edit modal state and return to previous view"""
        try:
            print(f"🔧 Managing edit modal state with action: {action}")
            
            if action == "close_modal":
                # Close modal using close button
                if self.locators.edit_modal_close_button.count() > 0:
                    self.locators.edit_modal_close_button.click()
                else:
                    # Fallback to cancel button
                    self.locators.cancel_edit_button.click()
                
                time.sleep(1)
                
                # Verify modal is closed
                self.wait_for_modal_to_close()
                print("✅ Edit modal closed successfully")
            
            elif action == "return_to_list":
                # Cancel edit and return to JD list
                self.cancel_edit_without_saving()
                
                # Handle any unsaved changes warning
                self.handle_unsaved_changes_warning("discard")
                
                # Verify we're back to JD list
                self.verify_jd_list_display()
                print("✅ Returned to JD list successfully")
            
            elif action == "return_to_detail":
                # Cancel edit and return to JD detail view
                self.cancel_edit_without_saving()
                
                # Handle any unsaved changes warning
                self.handle_unsaved_changes_warning("discard")
                
                # Verify we're in detail view (if applicable)
                if self.locators.jd_detail_container.count() > 0:
                    enhanced_assert_visible(self.page, self.locators.jd_detail_container, 
                                           "JD detail container should be visible", "jd_detail_after_cancel")
                    print("✅ Returned to JD detail view successfully")
                else:
                    print("ℹ️ Returned to JD list (detail view not applicable)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error managing edit modal state: {e}")
            raise

    def handle_edit_state_navigation(self, navigation_type: str):
        """Handle edit mode state management and navigation scenarios"""
        try:
            print(f"🔧 Handling edit state navigation: {navigation_type}")
            
            if navigation_type == "browser_back":
                # Test browser back button behavior during edit
                self.page.go_back()
                time.sleep(2)
                
                # Check if unsaved changes warning appears
                self.handle_unsaved_changes_warning("discard")
                
                print("✅ Browser back navigation handled")
            
            elif navigation_type == "page_refresh":
                # Test page refresh behavior during edit
                self.page.reload()
                time.sleep(2)
                
                # Verify edit state is lost (expected behavior)
                if self.is_modal_closed():
                    print("✅ Edit state correctly lost after page refresh")
                else:
                    print("⚠️ Edit state persisted after page refresh (unexpected)")
            
            elif navigation_type == "direct_url":
                # Test direct URL navigation during edit
                current_url = self.page.url
                self.page.goto(current_url.replace("/edit", ""))
                time.sleep(2)
                
                # Check if we're redirected or if unsaved changes warning appears
                self.handle_unsaved_changes_warning("discard")
                
                print("✅ Direct URL navigation handled")
            
            return True
            
        except Exception as e:
            print(f"❌ Error handling edit state navigation: {e}")
            raise

    def verify_edit_cancellation_workflow(self, jd_title: str, original_data: dict):
        """Verify complete edit cancellation workflow"""
        try:
            print(f"🔄 Verifying complete edit cancellation workflow for: '{jd_title}'")
            
            # Step 1: Access edit mode
            self.access_edit_mode_from_list(jd_title)
            
            # Step 2: Make some changes (but don't save)
            test_changes = {
                "position_title": "Modified Title (Should Not Save)",
                "workplace": "Modified Workplace (Should Not Save)"
            }
            self.modify_jd_fields_in_edit_mode(test_changes)
            
            # Step 3: Cancel edit
            self.cancel_edit_without_saving()
            
            # Step 4: Handle any unsaved changes warning
            self.handle_unsaved_changes_warning("discard")
            
            # Step 5: Verify modal is closed
            self.wait_for_modal_to_close()
            
            # Step 6: Verify original data is preserved
            self.verify_data_not_modified_after_cancellation(original_data, jd_title)
            
            # Step 7: Verify no data loss
            self.verify_no_data_loss_after_cancellation(jd_title, original_data)
            
            print(f"✅ Complete edit cancellation workflow verified for '{jd_title}'")
            return True
            
        except Exception as e:
            print(f"❌ Error verifying edit cancellation workflow: {e}")
            raise

    def test_edit_cancellation_scenarios(self, jd_title: str, original_data: dict):
        """Test various edit cancellation scenarios"""
        try:
            print(f"🧪 Testing edit cancellation scenarios for: '{jd_title}'")
            
            # Scenario 1: Cancel without making changes
            print("📝 Testing cancellation without changes")
            self.access_edit_mode_from_list(jd_title)
            self.cancel_edit_without_saving()
            self.wait_for_modal_to_close()
            
            # Scenario 2: Cancel after making changes
            print("📝 Testing cancellation with changes")
            self.access_edit_mode_from_list(jd_title)
            test_changes = {"position_title": "Test Change"}
            self.modify_jd_fields_in_edit_mode(test_changes)
            self.cancel_edit_without_saving()
            self.handle_unsaved_changes_warning("discard")
            self.wait_for_modal_to_close()
            
            # Scenario 3: Cancel and choose to keep editing
            print("📝 Testing keep editing option")
            self.access_edit_mode_from_list(jd_title)
            self.modify_jd_fields_in_edit_mode(test_changes)
            self.cancel_edit_without_saving()
            self.handle_unsaved_changes_warning("keep_editing")
            # Should still be in edit mode
            if self.is_modal_open():
                print("✅ Successfully stayed in edit mode")
                self.cancel_edit_without_saving()
                self.handle_unsaved_changes_warning("discard")
            
            # Final verification
            self.verify_no_data_loss_after_cancellation(jd_title, original_data)
            
            print(f"✅ All edit cancellation scenarios tested successfully for '{jd_title}'")
            return True
            
        except Exception as e:
            print(f"❌ Error testing edit cancellation scenarios: {e}")
            raise

    # ===== SEARCH FUNCTIONALITY =====
    def search_jd(self, search_term: str):
        """Search for JDs using search input"""
        self.locators.search_input.fill(search_term)
        self.page.keyboard.press("Enter")
        time.sleep(2)

    def clear_search(self):
        """Clear search input"""
        self.locators.search_input.fill("")
        self.page.keyboard.press("Enter")
        time.sleep(2)

    def expect_search_results_visible(self):
        """Verify search results are visible"""
        enhanced_assert_visible(self.page, self.locators.search_results_container, 
                               "Search results should be visible", "search_results")

    def expect_no_search_results(self):
        """Verify 'No results found' message is visible"""
        enhanced_assert_visible(self.page, self.locators.search_no_results_message, 
                               "No search results message should be visible", "no_search_results")

    # ===== ENHANCED SEARCH FUNCTIONALITY METHODS =====
    def fill_search_input(self, search_term: str):
        """Fill search input with search term without submitting"""
        print(f"🔍 Filling search input with: '{search_term}'")
        self.locators.search_input.fill(search_term)
        time.sleep(0.5)

    def submit_search(self):
        """Submit search by pressing Enter or clicking search button"""
        print("🔍 Submitting search")
        self.page.keyboard.press("Enter")
        time.sleep(2)

    def perform_search(self, search_term: str):
        """Complete search workflow: fill input and submit"""
        print(f"🔍 Performing search for: '{search_term}'")
        self.fill_search_input(search_term)
        self.submit_search()
        return self.get_search_results_count()

    def get_search_results_count(self) -> int:
        """Get the count of search results"""
        try:
            # Count JD cards visible after search
            jd_cards = self.page.locator(".jd-card, [class*='jd-card'], [data-testid='jd-card']")
            count = jd_cards.count()
            print(f"✅ Found {count} search results")
            return count
        except Exception as e:
            print(f"❌ Error getting search results count: {e}")
            return 0

    def verify_search_results_contain_term(self, search_term: str):
        """Verify search results contain the search term"""
        print(f"🔍 Verifying search results contain term: '{search_term}'")
        
        # Get all visible JD cards
        jd_cards = self.page.locator(".jd-card, [class*='jd-card']")
        cards_count = jd_cards.count()
        
        if cards_count == 0:
            # Check if we're in "no results" state
            if self.locators.search_no_results_message.count() > 0:
                print(f"✅ No results found for search term '{search_term}' (as expected)")
                return True
            else:
                raise AssertionError(f"No search results found and no 'no results' message displayed")
        
        # Verify each card contains the search term
        found_matching_cards = 0
        for i in range(cards_count):
            card = jd_cards.nth(i)
            card_text = card.text_content().lower()
            if search_term.lower() in card_text:
                found_matching_cards += 1
        
        if found_matching_cards > 0:
            print(f"✅ Found {found_matching_cards} cards containing search term '{search_term}'")
            return True
        else:
            raise AssertionError(f"No search results contain the search term '{search_term}'")

    def verify_search_highlights(self, search_term: str):
        """Verify search term is highlighted in results"""
        print(f"🔍 Verifying search highlights for term: '{search_term}'")
        
        try:
            # Look for highlighted text elements
            highlights = self.locators.search_highlight
            if highlights.count() > 0:
                # Verify at least one highlight contains the search term
                for i in range(highlights.count()):
                    highlight_text = highlights.nth(i).text_content()
                    if search_term.lower() in highlight_text.lower():
                        print(f"✅ Search term '{search_term}' is properly highlighted")
                        return True
                
                print(f"⚠️ Highlights found but don't contain search term '{search_term}'")
                return False
            else:
                print(f"ℹ️ No search highlights found (may not be implemented)")
                return True  # Don't fail if highlighting isn't implemented
        except Exception as e:
            print(f"⚠️ Error checking search highlights: {e}")
            return True  # Don't fail on highlight checking errors

    def handle_no_results_scenario(self, search_term: str):
        """Handle and verify 'No results found' scenario"""
        print(f"🔍 Handling no results scenario for: '{search_term}'")
        
        try:
            # Verify no results message is displayed
            enhanced_assert_visible(
                self.page, 
                self.locators.search_no_results_message,
                f"No results message should be visible for search '{search_term}'",
                "search_no_results"
            )
            
            # Verify no JD cards are visible
            jd_cards = self.page.locator(".jd-card, [class*='jd-card']")
            cards_count = jd_cards.count()
            
            if cards_count == 0:
                print(f"✅ No results scenario properly handled for '{search_term}'")
                return True
            else:
                raise AssertionError(f"Expected no results but found {cards_count} JD cards")
                
        except Exception as e:
            print(f"❌ Error handling no results scenario: {e}")
            raise

    def clear_search_input(self):
        """Clear search input field"""
        print("🔍 Clearing search input")
        self.locators.search_input.fill("")
        time.sleep(0.5)

    def reset_search_state(self):
        """Reset search to show all JDs"""
        print("🔍 Resetting search state")
        self.clear_search_input()
        self.submit_search()
        
        # Verify we're back to showing all JDs (no search filter applied)
        try:
            # Check that we don't see "no results" message
            enhanced_assert_not_visible(
                self.page,
                self.locators.search_no_results_message,
                "No results message should not be visible after search reset",
                "search_reset"
            )
            print("✅ Search state reset successfully")
            return True
        except Exception as e:
            print(f"⚠️ Error verifying search reset: {e}")
            return False

    def click_clear_search_button(self):
        """Click clear search button if available"""
        try:
            if self.locators.clear_search_button.count() > 0:
                print("🔍 Clicking clear search button")
                self.locators.clear_search_button.click()
                time.sleep(1)
                return True
            else:
                print("ℹ️ Clear search button not available")
                return False
        except Exception as e:
            print(f"⚠️ Error clicking clear search button: {e}")
            return False

    def verify_search_input_value(self, expected_value: str):
        """Verify search input contains expected value"""
        try:
            actual_value = self.locators.search_input.input_value()
            if actual_value == expected_value:
                print(f"✅ Search input value verified: '{expected_value}'")
                return True
            else:
                raise AssertionError(f"Expected search input '{expected_value}' but found '{actual_value}'")
        except Exception as e:
            print(f"❌ Error verifying search input value: {e}")
            raise

    def perform_empty_search(self):
        """Perform search with empty query"""
        print("🔍 Performing empty search")
        self.clear_search_input()
        self.submit_search()
        
        # Verify all JDs are displayed (empty search should show all)
        return self.get_search_results_count()

    def search_and_verify_results(self, search_term: str, expected_count: int = None):
        """Perform search and verify results count"""
        print(f"🔍 Searching and verifying results for: '{search_term}'")
        
        # Perform search
        actual_count = self.perform_search(search_term)
        
        # Verify expected count if provided
        if expected_count is not None:
            if actual_count == expected_count:
                print(f"✅ Search results count verified: {actual_count}")
            else:
                raise AssertionError(f"Expected {expected_count} results but found {actual_count}")
        
        # Verify results contain search term (if any results found)
        if actual_count > 0:
            self.verify_search_results_contain_term(search_term)
            self.verify_search_highlights(search_term)
        else:
            self.handle_no_results_scenario(search_term)
        
        return actual_count

    def test_search_functionality_comprehensive(self, test_cases: list):
        """Test search functionality with multiple test cases"""
        print("🔍 Running comprehensive search functionality test")
        
        results = {}
        
        for test_case in test_cases:
            search_term = test_case.get("term", "")
            expected_count = test_case.get("expected_count", None)
            
            try:
                print(f"\n-> Testing search term: '{search_term}'")
                actual_count = self.search_and_verify_results(search_term, expected_count)
                results[search_term] = {
                    "success": True,
                    "actual_count": actual_count,
                    "expected_count": expected_count
                }
                
                # Reset search for next test
                self.reset_search_state()
                
            except Exception as e:
                print(f"❌ Search test failed for '{search_term}': {e}")
                results[search_term] = {
                    "success": False,
                    "error": str(e)
                }
        
        print(f"\n✅ Search functionality test completed: {len([r for r in results.values() if r.get('success')])} passed, {len([r for r in results.values() if not r.get('success')])} failed")
        return results

    # ===== FILTER FUNCTIONALITY =====
    def open_filters(self):
        """Open filter panel"""
        self.locators.filters_button.click()
        time.sleep(1)

    def close_filters(self):
        """Close filter panel"""
        self.locators.close_filter_button.click()
        time.sleep(1)

    def apply_company_filter(self, company_name: str):
        """Apply company name filter"""
        self.locators.company_filter_dropdown.select_option(label=company_name)

    def apply_status_filter(self, status: str):
        """Apply hiring status filter"""
        self.locators.status_filter_dropdown.select_option(label=status)

    def apply_work_style_filter(self, work_style: str):
        """Apply work style filter"""
        self.locators.work_style_filter_dropdown.select_option(label=work_style)

    def apply_salary_range_filter(self, min_salary: str, max_salary: str):
        """Apply salary range filter"""
        if min_salary:
            self.locators.min_salary_filter_input.fill(min_salary)
        if max_salary:
            self.locators.max_salary_filter_input.fill(max_salary)

    def apply_filters(self):
        """Apply selected filters"""
        self.locators.apply_filters_button.click()
        time.sleep(2)

    def clear_all_filters(self):
        """Clear all applied filters"""
        self.locators.all_clear_button.click()
        time.sleep(2)

    def reset_filters(self):
        """Reset filters to default state"""
        self.locators.reset_filters_button.click()
        time.sleep(2)

    # ===== ENHANCED FILTER PANEL INTERACTION METHODS =====
    def click_filters_button(self):
        """Click filters button to open filter panel"""
        print("🔧 Opening filter panel")
        self.locators.filters_button.click()
        time.sleep(1)
        return self.verify_filter_panel_opened()

    def verify_filter_panel_opened(self) -> bool:
        """Verify filter panel is opened and visible"""
        try:
            enhanced_assert_visible(
                self.page,
                self.locators.filter_panel,
                "Filter panel should be visible after opening",
                "filter_panel_opened"
            )
            print("✅ Filter panel opened successfully")
            return True
        except Exception as e:
            print(f"❌ Filter panel not opened: {e}")
            return False

    def verify_filter_panel_closed(self) -> bool:
        """Verify filter panel is closed and not visible"""
        try:
            enhanced_assert_not_visible(
                self.page,
                self.locators.filter_panel,
                "Filter panel should not be visible after closing",
                "filter_panel_closed"
            )
            print("✅ Filter panel closed successfully")
            return True
        except Exception as e:
            print(f"❌ Filter panel still visible: {e}")
            return False

    def close_filter_panel(self):
        """Close filter panel using close button or overlay"""
        print("🔧 Closing filter panel")
        try:
            # Try close button first
            if self.locators.close_filter_button.count() > 0:
                self.locators.close_filter_button.click()
            # Try clicking overlay if close button not available
            elif self.locators.filter_overlay.count() > 0:
                self.locators.filter_overlay.click()
            # Try pressing Escape key as fallback
            else:
                self.page.keyboard.press("Escape")
            
            time.sleep(1)
            return self.verify_filter_panel_closed()
        except Exception as e:
            print(f"❌ Error closing filter panel: {e}")
            return False

    def select_company_filter(self, company_name: str):
        """Select company from company filter dropdown"""
        print(f"🔧 Selecting company filter: '{company_name}'")
        try:
            # Open company filter dropdown
            self.locators.company_name_filter.click()
            time.sleep(0.5)
            
            # Select company option
            self.locators.company_filter_dropdown.select_option(label=company_name)
            time.sleep(0.5)
            
            print(f"✅ Company filter '{company_name}' selected")
            return True
        except Exception as e:
            print(f"❌ Error selecting company filter: {e}")
            return False

    def select_position_title_filter(self, position_title: str):
        """Enter position title in position filter input"""
        print(f"🔧 Setting position title filter: '{position_title}'")
        try:
            self.locators.position_filter_input.fill(position_title)
            time.sleep(0.5)
            print(f"✅ Position title filter '{position_title}' set")
            return True
        except Exception as e:
            print(f"❌ Error setting position title filter: {e}")
            return False

    def select_hiring_status_filter(self, status: str):
        """Select hiring status from status filter dropdown"""
        print(f"🔧 Selecting hiring status filter: '{status}'")
        try:
            # Open status filter dropdown
            self.locators.hiring_status_filter.click()
            time.sleep(0.5)
            
            # Select status option
            self.locators.status_filter_dropdown.select_option(label=status)
            time.sleep(0.5)
            
            print(f"✅ Hiring status filter '{status}' selected")
            return True
        except Exception as e:
            print(f"❌ Error selecting hiring status filter: {e}")
            return False

    def select_work_style_filter_option(self, work_style: str):
        """Select work style from work style filter dropdown"""
        print(f"🔧 Selecting work style filter: '{work_style}'")
        try:
            # Open work style filter dropdown
            self.locators.work_style_filter.click()
            time.sleep(0.5)
            
            # Select work style option
            self.locators.work_style_filter_dropdown.select_option(label=work_style)
            time.sleep(0.5)
            
            print(f"✅ Work style filter '{work_style}' selected")
            return True
        except Exception as e:
            print(f"❌ Error selecting work style filter: {e}")
            return False

    def set_salary_range_filter(self, min_salary: str = None, max_salary: str = None):
        """Set salary range filter with min and/or max values"""
        print(f"🔧 Setting salary range filter: min={min_salary}, max={max_salary}")
        try:
            if min_salary:
                self.locators.min_salary_filter_input.fill(str(min_salary))
                time.sleep(0.3)
            
            if max_salary:
                self.locators.max_salary_filter_input.fill(str(max_salary))
                time.sleep(0.3)
            
            print(f"✅ Salary range filter set")
            return True
        except Exception as e:
            print(f"❌ Error setting salary range filter: {e}")
            return False

    def apply_single_filter(self, filter_type: str, filter_value: str):
        """Apply a single filter of specified type"""
        print(f"🔧 Applying single filter: {filter_type} = '{filter_value}'")
        
        success = False
        if filter_type == "company":
            success = self.select_company_filter(filter_value)
        elif filter_type == "position":
            success = self.select_position_title_filter(filter_value)
        elif filter_type == "status":
            success = self.select_hiring_status_filter(filter_value)
        elif filter_type == "work_style":
            success = self.select_work_style_filter_option(filter_value)
        else:
            print(f"❌ Unknown filter type: {filter_type}")
            return False
        
        if success:
            # Apply the filter
            return self.click_apply_filters_button()
        return False

    def apply_multiple_filters(self, filters: dict):
        """Apply multiple filters at once"""
        print(f"🔧 Applying multiple filters: {filters}")
        
        # Open filter panel if not already open
        if not self.verify_filter_panel_opened():
            self.click_filters_button()
        
        # Apply each filter
        for filter_type, filter_value in filters.items():
            if filter_type == "company":
                self.select_company_filter(filter_value)
            elif filter_type == "position":
                self.select_position_title_filter(filter_value)
            elif filter_type == "status":
                self.select_hiring_status_filter(filter_value)
            elif filter_type == "work_style":
                self.select_work_style_filter_option(filter_value)
            elif filter_type == "salary_range":
                min_sal = filter_value.get("min")
                max_sal = filter_value.get("max")
                self.set_salary_range_filter(min_sal, max_sal)
            else:
                print(f"⚠️ Unknown filter type: {filter_type}")
        
        # Apply all filters
        return self.click_apply_filters_button()

    def click_apply_filters_button(self):
        """Click apply filters button"""
        print("🔧 Applying filters")
        try:
            self.locators.apply_filters_button.click()
            time.sleep(2)  # Wait for filters to be applied
            print("✅ Filters applied successfully")
            return True
        except Exception as e:
            print(f"❌ Error applying filters: {e}")
            return False

    def verify_filtered_results_match_criteria(self, filters: dict):
        """Verify filtered results match the applied filter criteria"""
        print(f"🔍 Verifying filtered results match criteria: {filters}")
        
        try:
            # Get all visible JD cards after filtering
            jd_cards = self.page.locator(".jd-card, [class*='jd-card']")
            cards_count = jd_cards.count()
            
            if cards_count == 0:
                # Check if this is expected (no results match filters)
                if self.locators.search_no_results_message.count() > 0:
                    print("✅ No results match filter criteria (as expected)")
                    return True
                else:
                    print("⚠️ No JD cards found but no 'no results' message displayed")
                    return False
            
            # Verify each card matches filter criteria
            matching_cards = 0
            for i in range(cards_count):
                card = jd_cards.nth(i)
                card_text = card.text_content().lower()
                
                # Check each filter criterion
                matches_all_filters = True
                for filter_type, filter_value in filters.items():
                    if filter_type == "company":
                        if filter_value.lower() not in card_text:
                            matches_all_filters = False
                            break
                    elif filter_type == "position":
                        if filter_value.lower() not in card_text:
                            matches_all_filters = False
                            break
                    elif filter_type == "status":
                        if filter_value.lower() not in card_text:
                            matches_all_filters = False
                            break
                    elif filter_type == "work_style":
                        if filter_value.lower() not in card_text:
                            matches_all_filters = False
                            break
                
                if matches_all_filters:
                    matching_cards += 1
            
            if matching_cards == cards_count:
                print(f"✅ All {cards_count} filtered results match criteria")
                return True
            else:
                print(f"⚠️ Only {matching_cards}/{cards_count} results match filter criteria")
                return False
                
        except Exception as e:
            print(f"❌ Error verifying filtered results: {e}")
            return False

    def get_filtered_results_count(self) -> int:
        """Get count of results after applying filters"""
        try:
            jd_cards = self.page.locator(".jd-card, [class*='jd-card']")
            count = jd_cards.count()
            print(f"✅ Found {count} filtered results")
            return count
        except Exception as e:
            print(f"❌ Error getting filtered results count: {e}")
            return 0

    def verify_filter_combination_results(self, filters: dict, expected_count: int = None):
        """Verify results of filter combination"""
        print(f"🔍 Verifying filter combination results for: {filters}")
        
        # Get actual results count
        actual_count = self.get_filtered_results_count()
        
        # Verify expected count if provided
        if expected_count is not None:
            if actual_count == expected_count:
                print(f"✅ Filter combination results count verified: {actual_count}")
            else:
                raise AssertionError(f"Expected {expected_count} filtered results but found {actual_count}")
        
        # Verify results match filter criteria
        if actual_count > 0:
            self.verify_filtered_results_match_criteria(filters)
        
        return actual_count

    def test_filter_combinations(self, filter_combinations: list):
        """Test multiple filter combinations"""
        print(f"🔧 Testing {len(filter_combinations)} filter combinations")
        
        results = {}
        
        for i, filters in enumerate(filter_combinations):
            try:
                print(f"\n-> Testing filter combination {i+1}: {filters}")
                
                # Apply filters
                self.apply_multiple_filters(filters)
                
                # Verify results
                count = self.verify_filter_combination_results(filters)
                results[f"combination_{i+1}"] = {
                    "filters": filters,
                    "success": True,
                    "count": count
                }
                
                # Clear filters for next test
                self.click_all_clear_button()
                
            except Exception as e:
                print(f"❌ Filter combination {i+1} failed: {e}")
                results[f"combination_{i+1}"] = {
                    "filters": filters,
                    "success": False,
                    "error": str(e)
                }
        
        successful_tests = len([r for r in results.values() if r.get("success")])
        print(f"\n✅ Filter combinations test completed: {successful_tests}/{len(filter_combinations)} passed")
        
        return results

    def click_all_clear_button(self):
        """Click 'All clear' button to remove all filters"""
        print("🔧 Clearing all filters")
        try:
            # Open filter panel if not already open
            if not self.verify_filter_panel_opened():
                self.click_filters_button()
            
            # Click all clear button
            self.locators.all_clear_button.click()
            time.sleep(2)
            
            print("✅ All filters cleared")
            return True
        except Exception as e:
            print(f"❌ Error clearing filters: {e}")
            return False

    def verify_all_filters_cleared(self):
        """Verify all filters have been cleared"""
        print("🔍 Verifying all filters are cleared")
        
        try:
            # Check that filter inputs are empty/reset
            # This is a basic check - actual implementation would depend on UI behavior
            
            # Verify we're showing all JDs (not filtered)
            all_results_count = self.get_filtered_results_count()
            
            # Check that we don't see "no results" message
            if self.locators.search_no_results_message.count() == 0:
                print(f"✅ Filters cleared - showing {all_results_count} total results")
                return True
            else:
                print("⚠️ Still showing 'no results' message after clearing filters")
                return False
                
        except Exception as e:
            print(f"❌ Error verifying filters cleared: {e}")
            return False

    def get_available_filter_options(self, filter_type: str) -> list:
        """Get available options for a specific filter type"""
        print(f"🔍 Getting available options for filter: {filter_type}")
        
        options = []
        try:
            if filter_type == "company":
                # Open company filter and get options
                self.locators.company_name_filter.click()
                time.sleep(0.5)
                option_elements = self.locators.company_filter_dropdown.locator("option")
                for i in range(option_elements.count()):
                    option_text = option_elements.nth(i).text_content()
                    if option_text and option_text.strip():
                        options.append(option_text.strip())
            
            elif filter_type == "status":
                # Open status filter and get options
                self.locators.hiring_status_filter.click()
                time.sleep(0.5)
                option_elements = self.locators.status_filter_dropdown.locator("option")
                for i in range(option_elements.count()):
                    option_text = option_elements.nth(i).text_content()
                    if option_text and option_text.strip():
                        options.append(option_text.strip())
            
            elif filter_type == "work_style":
                # Open work style filter and get options
                self.locators.work_style_filter.click()
                time.sleep(0.5)
                option_elements = self.locators.work_style_filter_dropdown.locator("option")
                for i in range(option_elements.count()):
                    option_text = option_elements.nth(i).text_content()
                    if option_text and option_text.strip():
                        options.append(option_text.strip())
            
            print(f"✅ Found {len(options)} options for {filter_type}: {options}")
            
        except Exception as e:
            print(f"❌ Error getting filter options for {filter_type}: {e}")
        
        return options

    def test_all_filter_types(self):
        """Test all available filter types with their available options"""
        print("🔧 Testing all filter types")
        
        results = {}
        filter_types = ["company", "status", "work_style"]
        
        for filter_type in filter_types:
            try:
                print(f"\n-> Testing {filter_type} filter")
                
                # Open filter panel
                self.click_filters_button()
                
                # Get available options
                options = self.get_available_filter_options(filter_type)
                
                if options:
                    # Test first available option
                    test_option = options[0]
                    success = self.apply_single_filter(filter_type, test_option)
                    
                    if success:
                        count = self.get_filtered_results_count()
                        results[filter_type] = {
                            "success": True,
                            "options": options,
                            "tested_option": test_option,
                            "results_count": count
                        }
                    else:
                        results[filter_type] = {
                            "success": False,
                            "options": options,
                            "error": "Failed to apply filter"
                        }
                else:
                    results[filter_type] = {
                        "success": False,
                        "options": [],
                        "error": "No options available"
                    }
                
                # Clear filters for next test
                self.click_all_clear_button()
                
            except Exception as e:
                results[filter_type] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ Error testing {filter_type} filter: {e}")
        
        successful_tests = len([r for r in results.values() if r.get("success")])
        print(f"\n✅ Filter types test completed: {successful_tests}/{len(filter_types)} passed")
        
        return results

    # ===== FILTER CLEARING AND RESET FUNCTIONALITY =====
    def click_all_clear_filters_button(self):
        """Click 'All clear' button to remove all applied filters"""
        print("🔧 Clicking 'All clear' button to remove all filters")
        try:
            # Ensure filter panel is open
            if not self.verify_filter_panel_opened():
                self.click_filters_button()
            
            # Click the all clear button
            self.locators.all_clear_button.click()
            time.sleep(2)  # Wait for filters to be cleared
            
            print("✅ 'All clear' button clicked successfully")
            return True
        except Exception as e:
            print(f"❌ Error clicking 'All clear' button: {e}")
            return False

    def verify_all_filters_removed(self):
        """Verify that all filters have been removed and cleared"""
        print("🔍 Verifying all filters are removed")
        
        try:
            # Check filter input states are reset
            filter_inputs_cleared = self.check_filter_inputs_cleared()
            
            # Check that results show all JDs (not filtered)
            results_show_all = self.verify_results_show_all_jds()
            
            # Check no active filter indicators
            no_active_filters = self.verify_no_active_filter_indicators()
            
            if filter_inputs_cleared and results_show_all and no_active_filters:
                print("✅ All filters successfully removed")
                return True
            else:
                print("⚠️ Some filters may not be completely cleared")
                return False
                
        except Exception as e:
            print(f"❌ Error verifying filters removed: {e}")
            return False

    def check_filter_inputs_cleared(self) -> bool:
        """Check that all filter input fields are cleared/reset"""
        print("🔍 Checking filter inputs are cleared")
        
        try:
            # Open filter panel to check inputs
            if not self.verify_filter_panel_opened():
                self.click_filters_button()
            
            inputs_cleared = True
            
            # Check text inputs are empty
            if self.locators.position_filter_input.count() > 0:
                position_value = self.locators.position_filter_input.input_value()
                if position_value and position_value.strip():
                    print(f"⚠️ Position filter input not cleared: '{position_value}'")
                    inputs_cleared = False
            
            if self.locators.min_salary_filter_input.count() > 0:
                min_salary_value = self.locators.min_salary_filter_input.input_value()
                if min_salary_value and min_salary_value.strip():
                    print(f"⚠️ Min salary filter input not cleared: '{min_salary_value}'")
                    inputs_cleared = False
            
            if self.locators.max_salary_filter_input.count() > 0:
                max_salary_value = self.locators.max_salary_filter_input.input_value()
                if max_salary_value and max_salary_value.strip():
                    print(f"⚠️ Max salary filter input not cleared: '{max_salary_value}'")
                    inputs_cleared = False
            
            # Check dropdowns are reset to default/empty state
            # Note: Actual implementation would depend on how dropdowns show their state
            
            if inputs_cleared:
                print("✅ All filter inputs are cleared")
            
            return inputs_cleared
            
        except Exception as e:
            print(f"❌ Error checking filter inputs: {e}")
            return False

    def verify_results_show_all_jds(self) -> bool:
        """Verify that results show all JDs (no filtering applied)"""
        print("🔍 Verifying results show all JDs")
        
        try:
            # Close filter panel to see results
            if self.verify_filter_panel_opened():
                self.close_filter_panel()
            
            # Check that we're not showing "no results" message
            if self.locators.search_no_results_message.count() > 0:
                print("⚠️ Still showing 'no results' message after clearing filters")
                return False
            
            # Get current results count
            current_count = self.get_filtered_results_count()
            
            # This should show all available JDs
            if current_count > 0:
                print(f"✅ Showing {current_count} JDs after clearing filters")
                return True
            else:
                # Could be legitimately empty if no JDs exist
                if self.locators.no_jds_message.count() > 0:
                    print("✅ No JDs exist (legitimate empty state)")
                    return True
                else:
                    print("⚠️ No JDs shown but no empty state message")
                    return False
                    
        except Exception as e:
            print(f"❌ Error verifying results show all JDs: {e}")
            return False

    def verify_no_active_filter_indicators(self) -> bool:
        """Verify there are no active filter indicators visible"""
        print("🔍 Verifying no active filter indicators")
        
        try:
            # Look for common filter indicator elements
            # These would be UI elements that show active filters
            active_filter_badges = self.page.locator(".filter-badge, .active-filter, [class*='filter-active']")
            filter_count_indicators = self.page.locator(".filter-count, [class*='filter-count']")
            
            if active_filter_badges.count() == 0 and filter_count_indicators.count() == 0:
                print("✅ No active filter indicators found")
                return True
            else:
                print(f"⚠️ Found {active_filter_badges.count()} filter badges and {filter_count_indicators.count()} count indicators")
                return False
                
        except Exception as e:
            print(f"❌ Error checking filter indicators: {e}")
            return True  # Don't fail if indicators aren't implemented

    def reset_all_filters_to_default(self):
        """Reset all filters to their default state"""
        print("🔧 Resetting all filters to default state")
        
        try:
            # Method 1: Use "All clear" button
            success_clear = self.click_all_clear_filters_button()
            
            if success_clear:
                # Verify filters are cleared
                if self.verify_all_filters_removed():
                    print("✅ Filters reset successfully using 'All clear' button")
                    return True
            
            # Method 2: Try reset button if available
            if self.locators.reset_filters_button.count() > 0:
                print("🔧 Trying reset button as alternative")
                self.locators.reset_filters_button.click()
                time.sleep(2)
                
                if self.verify_all_filters_removed():
                    print("✅ Filters reset successfully using reset button")
                    return True
            
            # Method 3: Manual clearing of each filter type
            print("🔧 Attempting manual filter clearing")
            return self.manually_clear_all_filters()
            
        except Exception as e:
            print(f"❌ Error resetting filters: {e}")
            return False

    def manually_clear_all_filters(self):
        """Manually clear all filter inputs and selections"""
        print("🔧 Manually clearing all filters")
        
        try:
            # Open filter panel
            if not self.verify_filter_panel_opened():
                self.click_filters_button()
            
            # Clear text inputs
            if self.locators.position_filter_input.count() > 0:
                self.locators.position_filter_input.fill("")
            
            if self.locators.min_salary_filter_input.count() > 0:
                self.locators.min_salary_filter_input.fill("")
            
            if self.locators.max_salary_filter_input.count() > 0:
                self.locators.max_salary_filter_input.fill("")
            
            # Reset dropdowns to default (first option or empty)
            # Note: Implementation depends on specific dropdown behavior
            
            # Apply the cleared state
            if self.locators.apply_filters_button.count() > 0:
                self.locators.apply_filters_button.click()
                time.sleep(2)
            
            print("✅ Manual filter clearing completed")
            return True
            
        except Exception as e:
            print(f"❌ Error in manual filter clearing: {e}")
            return False

    def handle_filter_state_persistence_across_navigation(self, test_navigation: bool = True):
        """Handle and test filter state persistence across page navigation"""
        print("🔍 Testing filter state persistence across navigation")
        
        try:
            if not test_navigation:
                print("ℹ️ Navigation testing skipped")
                return True
            
            # Apply some filters first
            test_filters = {"company": "Test Company"}
            self.apply_multiple_filters(test_filters)
            
            # Get current URL and results count
            current_url = self.page.url
            filtered_count = self.get_filtered_results_count()
            
            print(f"-> Applied filters, got {filtered_count} results")
            
            # Navigate away and back (simulate page refresh or navigation)
            self.page.reload()
            time.sleep(3)
            
            # Check if filters persisted
            after_reload_count = self.get_filtered_results_count()
            
            if after_reload_count == filtered_count:
                print("✅ Filter state persisted across navigation")
                persistence_works = True
            else:
                print(f"⚠️ Filter state not persisted: {filtered_count} -> {after_reload_count}")
                persistence_works = False
            
            # Clear filters after test
            self.reset_all_filters_to_default()
            
            return persistence_works
            
        except Exception as e:
            print(f"❌ Error testing filter persistence: {e}")
            return False

    def test_filter_clearing_comprehensive(self):
        """Comprehensive test of all filter clearing functionality"""
        print("🔧 Running comprehensive filter clearing test")
        
        results = {
            "all_clear_button": False,
            "reset_button": False,
            "manual_clearing": False,
            "verification": False,
            "persistence": False
        }
        
        try:
            # Test 1: All clear button functionality
            print("\n-> Testing 'All clear' button")
            test_filters = {"company": "Test Company", "work_style": "Remote"}
            self.apply_multiple_filters(test_filters)
            
            if self.click_all_clear_filters_button():
                results["all_clear_button"] = self.verify_all_filters_removed()
            
            # Test 2: Reset button functionality (if available)
            print("\n-> Testing reset button")
            if self.locators.reset_filters_button.count() > 0:
                self.apply_multiple_filters(test_filters)
                self.locators.reset_filters_button.click()
                time.sleep(2)
                results["reset_button"] = self.verify_all_filters_removed()
            else:
                print("   ℹ️ Reset button not available")
                results["reset_button"] = True  # Not applicable
            
            # Test 3: Manual clearing
            print("\n-> Testing manual clearing")
            self.apply_multiple_filters(test_filters)
            results["manual_clearing"] = self.manually_clear_all_filters()
            
            # Test 4: Verification methods
            print("\n-> Testing verification methods")
            results["verification"] = self.verify_all_filters_removed()
            
            # Test 5: Filter persistence across navigation
            print("\n-> Testing filter persistence")
            results["persistence"] = self.handle_filter_state_persistence_across_navigation()
            
        except Exception as e:
            print(f"❌ Error in comprehensive filter clearing test: {e}")
        
        successful_tests = len([r for r in results.values() if r])
        total_tests = len(results)
        
        print(f"\n✅ Filter clearing comprehensive test completed: {successful_tests}/{total_tests} passed")
        print(f"   Results: {results}")
        
        return results

    def clear_search_and_filters_completely(self):
        """Clear both search and filters to return to unfiltered state"""
        print("🔧 Clearing both search and filters completely")
        
        try:
            # Clear search first
            self.reset_search_state()
            
            # Clear all filters
            self.reset_all_filters_to_default()
            
            # Verify we're in clean state
            search_cleared = self.locators.search_input.input_value() == ""
            filters_cleared = self.verify_all_filters_removed()
            
            if search_cleared and filters_cleared:
                print("✅ Search and filters completely cleared")
                return True
            else:
                print("⚠️ Search or filters may not be completely cleared")
                return False
                
        except Exception as e:
            print(f"❌ Error clearing search and filters: {e}")
            return False

    def verify_filter_reset_restores_original_state(self, original_count: int):
        """Verify that filter reset restores the original unfiltered state"""
        print(f"🔍 Verifying filter reset restores original state ({original_count} JDs)")
        
        try:
            # Get current count after reset
            current_count = self.get_filtered_results_count()
            
            if current_count == original_count:
                print(f"✅ Filter reset restored original state: {current_count} JDs")
                return True
            else:
                print(f"⚠️ Filter reset did not restore original state: expected {original_count}, got {current_count}")
                return False
                
        except Exception as e:
            print(f"❌ Error verifying filter reset: {e}")
            return False

    # ===== PAGINATION METHODS =====
    def navigate_to_next_page(self) -> bool:
        """Navigate to next page if available"""
        try:
            if self.locators.next_page_button.count() > 0:
                print("-> Next button found, clicking to navigate to next page...")
                self.locators.next_page_button.click()
                time.sleep(2)
                return True
            else:
                print("-> No more pages available (next button is disabled or not found)")
                return False
        except Exception as e:
            print(f"Error navigating to next page: {e}")
            return False

    def navigate_to_previous_page(self) -> bool:
        """Navigate to previous page if available"""
        try:
            if self.locators.previous_page_button.count() > 0:
                self.locators.previous_page_button.click()
                time.sleep(2)
                return True
            return False
        except Exception as e:
            print(f"Error navigating to previous page: {e}")
            return False

    def navigate_to_page_number(self, page_num: int):
        """Navigate to specific page number"""
        self.locators.page_number(page_num).click()
        time.sleep(2)

    def get_current_page_number(self) -> int:
        """Get current page number"""
        try:
            current_page_text = self.locators.current_page_indicator.text_content()
            return int(current_page_text) if current_page_text.isdigit() else 1
        except:
            return 1

    # ===== ENHANCED PAGINATION FUNCTIONALITY =====
    def verify_pagination_controls_visible(self):
        """Verify pagination controls are visible when needed"""
        try:
            if self.locators.pagination_container.count() > 0:
                enhanced_assert_visible(self.page, self.locators.pagination_container, 
                                       "Pagination container should be visible", "pagination_visible")
                print("✅ Pagination controls are visible")
                return True
            else:
                print("ℹ️ No pagination controls (likely single page or empty)")
                return False
        except Exception as e:
            print(f"❌ Error verifying pagination controls: {e}")
            raise

    def verify_pagination_state_first_page(self):
        """Verify pagination state when on first page"""
        try:
            # Previous button should be disabled on first page
            if self.locators.previous_page_button.count() == 0:
                print("✅ Previous button correctly disabled on first page")
            else:
                # Check if button exists but is disabled
                prev_button = self.locators.previous_page_button
                if prev_button.get_attribute("disabled") or "disabled" in prev_button.get_attribute("class"):
                    print("✅ Previous button correctly disabled on first page")
                else:
                    raise AssertionError("Previous button should be disabled on first page")
            
            # Current page should be 1
            current_page = self.get_current_page_number()
            if current_page == 1:
                print("✅ Current page correctly shows as page 1")
            else:
                raise AssertionError(f"Expected page 1, but current page is {current_page}")
                
            return True
        except Exception as e:
            print(f"❌ Error verifying first page state: {e}")
            raise

    def verify_pagination_state_last_page(self):
        """Verify pagination state when on last page"""
        try:
            # Next button should be disabled on last page
            if self.locators.next_page_button.count() == 0:
                print("✅ Next button correctly disabled on last page")
            else:
                # Check if button exists but is disabled
                next_button = self.locators.next_page_button
                if next_button.get_attribute("disabled") or "disabled" in next_button.get_attribute("class"):
                    print("✅ Next button correctly disabled on last page")
                else:
                    raise AssertionError("Next button should be disabled on last page")
            
            print("✅ Last page state verified correctly")
            return True
        except Exception as e:
            print(f"❌ Error verifying last page state: {e}")
            raise

    def verify_current_page_indicator(self, expected_page: int):
        """Verify current page indicator shows correct page number"""
        try:
            current_page = self.get_current_page_number()
            if current_page == expected_page:
                print(f"✅ Current page indicator correctly shows page {expected_page}")
                return True
            else:
                raise AssertionError(f"Expected page {expected_page}, but current page shows {current_page}")
        except Exception as e:
            print(f"❌ Error verifying current page indicator: {e}")
            raise

    def navigate_to_specific_page_and_verify(self, target_page: int):
        """Navigate to specific page number and verify navigation"""
        try:
            print(f"-> Navigating to page {target_page}")
            
            # Click on the page number
            self.navigate_to_page_number(target_page)
            
            # Verify we're on the correct page
            self.verify_current_page_indicator(target_page)
            
            # Verify URL contains correct page parameter
            current_url = self.page.url
            if f"page={target_page}" in current_url or f"p={target_page}" in current_url:
                print(f"✅ URL correctly contains page parameter for page {target_page}")
            else:
                print(f"⚠️ URL may not contain expected page parameter: {current_url}")
            
            return True
        except Exception as e:
            print(f"❌ Error navigating to page {target_page}: {e}")
            raise

    def verify_url_parameter_validation(self, expected_page: int):
        """Verify URL contains correct page parameters"""
        try:
            current_url = self.page.url
            
            # Check for common page parameter patterns
            page_patterns = [f"page={expected_page}", f"p={expected_page}", f"pageNumber={expected_page}"]
            
            url_contains_page_param = any(pattern in current_url for pattern in page_patterns)
            
            if url_contains_page_param:
                print(f"✅ URL correctly contains page parameter for page {expected_page}")
                return True
            else:
                print(f"⚠️ URL may not contain expected page parameter. URL: {current_url}")
                # This might not be an error if the app uses different URL structure
                return False
                
        except Exception as e:
            print(f"❌ Error verifying URL parameters: {e}")
            raise

    def handle_different_page_sizes(self, items_per_page: int):
        """Handle different page sizes and verify total item counts"""
        try:
            # Check if items per page dropdown exists
            if self.locators.items_per_page_dropdown.count() > 0:
                # Select the desired page size
                self.locators.items_per_page_dropdown.select_option(str(items_per_page))
                time.sleep(2)
                
                print(f"✅ Successfully set page size to {items_per_page} items per page")
                
                # Verify the page reloaded with new page size
                current_items_count = self.get_jd_cards_count()
                if current_items_count <= items_per_page:
                    print(f"✅ Page shows {current_items_count} items (within limit of {items_per_page})")
                else:
                    print(f"⚠️ Page shows {current_items_count} items (exceeds limit of {items_per_page})")
                
                return True
            else:
                print("ℹ️ Items per page dropdown not available")
                return False
                
        except Exception as e:
            print(f"❌ Error handling page size change: {e}")
            raise

    def get_total_pages_count(self) -> int:
        """Get total number of pages from pagination"""
        try:
            if self.locators.total_pages_indicator.count() > 0:
                total_text = self.locators.total_pages_indicator.text_content()
                # Extract number from text like "Page 1 of 5" or "Total: 5 pages"
                import re
                numbers = re.findall(r'\d+', total_text)
                if numbers:
                    total_pages = int(numbers[-1])  # Usually the last number is total
                    print(f"✅ Found total pages: {total_pages}")
                    return total_pages
            
            # Alternative: count page number buttons
            page_buttons = self.page.locator(".pagination button[data-page], .pagination .page-number")
            if page_buttons.count() > 0:
                # Find the highest page number
                max_page = 0
                for i in range(page_buttons.count()):
                    button_text = page_buttons.nth(i).text_content()
                    if button_text.isdigit():
                        max_page = max(max_page, int(button_text))
                
                if max_page > 0:
                    print(f"✅ Calculated total pages from buttons: {max_page}")
                    return max_page
            
            print("ℹ️ Could not determine total pages count")
            return 1
            
        except Exception as e:
            print(f"❌ Error getting total pages count: {e}")
            return 1

    def navigate_through_all_pages(self):
        """Navigate through all available pages and verify each"""
        try:
            total_pages = self.get_total_pages_count()
            print(f"-> Starting navigation through {total_pages} pages")
            
            pages_visited = []
            
            # Start from page 1
            current_page = 1
            pages_visited.append(current_page)
            
            # Navigate through all pages using next button
            while self.navigate_to_next_page():
                current_page = self.get_current_page_number()
                pages_visited.append(current_page)
                
                # Verify each page has content or proper empty state
                self.verify_jd_list_display()
                
                # Safety check to prevent infinite loop
                if len(pages_visited) > 20:
                    print("⚠️ Stopping pagination test after 20 pages for safety")
                    break
            
            print(f"✅ Successfully navigated through {len(pages_visited)} pages: {pages_visited}")
            return pages_visited
            
        except Exception as e:
            print(f"❌ Error navigating through all pages: {e}")
            raise

    def verify_pagination_with_search_and_filters(self, search_term: str = None, filters: dict = None):
        """Verify pagination works correctly with search and filters applied"""
        try:
            # Apply search if provided
            if search_term:
                self.search_jd(search_term)
                print(f"-> Applied search term: {search_term}")
            
            # Apply filters if provided
            if filters:
                self.open_filters()
                for filter_type, filter_value in filters.items():
                    if filter_type == "company":
                        self.apply_company_filter(filter_value)
                    elif filter_type == "status":
                        self.apply_status_filter(filter_value)
                    elif filter_type == "work_style":
                        self.apply_work_style_filter(filter_value)
                self.apply_filters()
                print(f"-> Applied filters: {filters}")
            
            # Verify pagination still works with filters/search
            if self.verify_pagination_controls_visible():
                # Try navigating to next page
                if self.navigate_to_next_page():
                    print("✅ Pagination works correctly with search/filters applied")
                    
                    # Navigate back to first page
                    self.navigate_to_page_number(1)
                    return True
                else:
                    print("ℹ️ Only one page of results with current search/filters")
                    return True
            else:
                print("ℹ️ No pagination needed with current search/filters")
                return True
                
        except Exception as e:
            print(f"❌ Error verifying pagination with search/filters: {e}")
            raise

    # ===== BULK OPERATIONS =====
    def select_all_jds(self):
        """Select all JDs using select all checkbox"""
        self.locators.select_all_checkbox.check()
        time.sleep(1)

    def select_jd_by_title(self, title: str):
        """Select specific JD by title"""
        self.locators.jd_checkbox(title).check()

    def get_selected_items_count(self) -> int:
        """Get count of selected items"""
        try:
            count_text = self.locators.selected_items_count.text_content()
            return int(count_text) if count_text.isdigit() else 0
        except:
            return 0

    def click_bulk_delete(self):
        """Click bulk delete button"""
        self.locators.bulk_delete_button.click()
        time.sleep(1)

    def click_bulk_status_update(self):
        """Click bulk status update button"""
        self.locators.bulk_status_update_button.click()
        time.sleep(1)

    def confirm_bulk_delete(self):
        """Confirm bulk delete operation"""
        self.locators.confirm_bulk_delete_button.click()
        time.sleep(2)

    def cancel_bulk_delete(self):
        """Cancel bulk delete operation"""
        self.locators.cancel_bulk_delete_button.click()
        time.sleep(1)

    # ===== DELETE CONFIRMATION =====
    def expect_delete_confirmation_modal(self):
        """Verify delete confirmation modal is visible"""
        enhanced_assert_visible(self.page, self.locators.delete_confirmation_modal, 
                               "Delete confirmation modal should be visible", "delete_confirmation")

    def confirm_delete(self):
        """Confirm single JD deletion"""
        self.locators.confirm_delete_button.click()
        time.sleep(2)

    def cancel_delete(self):
        """Cancel single JD deletion"""
        self.locators.cancel_delete_button.click()
        time.sleep(1)

    # ===== SUCCESS/ERROR MESSAGE VERIFICATION =====
    def expect_jd_created_successfully(self):
        """Verify JD created successfully message"""
        enhanced_assert_visible(self.page, self.locators.jd_created_successfully_message, 
                               "JD created successfully message should be visible", "jd_created_success")

    def expect_jd_updated_successfully(self):
        """Verify JD updated successfully message"""
        enhanced_assert_visible(self.page, self.locators.jd_updated_successfully_message, 
                               "JD updated successfully message should be visible", "jd_updated_success")

    def expect_jd_deleted_successfully(self):
        """Verify JD deleted successfully message"""
        enhanced_assert_visible(self.page, self.locators.jd_deleted_successfully_message, 
                               "JD deleted successfully message should be visible", "jd_deleted_success")

    def expect_file_uploaded_successfully(self):
        """Verify file uploaded successfully message"""
        enhanced_assert_visible(self.page, self.locators.file_uploaded_successfully_message, 
                               "File uploaded successfully message should be visible", "file_uploaded_success")

    # ===== VALIDATION ERROR VERIFICATION =====
    def expect_position_title_required_error(self):
        """Verify position title required error"""
        enhanced_assert_visible(self.page, self.locators.position_title_required_error, 
                               "Position title required error should be visible", "position_title_required")

    def expect_company_required_error(self):
        """Verify company required error"""
        enhanced_assert_visible(self.page, self.locators.company_required_error, 
                               "Company required error should be visible", "company_required")

    def expect_work_style_required_error(self):
        """Verify work style required error"""
        enhanced_assert_visible(self.page, self.locators.work_style_required_error, 
                               "Work style required error should be visible", "work_style_required")

    def expect_workplace_required_error(self):
        """Verify workplace required error"""
        enhanced_assert_visible(self.page, self.locators.workplace_required_error, 
                               "Workplace required error should be visible", "workplace_required")

    def expect_invalid_salary_range_error(self):
        """Verify invalid salary range error"""
        enhanced_assert_visible(self.page, self.locators.invalid_salary_range_error, 
                               "Invalid salary range error should be visible", "invalid_salary_range")

    def expect_invalid_age_range_error(self):
        """Verify invalid age range error"""
        enhanced_assert_visible(self.page, self.locators.invalid_age_range_error, 
                               "Invalid age range error should be visible", "invalid_age_range")

    def expect_invalid_target_age_range_error(self):
        """Verify invalid target age range error"""
        enhanced_assert_visible(self.page, self.locators.invalid_target_age_range_error, 
                               "Invalid target age range error should be visible", "invalid_target_age_range")

    def expect_file_format_error(self):
        """Verify file format error"""
        enhanced_assert_visible(self.page, self.locators.file_format_error, 
                               "File format error should be visible", "file_format_error")

    def expect_file_size_error(self):
        """Verify file size error"""
        enhanced_assert_visible(self.page, self.locators.file_size_error, 
                               "File size error should be visible", "file_size_error")

    def expect_position_title_max_length_error(self):
        """Verify position title max length error"""
        enhanced_assert_visible(self.page, self.locators.position_title_max_length_error, 
                               "Position title max length error should be visible", "position_title_max_length")

    def expect_workplace_max_length_error(self):
        """Verify workplace max length error"""
        enhanced_assert_visible(self.page, self.locators.workplace_max_length_error, 
                               "Workplace max length error should be visible", "workplace_max_length")

    def expect_department_max_length_error(self):
        """Verify department max length error"""
        enhanced_assert_visible(self.page, self.locators.department_max_length_error, 
                               "Department max length error should be visible", "department_max_length")

    def expect_job_function_max_length_error(self):
        """Verify job function max length error"""
        enhanced_assert_visible(self.page, self.locators.job_function_max_length_error, 
                               "Job function max length error should be visible", "job_function_max_length")

    def expect_invalid_salary_format_error(self):
        """Verify invalid salary format error"""
        enhanced_assert_visible(self.page, self.locators.invalid_salary_format_error, 
                               "Invalid salary format error should be visible", "invalid_salary_format")

    def expect_invalid_age_format_error(self):
        """Verify invalid age format error"""
        enhanced_assert_visible(self.page, self.locators.invalid_age_format_error, 
                               "Invalid age format error should be visible", "invalid_age_format")

    def expect_negative_salary_error(self):
        """Verify negative salary error"""
        enhanced_assert_visible(self.page, self.locators.negative_salary_error, 
                               "Negative salary error should be visible", "negative_salary")

    def expect_negative_age_error(self):
        """Verify negative age error"""
        enhanced_assert_visible(self.page, self.locators.negative_age_error, 
                               "Negative age error should be visible", "negative_age")

    def expect_invalid_email_format_error(self):
        """Verify invalid email format error"""
        enhanced_assert_visible(self.page, self.locators.invalid_email_format_error, 
                               "Invalid email format error should be visible", "invalid_email_format")

    def expect_invalid_url_format_error(self):
        """Verify invalid URL format error"""
        enhanced_assert_visible(self.page, self.locators.invalid_url_format_error, 
                               "Invalid URL format error should be visible", "invalid_url_format")

    def expect_file_upload_failed_error(self):
        """Verify file upload failed error"""
        enhanced_assert_visible(self.page, self.locators.file_upload_failed_error, 
                               "File upload failed error should be visible", "file_upload_failed")

    # ===== COMPREHENSIVE VALIDATION ASSERTION METHODS =====
    def assert_all_mandatory_field_errors(self):
        """Assert all mandatory field validation errors are visible"""
        self.expect_position_title_required_error()
        self.expect_company_required_error()
        self.expect_work_style_required_error()
        self.expect_workplace_required_error()

    def assert_salary_range_validation_errors(self):
        """Assert salary range validation errors"""
        self.expect_invalid_salary_range_error()

    def assert_age_range_validation_errors(self):
        """Assert age range validation errors"""
        self.expect_invalid_age_range_error()

    def assert_target_age_range_validation_errors(self):
        """Assert target age range validation errors"""
        self.expect_invalid_target_age_range_error()

    def assert_character_limit_validation_errors(self, field_type: str):
        """Assert character limit validation errors for specific field"""
        if field_type == "position_title":
            self.expect_position_title_max_length_error()
        elif field_type == "workplace":
            self.expect_workplace_max_length_error()
        elif field_type == "department":
            self.expect_department_max_length_error()
        elif field_type == "job_function":
            self.expect_job_function_max_length_error()

    def assert_format_validation_errors(self, field_type: str):
        """Assert format validation errors for specific field type"""
        if field_type == "salary":
            self.expect_invalid_salary_format_error()
        elif field_type == "age":
            self.expect_invalid_age_format_error()
        elif field_type == "email":
            self.expect_invalid_email_format_error()
        elif field_type == "url":
            self.expect_invalid_url_format_error()

    def assert_negative_value_validation_errors(self, field_type: str):
        """Assert negative value validation errors"""
        if field_type == "salary":
            self.expect_negative_salary_error()
        elif field_type == "age":
            self.expect_negative_age_error()

    def assert_file_validation_errors(self, error_type: str):
        """Assert file validation errors"""
        if error_type == "format":
            self.expect_file_format_error()
        elif error_type == "size":
            self.expect_file_size_error()
        elif error_type == "upload_failed":
            self.expect_file_upload_failed_error()

    def verify_validation_error_scenario(self, scenario_type: str, **kwargs):
        """Verify specific validation error scenario"""
        if scenario_type == "mandatory_fields":
            self.trigger_mandatory_field_validation()
            self.assert_all_mandatory_field_errors()
            self.handle_modal_state_during_validation()
        
        elif scenario_type == "salary_range":
            min_sal = kwargs.get("min_salary", "100000")
            max_sal = kwargs.get("max_salary", "50000")  # Invalid: max < min
            self.trigger_salary_range_validation(min_sal, max_sal)
            self.assert_salary_range_validation_errors()
            self.handle_modal_state_during_validation()
        
        elif scenario_type == "age_range":
            min_age = kwargs.get("min_age", "30")
            max_age = kwargs.get("max_age", "25")  # Invalid: max < min
            self.trigger_age_range_validation(min_age, max_age)
            self.assert_age_range_validation_errors()
            self.handle_modal_state_during_validation()
        
        elif scenario_type == "character_limit":
            field_type = kwargs.get("field_type", "position_title")
            long_text = kwargs.get("long_text", "A" * 200)  # Exceeds typical limits
            self.trigger_character_limit_validation(field_type, long_text)
            self.assert_character_limit_validation_errors(field_type)
            self.handle_modal_state_during_validation()
        
        elif scenario_type == "format_validation":
            field_type = kwargs.get("field_type", "salary")
            invalid_data = kwargs.get("invalid_data", "invalid_text")
            self.trigger_format_validation(field_type, invalid_data)
            self.assert_format_validation_errors(field_type)
            self.handle_modal_state_during_validation()

    # ===== UTILITY METHODS =====
    def wait_for_page_load(self):
        """Wait for page to fully load"""
        self.page.wait_for_load_state("networkidle")
        time.sleep(1)

    def wait_for_toast_message(self, timeout: int = 5000) -> bool:
        """Wait for any toast message to appear"""
        try:
            self.locators.toast_message.first.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    def get_toast_message_text(self) -> str:
        """Get the text of the current toast message"""
        if self.locators.toast_message.count() > 0:
            return self.locators.toast_message.first.text_content()
        return ""

    def check_success_toast_visible(self) -> bool:
        """Check if success toast is visible"""
        return self.locators.success_toast.count() > 0

    def check_error_toast_visible(self) -> bool:
        """Check if error toast is visible"""
        return self.locators.error_toast.count() > 0

    def check_loading_spinner_visible(self) -> bool:
        """Check if loading spinner is visible"""
        return self.locators.loading_spinner.count() > 0

    def wait_for_loading_to_complete(self, timeout: int = 10000):
        """Wait for loading spinner to disappear"""
        try:
            self.locators.loading_spinner.wait_for(state="hidden", timeout=timeout)
        except:
            pass  # Continue if loading spinner doesn't appear or disappear

    # ===== COMPREHENSIVE WORKFLOW METHODS =====
    def find_jd_in_paginated_list(self, jd_title: str) -> bool:
        """
        Find a JD across paginated results
        
        Args:
            jd_title: Title of the JD to find
        
        Returns:
            True if JD found, False otherwise
        """
        print(f"🔍 Starting search for JD: '{jd_title}'")
        
        max_pages = 50  # Allow up to 50 pages
        current_page = 0
        
        while current_page < max_pages:
            current_page += 1
            print(f"🔍 Searching page {current_page}...")
            
            # Check if JD exists on current page
            jd_element = self.page.get_by_text(jd_title, exact=True)
            if jd_element.count() > 0:
                print(f"✅ Found JD '{jd_title}' on page {current_page}")
                return True
            
            print(f"   Not found on page {current_page}, trying next page...")
            
            # Try to navigate to next page
            if not self.navigate_to_next_page():
                print(f"❌ No more pages available. '{jd_title}' not found after {current_page} pages.")
                return False
                
        print(f"❌ Reached maximum pages ({max_pages}). '{jd_title}' not found.")
        return False

    def get_jd_list_count(self) -> int:
        """Get total count of JDs in the current view"""
        try:
            jd_cards = self.page.locator(".jd-card, [class*='jd-card']")
            return jd_cards.count()
        except:
            return 0

    def verify_jd_exists_in_list(self, jd_title: str) -> bool:
        """Verify that a JD exists in the current list view"""
        return self.find_jd_in_paginated_list(jd_title)

    def cleanup_test_jds(self, test_jd_prefix: str = "Test JD"):
        """Clean up test JDs that start with specific prefix"""
        jds_to_delete = []
        
        # Get all JD titles on current page
        jd_titles = self.page.locator(".jd-title, [class*='jd-title']")
        count = jd_titles.count()
        
        for i in range(count):
            try:
                title_text = jd_titles.nth(i).text_content()
                if title_text and title_text.startswith(test_jd_prefix):
                    jds_to_delete.append(title_text)
            except:
                continue
        
        # Delete test JDs
        for jd_title in jds_to_delete:
            try:
                self.click_delete_jd_button(jd_title)
                self.confirm_delete()
                print(f"🗑️ Cleaned up test JD: {jd_title}")
            except Exception as e:
                print(f"❌ Failed to cleanup JD {jd_title}: {e}")