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
        self.agency_t_selector = page.locator("div").filter(has_text=re.compile(r"^T$")).nth(2)
        
        # Company list navigation locators
        self.first_company_link = page.locator(".text-primary-color.font-medium.text-base").first
        self.company_name_heading_link = lambda company_name: page.get_by_role("heading", name=company_name)
        self.company_name_text_link = lambda company_name: page.get_by_text(company_name, exact=True).first
        
        # Company details page - Summary tab editable fields
        # Field display locators
        self.company_name_display = page.locator("div").filter(has_text="Company name").locator("xpath=following-sibling::div").first
        self.web_page_display = page.locator("div").filter(has_text="Web page").locator("xpath=following-sibling::div").first
        self.industry_display = page.locator("div").filter(has_text="Industry").locator("xpath=following-sibling::div").first
        self.hq_in_jpn_display = page.locator("div").filter(has_text="HQ in JPN").locator("xpath=following-sibling::div").first
        self.global_hq_display = page.locator("div").filter(has_text="Global HQ").locator("xpath=following-sibling::div").first
        self.country_of_origin_display = page.locator("div").filter(has_text="Country of origin").locator("xpath=following-sibling::div").first
        self.company_address_display = page.locator("div").filter(has_text="Company address").locator("xpath=following-sibling::div").first
        self.company_hiring_status_display = page.locator("div").filter(has_text="Company hiring status").locator("xpath=following-sibling::div")
        self.job_opening_display = page.locator("div").filter(has_text="Job opening").locator("xpath=following-sibling::div")
        self.total_employees_jpn_display = page.locator("div").filter(has_text="Total employees JPN").locator("xpath=following-sibling::div")
        self.company_grade_display = page.locator("div").filter(has_text="Company grade").locator("xpath=following-sibling::div")
        self.company_client_owner_display = page.locator("div").filter(has_text="Company client owner").locator("xpath=following-sibling::div")
        self.telephone_display = page.locator("div").filter(has_text="Telephone").locator("xpath=following-sibling::div")
        
        # Edit icon locators for each field
        self.company_name_edit_icon = page.locator("div").filter(has_text=re.compile(r"^:.*$")).filter(has_text="Company name").get_by_role("img")
        self.web_page_edit_icon = page.locator("div").filter(has_text=re.compile(r"^:.*$")).filter(has_text="Web page").get_by_role("img") 
        self.industry_edit_icon = page.locator("div").filter(has_text=re.compile(r"^:.*$")).filter(has_text="Industry").get_by_role("img")
        self.hq_in_jpn_edit_icon = page.locator("div").filter(has_text=re.compile(r"^:.*$")).filter(has_text="HQ in JPN").get_by_role("img")
        self.global_hq_edit_icon = page.locator("div").filter(has_text=re.compile(r"^:.*$")).filter(has_text="Global HQ").get_by_role("img")
        self.country_of_origin_edit_icon = page.locator("div").filter(has_text=re.compile(r"^:.*$")).filter(has_text="Country of origin").get_by_role("img")
        self.company_address_edit_icon = page.locator("div").filter(has_text=re.compile(r"^:.*$")).filter(has_text="Company address").get_by_role("img")
        self.company_hiring_status_edit_icon = page.locator("div").filter(has_text=re.compile(r"^:.*$")).filter(has_text="Company hiring status").get_by_role("img")
        self.job_opening_edit_icon = page.locator("div").filter(has_text=re.compile(r"^:.*$")).filter(has_text="Job opening").get_by_role("img")
        self.total_employees_jpn_edit_icon = page.locator("div").filter(has_text=re.compile(r"^:.*$")).filter(has_text="Total employees JPN").get_by_role("img")
        self.company_grade_edit_icon = page.locator("div").filter(has_text=re.compile(r"^:.*$")).filter(has_text="Company grade").get_by_role("img")
        self.company_client_owner_edit_icon = page.locator("div").filter(has_text=re.compile(r"^:.*$")).filter(has_text="Company client owner").get_by_role("img")
        self.telephone_edit_icon = page.locator("div").filter(has_text=re.compile(r"^:.*$")).filter(has_text="Telephone").get_by_role("img")
        
        # Edit modal input fields  
        self.edit_company_name_input = page.get_by_role("textbox", name="Company name")
        self.edit_web_page_input = page.get_by_role("textbox", name="Web page")
        self.edit_industry_dropdown = page.locator(".select-trigger")
        self.edit_hq_in_jpn_dropdown = page.locator(".select-trigger")
        self.edit_global_hq_input = page.get_by_role("textbox", name="Global HQ")
        self.edit_country_of_origin_input = page.get_by_role("textbox", name="Country of origin")
        self.edit_company_address_input = page.get_by_role("textbox", name="Company address")
        self.edit_company_hiring_status_dropdown = page.locator(".select-trigger")
        self.edit_job_opening_dropdown = page.locator(".select-trigger")
        self.edit_total_employees_jpn_input = page.get_by_role("textbox", name="Total employees JPN")
        self.edit_company_grade_dropdown = page.locator(".select-trigger")
        self.edit_company_client_owner_dropdown = page.locator(".select-trigger")
        self.edit_telephone_input = page.get_by_role("textbox", name="Telephone")
        
        # Edit modal buttons
        self.edit_modal_save_button = page.get_by_role("button", name="Save")
        self.edit_modal_cancel_button = page.get_by_role("button", name="Cancel")
        
        # Company details page navigation
        self.summary_tab = page.get_by_role("button", name="Summary")
        self.company_details_heading = lambda company_name: page.get_by_role("heading", name=company_name, level=1)
        
        # Company list page locators
        self.add_new_company_button = page.get_by_role("button", name="Add new company")
        self.create_new_company_button = page.get_by_role("button", name="Create new company")
        self.add_company_button = page.get_by_text("Add company")
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
        self.hiring_status_dropdown = page.locator("div:nth-child(5) > .custom-searchable-select > .searchable-select > .select-trigger > .trigger-content")
        self.hiring_active_option = page.locator("div").filter(has_text=re.compile(r"^Active$")).nth(1)
        self.hiring_inactive_option = page.locator("div").filter(has_text=re.compile(r"^Inactive$")).nth(1)
        self.hiring_on_hold_option = page.locator("div").filter(has_text=re.compile(r"^On Hold$"))
        self.hiring_recruiting_option = page.locator("div").filter(has_text=re.compile(r"^Recruiting$"))
        
        # Company grade dropdown and options
        self.company_grade_dropdown = page.locator("div:nth-child(7) > .custom-searchable-select > .searchable-select > .select-trigger")
        self.grade_aaa_option = page.get_by_text("AAA", exact=True)
        self.grade_aa_option = page.get_by_text("AA", exact=True)
        self.grade_a_option = page.get_by_text("A", exact=True)
        self.grade_bbb_option = page.get_by_text("BBB", exact=True)
        
        # HQ in Japan dropdown and options
        self.hq_in_japan_dropdown = page.locator("div:nth-child(8) > .custom-searchable-select > .searchable-select > .select-trigger")
        self.hq_yes_option = page.locator(".select-options").get_by_text("Yes", exact=True)
        self.hq_no_option = page.get_by_text("No", exact=True)

        # Job opening dropdown and options
        self.job_opening_dropdown = page.locator("div:nth-child(9) > .custom-searchable-select > .searchable-select > .select-trigger")
        self.job_opening_yes_option = page.locator("div").filter(has_text=re.compile(r"^Yes$")).nth(1)
        self.job_opening_no_option = page.locator("div").filter(has_text=re.compile(r"^No$"))
        
        # Owner dropdown
        self.owner_dropdown = page.locator("div:nth-child(10) > .custom-searchable-select > .searchable-select > .select-trigger")
        # Use more specific locator to avoid strict mode violation
        self.owner_option = page.locator("div").filter(has_text=re.compile(r"^test$")).nth(3)
        
        # File upload
        # self.company_logo_upload = page.locator("body")
        self.upload_logo_text = page.get_by_text("Upload Logo")
        
        # Action buttons
        self.create_button = page.get_by_role("button", name="Create")
        self.save_button = page.get_by_role("button", name="Save")
        self.update_button = page.get_by_role("button", name="Update")
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.close_modal_button = page.get_by_role("button", name="Close modal")
        
        # Company actions and menus (global locators using company card siblings)
        self.view_details_button = page.get_by_role("button", name="View Details")
        self.three_dot_menu_global = page.locator("button.w-\\[42px\\]")  # Global locator for all three dot menus
        self.three_dot_menu_by_company = lambda company_name: page.get_by_role("heading", name=company_name).locator("xpath=ancestor::div[contains(@class,'flex')]").locator("button.w-\\[42px\\]").first  # Specific three dot for a company
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
        self.company_created_successfully_message = page.get_by_text("Company added successfully")
        self.company_added_successfully_message = page.get_by_text("Company added successfully")
        self.company_updated_successfully_message = page.get_by_text("Company info updated successfully")
        self.company_deleted_successfully_message = page.get_by_text("Company deleted successfully")  # Used by both TC_12 and TC_14
        # Alternative bulk deletion messages
        self.companies_deleted_successfully_message = page.get_by_text("Companies removed successfully")
        self.bulk_delete_success_message = page.get_by_text("successfully", exact=False)  # Generic success
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
        
        # Company multiple selection and bulk operations
        self.company_checkbox = page.locator("input[type='checkbox']")  # Individual company checkboxes
        self.select_all_companies_checkbox = page.locator("input[type='checkbox']").first  # Header select all checkbox
        # Better checkbox locators based on live site inspection
        self.company_checkbox_labels = page.locator("label[for*='companySelect']")  # Click labels instead of checkboxes
        self.select_all_companies_label = page.locator("label").first  # Header select all label
        self.individual_company_checkboxes = page.locator("input[id*='companySelect-']")  # Specific company checkboxes
        self.bulk_delete_button = lambda count: page.get_by_text(f"Delete ({count})")  # Dynamic delete button based on count
        self.bulk_delete_button_pattern = page.locator("text=/Delete \\(\\d+\\)/")  # Pattern matcher for any Delete (N) button
        self.selected_count_text = lambda count: page.get_by_text(f"Selected ({count})")  # Shows selected count
        
        # Company list and search
        self.company_list_container = page.locator(".company-list, [data-testid='company-list']")
        self.company_search_input = page.get_by_placeholder("Search companies...")
        self.search_input = page.get_by_placeholder("Search", exact=False)
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
