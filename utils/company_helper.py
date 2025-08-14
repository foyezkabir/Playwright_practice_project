"""
Company Helper Module
Contains utility functions for company tests
"""

from playwright.sync_api import Page
from utils.config import BASE_URL
from utils.login_helper import do_login
from conftest import wait_for_action_completion
from utils.enhanced_assertions import enhanced_assert_visible, enhanced_assert_not_visible
import time

def do_company_login(page: Page, email: str, password: str):
    """
    Helper function to login and return company page instance
    
    Args:
        page: Playwright page object
        email: User email
        password: User password
    
    Returns:
        CompanyPage instance
    """
    from pages.company_page import CompanyPage
    company_page = CompanyPage(page)
    do_login(page, email, password)
    time.sleep(2)
    return company_page

def navigate_to_company_creation_form(page: Page, email: str, password: str):
    """
    Complete navigation flow to company creation form with conditional logic
    
    Args:
        page: Playwright page object
        email: User email  
        password: User password
        
    Returns:
        CompanyPage instance positioned at company creation form
    """
    company_page = do_company_login(page, email, password)
    
    # Assess the current page to determine navigation path
    current_url = page.url
    
    # Check if we're on agency details page (single agency) or all agencies page (multiple agencies)
    if "agency/" in current_url and current_url.split("agency/")[-1].strip("/"):
        # We're on an Agency Details page (single agency exists)
        print("📍 On Agency Details page - proceeding to Company tab")
        company_page.click_company_tab()
        company_page.click_add_new_company_button()
        
    else:
        # We're on All Agencies list page (multiple agencies exist)
        print("📍 On All Agencies list page - selecting agency first")
        company_page.click_agency_card("Test this agency")
        company_page.wait_for_page_load()
        company_page.click_company_tab()
        company_page.click_add_new_company_button()
    
    # Verify we're on the company creation form
    company_page.expect_home_company_heading("navigate_to_company_creation")
    
    return company_page

def create_company_with_basic_info(page: Page, company_name: str, industry: str = "Finance", 
                                 email: str = "nua26i@onemail.host", password: str = "Kabir123#"):
    """
    Create a company with basic required information
    
    Args:
        page: Playwright page object
        company_name: Name of the company to create
        industry: Industry to select (default: Finance)
        email: Login email
        password: Login password
        
    Returns:
        CompanyPage instance
    """
    company_page = navigate_to_company_creation_form(page, email, password)
    
    # Fill required fields using new page methods
    company_page.fill_company_name_input(company_name)
    company_page.select_industry_option(industry)
    
    # Submit form
    company_page.click_create_button()
    
    return company_page

def create_company_with_full_info(page: Page, company_name: str, industry: str = "Finance", 
                                website: str = None, address: str = None, total_employees: str = None,
                                main_tel: str = None, hr_tel: str = None, hiring_status: str = None,
                                company_grade: str = None, hq_in_japan: str = None, 
                                job_opening: str = None, owner: str = None,
                                email: str = "nua26i@onemail.host", password: str = "Kabir123#"):
    """
    Create a company with full information including optional fields
    
    Args:
        page: Playwright page object
        company_name: Name of the company to create
        industry: Industry to select
        website: Optional website URL
        address: Optional address
        total_employees: Optional total employees count
        main_tel: Optional main telephone
        hr_tel: Optional HR telephone
        hiring_status: Optional hiring status
        company_grade: Optional company grade
        hq_in_japan: Optional HQ in Japan
        job_opening: Optional job opening status
        owner: Optional owner
        email: Login email
        password: Login password
        
    Returns:
        CompanyPage instance
    """
    company_page = navigate_to_company_creation_form(page, email, password)
    
    # Fill required fields
    company_page.fill_company_name_input(company_name)
    company_page.select_industry_option(industry)
    
    # Fill optional fields if provided
    if website:
        company_page.fill_website_input(website)
    if address:
        company_page.fill_address_input(address)
    if total_employees:
        company_page.fill_total_employees_input(total_employees)
    if main_tel:
        company_page.fill_main_tel_input(main_tel)
    if hr_tel:
        company_page.fill_hr_tel_input(hr_tel)
    if hiring_status:
        company_page.select_hiring_status_option(hiring_status)
    if company_grade:
        company_page.select_company_grade_option(company_grade)
    if hq_in_japan:
        company_page.select_hq_in_japan_option(hq_in_japan)
    if job_opening:
        company_page.select_job_opening_option(job_opening)
    if owner:
        company_page.select_owner_option(owner)
    
    # Submit form
    company_page.click_create_button()
    
    return company_page

