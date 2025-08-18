"""
Company Field Editing Test Module
Contains test cases for editing individual Summary tab fields in company details page
Following strict Page Object Model patterns with individual test cases per field
"""

import pytest
import time
from playwright.sync_api import Page
from pages import company_page
from utils import company_helper
from random_values_generator.random_company_name import generate_company_name
from utils.company_helper import do_company_login
from utils.enhanced_assertions import enhanced_assert_visible

@pytest.fixture(scope="module")
def created_company_name():
    """Generate unique company name for the test session."""
    return generate_company_name()

def test_TC_09(page: Page, created_company_name):
    """Verify successful company creation with all mandatory fields."""
    company_page = company_helper.navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill all mandatory fields: name, industry, website, owner, address
    company_page.fill_company_name_input(created_company_name)
    company_page.select_industry_option("Finance")
    company_page.fill_website_input("https://www.example.com")
    company_page.select_owner_option("test")
    company_page.fill_address_input("123 Business Street, City")
    
    company_page.click_create_button()
    time.sleep(2)
    company_helper.assert_company_created_successfully(page, company_page, created_company_name, "test_TC_09")


# def test_TC_17_edit_company_name_field(page: Page):
#     """Verify that company name field can be edited and updated value is displayed correctly."""
#     # Navigate directly to company details page using POM function
#     company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
#     # Test company name field editing
#     company_helper.CompanyFieldEditingHelper.edit_and_assert_company_name(page, company_page, "Updated Test Company Name 2024")

# def test_TC_18_edit_web_page_field(page: Page):
#     """Verify that web page field can be edited and updated value is displayed correctly."""
#     # Navigate directly to company details page using POM function
#     company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
#     # Test web page field editing
#     company_helper.CompanyFieldEditingHelper.edit_and_assert_web_page(page, company_page, "https://www.updated-test-website.com")

# def test_TC_19_edit_industry_field(page: Page):
#     """Verify that industry field can be edited and updated value is displayed correctly."""
#     # Navigate directly to company details page using POM function
#     company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
#     # Test industry field editing (must use valid dropdown option)
#     company_helper.CompanyFieldEditingHelper.edit_and_assert_industry(page, company_page, "Technology")

# def test_TC_20_edit_hq_in_jpn_field(page: Page):
#     """Verify that HQ in JPN field can be edited and updated value is displayed correctly."""
#     # Navigate directly to company details page using POM function
#     company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
#     # Test HQ in JPN field editing (must use valid dropdown option)
#     company_helper.CompanyFieldEditingHelper.edit_and_assert_hq_in_jpn(page, company_page, "Tokyo")

# def test_TC_21_edit_global_hq_field(page: Page):
#     """Verify that Global HQ field can be edited and updated value is displayed correctly."""
#     # Navigate directly to company details page using POM function
#     company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
#     # Test Global HQ field editing
#     company_helper.CompanyFieldEditingHelper.edit_and_assert_global_hq(page, company_page, "New York, USA")

# def test_TC_22_edit_country_of_origin_field(page: Page):
#     """Verify that Country of origin field can be edited and updated value is displayed correctly."""
#     # Navigate directly to company details page using POM function
#     company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
#     # Test Country of origin field editing
#     company_helper.CompanyFieldEditingHelper.edit_and_assert_country_of_origin(page, company_page, "United States")

# def test_TC_23_edit_company_address_field(page: Page):
#     """Verify that Company address field can be edited and updated value is displayed correctly."""
#     # Navigate directly to company details page using POM function
#     company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
#     # Test Company address field editing
#     company_helper.CompanyFieldEditingHelper.edit_and_assert_company_address(page, company_page, "123 Updated Test Street, Test City, 12345")

# def test_TC_24_edit_company_hiring_status_field(page: Page):
#     """Verify that Company hiring status field can be edited and updated value is displayed correctly."""
#     # Navigate directly to company details page using POM function
#     company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
#     # Test Company hiring status field editing (must use valid dropdown option)
#     company_helper.CompanyFieldEditingHelper.edit_and_assert_company_hiring_status(page, company_page, "Actively Hiring")

# def test_TC_25_edit_job_opening_field(page: Page):
#     """Verify that job opening field can be edited and updated value is displayed correctly."""
#     # Navigate directly to company details page using POM function
#     company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
#     # Test Job opening field editing (must use valid dropdown option)
#     company_helper.CompanyFieldEditingHelper.edit_and_assert_job_opening(page, company_page, "Available")

