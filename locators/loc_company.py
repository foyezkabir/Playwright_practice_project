from playwright.sync_api import Page, Locator
import re

class CompanyLocators:
    def __init__(self, page: Page):
        self.page = page

        # Login page locators
        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.sign_in_button = page.get_by_role("button", name="Sign in")
        
        # Navigation locators
        self.company_tab = page.get_by_role("link", name="Company")
        self.company_tab_alt = page.locator("text=Company").first
        
        # Agency selection locators  
        self.agency_card = lambda agency_name: page.locator(f"text={agency_name}").first
        self.test_agency_card = page.get_by_text("Test this agency")
        
        # Company list page locators
        self.add_new_company_button = page.get_by_role("button", name="Add new company")
        self.create_new_company_button = page.get_by_role("button", name="Create new company")
        self.add_company_button = page.get_by_text("Add new company")
        self.no_companies_found_message = page.get_by_text("No companies found Add new")
        
        # Company form locators - Basic fields
        self.company_name_input = page.get_by_role("textbox", name="Name")
        self.company_name_field = page.locator("input[name='companyName'], input[placeholder*='Company'], input[placeholder*='company']")
        
        # Industry dropdown and options
        self.industry_dropdown = page.locator(".select-trigger").first
        self.information_technology_option = page.locator("div").filter(has_text=re.compile(r"^Information Technology$"))
        self.finance_option = page.get_by_text("Finance", exact=True)
        self.healthcare_option = page.get_by_text("Healthcare", exact=True) 
        self.technology_option = page.get_by_text("Technology", exact=True)
        self.education_option = page.get_by_text("Education", exact=True)
        self.retail_option = page.get_by_text("Retail")
        
        # Extended company form fields
        self.website_input = page.get_by_role("textbox", name="Web page")
        self.total_employees_input = page.get_by_role("textbox", name="Total Employees JPN")
        self.address_input = page.get_by_role("textbox", name="Address")
        self.main_tel_input = page.get_by_role("textbox", name="Main Tel")
        self.hr_tel_input = page.get_by_role("textbox", name="HR TEL")
        
        # Hiring status dropdown and options
        self.hiring_status_dropdown = page.locator(".select-trigger.open")
        # self.hiring_active_option = page.get_by_text("Active", exact=True)
        self.hiring_active_option = page.get_by_text("Active")
        self.hiring_inactive_option = page.get_by_text("Inactive")
        self.hiring_on_hold_option = page.get_by_text("On Hold")
        self.hiring_recruiting_option = page.get_by_text("Recruiting")
        
        # Company grade dropdown and options
        self.company_grade_dropdown = page.locator("div:nth-child(7) > .custom-searchable-select > .searchable-select > .select-trigger")
        # self.grade_aaa_option = page.locator("div").filter(has_text=re.compile(r"^AAA$"))
        #self.grade_aa_option = page.get_by_text("AA", exact=True)
        self.grade_aa_option = page.get_by_text("AA")
        self.grade_bbb_option = page.get_by_text("BBB")
        self.grade_aaa_option = page.get_by_text("AAA")
        
        # HQ in Japan dropdown and options
        self.hq_in_japan_dropdown = page.locator("div:nth-child(8) > .custom-searchable-select > .searchable-select > .select-trigger")
        self.hq_yes_option = page.get_by_text("Yes")
        self.hq_no_option = page.get_by_text("No")
        # self.hq_no_option = page.get_by_text("No", exact=True)
        
        # Job opening dropdown and options
        self.job_opening_dropdown = page.locator("div:nth-child(9) > .custom-searchable-select > .searchable-select > .select-trigger")
        self.job_opening_yes_option = page.get_by_text("Yes")
        self.job_opening_no_option = page.get_by_text("No")
        # self.job_opening_no_option = page.get_by_text("No").nth(2)
        
        # Owner dropdown
        self.owner_dropdown = page.locator("div:nth-child(10) > .custom-searchable-select > .searchable-select > .select-trigger")
        # self.owner_test_option = page.locator("div").filter(has_text=re.compile(r"^test$")).nth(3)
        self.owner_option = page.get_by_text("test")
        
        # File upload
        # self.company_logo_upload = page.locator("body")
        self.upload_logo_text = page.get_by_text("Upload Logo")
        
        # Action buttons
        self.create_button = page.get_by_role("button", name="Create")
        self.save_button = page.get_by_role("button", name="Save")
        self.update_button = page.get_by_role("button", name="Update")
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.close_modal_button = page.get_by_role("button", name="Close modal")
        
        # Company actions and menus
        self.view_details_button = page.get_by_role("button", name="View Details")
        self.three_dot_menu = page.get_by_role("main").get_by_role("button").filter(has_text=re.compile(r"^$"))
        self.edit_company_button = page.get_by_role("button", name="Edit")
        self.delete_company_button = page.get_by_role("button", name="Delete")
        
        # Delete confirmation modal
        self.delete_confirm_modal = page.get_by_text("Are you sure you want to delete this company?This action cannot be undone. All")
        self.confirm_delete_button = page.get_by_role("button", name="Confirm")
        
        # Company profile page tabs
        self.summary_tab = page.get_by_role("button", name="Summary")
        self.basic_company_info_tab = page.get_by_role("button", name="Basic company info")
        self.web_contact_info_tab = page.get_by_role("button", name="Web & Contact info")
        self.location_details_tab = page.get_by_role("button", name="Location details")
        self.employees_business_info_tab = page.get_by_role("button", name="Employees & Business info")
        
        # Navigation breadcrumb
        self.home_company_heading = page.get_by_text("Home>Company")
        self.breadcrumb_home = page.get_by_text("Home")
        self.breadcrumb_company = page.get_by_text("Company")
        
        # Success and validation messages
        self.company_created_successfully_message = page.get_by_text("Company created successfully")
        self.company_added_successfully_message = page.get_by_text("Company added successfully")
        self.company_updated_successfully_message = page.get_by_text("Company info updated successfully")
        self.company_deleted_successfully_message = page.get_by_text("Company remove successfully")
        self.file_size_error = page.get_by_text("File can't be larger than 5 MB")
        self.file_type_error = page.get_by_text("Only accept jpg, png, jpeg, gif file")
        
        # Validation error messages - Company Name
        self.company_name_required_error = page.get_by_text("Company name is required.")
        self.company_name_already_exists_error = page.get_by_text("Company name already exists")
        self.company_name_min_length_error = page.get_by_text("Company name must be at least 3 characters.")
        self.company_name_max_length_error = page.get_by_text("Company name must be at most 80 characters.")
        self.company_name_special_char_error = page.get_by_text("Company name should not start or end with special characters.")
        
        # Validation error messages - Other fields
        self.industry_required_error = page.get_by_text("Industry is required.")
        self.website_required_error = page.get_by_text("Website is required.")
        self.address_required_error = page.get_by_text("Address is required.")
        self.owner_required_error = page.get_by_text("Owner is required")
        self.division_required_error = page.get_by_text("Division is required")
        
        # Company dependency messages
        self.company_required_error = page.get_by_text("Company is required.")
        self.company_required_for_client_error = page.get_by_text("Company must be selected before choosing a client")
        
        # Company profile page locators
        self.company_profile_heading = lambda company_name: page.get_by_role("heading", name=company_name)
        self.company_details_section = page.locator(".company-details, [data-testid='company-details']")
        
        # Client tab and management
        self.client_tab = page.get_by_role("button", name="Client")
        # self.clients_tab = page.get_by_text("Client", exact=True)
        self.no_clients_found_message = page.get_by_text("No clients found Add new")
        self.add_new_client_button = page.get_by_role("button", name="Add new client")
        self.create_client_button = page.get_by_role("button", name="Create")
        self.add_client_button = page.get_by_text("Add Client")
        
        # Client form fields - Names and Basic Info
        self.client_english_name_input = page.get_by_role("textbox", name="English name")
        self.client_japanese_name_input = page.get_by_role("textbox", name="Japanese name")
        self.client_job_title_input = page.get_by_role("textbox", name="Job title")
        self.client_department_input = page.get_by_role("textbox", name="Department")
        
        # Client gender dropdown
        self.client_gender_dropdown = page.locator(".select-trigger").first
        self.client_female_option = page.get_by_text("Female")
        self.client_male_option = page.get_by_text("Male")
        # self.client_male_option = page.get_by_text("Male", exact=True)
        
        # Client language skills dropdowns
        self.client_english_skill_dropdown = page.locator("div:nth-child(6) > .searchable-select > .select-trigger")
        # self.client_basic_option = page.get_by_text("Basic", exact=True)
        self.client_basic_option = page.get_by_text("Basic")
        self.client_japanese_skill_dropdown = page.locator("div:nth-child(7) > .searchable-select > .select-trigger")
        self.client_conversational_option = page.get_by_text("Conversational")
        
        # Client contact information
        self.client_phone_name_input = page.locator("[id=\"phone_contacts[0].name\"]")
        self.client_phone_number_input = page.get_by_role("textbox", name="Number")

        self.client_email_name_input = page.locator("[id=\"email_contacts[0].name\"]")
        self.client_email_input = page.get_by_role("textbox", name="Email")

        self.add_email_button = page.get_by_role("button", name="+ Add Email Address")
        
        # Client validation messages
        self.client_name_required_error = page.get_by_text("Client name is required")
        self.client_email_required_error = page.get_by_text("At least one email address is")
        self.client_created_successfully_message = page.get_by_text("Client created successfully")
        
        # Client management
        self.select_all_clients = page.get_by_text("Select All")
        self.selected_delete_text = page.get_by_text("SelectedDelete (1)").first
        self.add_new_client_modal_heading = page.get_by_role("heading", name="Add New Client")
        
        # Company list and search
        self.company_list_container = page.locator(".company-list, [data-testid='company-list']")
        self.company_search_input = page.get_by_placeholder("Search companies...")
        self.no_companies_message = page.get_by_text("No companies found")
        
        # Created company reference (dynamic)
        self.created_company_heading = lambda company_name: page.get_by_role("heading", name=company_name)
        self.created_client_heading = lambda client_name: page.get_by_role("heading", name=client_name)
        
        # Modal and overlay
        self.modal_overlay = page.locator(".modal-overlay, .backdrop")
        self.company_modal = page.locator(".modal, [role='dialog']")
        
        # Toast notifications
        self.toast_message = page.get_by_role("alert")
        self.success_toast = page.locator(".toast-success, .alert-success")
        self.error_toast = page.locator(".toast-error, .alert-error")
