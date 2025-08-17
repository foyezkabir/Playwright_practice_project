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
from utils.company_helper import do_company_login
from utils.enhanced_assertions import enhanced_assert_visible

def test_TC_17_edit_company_name_field(page: Page):
    """Verify that company name field can be edited and updated value is displayed correctly."""
    # Navigate directly to company details page for field editing
    company_page = company_helper.navigate_to_company_details(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)
    
    # Test company name field editing
    company_helper.CompanyFieldEditingHelper.edit_and_assert_company_name(page, company_page, "Updated Test Company Name 2024")


def test_TC_01(page: Page):
    company_page = do_company_login(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)

def test_TC_18_edit_web_page_field(page: Page):
    """Verify that web page field can be edited and updated value is displayed correctly."""
    company_page = do_company_login(page, "nua26i@onemail.host", "Kabir123#")
    company_page.click_agency_card("Test this agency")
    company_page.click_companies_link
    time.sleep(2)
    
    # Navigate to any company details page
    company_page.click_first_company_link()
    time.sleep(2)
    
    # Test web page field editing
    company_helper.CompanyFieldEditingHelper.edit_and_assert_web_page(page, company_page, "https://www.updated-test-website.com")

def test_TC_19_edit_industry_field(page: Page):
    """Verify that industry field can be edited and updated value is displayed correctly."""
    company_page = do_company_login(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)
    
    # Navigate to any company details page
    company_page.click_first_company_link()
    time.sleep(2)
    
    # Test industry field editing (must use valid dropdown option)
    company_helper.CompanyFieldEditingHelper.edit_and_assert_industry(page, company_page, "Technology")

def test_TC_20_edit_hq_in_jpn_field(page: Page):
    """Verify that HQ in JPN field can be edited and updated value is displayed correctly."""
    company_page = do_company_login(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)
    
    # Navigate to any company details page
    company_page.click_first_company_link()
    time.sleep(2)
    
    # Test HQ in JPN field editing (must use valid dropdown option)
    company_helper.CompanyFieldEditingHelper.edit_and_assert_hq_in_jpn(page, company_page, "Tokyo")

def test_TC_21_edit_global_hq_field(page: Page):
    """Verify that Global HQ field can be edited and updated value is displayed correctly."""
    company_page = do_company_login(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)
    
    # Navigate to any company details page
    company_page.click_first_company_link()
    time.sleep(2)
    
    # Test Global HQ field editing
    company_helper.CompanyFieldEditingHelper.edit_and_assert_global_hq(page, company_page, "New York, USA")

def test_TC_22_edit_country_of_origin_field(page: Page):
    """Verify that Country of origin field can be edited and updated value is displayed correctly."""
    company_page = do_company_login(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)
    
    # Navigate to any company details page
    company_page.click_first_company_link()
    time.sleep(2)
    
    # Test Country of origin field editing
    company_helper.CompanyFieldEditingHelper.edit_and_assert_country_of_origin(page, company_page, "United States")

def test_TC_23_edit_company_address_field(page: Page):
    """Verify that Company address field can be edited and updated value is displayed correctly."""
    company_page = do_company_login(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)
    
    # Navigate to any company details page
    company_page.click_first_company_link()
    time.sleep(2)
    
    # Test Company address field editing
    company_helper.CompanyFieldEditingHelper.edit_and_assert_company_address(page, company_page, "123 Updated Test Street, Test City, 12345")

def test_TC_24_edit_company_hiring_status_field(page: Page):
    """Verify that Company hiring status field can be edited and updated value is displayed correctly."""
    company_page = do_company_login(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)
    
    # Navigate to any company details page
    company_page.click_first_company_link()
    time.sleep(2)
    
    # Test Company hiring status field editing (must use valid dropdown option)
    company_helper.CompanyFieldEditingHelper.edit_and_assert_company_hiring_status(page, company_page, "Actively Hiring")

def test_TC_25_edit_job_opening_field(page: Page):
    """Verify that job opening field can be edited and updated value is displayed correctly."""
    company_page = do_company_login(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)
    
    # Navigate to any company details page
    company_page.click_first_company_link()
    time.sleep(2)
    
    # Test Job opening field editing (must use valid dropdown option)
    company_helper.CompanyFieldEditingHelper.edit_and_assert_job_opening(page, company_page, "Available")

def test_TC_26_edit_total_employees_jpn_field(page: Page):
    """Verify that Total employees JPN field can be edited and updated value is displayed correctly."""
    company_page = do_company_login(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)
    
    # Navigate to any company details page
    company_page.click_first_company_link()
    time.sleep(2)
    
    # Test Total employees JPN field editing
    company_helper.CompanyFieldEditingHelper.edit_and_assert_total_employees_jpn(page, company_page, "250")

def test_TC_27_edit_company_grade_field(page: Page):
    """Verify that Company grade field can be edited and updated value is displayed correctly."""
    company_page = do_company_login(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)
    
    # Navigate to any company details page
    company_page.click_first_company_link()
    time.sleep(2)
    
    # Test Company grade field editing (must use valid dropdown option)
    company_helper.CompanyFieldEditingHelper.edit_and_assert_company_grade(page, company_page, "A+")

def test_TC_28_edit_company_client_owner_field(page: Page):
    """Verify that Company client owner field can be edited and updated value is displayed correctly."""
    company_page = do_company_login(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)
    
    # Navigate to any company details page
    company_page.click_first_company_link()
    time.sleep(2)
    
    # Test Company client owner field editing (must use valid dropdown option)
    company_helper.CompanyFieldEditingHelper.edit_and_assert_company_client_owner(page, company_page, "John Smith")

def test_TC_29_edit_telephone_field(page: Page):
    """Verify that Telephone field can be edited and updated value is displayed correctly."""
    company_page = do_company_login(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)
    
    # Navigate to any company details page
    company_page.click_first_company_link()
    time.sleep(2)
    
    # Test Telephone field editing
    company_helper.CompanyFieldEditingHelper.edit_and_assert_telephone(page, company_page, "+1-555-0123")

def test_TC_30_comprehensive_all_fields_editing(page: Page):
    """Verify that all Summary tab fields can be edited comprehensively in sequence."""
    company_page = do_company_login(page, "nua26i@onemail.host", "Kabir123#")
    time.sleep(2)
    
    # Navigate to any company details page
    company_page.click_first_company_link()
    time.sleep(2)
    
    # Test all Summary tab fields editing in sequence
    company_helper.CompanyFieldEditingHelper.test_all_summary_fields_editing(page, company_page)
