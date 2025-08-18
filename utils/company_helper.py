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
import re

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

def navigate_to_company_list(page: Page, email: str, password: str):
    """
    Complete navigation flow to company list page following the sequence:
    Login → Select "Test this agency" → Company Sidebar Link
    
    Args:
        page: Playwright page object
        email: User email  
        password: User password
        
    Returns:
        CompanyPage instance positioned at company list page
    """
    import time
    
    print("📍 Starting navigation to company list...")
    
    # Step 1: Use existing login helper which handles the full login flow
    company_page = do_company_login(page, email, password)
    time.sleep(2)
    
    current_url = page.url
    print(f"📍 Current URL after login: {current_url}")
    
    # Step 2: Check if we're on agency list or already on agency dashboard
    if "/agency/" in current_url and current_url.split("/agency/")[-1].replace("/", "").isdigit():
        # We're already on a specific agency dashboard
        print("📍 Already on agency dashboard - clicking Company sidebar link")
        company_page.click_company_tab()
    else:
        # We're on All Agencies list - MUST select the Test agency first
        print("📍 On All Agencies page - selecting 'Test this agency'")
        company_page.click_agency_card("Test this agency")
        time.sleep(3)
        
        # Step 3: Now we should be on agency dashboard, click Company tab
        print("📍 On agency dashboard - clicking Company sidebar link")  
        company_page.click_company_tab()
    
    time.sleep(2)
    print(f"📍 Final URL - Company list: {page.url}")
    print("✅ Successfully navigated to company list page")
    
    return company_page

def navigate_to_company_details_direct(page: Page, email: str, password: str):
    """
    Direct navigation flow to company details page using exact working locators
    
    Args:
        page: Playwright page object
        email: User email  
        password: User password
        
    Returns:
        CompanyPage instance positioned at company details page
    """
    import time
    from pages.company_page import CompanyPage
    
    print("📍 Starting direct navigation to company details...")
    
    # Direct login flow
    page.goto("https://bprp-qa.shadhinlab.xyz/login")
    page.get_by_role("textbox", name="Email").fill(email)
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Sign in").click()
    time.sleep(2)

    # Finding the agency and clicking it
    page.get_by_role("heading", name="Test this agency").click()
    time.sleep(2)

    # Going to company list
    page.get_by_role("link", name="Company").click()
    time.sleep(2)

    # 1st company card on the list
    page.locator(".flex.flex-col.sm\\:flex-row").first.wait_for(state="visible")

    # View details button on the card
    page.get_by_role("button", name="View Details").first.click()
    time.sleep(2)
    
    # Create company page instance 
    company_page = CompanyPage(page)
    
    print("✅ Successfully navigated to company details page")
    return company_page

def navigate_to_company_details(page: Page, email: str, password: str):
    """
    Complete navigation flow to company details page for field editing tests
    
    Args:
        page: Playwright page object
        email: User email  
        password: User password
        
    Returns:
        CompanyPage instance positioned at company details page
    """
    # First navigate to company list
    company_page = navigate_to_company_list(page, email, password)
    time.sleep(3)
    
    # Debug current page URL and check for View Details buttons
    current_url = page.url
    print(f"📍 Current URL after navigation: {current_url}")
    
    # Check if View Details buttons exist
    view_details_buttons = page.get_by_role("button", name="View Details")
    button_count = view_details_buttons.count()
    print(f"📍 Found {button_count} View Details buttons")
    
    if button_count > 0:
        # Click the first View Details button to go to company details page
        print("📍 Clicking View Details button for first company")
        view_details_buttons.first.click()
        time.sleep(2)
    else:
        # Try alternative locator or approach
        print("📍 No View Details buttons found, trying alternative approach")
        # Check if there are any companies listed
        companies = page.locator("button:has-text('View Details')")
        alt_count = companies.count()
        print(f"📍 Found {alt_count} alternative View Details buttons")
        
        if alt_count > 0:
            companies.first.click()
            time.sleep(2)
        else:
            print("📍 No companies found on the page")
            raise Exception("No companies or View Details buttons found on the page")
    
    print("📍 Successfully navigated to company details page")
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

def assert_company_logo_visible_with_name(page: Page, company_page, company_name: str, test_name: str = None):
    """
    Assert that company logo is visible with company name in the list
    
    Args:
        page: Playwright page object
        company_page: CompanyPage instance
        company_name: Name of the company to verify logo for
        test_name: Name of the test for screenshot purposes
    """
    company_page.expect_company_logo_with_name(company_name, test_name)
    print(f"✅ Company logo visible with name: {company_name}")

def assert_on_company_details_page(page: Page, company_page, company_name: str, test_name: str = None):
    """
    Assert that we are on the company details page
    
    Args:
        page: Playwright page object
        company_page: CompanyPage instance  
        company_name: Name of the company to verify details page for
        test_name: Name of the test for screenshot purposes
    """
    company_page.expect_company_details_page(company_name, test_name)
    print(f"✅ On company details page for: {company_name}")

def navigate_to_company_list(page: Page, email: str, password: str):
    """
    Navigate to company list page
    
    Args:
        page: Playwright page object
        email: User email
        password: User password
        
    Returns:
        CompanyPage instance positioned at company list
    """
    company_page = do_company_login(page, email, password)
    
    # Navigate to Companies section
    company_page.click_companies_link()
    time.sleep(2)
    
    print("✅ Navigated to company list page")
    return company_page

def assert_duplicate_company_name_error(page: Page, company_page, test_name: str = None):
    """
    Assert that duplicate company name validation error appears
    
    Args:
        page: Playwright page object
        company_page: CompanyPage instance
        test_name: Name of the test for screenshot purposes
    """
    company_page.expect_company_name_already_exists_error(test_name)
    print("✅ Duplicate company name validation error displayed correctly")

def create_company_with_all_fields_and_image(page: Page, company_name: str, email: str = "nua26i@onemail.host", password: str = "Kabir123#"):
    """
    Complete company creation workflow with all fields including image upload
    
    Args:
        page: Playwright page object
        company_name: Name of the company to create
        email: Login email
        password: Login password
        
    Returns:
        CompanyPage instance
    """
    import time
    
    # Navigate to company creation form
    company_page = navigate_to_company_creation_form(page, email, password)
    
    # Fill mandatory fields
    print("🔧 Filling mandatory fields...")
    company_page.fill_company_name_input(company_name)
    time.sleep(1)
    
    company_page.select_industry_option("Information Technology")
    time.sleep(1)
    
    company_page.fill_website_input("https://www.example.com")
    time.sleep(1)
    
    company_page.fill_address_input("123 Business Street")
    time.sleep(1)
    
    company_page.select_owner_option("test")
    time.sleep(1)
    
    # Fill optional text fields
    print("🔧 Filling optional text fields...")
    company_page.fill_total_employees_input("100")
    time.sleep(0.5)
    
    company_page.fill_main_tel_input("+1234567890")
    time.sleep(0.5)
    
    company_page.fill_hr_tel_input("+1234567891")
    time.sleep(0.5)
    
    # Fill dropdown fields using direct working locators from browser investigation
    print("🔧 Selecting dropdown options...")
    
    # Hiring Status - Use exact locators that worked in browser
    page.locator("div:nth-child(5) > .custom-searchable-select > .searchable-select > .select-trigger > .self-center > .chevron").click()
    time.sleep(1)
    page.get_by_text("Active", exact=True).click()
    time.sleep(1)
    
    # Company Grade - Use exact locators that worked in browser  
    page.locator("div:nth-child(7) > .custom-searchable-select > .searchable-select > .select-trigger > .self-center > .chevron").click()
    time.sleep(1)
    page.get_by_text("A", exact=True).click()
    time.sleep(1)
    
    # HQ in Japan
    company_page.select_hq_in_japan_option("No")
    time.sleep(1)
    
    # Job Opening - Use exact locators that worked in browser
    page.locator("div:nth-child(9) > .custom-searchable-select > .searchable-select > .select-trigger > .self-center > .chevron").click()
    time.sleep(1)
    page.get_by_text("Yes", exact=True).click()
    time.sleep(1)
    
    # Upload image
    print("🔧 Uploading company logo...")
    company_page.upload_file("images_for_test/pexels-photo.jpeg")
    time.sleep(2)
    
    # Create company
    print("🔧 Creating company...")
    company_page.click_create_button()
    time.sleep(3)
    
    print(f"✅ Company '{company_name}' created with all fields and image")
    return company_page

