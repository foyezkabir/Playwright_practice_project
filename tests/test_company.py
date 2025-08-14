import pytest
import time
from playwright.sync_api import Page
from utils.company_helper import (
    navigate_to_company_creation_form, 
    create_company_with_basic_info,
    create_company_with_full_info,
    assert_company_created_successfully,
    assert_company_name_already_exists_error,
    assert_company_name_required_error,
    assert_company_name_min_length_error,
    assert_company_name_max_length_error,
    assert_company_name_special_char_error,
    assert_industry_required_error,
    assert_file_size_validation_error,
    assert_file_type_validation_error,
    create_client_under_company,
    assert_client_name_required_error,
    edit_company_info
)
from random_values_generator.random_company_name import generate_company_name
from utils.enhanced_assertions import enhanced_assert_visible

@pytest.fixture(scope="module")
def created_company_name():
    """Generate unique company name for the test session."""
    return generate_company_name()

#Test cases starts from here

def test_TC_01(page: Page):
    """Verify navigation to company creation form with breadcrumb verification."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    # Verify breadcrumb shows "Home>Company" to confirm we're on the right page
    company_page.expect_home_company_heading("test_TC_01")

def test_TC_02(page: Page, created_company_name):
    """Verify successful company creation with all mandatory fields."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill all mandatory fields: name, industry, website, owner, address
    company_page.fill_company_name_input(created_company_name)
    company_page.select_industry_option("Finance")
    company_page.fill_website_input("https://www.example.com")
    company_page.select_owner_option("test")
    company_page.fill_address_input("123 Business Street, City")
    
    company_page.click_create_button()
    time.sleep(2)
    assert_company_created_successfully(page, company_page, created_company_name, "test_TC_02")

def test_TC_03(page: Page, created_company_name):
    """Verify duplicate company name validation error message."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill all mandatory fields with same company name to test duplicate validation
    company_page.fill_company_name_input(created_company_name)
    company_page.select_industry_option("Finance")
    company_page.fill_website_input("https://www.example.com")
    company_page.select_owner_option("test")
    company_page.fill_address_input("123 Business Street, City")
    
    company_page.click_create_button()
    time.sleep(2)
    assert_company_name_already_exists_error(page, company_page, "test_TC_03")

def test_TC_04(page: Page):
    """Verify company name required validation error message."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    # Submit without company name (leave empty)
    company_page.click_create_button()
    time.sleep(2)
    assert_company_name_required_error(page, company_page, "test_TC_04")

def test_TC_05(page: Page):
    """Verify company name minimum length validation error message."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill mandatory fields with invalid short company name
    company_page.fill_company_name_input("AB")
    company_page.select_industry_option("Finance")
    company_page.fill_website_input("https://www.example.com")
    company_page.select_owner_option("test")
    company_page.fill_address_input("123 Business Street, City")
    
    company_page.click_create_button()
    time.sleep(2)
    assert_company_name_min_length_error(page, company_page, "test_TC_05")

def test_TC_06(page: Page):
    """Verify company name maximum length validation error message."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill mandatory fields with invalid long company name
    company_page.fill_company_name_input("A" * 85)
    company_page.select_industry_option("Finance")
    company_page.fill_website_input("https://www.example.com")
    company_page.select_owner_option("test")
    company_page.fill_address_input("123 Business Street, City")
    
    company_page.click_create_button()
    time.sleep(2)
    assert_company_name_max_length_error(page, company_page, "test_TC_06")

def test_TC_07(page: Page):
    """Verify company name special character validation error message."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill mandatory fields with invalid special character company name
    company_page.fill_company_name_input("#Invalid Company")
    company_page.select_industry_option("Finance")
    company_page.fill_website_input("https://www.example.com")
    company_page.select_owner_option("test")
    company_page.fill_address_input("123 Business Street, City")
    
    company_page.click_create_button()
    time.sleep(2)
    assert_company_name_special_char_error(page, company_page, "test_TC_07")

def test_TC_08(page: Page):
    """Verify industry required validation error message."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill other mandatory fields but leave industry empty
    company_page.fill_company_name_input("Valid Company Name")
    company_page.fill_website_input("https://www.example.com")
    company_page.select_owner_option("test")
    company_page.fill_address_input("123 Business Street, City")
    
    company_page.click_create_button()
    time.sleep(2)
    assert_industry_required_error(page, company_page, "test_TC_08")