# def test_TC_26_edit_total_employees_jpn_field(page: Page):
#     """Verify that Total employees JPN field can be edited and updated value is displayed correctly."""
#     # Navigate directly to company details page using POM function
#     company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
#     # Test Total employees JPN field editing
#     company_helper.CompanyFieldEditingHelper.edit_and_assert_total_employees_jpn(page, company_page, "250")

# def test_TC_27_edit_company_grade_field(page: Page):
#     """Verify that Company grade field can be edited and updated value is displayed correctly."""
#     # Navigate directly to company details page using POM function
#     company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
#     # Test Company grade field editing (must use valid dropdown option)
#     company_helper.CompanyFieldEditingHelper.edit_and_assert_company_grade(page, company_page, "A+")

# def test_TC_28_edit_company_client_owner_field(page: Page):
#     """Verify that Company client owner field can be edited and updated value is displayed correctly."""
#     # Navigate directly to company details page using POM function
#     company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
#     # Test Company client owner field editing (must use valid dropdown option)
#     company_helper.CompanyFieldEditingHelper.edit_and_assert_company_client_owner(page, company_page, "John Smith")

# def test_TC_29_edit_telephone_field(page: Page):
#     """Verify that Telephone field can be edited and updated value is displayed correctly."""
#     # Navigate directly to company details page using POM function
#     company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
#     # Test Telephone field editing
#     company_helper.CompanyFieldEditingHelper.edit_and_assert_telephone(page, company_page, "+1-555-0123")

# def test_TC_30_comprehensive_all_fields_editing(page: Page):
#     """Verify that all Summary tab fields can be edited comprehensively in sequence."""
#     # Navigate directly to company details page using POM function
#     company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
#     # Test all Summary tab fields editing in sequence
#     company_helper.CompanyFieldEditingHelper.test_all_summary_fields_editing(page, company_page)


#different cases

def test_TC_31_direct_company_fields_editing(page: Page):
    """Verify comprehensive company fields editing using direct locators approach."""
    # Navigate directly to company details page using POM function
    company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
    # Execute comprehensive field editing using POM function
    company_helper.comprehensive_company_fields_editing_direct(page)

def test_TC_32_edit_company_name_individual(page: Page):
    """Verify individual company name field editing with current value."""
    # Navigate directly to company details page using POM function
    company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
    # Edit company name using POM function
    company_helper.edit_and_assert_company_name_direct(page, "Updated Modern Company")

def test_TC_33_edit_website_individual(page: Page):
    """Verify individual website field editing with current value."""
    # Navigate directly to company details page using POM function
    company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
    # Edit website using POM function
    company_helper.edit_and_assert_website_direct(page, "https://www.new-updated-modern.com")

def test_TC_34_edit_industry_individual(page: Page):
    """Verify individual industry field editing with current value."""
    # Navigate directly to company details page using POM function
    company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
    # Edit industry using POM function
    company_helper.edit_and_assert_industry_direct(page, "Finance")

def test_TC_35_edit_hq_in_jpn_individual(page: Page):
    """Verify individual HQ in JPN field editing with current value."""
    # Navigate directly to company details page using POM function
    company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
    # Edit HQ in JPN using POM function
    company_helper.edit_and_assert_hq_in_jpn_direct(page, "Yes")

def test_TC_36_edit_global_hq_individual(page: Page):
    """Verify individual Global HQ field editing with current value."""
    # Navigate directly to company details page using POM function
    company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
    # Edit Global HQ using POM function
    company_helper.edit_and_assert_global_hq_direct(page, "Australia")

def test_TC_37_edit_country_of_origin_individual(page: Page):
    """Verify individual Country of origin field editing with current value."""
    # Navigate directly to company details page using POM function
    company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
    # Edit Country of origin using POM function
    company_helper.edit_and_assert_country_of_origin_direct(page, "Canada")

def test_TC_38_edit_company_address_individual(page: Page):
    """Verify individual Company address field editing with current value."""
    # Navigate directly to company details page using POM function
    company_page = company_helper.navigate_to_company_details_direct(page, "nua26i@onemail.host", "Kabir123#")
    
    # Edit Company address using POM function
    company_helper.edit_and_assert_company_address_direct(page, "789 New Business Plaza, Floor 5")