def navigate_to_company_details_via_first_link(page: Page, email: str, password: str, company_name: str, test_name: str = None):
    """
    Helper function for TC_11 - Navigate to company details via first company link
    
    Args:
        page: Playwright page object
        email: User email
        password: User password
        company_name: Expected company name on details page
        test_name: Test case name for screenshots
    """
    # Login
    company_page = do_company_login(page, email, password)
    time.sleep(2)
    
    # Select agency T
    company_page.select_agency_t()
    time.sleep(2)
    
    # Navigate to Company section
    company_page.click_company_tab()
    time.sleep(2)
    
    # Click first company link
    company_page.click_first_company_link()
    time.sleep(3)
    
    # Verify company details page
    company_page.verify_company_details_page(company_name, test_name)
    
    return company_page

def navigate_to_company_details_via_name_heading(page: Page, email: str, password: str, company_name: str, test_name: str = None):
    """
    Helper function for TC_12 - Navigate to company details via company name heading
    
    Args:
        page: Playwright page object
        email: User email
        password: User password
        company_name: Company name to click and verify
        test_name: Test case name for screenshots
    """
    # Login
    company_page = do_company_login(page, email, password)
    time.sleep(2)
    
    # Select agency T
    company_page.select_agency_t()
    time.sleep(2)
    
    # Navigate to Company section
    company_page.click_company_tab()
    time.sleep(2)
    
    # Click company name heading
    company_page.click_company_name_heading(company_name)
    time.sleep(3)
    
    # Verify company details page
    company_page.verify_company_details_page(company_name, test_name)
    
    return company_page

def delete_company_and_verify(page: Page, email: str, password: str, company_name: str, test_name: str = None):
    """
    Helper function for TC_12 - Delete company and verify removal from list
    
    Args:
        page: Playwright page object
        email: User email
        password: User password
        company_name: Company name to delete
        test_name: Test case name for screenshots
    """
    # Login
    company_page = do_company_login(page, email, password)
    time.sleep(2)
    
    # Select agency T
    company_page.select_agency_t()
    time.sleep(2)
    
    # Navigate to Company section
    company_page.click_company_tab()
    time.sleep(2)
    
    # Find company in paginated list (no search bar usage)
    found = company_page.find_company_in_paginated_list(page, company_name)
    
    if found:
        # Delete company using the new method
        success = company_page.delete_company_by_name(company_name)
        
        if success:
            # Assert delete confirmation message
            print(f"🔍 TC_12: Asserting delete confirmation message for '{company_name}'...")
            enhanced_assert_visible(page, company_page.locators.company_deleted_successfully_message, 
                                  "Company removed successfully message should be visible", f"{test_name}_delete_confirmation")
            
            # Verify company is no longer in the list by searching again using pagination
            time.sleep(2)  # Wait for list to refresh
            still_exists = company_page.find_company_in_paginated_list(page, company_name)
            
            if not still_exists:
                print(f"✅ TC_12: Company '{company_name}' successfully deleted and verified through pagination!")
                
                # ADDITIONAL VERIFICATION: Use search bar to confirm deletion
                print(f"🔍 TC_12: Now using search bar to double-verify deletion of '{company_name}'...")
                try:
                    # Use search functionality to search for the deleted company
                    company_page.search_company(company_name)
                    time.sleep(3)  # Wait for search results
                    
                    # Check if "No companies found" message appears
                    if company_page.locators.no_companies_message.count() > 0 or company_page.locators.no_companies_found_message.count() > 0:
                        print(f"✅ TC_12: SEARCH VERIFICATION PASSED - No companies found when searching for '{company_name}'!")
                        print(f"🎉 TC_12: Company '{company_name}' is CONFIRMED DELETED - search shows no results!")
                    else:
                        # Check if the company still appears in search results
                        company_in_search = page.get_by_text(company_name, exact=True)
                        if company_in_search.count() == 0:
                            print(f"✅ TC_12: SEARCH VERIFICATION PASSED - Company '{company_name}' not found in search results!")
                            print(f"🎉 TC_12: Company '{company_name}' is CONFIRMED DELETED!")
                        else:
                            print(f"⚠️ TC_12: Company '{company_name}' still appears in search results after deletion!")
                            
                except Exception as e:
                    print(f"⚠️ TC_12: Search verification failed with error: {e}")
                    print(f"✅ TC_12: But pagination verification confirmed deletion of '{company_name}'")
                    
            else:
                print(f"⚠️ TC_12: Company '{company_name}' was deleted but still appears in paginated list")
        else:
            print(f"❌ TC_12: Failed to delete company '{company_name}'")
    else:
        print(f"❌ TC_12: Company '{company_name}' not found in paginated list")
    
    return company_page


def bulk_delete_companies_and_verify(page: Page, email: str = "nua26i@onemail.host", password: str = "Kabir123#", 
                                    select_all: bool = True, individual_count: int = 0, test_name: str = None):
    """
    Helper function for bulk deletion of companies with verification
    
    Args:
        page: Playwright page object
        email: User email
        password: User password
        select_all: If True, select all companies on page. If False, select individual_count companies.
        individual_count: Number of individual companies to select (only used if select_all is False)
        test_name: Test case name for screenshots
    """
    # Login and navigate to company list
    company_page = do_company_login(page, email, password)
    time.sleep(2)
    
    # Select agency T
    company_page.select_agency_t()
    time.sleep(2)
    
    # Navigate to Company section
    company_page.click_company_tab()
    time.sleep(2)
    
    # Perform bulk deletion
    if select_all:
        success = company_page.perform_bulk_company_deletion(select_all=True)
        expected_count = 10
    else:
        success = company_page.perform_bulk_company_deletion(select_all=False, individual_count=individual_count)
        expected_count = individual_count
    
    if success:
        # Assert delete confirmation message for bulk deletion
        enhanced_assert_visible(page, company_page.locators.company_deleted_successfully_message, "Company deleted successfully message should be visible", f"{test_name}_bulk_delete_confirmation")
        
        # Wait for page to refresh and verify deletion
        time.sleep(3)
        
        # Check if no companies found message appears (if all were deleted)
        if select_all:
            if company_page.is_no_companies_found_message_visible():
                print(f"✅ BULK DELETE VERIFIED - No companies found message appears after deleting all!")
            else:
                print(f"✅ BULK DELETE COMPLETED - Page refreshed after bulk deletion")
        else:
            print(f"✅ BULK DELETE COMPLETED - {individual_count} companies deleted successfully")
            
    else:
        print(f"❌ Bulk deletion failed")
    
    return company_page

