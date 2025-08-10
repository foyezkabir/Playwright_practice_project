import pytest
import time
from playwright.sync_api import Page, expect
from pages.agency_page import AgencyPage   
from utils.config import BASE_URL


def test_agency_01_verify_agency_modal_appearing_in_first_time_login(page: Page):
    """Test agency modal appears on first time login."""

    agency_page = AgencyPage(page)
    agency_page.navigate_to_login_page(BASE_URL + "/login")
    agency_page.fill_email("867da9@onemail.host")
    agency_page.fill_password("Kabir123#")
    agency_page.click_sign_in()

    # Wait for page to load after login
    page.wait_for_load_state("networkidle")

    agency_page.expect_agency_modal_heading()
    time.sleep(1)
    agency_page.expect_agency_modal_body()
    time.sleep(1)
    agency_page.click_cancel_button()
    time.sleep(1)
    agency_page.expect_all_agencies_message()


def test_agency_02_verify_agency_page_with_existing_agencies(page: Page):
    """Test agency page with existing agencies."""
    agency_page = AgencyPage(page)
    agency_page.navigate_to_login_page(BASE_URL + "/login")
    agency_page.fill_email("50st3o@mepost.pw")
    agency_page.fill_password("Kabir123#")
    agency_page.click_sign_in()
    time.sleep(5)
    agency_page.expect_no_agency_modal()
    agency_page.verify_agency_page_url()


def test_agency_03_verify_create_new_agency_modal(page: Page):
    """Test create new agency modal."""
    agency_page = AgencyPage(page)
    agency_page.navigate_to_login_page(BASE_URL + "/login")
    agency_page.fill_email("50st3o@mepost.pw")
    agency_page.fill_password("Kabir123#")
    agency_page.click_sign_in()
    time.sleep(5)
    agency_page.click_create_new_agency()
    time.sleep(1)
    agency_page.expect_agency_modal_heading()
    time.sleep(1)
    agency_page.expect_agency_modal_body()
    time.sleep(1)
    agency_page.click_close_modal_button()


def test_agency_04_verify_create_new_agency_functionality(page: Page):
    """Test: Delete all agencies if any exist, logout, login, create new agency, verify dashboard, go back and check agency in list."""
    from random_values_generator.random_agency_name import generate_agency_name
    agency_name = generate_agency_name()
    agency_page = AgencyPage(page)

    # Step 1: Login with new account
    agency_page.navigate_to_login_page(BASE_URL + "/login")
    agency_page.fill_email("gi7j8d@mepost.pw")
    agency_page.fill_password("Kabir123#")
    agency_page.click_sign_in()
    time.sleep(5)

    # Step 2: Delete all existing agencies if any
    try:
        agency_page.delete_all_agencies_if_exist()  # You may need to implement this helper in AgencyPage
    except Exception:
        pass

    # Step 3: Logout
    try:
        agency_page.logout()  # You may need to implement this helper in AgencyPage
        time.sleep(2)
    except Exception:
        pass

    # Step 4: Login again
    agency_page.navigate_to_login_page(BASE_URL + "/login")
    agency_page.fill_email("gi7j8d@mepost.pw")
    agency_page.fill_password("Kabir123#")
    agency_page.click_sign_in()
    time.sleep(5)

    # Step 5: Modal should appear automatically
    agency_page.expect_agency_modal_heading()

    # Step 6: Fill agency details and save
    agency_page.fill_agency_name(agency_name)
    agency_page.click_industry_dropdown()
    agency_page.click_healthcare_option()
    agency_page.fill_website("https://testagency123.com")
    agency_page.fill_address("123 Test Agency St")
    agency_page.fill_description("This is a test agency for automation.")
    agency_page.click_agency_save_button()
    time.sleep(5)

    # Step 7: Verify dashboard sentence
    expect(page.locator("text=Dashboard\nThis is a protected route for authenticated users only.")).to_be_visible()

    # Step 8: Use browser back button to go to All Agencies
    page.go_back()
    time.sleep(3)

    # Step 9: Verify the created agency appears in the list
    agency_page.verify_created_agency_appears_in_list(agency_name)