def assert_company_created_successfully(page: Page, company_page, company_name: str, test_name: str = None):
    """
    Assert that company was created successfully with proper validations
    
    Args:
        page: Playwright page object
        company_page: CompanyPage instance
        company_name: Expected company name
        test_name: Test name for screenshot purposes
    """
    # Check for success message using new page methods
    company_page.expect_company_created_successfully_message(test_name)
    
    # Verify redirect to company profile page
    time.sleep(2)
    company_page.expect_created_company_heading(company_name, test_name)
    
    print(f"✅ Company '{company_name}' created successfully and profile page loaded")

def assert_company_name_already_exists_error(page: Page, company_page, test_name: str = None):
    """
    Assert that duplicate company name validation error appears
    
    Args:
        page: Playwright page object
        company_page: CompanyPage instance  
        test_name: Test name for screenshot purposes
    """
    company_page.expect_company_name_already_exists_validation_error(test_name)
    print("✅ Duplicate company name validation error displayed correctly")

def assert_company_name_required_error(page: Page, company_page, test_name: str = None):
    """
    Assert that required company name validation error appears
    
    Args:
        page: Playwright page object
        company_page: CompanyPage instance
        test_name: Test name for screenshot purposes
    """
    company_page.expect_company_name_required_validation_error(test_name)
    print("✅ Required company name validation error displayed correctly")

def assert_company_name_min_length_error(page: Page, company_page, test_name: str = None):
    """
    Assert that minimum length company name validation error appears
    """
    company_page.expect_company_name_min_length_validation_error(test_name)
    print("✅ Minimum length company name validation error displayed correctly")

def assert_company_name_max_length_error(page: Page, company_page, test_name: str = None):
    """
    Assert that maximum length company name validation error appears
    """
    company_page.expect_company_name_max_length_validation_error(test_name)
    print("✅ Maximum length company name validation error displayed correctly")

def assert_company_name_special_char_error(page: Page, company_page, test_name: str = None):
    """
    Assert that special character company name validation error appears
    """
    company_page.expect_company_name_special_char_validation_error(test_name)
    print("✅ Special character company name validation error displayed correctly")

def assert_industry_required_error(page: Page, company_page, test_name: str = None):
    """
    Assert that required industry validation error appears
    
    Args:
        page: Playwright page object
        company_page: CompanyPage instance
        test_name: Test name for screenshot purposes
    """
    company_page.expect_industry_required_validation_error(test_name)
    print("✅ Required industry validation error displayed correctly")

def assert_file_size_validation_error(page: Page, company_page, test_name: str = None):
    """
    Assert that file size validation error appears
    """
    company_page.expect_file_size_validation_error(test_name)
    print("✅ File size validation error displayed correctly")

def assert_file_type_validation_error(page: Page, company_page, test_name: str = None):
    """
    Assert that file type validation error appears
    """
    company_page.expect_file_type_validation_error(test_name)
    print("✅ File type validation error displayed correctly")

def find_company_in_list_and_action(page: Page, company_name: str, action: str = "view"):
    """
    Find a company in the list and perform an action
    
    Args:
        page: Playwright page object
        company_name: Name of company to find
        action: Action to perform ('view', 'edit', 'delete')
        
    Returns:
        Boolean indicating if company was found and action was performed
    """
    from pages.company_page import CompanyPage
    company_page = CompanyPage(page)
    
    # Search for company in list
    if company_page.find_company_in_list(company_name):
        if action == "view":
            company_page.click_view_details_button()
        elif action == "edit":
            company_page.click_three_dot_menu()
            company_page.click_edit_company_button()
        elif action == "delete":
            company_page.click_three_dot_menu()
            company_page.click_delete_company_button()
        
        time.sleep(2)
        return True
    
    print(f"❌ Company '{company_name}' not found in list")
    return False