class CompanyFieldEditingHelper:
    """Helper class for company field editing operations."""
    
    @staticmethod
    def edit_and_assert_company_name(page: Page, company_page, new_value: str):
        """Edit company name field and assert the value is updated."""
        print(f"🔧 Testing company name field edit to: {new_value}")
        
        # Get original value
        original_value = company_page.get_company_name_display_value()
        print(f"📋 Original company name: {original_value}")
        
        # Edit the field
        company_page.edit_company_name_field(new_value)
        
        # Assert success message
        enhanced_assert_visible(page, company_page.locators.company_info_updated_message, "Company info updated success message should be visible", "edit_company_name")
        
        # Assert updated value is displayed
        time.sleep(1)
        updated_value = company_page.get_company_name_display_value()
        assert updated_value == new_value, f"Expected company name '{new_value}', but got '{updated_value}'"
        print(f"✅ Company name successfully updated from '{original_value}' to '{updated_value}'")

    @staticmethod
    def edit_and_assert_web_page(page: Page, company_page, new_value: str):
        """Edit web page field and assert the value is updated."""
        print(f"🔧 Testing web page field edit to: {new_value}")
        
        # Get original value
        original_value = company_page.get_web_page_display_value()
        print(f"📋 Original web page: {original_value}")
        
        # Edit the field
        company_page.edit_web_page_field(new_value)
        
        # Assert success message
        enhanced_assert_visible(page, company_page.locators.company_info_updated_message, "Company info updated success message should be visible", "edit_web_page")
        
        # Assert updated value is displayed
        time.sleep(1)
        updated_value = company_page.get_web_page_display_value()
        assert updated_value == new_value, f"Expected web page '{new_value}', but got '{updated_value}'"
        print(f"✅ Web page successfully updated from '{original_value}' to '{updated_value}'")

    @staticmethod
    def edit_and_assert_industry(page: Page, company_page, new_value: str):
        """Edit industry field and assert the value is updated."""
        print(f"🔧 Testing industry field edit to: {new_value}")
        
        # Get original value
        original_value = company_page.get_industry_display_value()
        print(f"📋 Original industry: {original_value}")
        
        # Edit the field
        company_page.edit_industry_field(new_value)
        
        # Assert success message
        enhanced_assert_visible(page, company_page.locators.company_info_updated_message, "Company info updated success message should be visible", "edit_industry")
        
        # Assert updated value is displayed
        time.sleep(1)
        updated_value = company_page.get_industry_display_value()
        assert updated_value == new_value, f"Expected industry '{new_value}', but got '{updated_value}'"
        print(f"✅ Industry successfully updated from '{original_value}' to '{updated_value}'")

    @staticmethod
    def edit_and_assert_hq_in_jpn(page: Page, company_page, new_value: str):
        """Edit HQ in JPN field and assert the value is updated."""
        print(f"🔧 Testing HQ in JPN field edit to: {new_value}")
        
        # Get original value
        original_value = company_page.get_hq_in_jpn_display_value()
        print(f"📋 Original HQ in JPN: {original_value}")
        
        # Edit the field
        company_page.edit_hq_in_jpn_field(new_value)
        
        # Assert success message
        enhanced_assert_visible(page, company_page.locators.company_info_updated_message, "Company info updated success message should be visible", "edit_hq_in_jpn")
        
        # Assert updated value is displayed
        time.sleep(1)
        updated_value = company_page.get_hq_in_jpn_display_value()
        assert updated_value == new_value, f"Expected HQ in JPN '{new_value}', but got '{updated_value}'"
        print(f"✅ HQ in JPN successfully updated from '{original_value}' to '{updated_value}'")

    @staticmethod
    def edit_and_assert_global_hq(page: Page, company_page, new_value: str):
        """Edit Global HQ field and assert the value is updated."""
        print(f"🔧 Testing Global HQ field edit to: {new_value}")
        
        # Get original value
        original_value = company_page.get_global_hq_display_value()
        print(f"📋 Original Global HQ: {original_value}")
        
        # Edit the field
        company_page.edit_global_hq_field(new_value)
        
        # Assert success message
        enhanced_assert_visible(page, company_page.locators.company_info_updated_message, "Company info updated success message should be visible", "edit_global_hq")
        
        # Assert updated value is displayed
        time.sleep(1)
        updated_value = company_page.get_global_hq_display_value()
        assert updated_value == new_value, f"Expected Global HQ '{new_value}', but got '{updated_value}'"
        print(f"✅ Global HQ successfully updated from '{original_value}' to '{updated_value}'")

    @staticmethod
    def edit_and_assert_country_of_origin(page: Page, company_page, new_value: str):
        """Edit Country of origin field and assert the value is updated."""
        print(f"🔧 Testing Country of origin field edit to: {new_value}")
        
        # Get original value
        original_value = company_page.get_country_of_origin_display_value()
        print(f"📋 Original Country of origin: {original_value}")
        
        # Edit the field
        company_page.edit_country_of_origin_field(new_value)
        
        # Assert success message
        enhanced_assert_visible(page, company_page.locators.company_info_updated_message, "Company info updated success message should be visible", "edit_country_of_origin")
        
        # Assert updated value is displayed
        time.sleep(1)
        updated_value = company_page.get_country_of_origin_display_value()
        assert updated_value == new_value, f"Expected Country of origin '{new_value}', but got '{updated_value}'"
        print(f"✅ Country of origin successfully updated from '{original_value}' to '{updated_value}'")

    @staticmethod
    def edit_and_assert_company_address(page: Page, company_page, new_value: str):
        """Edit Company address field and assert the value is updated."""
        print(f"🔧 Testing Company address field edit to: {new_value}")
        
        # Get original value
        original_value = company_page.get_company_address_display_value()
        print(f"📋 Original Company address: {original_value}")
        
        # Edit the field
        company_page.edit_company_address_field(new_value)
        
        # Assert success message
        enhanced_assert_visible(page, company_page.locators.company_info_updated_message, "Company info updated success message should be visible", "edit_company_address")
        
        # Assert updated value is displayed
        time.sleep(1)
        updated_value = company_page.get_company_address_display_value()
        assert updated_value == new_value, f"Expected Company address '{new_value}', but got '{updated_value}'"
        print(f"✅ Company address successfully updated from '{original_value}' to '{updated_value}'")

    @staticmethod
    def edit_and_assert_company_hiring_status(page: Page, company_page, new_value: str):
        """Edit Company hiring status field and assert the value is updated."""
        print(f"🔧 Testing Company hiring status field edit to: {new_value}")
        
        # Get original value
        original_value = company_page.get_company_hiring_status_display_value()
        print(f"📋 Original Company hiring status: {original_value}")
        
        # Edit the field
        company_page.edit_company_hiring_status_field(new_value)
        
        # Assert success message
        enhanced_assert_visible(page, company_page.locators.company_info_updated_message, "Company info updated success message should be visible", "edit_company_hiring_status")
        
        # Assert updated value is displayed
        time.sleep(1)
        updated_value = company_page.get_company_hiring_status_display_value()
        assert updated_value == new_value, f"Expected Company hiring status '{new_value}', but got '{updated_value}'"
        print(f"✅ Company hiring status successfully updated from '{original_value}' to '{updated_value}'")

    @staticmethod
    def edit_and_assert_job_opening(page: Page, company_page, new_value: str):
        """Edit Job opening field and assert the value is updated."""
        print(f"🔧 Testing Job opening field edit to: {new_value}")
        
        # Get original value
        original_value = company_page.get_job_opening_display_value()
        print(f"📋 Original Job opening: {original_value}")
        
        # Edit the field
        company_page.edit_job_opening_field(new_value)
        
        # Assert success message
        enhanced_assert_visible(page, company_page.locators.company_info_updated_message, "Company info updated success message should be visible", "edit_job_opening")
        
        # Assert updated value is displayed
        time.sleep(1)
        updated_value = company_page.get_job_opening_display_value()
        assert updated_value == new_value, f"Expected Job opening '{new_value}', but got '{updated_value}'"
        print(f"✅ Job opening successfully updated from '{original_value}' to '{updated_value}'")

    @staticmethod
    def edit_and_assert_total_employees_jpn(page: Page, company_page, new_value: str):
        """Edit Total employees JPN field and assert the value is updated."""
        print(f"🔧 Testing Total employees JPN field edit to: {new_value}")
        
        # Get original value
        original_value = company_page.get_total_employees_jpn_display_value()
        print(f"📋 Original Total employees JPN: {original_value}")
        
        # Edit the field
        company_page.edit_total_employees_jpn_field(new_value)
        
        # Assert success message
        enhanced_assert_visible(page, company_page.locators.company_info_updated_message, "Company info updated success message should be visible", "edit_total_employees_jpn")
        
        # Assert updated value is displayed
        time.sleep(1)
        updated_value = company_page.get_total_employees_jpn_display_value()
        assert updated_value == new_value, f"Expected Total employees JPN '{new_value}', but got '{updated_value}'"
        print(f"✅ Total employees JPN successfully updated from '{original_value}' to '{updated_value}'")

    @staticmethod
    def edit_and_assert_company_grade(page: Page, company_page, new_value: str):
        """Edit Company grade field and assert the value is updated."""
        print(f"🔧 Testing Company grade field edit to: {new_value}")
        
        # Get original value
        original_value = company_page.get_company_grade_display_value()
        print(f"📋 Original Company grade: {original_value}")
        
        # Edit the field
        company_page.edit_company_grade_field(new_value)
        
        # Assert success message
        enhanced_assert_visible(page, company_page.locators.company_info_updated_message, "Company info updated success message should be visible", "edit_company_grade")
        
        # Assert updated value is displayed
        time.sleep(1)
        updated_value = company_page.get_company_grade_display_value()
        assert updated_value == new_value, f"Expected Company grade '{new_value}', but got '{updated_value}'"
        print(f"✅ Company grade successfully updated from '{original_value}' to '{updated_value}'")

    @staticmethod
    def edit_and_assert_company_client_owner(page: Page, company_page, new_value: str):
        """Edit Company client owner field and assert the value is updated."""
        print(f"🔧 Testing Company client owner field edit to: {new_value}")
        
        # Get original value
        original_value = company_page.get_company_client_owner_display_value()
        print(f"📋 Original Company client owner: {original_value}")
        
        # Edit the field
        company_page.edit_company_client_owner_field(new_value)
        
        # Assert success message
        enhanced_assert_visible(page, company_page.locators.company_info_updated_message, "Company info updated success message should be visible", "edit_company_client_owner")
        
        # Assert updated value is displayed
        time.sleep(1)
        updated_value = company_page.get_company_client_owner_display_value()
        assert updated_value == new_value, f"Expected Company client owner '{new_value}', but got '{updated_value}'"
        print(f"✅ Company client owner successfully updated from '{original_value}' to '{updated_value}'")

    @staticmethod
    def edit_and_assert_telephone(page: Page, company_page, new_value: str):
        """Edit Telephone field and assert the value is updated."""
        print(f"🔧 Testing Telephone field edit to: {new_value}")
        
        # Get original value
        original_value = company_page.get_telephone_display_value()
        print(f"📋 Original Telephone: {original_value}")
        
        # Edit the field
        company_page.edit_telephone_field(new_value)
        
        # Assert success message
        enhanced_assert_visible(page, company_page.locators.company_info_updated_message, "Company info updated success message should be visible", "edit_telephone")
        
        # Assert updated value is displayed
        time.sleep(1)
        updated_value = company_page.get_telephone_display_value()
        assert updated_value == new_value, f"Expected Telephone '{new_value}', but got '{updated_value}'"
        print(f"✅ Telephone successfully updated from '{original_value}' to '{updated_value}'")

    @staticmethod
    def test_all_summary_fields_editing(page: Page, company_page):
        """Test editing all Summary tab fields with predefined test values."""
        print("🚀 Starting comprehensive Summary tab field editing tests...")
        
        # Test data for each field
        test_values = {
            'company_name': 'Updated Test Company 2024',
            'web_page': 'https://www.updated-test-company.com',
            'industry': 'Technology',  # Must be a valid dropdown option
            'hq_in_jpn': 'Tokyo',  # Must be a valid dropdown option
            'global_hq': 'New York, USA',
            'country_of_origin': 'United States',
            'company_address': '123 Updated Test Street, Test City, 12345',
            'company_hiring_status': 'Actively Hiring',  # Must be a valid dropdown option
            'job_opening': 'Available',  # Must be a valid dropdown option
            'total_employees_jpn': '150',
            'company_grade': 'A+',  # Must be a valid dropdown option
            'company_client_owner': 'John Smith',  # Must be a valid dropdown option
            'telephone': '+1-555-0123'
        }
        
        # Execute field editing tests using class methods
        CompanyFieldEditingHelper.edit_and_assert_company_name(page, company_page, test_values['company_name'])
        CompanyFieldEditingHelper.edit_and_assert_web_page(page, company_page, test_values['web_page'])
        CompanyFieldEditingHelper.edit_and_assert_industry(page, company_page, test_values['industry'])
        CompanyFieldEditingHelper.edit_and_assert_hq_in_jpn(page, company_page, test_values['hq_in_jpn'])
        CompanyFieldEditingHelper.edit_and_assert_global_hq(page, company_page, test_values['global_hq'])
        CompanyFieldEditingHelper.edit_and_assert_country_of_origin(page, company_page, test_values['country_of_origin'])
        CompanyFieldEditingHelper.edit_and_assert_company_address(page, company_page, test_values['company_address'])
        CompanyFieldEditingHelper.edit_and_assert_company_hiring_status(page, company_page, test_values['company_hiring_status'])
        CompanyFieldEditingHelper.edit_and_assert_job_opening(page, company_page, test_values['job_opening'])
        CompanyFieldEditingHelper.edit_and_assert_total_employees_jpn(page, company_page, test_values['total_employees_jpn'])
        CompanyFieldEditingHelper.edit_and_assert_company_grade(page, company_page, test_values['company_grade'])
        CompanyFieldEditingHelper.edit_and_assert_company_client_owner(page, company_page, test_values['company_client_owner'])
        CompanyFieldEditingHelper.edit_and_assert_telephone(page, company_page, test_values['telephone'])
        
        print("🎉 All Summary tab field editing tests completed successfully!")

