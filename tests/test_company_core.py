import pytest
import time
import re
from playwright.sync_api import Page, expect
from utils import company_helper
from utils.company_helper import do_company_login
from random_values_generator.random_company_name import generate_company_name
from utils.enhanced_assertions import enhanced_assert_visible
from pages.company_page import CompanyPage

@pytest.fixture(scope="module")
def created_company_name():
    """Generate unique company name for the test session."""
    return generate_company_name()

#Test cases starts from here

def test_TC_01(page: Page):
    """Verify navigation to company creation form with breadcrumb verification."""
    company_page = company_helper.navigate_to_company_creation_form(page, "3ek690@givememail.club", "Kabir123#")
    # Verify breadcrumb shows "Home>Company" to confirm we're on the right page
    company_page.expect_home_company_heading("test_TC_01")

def test_TC_02(page: Page):
    """Verify all mandatory field validation errors are displayed when form is submitted empty."""
    company_page = company_helper.navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Submit the form without filling any mandatory fields
    company_page.click_create_button()
    time.sleep(2)
    
    # Assert all mandatory field validation errors
    company_helper.assert_company_name_required_error(page, company_page, "test_TC_02")
    company_helper.assert_industry_required_error(page, company_page, "test_TC_02")
    company_helper.assert_website_required_error(page, company_page, "test_TC_02")
    company_helper.assert_address_required_error(page, company_page, "test_TC_02")
    company_helper.assert_owner_required_error(page, company_page, "test_TC_02")

def test_TC_03(page: Page):
    """Verify company name minimum length validation error message."""
    company_page = company_helper.navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill mandatory fields with invalid short company name
    company_page.fill_company_name_input("AB")
    
    company_page.click_industry_dropdown()
    time.sleep(2)
    company_helper.assert_company_name_min_length_error(page, company_page, "test_TC_03")

def test_TC_04(page: Page):
    """Verify company name maximum length validation error message."""
    company_page = company_helper.navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill mandatory fields with invalid long company name
    company_page.fill_company_name_input("A" * 85)
    
    company_page.click_main_tel_input()
    time.sleep(2)
    company_helper.assert_company_name_max_length_error(page, company_page, "test_TC_04")

def test_TC_05(page: Page):
    """Verify company name special character validation error message."""
    company_page = company_helper.navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill mandatory fields with invalid special character company name
    company_page.fill_company_name_input("#Invalid Company")

    company_page.click_address_input()
    time.sleep(2)
    company_helper.assert_company_name_special_char_error(page, company_page, "test_TC_05")

def test_TC_06(page: Page):
    """Verify file upload size validation error."""
    company_page = company_helper.navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    company_page.upload_file("images_for_test/pexels-6MB.jpg")
    time.sleep(2)
    company_helper.assert_file_size_validation_error(page, company_page, "test_TC_06")

def test_TC_07(page: Page):
    """Verify file type upload validation error."""
    company_page = company_helper.navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    company_page.upload_file("images_for_test/file-PDF_1MB.pdf")
    time.sleep(2)
    company_helper.assert_file_type_validation_error(page, company_page, "test_TC_07")

def test_TC_08(page: Page):
    """Verify company creation with all optional fields including image upload."""
    unique_company_name = generate_company_name()
    
    # Create company with all fields and image upload
    company_page = company_helper.create_company_with_all_fields_and_image(page, unique_company_name)
    
    # Verify company created successfully
    company_helper.assert_company_created_successfully(page, company_page, unique_company_name, "test_TC_08")
    company_helper.assert_company_logo_visible_with_name(page, company_page, unique_company_name, "test_TC_08")
    # company_helper.assert_company_logo_visible_with_name(page, company_page, unique_company_name, "test_TC_08")

#Test case 09 & 10 will use the same random generated company name.
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

def test_TC_10(page: Page, created_company_name):
    """Verify duplicate company name validation using the company created in TC_09."""
    # Login and navigate to company page (same as any other test)
    company_page = company_helper.navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill form with the SAME company name from TC_09 (guaranteed duplicate)
    company_page.fill_company_name_input(created_company_name)
    company_page.select_industry_option("Healthcare")  # Different industry but same name
    company_page.fill_website_input("https://www.duplicate-test.com")
    company_page.fill_address_input("789 Duplicate Street, City")
    company_page.select_owner_option("test")
    
    # Submit form
    company_page.click_create_button()
    time.sleep(2)
    
    # Verify duplicate company name validation error
    company_helper.assert_company_name_already_exists_error(page, company_page, "test_TC_10")
    print(f"✅ Duplicate validation confirmed for company name: '{created_company_name}'")

def test_TC_11(page: Page, created_company_name):
    """Verify navigation to company details page via clicking first company."""
    company_helper.navigate_to_company_details_via_first_link(page, "nua26i@onemail.host", "Kabir123#", created_company_name, "test_TC_11")

def test_TC_12(page: Page, created_company_name):
    """Verify deletion of company created in TC_09."""
    company_helper.delete_company_and_verify(page, "nua26i@onemail.host", "Kabir123#", created_company_name, "test_TC_12")
    print(f"✅ TC_12: Successfully deleted company: '{created_company_name}'")

def test_TC_13(page: Page):
    """Verify bulk deletion of few individual companies (3-5) using individual checkboxes."""
    # Use existing bulk deletion helper with individual selection
    company_helper.bulk_delete_companies_and_verify(page, "nua26i@onemail.host", "Kabir123#", select_all=False, individual_count=4, test_name="test_TC_13")