def edit_company_info(page: Page, company_name: str, new_company_name: str = None, 
                     new_industry: str = None, email: str = "nua26i@onemail.host", 
                     password: str = "Kabir123#"):
    """
    Edit company information
    
    Args:
        page: Playwright page object
        company_name: Current company name to find
        new_company_name: New company name (optional)
        new_industry: New industry (optional)
        email: Login email
        password: Login password
        
    Returns:
        CompanyPage instance
    """
    company_page = do_company_login(page, email, password)
    
    # Navigate to company and edit
    if find_company_in_list_and_action(page, company_name, "edit"):
        if new_company_name:
            company_page.fill_company_name_input(new_company_name)
        if new_industry:
            company_page.select_industry_option(new_industry)
            
        company_page.click_update_button()
        
        # Verify update success using new page method
        company_page.expect_company_updated_successfully_message("edit_company_success")
        
        print(f"✅ Company '{company_name}' updated successfully")
    
    return company_page

def create_client_under_company(page: Page, company_name: str, english_name: str, 
                               japanese_name: str = None, job_title: str = None,
                               department: str = None, gender: str = None,
                               english_skill: str = None, japanese_skill: str = None,
                               phone_name: str = None, phone_number: str = None,
                               email_name: str = None, email_address: str = None):
    """
    Create a client under a specific company using new page methods
    
    Args:
        page: Playwright page object
        company_name: Name of the company
        english_name: English name of the client
        japanese_name: Optional Japanese name
        job_title: Optional job title
        department: Optional department
        gender: Optional gender
        english_skill: Optional English skill level
        japanese_skill: Optional Japanese skill level
        phone_name: Optional phone contact name
        phone_number: Optional phone number
        email_name: Optional email contact name
        email_address: Optional email address
        
    Returns:
        CompanyPage instance
    """
    from pages.company_page import CompanyPage
    company_page = CompanyPage(page)
    
    # Navigate to company details
    if find_company_in_list_and_action(page, company_name, "view"):
        # Click Client tab
        company_page.click_client_tab()
        
        # Add new client
        company_page.click_add_new_client_button()
        
        # Fill required fields
        company_page.fill_client_english_name_input(english_name)
        
        # Fill optional fields if provided
        if japanese_name:
            company_page.fill_client_japanese_name_input(japanese_name)
        if job_title:
            company_page.fill_client_job_title_input(job_title)
        if department:
            company_page.fill_client_department_input(department)
        if gender:
            company_page.select_client_gender_option(gender)
        if english_skill:
            company_page.select_client_english_skill_option(english_skill)
        if japanese_skill:
            company_page.select_client_japanese_skill_option(japanese_skill)
        if phone_name:
            company_page.fill_client_phone_name_input(phone_name)
        if phone_number:
            company_page.fill_client_phone_number_input(phone_number)
        if email_name:
            company_page.fill_client_email_name_input(email_name)
        if email_address:
            company_page.fill_client_email_input(email_address)
        
        # Create client
        company_page.click_create_client_button()
        
        # Verify success
        company_page.expect_client_created_successfully_message("create_client_success")
        
        print(f"✅ Client '{english_name}' created under company '{company_name}'")
    
    return company_page

def assert_client_name_required_error(page: Page, company_page, test_name: str = None):
    """
    Assert that client name required validation error appears
    """
    company_page.expect_client_name_required_validation_error(test_name)
    print("✅ Client name required validation error displayed correctly")

def assert_client_email_required_error(page: Page, company_page, test_name: str = None):
    """
    Assert that client email required validation error appears
    """
    company_page.expect_client_email_required_validation_error(test_name)
    print("✅ Client email required validation error displayed correctly")

def assert_breadcrumb_navigation(page: Page, company_page, test_name: str = None):
    """
    Assert that breadcrumb navigation shows Home>Company
    
    Args:
        page: Playwright page object
        company_page: CompanyPage instance
        test_name: Test name for screenshot purposes
    """
    company_page.expect_home_company_heading(test_name)
    print("✅ Breadcrumb navigation 'Home>Company' verified")

def wait_for_company_action_completion(page: Page, action_type: str = "create"):
    """
    Wait for company-related action to complete
    
    Args:
        page: Playwright page object
        action_type: Type of action ('create', 'update', 'delete')
    """
    try:
        if action_type == "create":
            page.wait_for_url("**/company/**", timeout=10000)
        elif action_type in ["update", "delete"]:
            page.wait_for_load_state("networkidle", timeout=8000)
        time.sleep(2)
    except:
        # Fallback wait
        time.sleep(3)