# =============================================================================
# DIRECT FIELD EDITING FUNCTIONS (Using Direct Locators)
# =============================================================================

def edit_and_assert_company_name_direct(page: Page, new_value: str):
    """Edit company name field using direct locators and assert the update."""
    import re
    import time
    from playwright.sync_api import expect
    
    print(f"🔧 Editing company name to: {new_value}")
    
    # Click edit icon for company name
    page.locator("div").filter(has_text=re.compile(r"^:Updated Modern Company$")).get_by_role("img").click()
    page.get_by_role("textbox", name="Company name").fill(new_value)
    page.get_by_role("button", name="Save").click()
    time.sleep(1)
    
    # Assert the updated value is visible
    expect(page.get_by_text(new_value).first).to_be_visible()
    print(f"✅ Company name successfully updated to: {new_value}")

def edit_and_assert_website_direct(page: Page, new_value: str):
    """Edit website field using direct locators and assert the update."""
    import re
    import time
    from playwright.sync_api import expect
    
    print(f"🔧 Editing website to: {new_value}")
    
    # Click edit icon for website
    page.locator("div").filter(has_text=re.compile(r"^:https://www\.updated-modern\.com$")).get_by_role("img").click()
    page.get_by_role("textbox", name="Website").clear()
    page.get_by_role("textbox", name="Website").fill(new_value)
    page.get_by_role("button", name="Save").click()
    time.sleep(1)
    
    # Assert the updated value is visible
    expect(page.get_by_text(new_value).first).to_be_visible()
    print(f"✅ Website successfully updated to: {new_value}")

def edit_and_assert_industry_direct(page: Page, new_value: str):
    """Edit industry field using direct locators and assert the update."""
    import re
    import time
    from playwright.sync_api import expect
    
    print(f"🔧 Editing industry to: {new_value}")
    
    # Click edit icon for industry
    page.locator("div").filter(has_text=re.compile(r"^:Technology$")).get_by_role("img").click()
    page.locator("div").filter(has_text=re.compile(r"^Technology$")).nth(2).click()
    page.get_by_text(new_value).click()
    page.get_by_role("button", name="Save").click()
    time.sleep(1)
    
    # Assert the updated value is visible
    expect(page.get_by_text(new_value).first).to_be_visible()
    print(f"✅ Industry successfully updated to: {new_value}")

def edit_and_assert_hq_in_jpn_direct(page: Page, new_value: str):
    """Edit HQ in JPN field using direct locators and assert the update."""
    import re
    import time
    from playwright.sync_api import expect
    
    print(f"🔧 Editing HQ in JPN to: {new_value}")
    
    # Click edit icon for HQ in JPN
    page.locator("div").filter(has_text=re.compile(r"^:No$")).get_by_role("img").click()
    page.locator("div").filter(has_text=re.compile(r"^No$")).nth(2).click()
    page.get_by_text(new_value).click()
    page.get_by_role("button", name="Save").click()
    time.sleep(1)
    
    # Assert the updated value is visible
    expect(page.get_by_text(new_value).first).to_be_visible()
    print(f"✅ HQ in JPN successfully updated to: {new_value}")

def edit_and_assert_global_hq_direct(page: Page, new_value: str):
    """Edit Global HQ field using direct locators and assert the update."""
    import re
    import time
    from playwright.sync_api import expect
    
    print(f"🔧 Editing Global HQ to: {new_value}")
    
    # Click edit icon for Global HQ
    page.locator("div").filter(has_text=re.compile(r"^Global HQ:United Kingdom$")).get_by_role("img").click()
    page.get_by_role("textbox", name="Global HQ").clear()
    page.get_by_role("textbox", name="Global HQ").fill(new_value)
    page.get_by_role("button", name="Save").click()
    time.sleep(1)
    
    # Assert the updated value is visible
    expect(page.get_by_text(new_value).first).to_be_visible()
    print(f"✅ Global HQ successfully updated to: {new_value}")

def edit_and_assert_country_of_origin_direct(page: Page, new_value: str):
    """Edit Country of origin field using direct locators and assert the update."""
    import re
    import time
    from playwright.sync_api import expect
    
    print(f"🔧 Editing Country of origin to: {new_value}")
    
    # Click edit icon for Country of origin
    page.locator("div").filter(has_text=re.compile(r"^Country of origin:Bangladesh$")).get_by_role("img").click()
    page.get_by_role("textbox", name="Country of Origin").clear()
    page.get_by_role("textbox", name="Country of Origin").fill(new_value)
    page.get_by_role("button", name="Save").click()
    time.sleep(1)
    
    # Assert the updated value is visible
    expect(page.get_by_text(new_value).first).to_be_visible()
    print(f"✅ Country of origin successfully updated to: {new_value}")

def edit_and_assert_company_address_direct(page: Page, new_value: str):
    """Edit Company address field using direct locators and assert the update."""
    import re
    import time
    from playwright.sync_api import expect
    
    print(f"🔧 Editing Company address to: {new_value}")
    
    # Click edit icon for Company address
    page.locator("div").filter(has_text=re.compile(r"^:456 Corporate Avenue, Suite 100$")).get_by_role("img").click()
    page.get_by_role("textbox", name="Address").clear()
    page.get_by_role("textbox", name="Address").fill(new_value)
    page.get_by_role("button", name="Save").click()
    time.sleep(1)
    
    # Assert the updated value is visible
    expect(page.get_by_text(new_value).first).to_be_visible()
    print(f"✅ Company address successfully updated to: {new_value}")