def test_TC_11(page: Page):
    """Verify file upload size validation error."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    company_page.upload_file("images_for_test/pexels-6MB.jpg")
    time.sleep(2)
    assert_file_size_validation_error(page, company_page, "test_TC_11")

def test_TC_12(page: Page):
    """Verify file upload type validation error."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    company_page.upload_file("images_for_test/file-PDF_1MB.pdf")
    time.sleep(2)
    assert_file_type_validation_error(page, company_page, "test_TC_12")

def test_TC_09(page: Page):
    """Verify company creation with all optional fields."""
    unique_company_name = generate_company_name()
    company_page = create_company_with_full_info(page, unique_company_name, industry="Technology",website="https://www.example.com",address="123 Business Street",total_employees="100",main_tel="+1234567890",hr_tel="+1234567891")
    assert_company_created_successfully(page, company_page, unique_company_name, "test_TC_09")

def test_TC_02(page: Page, created_company_name):
    """Verify successful company creation with all mandatory fields."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill all mandatory fields: name, industry, website, owner, address
    company_page.fill_company_name_input(created_company_name)
    company_page.select_industry_option("Finance")
    company_page.fill_website_input("https://www.example.com")
    company_page.select_owner_option("test")
    company_page.fill_address_input("123 Business Street, City")
    
    company_page.click_create_button()
    time.sleep(2)
    assert_company_created_successfully(page, company_page, created_company_name, "test_TC_02")

def test_TC_03(page: Page, created_company_name):
    """Verify duplicate company name validation error message."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill all mandatory fields with same company name to test duplicate validation
    company_page.fill_company_name_input(created_company_name)
    company_page.select_industry_option("Finance")
    company_page.fill_website_input("https://www.example.com")
    company_page.select_owner_option("test")
    company_page.fill_address_input("123 Business Street, City")
    
    company_page.click_create_button()
    time.sleep(2)
    assert_company_name_already_exists_error(page, company_page, "test_TC_03")

def test_TC_10(page: Page, created_company_name):
    """Verify editing company information."""
    new_company_name = f"{created_company_name} Edited"
    company_page = edit_company_info(page, created_company_name, new_company_name, "Healthcare")
    enhanced_assert_visible(page, company_page.locators.company_updated_successfully_message, "Company updated message should be visible", "test_TC_10")

def test_TC_13(page: Page, created_company_name):
    """Verify creating client under company with all mandatory fields."""
    edited_company_name = f"{created_company_name} Edited"
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Navigate to company and create client with all mandatory fields
    company_page = create_client_under_company(page, edited_company_name, english_name="Test Client", email_address="client@test.com", email_name="Work Email", job_title="Manager", department="HR")
    enhanced_assert_visible(page, company_page.locators.client_created_successfully_message, "Client created message should be visible", "test_TC_13")

def test_TC_14(page: Page):
    """Verify website field required validation error message."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill other mandatory fields but leave website empty
    company_page.fill_company_name_input("Valid Company Name")
    company_page.select_industry_option("Finance")
    company_page.select_owner_option("test")
    company_page.fill_address_input("123 Business Street, City")
    
    company_page.click_create_button()
    time.sleep(2)
    # Add helper function for website required validation
    enhanced_assert_visible(page, company_page.locators.website_required_validation_error, "Website required error should be visible", "test_TC_14")

def test_TC_15(page: Page):
    """Verify owner field required validation error message."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill other mandatory fields but leave owner empty
    company_page.fill_company_name_input("Valid Company Name")
    company_page.select_industry_option("Finance")
    company_page.fill_website_input("https://www.example.com")
    company_page.fill_address_input("123 Business Street, City")
    
    company_page.click_create_button()
    time.sleep(2)
    # Add helper function for owner required validation
    enhanced_assert_visible(page, company_page.locators.owner_required_validation_error, "Owner required error should be visible", "test_TC_15")

def test_TC_16(page: Page):
    """Verify address field required validation error message."""
    company_page = navigate_to_company_creation_form(page, "nua26i@onemail.host", "Kabir123#")
    
    # Fill other mandatory fields but leave address empty
    company_page.fill_company_name_input("Valid Company Name")
    company_page.select_industry_option("Finance")
    company_page.fill_website_input("https://www.example.com")
    company_page.select_owner_option("test")
    
    company_page.click_create_button()
    time.sleep(2)
    # Add helper function for address required validation
    enhanced_assert_visible(page, company_page.locators.address_required_validation_error, "Address required error should be visible", "test_TC_16")
