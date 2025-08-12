import time
import pytest
from playwright.sync_api import Page, expect
from utils.config import BASE_URL
from pages.login_page import LoginPage
from utils.login_helper import do_login

def test_login_01_successful_login(page: Page):
    """Verify user can do successful login with valid credentials."""
    do_login(page, "50st3o@mepost.pw", "Kabir123#j")
    expect(page.get_by_text("Logged in successfully")).to_be_visible()

def test_login_02_verify_nonverified_email_instruction_message(page: Page):
    """Verify user can not login with non-verified email."""
    login_page = do_login(page, "50df@mailtor.com", "Kabir123#")
    login_page.expect_nonverified_email_error()

def test_login_03_verify_email_field_required(page: Page):
    """Verify visibility of email field required error."""
    login_page = do_login(page, "", "password123")
    login_page.expect_email_required_error()

def test_login_04_verify_password_field_required(page: Page):
    """Verify visibility of password field required error."""
    login_page = do_login(page, "50st3o@mepost.pw", "")
    login_page.expect_password_required_error()

def test_login_05_verify_public_domain_warning(page: Page):
    """Verify visibility of public domain email warning."""
    login_page = do_login(page, "kabirwiit@gmail.com", "")
    login_page.expect_public_domain_warning()

def test_login_06_verify_fields_are_required_with_empty_values(page: Page):
    """Verify visibility of email and password fields required error."""
    login_page = do_login(page, "", "")
    login_page.expect_email_required_error()
    login_page.expect_password_required_error()

def test_login_07_verify_invalid_email(page: Page):
    """Verify user can not login with invalid email format."""
    login_page = do_login(page, "invalid-email", "Kabir123#")
    login_page.expect_invalid_email_error()

def test_login_08_verify_invalid_credentials(page: Page):
    """Verify user can not login with invalid credentials."""
    login_page = do_login(page, "50st3o@mepost.pw", "wrong-password")
    page.screenshot(path="./screenshots/login_screenshot/ss_invalid_credentials.png")
    login_page.expect_invalid_credentials_error()

def test_login_09_verify_show_hide_mask_password_field(page: Page):
    """Verify show/hide password functionality works."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50st3o@mepost.pw")
    login_page.fill_password("Kabir123#")
    login_page.expect_show_password_button()
    login_page.locators.show_password_button.click()
    login_page.expect_hide_password_button()
    login_page.locators.hide_password_button.click()
    login_page.expect_show_password_button()

def test_login_10_verify_forgot_password_link_visibility(page: Page):
    """Verify forgot password link is visible on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_forgot_password_link()

def test_login_11_verify_sign_in_heading_visibility(page: Page):
    """Verify visibility of sign in heading on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_sign_in_heading()

def test_login_12_verify_black_pigeon_heading_visibility(page: Page):
    """Verify visibility of Black Pigeon heading on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_black_pigeon_link()

def test_login_13_verify_sign_in_button_visibility(page: Page):
    """Verify visibility of sign in button on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_sign_in_button_visible()

def test_login_14_verify_email_label_visibility(page: Page):
    """Verify visibility of email label on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_email_label()

def test_login_15_verify_password_label_visibility(page: Page):
    """Verify visibility of password label on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_password_label()

def test_login_16_verify_unregistered_email_error(page: Page):
    """Verify user can not login with unregistered email."""
    login_page = do_login(page, "unregistered@example.com", "Kabir123#")
    login_page.expect_unregistered_email_error()

def test_login_17_verify_dont_have_account_text_visibility(page: Page):
    """Verify visibility of 'don't have an account' text on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_dont_have_account_text()

def test_login_18_verify_login_form_elements_presence(page: Page):
    """Verify all essential login form elements are present."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    
    # Check all form elements
    login_page.expect_sign_in_heading()
    login_page.expect_email_label()
    login_page.expect_password_label()
    login_page.expect_sign_in_button_visible()
    login_page.expect_forgot_password_link()
    login_page.expect_dont_have_account_text()

def test_login_19_verify_email_validation_on_focus_loss(page: Page):
    """Verify email validation triggers on focus loss."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("invalid-email")
    login_page.locators.password_input.click()  # Focus on password to trigger validation
    login_page.expect_invalid_email_error()

def test_login_20_verify_password_field_masking(page: Page):
    """Verify password field is masked by default."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_password("TestPassword123")
    
    # Check if password field has type="password" attribute
    password_type = login_page.locators.password_input.get_attribute("type")
    assert password_type == "password", "Password field should be masked"