def comprehensive_company_fields_editing_direct(page: Page):
    """Comprehensive editing of all company fields using direct locators."""
    import re
    import time
    from playwright.sync_api import expect
    
    print("🚀 Starting comprehensive company fields editing...")
    
    # Edit company name
    page.get_by_text("Modern Consulting").nth(2).click()
    expect(page.locator("div").filter(has_text=re.compile(r"^:Modern Consulting 08171741$")).get_by_role("img")).to_be_visible()
    page.locator("div").filter(has_text=re.compile(r"^:Modern Consulting 08171741$")).get_by_role("img").click()
    page.get_by_role("textbox", name="Company name").fill("Modern")
    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("Modern").nth(2)).to_be_visible()
    time.sleep(1)
    
    # Edit website
    page.locator("div").filter(has_text=re.compile(r"^:https://www\.example\.com$")).get_by_role("img").click()
    page.get_by_role("textbox", name="Website").fill("https://www.exe.com")
    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("https://www.exe.com").nth(1)).to_be_visible()
    time.sleep(1)
    
    # Edit industry
    page.locator("div").filter(has_text=re.compile(r"^:Finance$")).get_by_role("img").click()
    page.locator("div").filter(has_text=re.compile(r"^Finance$")).nth(2).click()
    page.get_by_text("Healthcare").click()
    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("Healthcare")).to_be_visible()
    time.sleep(1)
    
    # Edit HQ in JPN
    page.locator("div").filter(has_text=re.compile(r"^:No$")).get_by_role("img").click()
    page.locator("div").filter(has_text=re.compile(r"^No$")).nth(2).click()
    page.get_by_text("Yes").click()
    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("Yes")).to_be_visible()
    time.sleep(1)
    
    # Edit Global HQ
    page.locator("div").filter(has_text=re.compile(r"^Global HQ:N/A$")).get_by_role("img").click()
    page.get_by_role("textbox", name="Global HQ").click()
    page.get_by_role("textbox", name="Global HQ").fill("USA")
    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("USA")).to_be_visible()
    time.sleep(1)
    
    # Edit Country of origin
    page.locator("div").filter(has_text=re.compile(r"^Country of origin:N/A$")).get_by_role("img").click()
    page.get_by_role("textbox", name="Country of Origin").fill("bangu")
    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("bangu")).to_be_visible()
    time.sleep(1)
    
    # Edit company address
    page.locator("div").filter(has_text=re.compile(r"^:123 Business Street, City$")).get_by_role("img").click()
    page.get_by_role("textbox", name="Address").fill("123 Business Street")
    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("Business Street").nth(1)).to_be_visible()
    time.sleep(1)
    
    print("🎉 Comprehensive company fields editing completed successfully!")


class CompanyTestDataManager:
    """Manages test data for comprehensive company editing tests."""
    
    @staticmethod
    def get_test_data():
        """Generate initial and updated values for comprehensive company testing."""
        from random_values_generator.random_company_name import generate_company_name
        
        # Generate unique company name
        unique_company_name = generate_company_name()
        
        # Initial values (from original test_TC_08)
        initial_values = {
            'company_name': unique_company_name,
            'industry': 'Information Technology',
            'website': 'https://www.example.com',
            'address': '123 Business Street',
            'owner': 'test',
            'total_employees': '100',
            'main_tel': '+1234567890',
            'hr_tel': '+1234567891',
            'hiring_status': 'Active',
            'company_grade': 'A',
            'hq_in_japan': 'No',
            'job_opening': 'Yes'
        }
        
        # Updated values for editing (different from initial)
        updated_values = {
            'company_name': f'{unique_company_name} - EDITED',
            'industry': 'Healthcare',  # Different dropdown value
            'website': 'https://www.updated-example.com',
            'address': '456 Updated Business Avenue, Suite 100',
            'total_employees': '250',
            'main_tel': '+1987654321',
            'hr_tel': '+1987654322',
            'hiring_status': 'Recruiting',  # Different dropdown value
            'company_grade': 'AA',  # Different dropdown value  
            'hq_in_japan': 'Yes',  # Different dropdown value
            'job_opening': 'No',  # Different dropdown value
            'global_hq': 'Tokyo, Japan',  # New field
            'country_of_origin': 'Japan'  # New field
        }
        
        return initial_values, updated_values


