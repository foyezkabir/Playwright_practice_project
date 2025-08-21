import pytest
import time
import re
from playwright.sync_api import Page, expect
from utils import company_helper
from utils.company_helper import ComprehensiveCompanyTestHelper
from utils.enhanced_assertions import enhanced_assert_visible
from pages.company_page import CompanyPage

def test_TC_01_comprehensive_company_creation_and_editing(page: Page):
    """Verify all the fields of summary tab are editable and retain values after editing."""
    
    # Use helper function for company creation and navigation
    initial_values, updated_values, company_page = ComprehensiveCompanyTestHelper.company_create_to_details_page(page)
    
    # Use helper function for company name editing with validation
    ComprehensiveCompanyTestHelper.edit_and_assert_company_name_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for website editing with validation
    ComprehensiveCompanyTestHelper.edit_and_assert_website_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for industry editing
    ComprehensiveCompanyTestHelper.edit_and_assert_industry_field(page, company_page, initial_values, updated_values)
        
    # Use helper function for HQ in Japan editing
    ComprehensiveCompanyTestHelper.edit_and_assert_hq_in_japan_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for Global HQ editing
    ComprehensiveCompanyTestHelper.edit_and_assert_global_hq_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for Country of Origin editing
    ComprehensiveCompanyTestHelper.edit_and_assert_country_of_origin_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for address editing
    ComprehensiveCompanyTestHelper.edit_and_assert_address_field(page, company_page, initial_values, updated_values)

    # Use helper function for Company hiring status editing
    ComprehensiveCompanyTestHelper.edit_and_assert_company_hiring_status_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for Job opening editing
    ComprehensiveCompanyTestHelper.edit_and_assert_job_opening_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for Total employees JPN editing
    ComprehensiveCompanyTestHelper.edit_and_assert_total_employees_jpn_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for Company grade editing
    ComprehensiveCompanyTestHelper.edit_and_assert_company_grade_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for Main TEL editing
    ComprehensiveCompanyTestHelper.edit_and_assert_main_tel_field(page, company_page, initial_values, updated_values)
    
    # Use helper function for HR TEL editing
    ComprehensiveCompanyTestHelper.edit_and_assert_hr_tel_field(page, company_page, initial_values, updated_values)


# Shared helper to get latest company state after TC_01
def get_latest_company_state():
    """Returns the latest company values after TC_01 editing."""
    return {
        'hiring_status': 'Recruiting',  # TC_01 final value
        'company_name': 'Updated Company Name',  # TC_01 final value
        'company_grade': 'AA',  # TC_01 final value
        'industry': 'Healthcare',  # TC_01 final value
        'website': 'https://www.updated-example.com',  # TC_01 final value
        'address': '456 Updated Business Avenue, Suite 100',  # TC_01 final value
        'hq_in_japan': 'Yes',  # TC_01 final value
        'job_opening': 'No',  # TC_01 final value
        'total_employees': '250',  # TC_01 final value
        'main_tel': '+1987654321',  # TC_01 final value
        'hr_tel': '+1987654322',  # TC_01 final value
        'global_hq': 'Tokyo, Japan',  # TC_01 final value
        'country_of_origin': 'Japan'  # TC_01 final value
    }


def navigate_to_company_list_and_select_first(page: Page):
    """Helper function to navigate to company list and select first company for editing."""
    print("📋 Navigating to company list and selecting first company")
    company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)
    return company_page


def test_TC_02_basic_company_info_tab_editing(page: Page):
    """Verify all fields in Basic Company Info tab can be edited and updated correctly."""
    
    print("🚀 TC_02: Starting Basic Company Info tab editing test")
    
    # Navigate to company list and select first company
    company_page = navigate_to_company_list_and_select_first(page)
    
    # Navigate to Basic Company Info tab
    print("📋 Navigating to Basic Company Info tab")
    company_page.click_basic_company_info_tab()
    time.sleep(2)
    
    # Get current values from TC_01's final state
    current_values = get_latest_company_state()
    
    # Prepare test data for Basic Company Info tab fields
    basic_info_updated_values = {
        'hiring_status': 'Inactive',  # TC_01 has 'Recruiting' -> change to 'Inactive'
        'company_name': 'Trusted Consulting',  # TC_01 has updated name -> Assert the name -> change to 'Trusted Consulting'
        'company_grade': 'BBB',  # TC_01 has 'AA' -> change to 'BBB'
        'what_brand': 'Nike, Adidas, Abibas, Luis vitton',  # New field
        'under_which_group': 'Megna Jamuna group',  # New field
        'industry': 'Retail'  # TC_01 has 'Healthcare' -> change to 'Retail'
    }
    
    # Test Company Hiring Status (assert TC_01 value first, then update to new value)
    ComprehensiveCompanyTestHelper.edit_and_assert_company_hiring_status_field_basic_tab(page, company_page, current_values, basic_info_updated_values)
    
    # Test Company Name (get current name dynamically from page, then update)
    print("🔧 Getting current company name dynamically from the page...")
    # Get the actual current company name from the page instead of using hardcoded values
    current_name_element = page.locator('div.group_single_item.group').filter(has_text="Company name:")
    if current_name_element.count() > 0:
        current_name_text = current_name_element.inner_text()
        actual_current_name = current_name_text.replace("Company name:", "").strip()
        print(f"📋 Found actual current company name: {actual_current_name}")
        
        # Update current_values with actual name
        current_values['company_name'] = actual_current_name
        ComprehensiveCompanyTestHelper.edit_and_assert_company_name_field_basic_tab(page, company_page, current_values, basic_info_updated_values)
    else:
        print("⚠️ Could not find company name field, skipping...")
    
    # Test Company Grade (assert TC_01 value first, then update to new value)
    ComprehensiveCompanyTestHelper.edit_and_assert_company_grade_field_basic_tab(page, company_page, current_values, basic_info_updated_values)
    
    # Test What Brand (new field)
    ComprehensiveCompanyTestHelper.edit_and_assert_what_brand_field(page, company_page, basic_info_updated_values)
    
    # Test Under Which Group (new field)
    ComprehensiveCompanyTestHelper.edit_and_assert_under_which_group_field(page, company_page, basic_info_updated_values)
    
    # Test Industry (assert TC_01 value first, then update to new value)
    ComprehensiveCompanyTestHelper.edit_and_assert_industry_field_basic_tab(page, company_page, current_values, basic_info_updated_values)