class ComprehensiveCompanyTestHelper:
    """Helper class for comprehensive company creation and editing tests."""
    
    @staticmethod
    def company_create_to_details_page(page: Page):
        """
        Complete workflow from login to company creation and navigation to details page.
        
        Returns:
            tuple: (initial_values, updated_values, company_page)
        """
        # Get test data
        initial_values, updated_values = CompanyTestDataManager.get_test_data()
        
        print(f"🚀 Starting comprehensive company test with: {initial_values['company_name']}")
        print("📋 STEP 1: Creating company with all initial values...")
        
        # Navigate to company creation form
        company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
        
        # Fill all fields with initial values
        print("🔧 Filling mandatory fields...")
        company_page.fill_company_name_input(initial_values['company_name'])
        time.sleep(1)
        
        company_page.select_industry_option(initial_values['industry'])
        time.sleep(1)
        
        company_page.fill_website_input(initial_values['website'])
        time.sleep(1)
        
        company_page.fill_address_input(initial_values['address'])
        time.sleep(1)
        
        company_page.select_owner_option(initial_values['owner'])
        time.sleep(1)
        
        # Fill optional text fields
        print("🔧 Filling optional text fields...")
        company_page.fill_total_employees_input(initial_values['total_employees'])
        time.sleep(0.5)
        
        company_page.fill_main_tel_input(initial_values['main_tel'])
        time.sleep(0.5)
        
        company_page.fill_hr_tel_input(initial_values['hr_tel'])
        time.sleep(0.5)
        
        # Fill dropdown fields using verified working locators
        print("🔧 Selecting dropdown options...")
        
        # Hiring Status - Use form context to avoid ambiguity
        page.locator("div:nth-child(5) > .custom-searchable-select > .searchable-select > .select-trigger > .self-center > .chevron").click()
        time.sleep(1)
        page.locator("form").get_by_text(initial_values['hiring_status'], exact=True).click()
        time.sleep(1)
        
        # Company Grade - Use form context to avoid ambiguity
        page.locator("div:nth-child(7) > .custom-searchable-select > .searchable-select > .select-trigger > .self-center > .chevron").click()
        time.sleep(1)
        page.locator("form").get_by_text(initial_values['company_grade'], exact=True).click()
        time.sleep(1)
        
        # HQ in Japan
        company_page.select_hq_in_japan_option(initial_values['hq_in_japan'])
        time.sleep(1)
        
        # Job Opening - Use form context to avoid ambiguity  
        page.locator("div:nth-child(9) > .custom-searchable-select > .searchable-select > .select-trigger > .self-center > .chevron").click()
        time.sleep(1)
        page.locator("form").get_by_text(initial_values['job_opening'], exact=True).click()
        time.sleep(1)
        
        # Upload image
        print("🔧 Uploading company logo...")
        company_page.upload_file("images_for_test/pexels-photo.jpeg")
        time.sleep(2)
        
        # Create company
        print("🔧 Creating company...")
        company_page.click_create_button()
        time.sleep(3)
        
        # Verify company created successfully
        assert_company_created_successfully(page, company_page, initial_values['company_name'], "comprehensive_test_creation")
        print(f"✅ Company '{initial_values['company_name']}' created successfully with all initial values")
        
        # Navigate to company details page
        print("📋 STEP 2: Navigating to company details page...")
        print(f"🔍 Looking for company: {initial_values['company_name']}")
        
        # Always click the first "View Details" button (created company is always first)
        page.get_by_role("button", name="View Details").first.click()
        time.sleep(3)
        
        print("✅ Successfully navigated to company details page")
        
        # Create company page instance for editing operations
        from pages.company_page import CompanyPage
        company_page = CompanyPage(page)
        
        return initial_values, updated_values, company_page
    
    @staticmethod
    def edit_and_assert_company_name_field(page: Page, company_page, initial_values: dict, updated_values: dict):
        """
        Edit company name field with validation testing and full assertion.
        
        Args:
            page: Playwright page object
            company_page: CompanyPage instance
            initial_values: Dictionary containing initial company values
            updated_values: Dictionary containing updated company values
        """
        from playwright.sync_api import expect
        
        print(f"🔧 Editing company name from '{initial_values['company_name']}' to '{updated_values['company_name']}'")
        
        # Step 1: Locate the specific company name field container in the summary section
        company_name_container = page.locator('div.group_single_item.group').filter(has_text=f"Company name:{initial_values['company_name']}")
        
        # Step 2: First ensure the container is visible
        expect(company_name_container).to_be_visible()
        
        # Step 3: Hover over the container to make the edit icon appear
        print("🔍 Hovering over company name field to reveal edit icon...")
        company_name_container.hover()
        time.sleep(2)  # Wait longer for edit icon to appear
        
        # Step 4: Locate the edit icon within that specific container
        edit_icon = company_name_container.locator('.group_single_edit_icon')
        
        # Step 5: Wait for the icon to be visible and then click
        print("🔍 Waiting for edit icon to become visible...")
        expect(edit_icon).to_be_visible(timeout=5000)
        
        print("🔍 Clicking edit icon...")
        edit_icon.click()
        time.sleep(1)  # Wait for modal to open
        
        # Step 6: Wait for the textbox and first test validation with space at end
        company_name_textbox = page.get_by_role("textbox", name="Company name")
        company_name_textbox.wait_for(state="visible", timeout=10000)
        
        # Test validation: Add space at the end to trigger validation error
        print("🔍 Testing validation: Adding space at end of company name...")
        company_name_textbox.clear()
        company_name_textbox.fill(f"{updated_values['company_name']} ")  # Add space at end
        time.sleep(0.5)
        
        # Try to save with invalid data (space at end)
        page.get_by_role("button", name="Save").click()
        time.sleep(2)  # Wait for validation message
        
        # Assert validation error appears
        validation_error = page.get_by_text("Company name should not start or end with special characters.")
        enhanced_assert_visible(page, validation_error, "Validation error should appear for space at end", "validation_space_at_end")
        print("✅ Validation error correctly appeared for space at end")
        
        # Now clear and input the correct data
        print("🔧 Now inputting correct company name without space...")
        company_name_textbox.clear()
        company_name_textbox.fill(updated_values['company_name'])
        time.sleep(0.5)
        
        # Step 7: Save the changes
        page.get_by_role("button", name="Save").click()
        time.sleep(2)  # Wait for save to complete
        
        # Step 8: Assert the update message appears
        enhanced_assert_visible(page, company_page.locators.company_updated_successfully_message, "Company info updated message should appear", "edit_company_name")
        time.sleep(1)
        
        # Step 9: Assert the updated company name is visible on the page
        print(f"🔍 Verifying company name was updated to: {updated_values['company_name']}")
        # Use more specific locator targeting the Summary section field
        updated_name_visible = page.locator("div.group_single_item.group").filter(has_text=f"Company name:{updated_values['company_name']}")
        expect(updated_name_visible).to_be_visible()
        print(f"✅ Company name successfully updated to: {updated_values['company_name']}")
    
    @staticmethod
    def edit_and_assert_website_field(page: Page, company_page, initial_values: dict, updated_values: dict):
        """
        Edit website field with validation testing and full assertion.
        
        Args:
            page: Playwright page object
            company_page: CompanyPage instance
            initial_values: Dictionary containing initial company values
            updated_values: Dictionary containing updated company values
        """
        from playwright.sync_api import expect
        
        print(f"🔧 Editing website from '{initial_values['website']}' to '{updated_values['website']}'")
        
        # Step 1: Locate the specific website field container in the summary section
        website_container = page.locator('div.group_single_item.group').filter(has_text=f"Web page:{initial_values['website']}")
        
        # Step 2: First ensure the container is visible
        expect(website_container).to_be_visible()
        
        # Step 3: Hover over the container to make the edit icon appear
        print("🔍 Hovering over website field to reveal edit icon...")
        website_container.hover()
        time.sleep(2)  # Wait for edit icon to appear
        
        # Step 4: Locate and click the edit icon
        edit_icon = website_container.locator('.group_single_edit_icon')
        expect(edit_icon).to_be_visible(timeout=5000)
        edit_icon.click()
        time.sleep(1)  # Wait for modal to open
        
        # Step 5: Test validation with invalid website (without https)
        website_textbox = page.get_by_role("textbox", name="Web page")
        website_textbox.wait_for(state="visible", timeout=10000)
        
        print("🔍 Testing validation: Adding invalid website without https...")
        website_textbox.clear()
        website_textbox.fill("www.invalid-website.com")  # Invalid without https
        time.sleep(0.5)
        
        # Try to save with invalid data
        page.get_by_role("button", name="Save").click()
        time.sleep(2)  # Wait for validation message
        
        # Assert validation error appears
        validation_error = page.get_by_text("Please enter a valid website URL")
        enhanced_assert_visible(page, validation_error, "Validation error should appear for invalid website", "validation_invalid_website")
        print("✅ Validation error correctly appeared for invalid website")
        
        # Now clear and input the correct data
        print("🔧 Now inputting correct website...")
        website_textbox.clear()
        website_textbox.fill(updated_values['website'])
        time.sleep(0.5)
        
        # Step 6: Save the changes
        page.get_by_role("button", name="Save").click()
        time.sleep(2)  # Wait for save to complete
        
        # Step 7: Assert the update message appears
        enhanced_assert_visible(page, company_page.locators.company_updated_successfully_message, "Company info updated message should appear", "edit_website")
        time.sleep(1)
        
        # Step 8: Assert the updated website is visible on the page
        print(f"🔍 Verifying website was updated to: {updated_values['website']}")
        updated_website_visible = page.locator("div.group_single_item.group").filter(has_text=f"Web page:{updated_values['website']}")
        expect(updated_website_visible).to_be_visible()
        print(f"✅ Website successfully updated to: {updated_values['website']}")
    
    @staticmethod
    def edit_and_assert_industry_field(page: Page, company_page, initial_values: dict, updated_values: dict):
        """
        Edit industry field with validation and full assertion.
        """
        from playwright.sync_api import expect
        
        print(f"🔧 Editing industry from '{initial_values['industry']}' to '{updated_values['industry']}'")
        
        # Step 1: Locate the specific industry field container
        industry_container = page.locator('div.group_single_item.group').filter(has_text=f"Industry:{initial_values['industry']}")
        
        # Step 2: Hover and click edit icon
        print("🔍 Hovering over industry field to reveal edit icon...")
        expect(industry_container).to_be_visible()
        industry_container.hover()
        time.sleep(2)
        
        edit_icon = industry_container.locator('.group_single_edit_icon')
        expect(edit_icon).to_be_visible(timeout=5000)
        edit_icon.click()
        time.sleep(1)
        
        # Step 3: Select new industry from dropdown
        print(f"🔧 Selecting new industry: {updated_values['industry']}")
        industry_dropdown = page.locator(".select-trigger")
        industry_dropdown.click()
        time.sleep(1)
        
        page.get_by_text(updated_values['industry'], exact=True).click()
        time.sleep(0.5)
        
        # Step 4: Save changes
        page.get_by_role("button", name="Save").click()
        time.sleep(2)
        
        # Step 5: Assert success and updated value
        enhanced_assert_visible(page, company_page.locators.company_updated_successfully_message, "Company info updated message should appear", "edit_industry")
        time.sleep(1)
        
        print(f"🔍 Verifying industry was updated to: {updated_values['industry']}")
        updated_industry_visible = page.locator("div.group_single_item.group").filter(has_text=f"Industry:{updated_values['industry']}")
        expect(updated_industry_visible).to_be_visible()
        print(f"✅ Industry successfully updated to: {updated_values['industry']}")
    
    @staticmethod
    def edit_and_assert_address_field(page: Page, company_page, initial_values: dict, updated_values: dict):
        """
        Edit company address field with validation and full assertion.
        """
        from playwright.sync_api import expect
        
        print(f"🔧 Editing address from '{initial_values['address']}' to '{updated_values['address']}'")
        
        # Step 1: Locate the specific address field container
        address_container = page.locator('div.group_single_item.group').filter(has_text=f"Company address:{initial_values['address']}")
        
        # Step 2: Hover and click edit icon
        print("🔍 Hovering over address field to reveal edit icon...")
        expect(address_container).to_be_visible()
        address_container.hover()
        time.sleep(2)
        
        edit_icon = address_container.locator('.group_single_edit_icon')
        expect(edit_icon).to_be_visible(timeout=5000)
        edit_icon.click()
        time.sleep(1)
        
        # Step 3: Fill address field
        address_textbox = page.get_by_role("textbox", name="Company address")
        address_textbox.wait_for(state="visible", timeout=10000)
        address_textbox.clear()
        address_textbox.fill(updated_values['address'])
        time.sleep(0.5)
        
        # Step 4: Save changes
        page.get_by_role("button", name="Save").click()
        time.sleep(2)
        
        # Step 5: Assert success and updated value
        enhanced_assert_visible(page, company_page.locators.company_updated_successfully_message, "Company info updated message should appear", "edit_address")
        time.sleep(1)
        
        print(f"🔍 Verifying address was updated to: {updated_values['address']}")
        updated_address_visible = page.locator("div.group_single_item.group").filter(has_text=f"Company address:{updated_values['address']}")
        expect(updated_address_visible).to_be_visible()
        print(f"✅ Address successfully updated to: {updated_values['address']}")
    
    @staticmethod
    def edit_and_assert_hq_in_japan_field(page: Page, company_page, initial_values: dict, updated_values: dict):
        """
        Edit HQ in Japan field with validation and full assertion.
        """
        from playwright.sync_api import expect
        
        print(f"🔧 Editing HQ in Japan from '{initial_values['hq_in_japan']}' to '{updated_values['hq_in_japan']}'")
        
        # Step 1: Locate the specific HQ in Japan field container
        hq_container = page.locator('div.group_single_item.group').filter(has_text=f"HQ in JPN:{initial_values['hq_in_japan']}")
        
        # Step 2: Hover and click edit icon
        print("🔍 Hovering over HQ in Japan field to reveal edit icon...")
        expect(hq_container).to_be_visible()
        hq_container.hover()
        time.sleep(2)
        
        edit_icon = hq_container.locator('.group_single_edit_icon')
        expect(edit_icon).to_be_visible(timeout=5000)
        edit_icon.click()
        time.sleep(1)
        
        # Step 3: Select new option from dropdown
        print(f"🔧 Selecting new HQ in Japan option: {updated_values['hq_in_japan']}")
        hq_dropdown = page.locator(".select-trigger")
        hq_dropdown.click()
        time.sleep(1)
        
        page.get_by_text(updated_values['hq_in_japan'], exact=True).click()
        time.sleep(0.5)
        
        # Step 4: Save changes
        page.get_by_role("button", name="Save").click()
        time.sleep(2)
        
        # Step 5: Assert success and updated value
        enhanced_assert_visible(page, company_page.locators.company_updated_successfully_message, "Company info updated message should appear", "edit_hq_in_japan")
        time.sleep(1)
        
        print(f"🔍 Verifying HQ in Japan was updated to: {updated_values['hq_in_japan']}")
        updated_hq_visible = page.locator("div.group_single_item.group").filter(has_text=f"HQ in JPN:{updated_values['hq_in_japan']}")
        expect(updated_hq_visible).to_be_visible()
        print(f"✅ HQ in Japan successfully updated to: {updated_values['hq_in_japan']}")
    
    @staticmethod
    def edit_and_assert_global_hq_field(page: Page, company_page, initial_values: dict, updated_values: dict):
        """
        Edit Global HQ field with validation and full assertion.
        """
        from playwright.sync_api import expect
        
        print(f"🔧 Editing Global HQ to '{updated_values['global_hq']}'")
        
        # Step 1: Locate the Global HQ field container (initially N/A)
        global_hq_container = page.locator('div.group_single_item.group').filter(has_text="Global HQ:N/A")
        
        # Step 2: Hover and click edit icon
        print("🔍 Hovering over Global HQ field to reveal edit icon...")
        expect(global_hq_container).to_be_visible()
        global_hq_container.hover()
        time.sleep(2)
        
        edit_icon = global_hq_container.locator('.group_single_edit_icon')
        expect(edit_icon).to_be_visible(timeout=5000)
        edit_icon.click()
        time.sleep(1)
        
        # Step 3: Fill Global HQ field
        global_hq_textbox = page.get_by_role("textbox", name="Global HQ")
        global_hq_textbox.wait_for(state="visible", timeout=10000)
        global_hq_textbox.clear()
        global_hq_textbox.fill(updated_values['global_hq'])
        time.sleep(0.5)
        
        # Step 4: Save changes
        page.get_by_role("button", name="Save").click()
        time.sleep(2)
        
        # Step 5: Assert success and updated value
        enhanced_assert_visible(page, company_page.locators.company_updated_successfully_message, "Company info updated message should appear", "edit_global_hq")
        time.sleep(1)
        
        print(f"🔍 Verifying Global HQ was updated to: {updated_values['global_hq']}")
        updated_global_hq_visible = page.locator("div.group_single_item.group").filter(has_text=f"Global HQ:{updated_values['global_hq']}")
        expect(updated_global_hq_visible).to_be_visible()
        print(f"✅ Global HQ successfully updated to: {updated_values['global_hq']}")
    
    @staticmethod
    def edit_and_assert_country_of_origin_field(page: Page, company_page, initial_values: dict, updated_values: dict):
        """
        Edit Country of Origin field with validation and full assertion.
        """
        from playwright.sync_api import expect
        
        print(f"🔧 Editing Country of Origin to '{updated_values['country_of_origin']}'")
        
        # Step 1: Locate the Country of Origin field container (initially N/A)
        country_container = page.locator('div.group_single_item.group').filter(has_text="Country of origin:N/A")
        
        # Step 2: Hover and click edit icon
        print("🔍 Hovering over Country of Origin field to reveal edit icon...")
        expect(country_container).to_be_visible()
        country_container.hover()
        time.sleep(2)
        
        edit_icon = country_container.locator('.group_single_edit_icon')
        expect(edit_icon).to_be_visible(timeout=5000)
        edit_icon.click()
        time.sleep(1)
        
        # Step 3: Fill Country of Origin field
        country_textbox = page.get_by_role("textbox", name="Country of origin")
        country_textbox.wait_for(state="visible", timeout=10000)
        country_textbox.clear()
        country_textbox.fill(updated_values['country_of_origin'])
        time.sleep(0.5)
        
        # Step 4: Save changes
        page.get_by_role("button", name="Save").click()
        time.sleep(2)
        
        # Step 5: Assert success and updated value
        enhanced_assert_visible(page, company_page.locators.company_updated_successfully_message, "Company info updated message should appear", "edit_country_of_origin")
        time.sleep(1)
        
        print(f"🔍 Verifying Country of Origin was updated to: {updated_values['country_of_origin']}")
        updated_country_visible = page.locator("div.group_single_item.group").filter(has_text=f"Country of origin:{updated_values['country_of_origin']}")
        expect(updated_country_visible).to_be_visible()
        print(f"✅ Country of Origin successfully updated to: {updated_values['country_of_origin']}")
    
    @staticmethod
    def edit_and_assert_company_hiring_status_field(page: Page, company_page, initial_values: dict, updated_values: dict):
        """
        Edit Company hiring status field with validation and full assertion.
        """
        from playwright.sync_api import expect
        
        print(f"🔧 Editing Company hiring status from '{initial_values['hiring_status']}' to '{updated_values['hiring_status']}'")
        
        # Step 1: Locate the Company hiring status field container
        hiring_status_container = page.locator('div.group_single_item.group').filter(has_text=f"Company hiring status:{initial_values['hiring_status']}")
        
        # Step 2: Hover and click edit icon
        print("🔍 Hovering over Company hiring status field to reveal edit icon...")
        expect(hiring_status_container).to_be_visible()
        hiring_status_container.hover()
        time.sleep(2)
        
        edit_icon = hiring_status_container.locator('.group_single_edit_icon')
        expect(edit_icon).to_be_visible(timeout=5000)
        edit_icon.click()
        time.sleep(1)
        
        # Step 3: Select new option from dropdown
        print(f"🔧 Selecting new hiring status: {updated_values['hiring_status']}")
        hiring_dropdown = page.locator(".select-trigger")
        hiring_dropdown.click()
        time.sleep(1)
        
        page.get_by_text(updated_values['hiring_status'], exact=True).click()
        time.sleep(0.5)
        
        # Step 4: Save changes
        page.get_by_role("button", name="Save").click()
        time.sleep(2)
        
        # Step 5: Assert success and updated value
        enhanced_assert_visible(page, company_page.locators.company_updated_successfully_message, "Company info updated message should appear", "edit_hiring_status")
        time.sleep(1)
        
        print(f"🔍 Verifying Company hiring status was updated to: {updated_values['hiring_status']}")
        updated_hiring_visible = page.locator("div.group_single_item.group").filter(has_text=f"Company hiring status:{updated_values['hiring_status']}")
        expect(updated_hiring_visible).to_be_visible()
        print(f"✅ Company hiring status successfully updated to: {updated_values['hiring_status']}")
    
    @staticmethod
    def edit_and_assert_job_opening_field(page: Page, company_page, initial_values: dict, updated_values: dict):
        """
        Edit Job opening field with validation and full assertion.
        """
        from playwright.sync_api import expect
        
        print(f"🔧 Editing Job opening from '{initial_values['job_opening']}' to '{updated_values['job_opening']}'")
        
        # Step 1: Locate the Job opening field container
        job_opening_container = page.locator('div.group_single_item.group').filter(has_text=f"Job opening:{initial_values['job_opening']}")
        
        # Step 2: Hover and click edit icon
        print("🔍 Hovering over Job opening field to reveal edit icon...")
        expect(job_opening_container).to_be_visible()
        job_opening_container.hover()
        time.sleep(2)
        
        edit_icon = job_opening_container.locator('.group_single_edit_icon')
        expect(edit_icon).to_be_visible(timeout=5000)
        edit_icon.click()
        time.sleep(1)
        
        # Step 3: Select new option from dropdown
        print(f"🔧 Selecting new job opening option: {updated_values['job_opening']}")
        job_dropdown = page.locator(".select-trigger")
        job_dropdown.click()
        time.sleep(1)
        
        page.get_by_text(updated_values['job_opening'], exact=True).click()
        time.sleep(0.5)
        
        # Step 4: Save changes
        page.get_by_role("button", name="Save").click()
        time.sleep(2)
        
        # Step 5: Assert success and updated value
        enhanced_assert_visible(page, company_page.locators.company_updated_successfully_message, "Company info updated message should appear", "edit_job_opening")
        time.sleep(1)
        
        print(f"🔍 Verifying Job opening was updated to: {updated_values['job_opening']}")
        updated_job_visible = page.locator("div.group_single_item.group").filter(has_text=f"Job opening:{updated_values['job_opening']}")
        expect(updated_job_visible).to_be_visible()
        print(f"✅ Job opening successfully updated to: {updated_values['job_opening']}")
    
    @staticmethod
    def edit_and_assert_total_employees_jpn_field(page: Page, company_page, initial_values: dict, updated_values: dict):
        """
        Edit Total employees JPN field with validation and full assertion.
        """
        from playwright.sync_api import expect
        
        print(f"🔧 Editing Total employees JPN from '{initial_values['total_employees']}' to '{updated_values['total_employees']}'")
        
        # Step 1: Locate the Total employees JPN field container
        total_employees_container = page.locator('div.group_single_item.group').filter(has_text=f"Total employees JPN:{initial_values['total_employees']}")
        
        # Step 2: Hover and click edit icon
        print("🔍 Hovering over Total employees JPN field to reveal edit icon...")
        expect(total_employees_container).to_be_visible()
        total_employees_container.hover()
        time.sleep(2)
        
        edit_icon = total_employees_container.locator('.group_single_edit_icon')
        expect(edit_icon).to_be_visible(timeout=5000)
        edit_icon.click()
        time.sleep(1)
        
        # Step 3: Fill Total employees JPN field
        total_employees_textbox = page.get_by_role("textbox", name="Total employees JPN")
        total_employees_textbox.wait_for(state="visible", timeout=10000)
        total_employees_textbox.clear()
        total_employees_textbox.fill(updated_values['total_employees'])
        time.sleep(0.5)
        
        # Step 4: Save changes
        page.get_by_role("button", name="Save").click()
        time.sleep(2)
        
        # Step 5: Assert success and updated value
        enhanced_assert_visible(page, company_page.locators.company_updated_successfully_message, "Company info updated message should appear", "edit_total_employees")
        time.sleep(1)
        
        print(f"🔍 Verifying Total employees JPN was updated to: {updated_values['total_employees']}")
        updated_employees_visible = page.locator("div.group_single_item.group").filter(has_text=f"Total employees JPN:{updated_values['total_employees']}")
        expect(updated_employees_visible).to_be_visible()
        print(f"✅ Total employees JPN successfully updated to: {updated_values['total_employees']}")
    
    @staticmethod
    def edit_and_assert_company_grade_field(page: Page, company_page, initial_values: dict, updated_values: dict):
        """
        Edit Company grade field with validation and full assertion.
        """
        from playwright.sync_api import expect
        
        print(f"🔧 Editing Company grade from '{initial_values['company_grade']}' to '{updated_values['company_grade']}'")
        
        # Step 1: Locate the Company grade field container
        company_grade_container = page.locator('div.group_single_item.group').filter(has_text=f"Company grade:{initial_values['company_grade']}")
        
        # Step 2: Hover and click edit icon
        print("🔍 Hovering over Company grade field to reveal edit icon...")
        expect(company_grade_container).to_be_visible()
        company_grade_container.hover()
        time.sleep(2)
        
        edit_icon = company_grade_container.locator('.group_single_edit_icon')
        expect(edit_icon).to_be_visible(timeout=5000)
        edit_icon.click()
        time.sleep(1)
        
        # Step 3: Select new option from dropdown
        print(f"🔧 Selecting new company grade: {updated_values['company_grade']}")
        grade_dropdown = page.locator(".select-trigger")
        grade_dropdown.click()
        time.sleep(1)
        
        page.get_by_text(updated_values['company_grade'], exact=True).click()
        time.sleep(0.5)
        
        # Step 4: Save changes
        page.get_by_role("button", name="Save").click()
        time.sleep(2)
        
        # Step 5: Assert success and updated value
        enhanced_assert_visible(page, company_page.locators.company_updated_successfully_message, "Company info updated message should appear", "edit_company_grade")
        time.sleep(1)
        
        print(f"🔍 Verifying Company grade was updated to: {updated_values['company_grade']}")
        updated_grade_visible = page.locator("div.group_single_item.group").filter(has_text=f"Company grade:{updated_values['company_grade']}")
        expect(updated_grade_visible).to_be_visible()
        print(f"✅ Company grade successfully updated to: {updated_values['company_grade']}")
    
    @staticmethod
    def edit_and_assert_main_tel_field(page: Page, company_page, initial_values: dict, updated_values: dict):
        """
        Edit Main TEL field with validation and full assertion.
        """
        from playwright.sync_api import expect
        
        print(f"🔧 Editing Main TEL from '{initial_values['main_tel']}' to '{updated_values['main_tel']}'")
        
        # Step 1: Locate the Main TEL field container
        main_tel_container = page.locator('div.group_single_item.group').filter(has_text=f"Main TEL:{initial_values['main_tel']}")
        
        # Step 2: Hover and click edit icon
        print("🔍 Hovering over Main TEL field to reveal edit icon...")
        expect(main_tel_container).to_be_visible()
        main_tel_container.hover()
        time.sleep(2)
        
        edit_icon = main_tel_container.locator('.group_single_edit_icon')
        expect(edit_icon).to_be_visible(timeout=5000)
        edit_icon.click()
        time.sleep(1)
        
        # Step 3: Fill Main TEL field
        main_tel_textbox = page.get_by_role("textbox", name="Main Tel")
        main_tel_textbox.wait_for(state="visible", timeout=10000)
        main_tel_textbox.clear()
        main_tel_textbox.fill(updated_values['main_tel'])
        time.sleep(0.5)
        
        # Step 4: Save changes
        page.get_by_role("button", name="Save").click()
        time.sleep(2)
        
        # Step 5: Assert success and updated value
        enhanced_assert_visible(page, company_page.locators.company_updated_successfully_message, "Company info updated message should appear", "edit_main_tel")
        time.sleep(1)
        
        print(f"🔍 Verifying Main TEL was updated to: {updated_values['main_tel']}")
        updated_main_tel_visible = page.locator("div.group_single_item.group").filter(has_text=f"Main TEL:{updated_values['main_tel']}")
        expect(updated_main_tel_visible).to_be_visible()
        print(f"✅ Main TEL successfully updated to: {updated_values['main_tel']}")
    
    @staticmethod
    def edit_and_assert_hr_tel_field(page: Page, company_page, initial_values: dict, updated_values: dict):
        """
        Edit HR TEL field with validation and full assertion.
        """
        from playwright.sync_api import expect
        
        print(f"🔧 Editing HR TEL from '{initial_values['hr_tel']}' to '{updated_values['hr_tel']}'")
        
        # Step 1: Locate the HR TEL field container
        hr_tel_container = page.locator('div.group_single_item.group').filter(has_text=f"HR TEL:{initial_values['hr_tel']}")
        
        # Step 2: Hover and click edit icon
        print("🔍 Hovering over HR TEL field to reveal edit icon...")
        expect(hr_tel_container).to_be_visible()
        hr_tel_container.hover()
        time.sleep(2)
        
        edit_icon = hr_tel_container.locator('.group_single_edit_icon')
        expect(edit_icon).to_be_visible(timeout=5000)
        edit_icon.click()
        time.sleep(1)
        
        # Step 3: Fill HR TEL field
        hr_tel_textbox = page.get_by_role("textbox", name="HR TEL")
        hr_tel_textbox.wait_for(state="visible", timeout=10000)
        hr_tel_textbox.clear()
        hr_tel_textbox.fill(updated_values['hr_tel'])
        time.sleep(0.5)
        
        # Step 4: Save changes
        page.get_by_role("button", name="Save").click()
        time.sleep(2)
        
        # Step 5: Assert success and updated value
        enhanced_assert_visible(page, company_page.locators.company_updated_successfully_message, "Company info updated message should appear", "edit_hr_tel")
        time.sleep(1)
        
        print(f"🔍 Verifying HR TEL was updated to: {updated_values['hr_tel']}")
        updated_hr_tel_visible = page.locator("div.group_single_item.group").filter(has_text=f"HR TEL:{updated_values['hr_tel']}")
        expect(updated_hr_tel_visible).to_be_visible()
        print(f"✅ HR TEL successfully updated to: {updated_values['hr_tel']}")