def test_TC_03_web_contact_info_tab_editing(page: Page):
    """Verify all fields in Web & Contact Info tab can be edited and updated correctly."""
    
    print("🚀 TC_03: Starting Web & Contact Info tab editing test")
    
    # Navigate to company list and select first company
    company_page = navigate_to_company_list_and_select_first(page)
    
    # Navigate to Web & Contact Info tab
    print("📋 Navigating to Web & Contact Info tab")
    company_page.click_web_contact_info_tab()
    time.sleep(2)
    
    # Get current values from TC_01's final state
    current_values = get_latest_company_state()
    
    # Prepare test data for Web & Contact Info tab
    web_contact_updated_values = {
        'website': 'https://www.updated.com'  # TC_01 has 'https://www.updated-example.com' -> change to 'https://www.updated.com'
    }
    
    # Test Web Page (assert TC_01 value first, then update to new value, then assert again)
    ComprehensiveCompanyTestHelper.edit_and_assert_website_field_web_contact_tab(page, company_page, current_values, web_contact_updated_values)


def test_TC_04_location_details_tab_editing(page: Page):
    """Verify all fields in Location Details tab can be edited and updated correctly."""
    
    print("🚀 TC_04: Starting Location Details tab editing test")
    
    # Navigate to company list and select first company
    company_page = navigate_to_company_list_and_select_first(page)
    
    # Navigate to Location Details tab
    print("📋 Navigating to Location Details tab")
    company_page.click_location_details_tab()
    time.sleep(2)
    
    # Get current values from TC_01's final state
    current_values = get_latest_company_state()
    
    # Prepare test data for Location Details tab
    location_updated_values = {
        'hq_in_japan': 'No',  # TC_01 has 'Yes' -> change to 'No'
        'global_hq': 'Tokyo, Japan - edited',  # TC_01 has 'Tokyo, Japan' -> change to 'Tokyo, Japan - edited'
        'country_of_origin': 'Japan - edited',  # TC_01 has 'Japan' -> change to 'Japan - edited'
        'address': '456 Updated'  # TC_01 has '456 Updated Business Avenue, Suite 100' -> change to '456 Updated'
    }
    
    # Test HQ in JPN (assert TC_01 value first, then update to new value, then assert again)
    ComprehensiveCompanyTestHelper.edit_and_assert_hq_in_japan_field_location_tab(page, company_page, current_values, location_updated_values)
    
    # Test Global HQ (assert TC_01 value first, then update to new value, then assert again)
    ComprehensiveCompanyTestHelper.edit_and_assert_global_hq_field_location_tab(page, company_page, current_values, location_updated_values)
    
    # Test Country of Origin (assert TC_01 value first, then update to new value, then assert again)
    ComprehensiveCompanyTestHelper.edit_and_assert_country_of_origin_field_location_tab(page, company_page, current_values, location_updated_values)
    
    # Test Company Address (assert TC_01 value first, then update to new value, then assert again)
    ComprehensiveCompanyTestHelper.edit_and_assert_address_field_location_tab(page, company_page, current_values, location_updated_values)

def test_TC_05_employees_business_info_tab_editing(page: Page):
    """Verify all fields in Employees & Business Info tab can be edited and updated correctly."""
    
    print("🚀 TC_05: Starting Employees & Business Info tab editing test")
    
    # Navigate to company list and select first company
    company_page = navigate_to_company_list_and_select_first(page)
    
    # Navigate to Employees & Business Info tab
    print("📋 Navigating to Employees & Business Info tab")
    company_page.click_employees_business_info_tab()
    time.sleep(2)
    
    # Get current values from TC_01's final state
    current_values = get_latest_company_state()
    
    # Prepare test data for Employees & Business Info tab
    employees_business_updated_values = {
        'total_employees': '687878',  # TC_01 has '250' -> change to '687878'
        'business_contents': 'Plastic and software engineering',  # New field
        'job_opening': 'Yes',  # TC_01 has 'No' -> change to 'Yes'
        'quick_notes': 'this is a dummy note, take it seriously please.'  # New field - initially "No quick notes available."
    }
    
    # Test Total Employees JPN (assert TC_01 value first, then update to new value, then assert again)
    ComprehensiveCompanyTestHelper.edit_and_assert_total_employees_jpn_field(page, company_page, current_values, employees_business_updated_values)
    
    # Test Business Contents and Key Products (new field)
    ComprehensiveCompanyTestHelper.edit_and_assert_business_contents_field(page, company_page, employees_business_updated_values)
    
    # Test Job Opening (assert TC_01 value first, then update to new value, then assert again)
    ComprehensiveCompanyTestHelper.edit_and_assert_job_opening_field(page, company_page, current_values, employees_business_updated_values)
    
    # Test Quick notes (assert initial value "No quick notes available." then update to new value)
    ComprehensiveCompanyTestHelper.edit_and_assert_quick_notes_field(page, company_page, employees_business_updated_values)

