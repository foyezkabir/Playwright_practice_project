
import time
import pytest
from playwright.sync_api import Page, expect
from utils.config import BASE_URL
from pages.login_page import LoginPage
from utils.login_helper import do_login


def test_login_01_successful_login(page: Page):
    """Test successful login."""
    do_login(page, "50st3o@mepost.pw", "Kabir123#")
    expect(page.get_by_text("Logged in successfully")).to_be_visible()


def test_login_02_verify_nonverified_email_instruction_message(page: Page):
    """Test login with non-verified email error."""
    login_page = do_login(page, "50df@mailtor.com", "Kabir123#")
    login_page.expect_nonverified_email_error()


# Parameterized verification page tests
@pytest.mark.parametrize("expect_method", [
    "expect_system_shows_email_verification_page",
    "expect_verification_page_heading",
    "expect_mailbox_image",
    "expect_verification_instructions",
    "expect_otp_input_box",
    "expect_input_box_title",
    "expect_verify_button",
    "expect_resend_otp_countdown"
])
def test_verification_page_elements(page: Page, expect_method):
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    getattr(login_page, expect_method)()


def test_login_11_Verification_page_has_resend_otp_button(page: Page):
    """Test visibility of resend OTP button on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    time.sleep(60)
    login_page.expect_resend_otp_button()


def test_login_12_resend_otp_shows_success_message(page: Page):
    """Test visibility of verification success message."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    time.sleep(60)
    login_page.click_resend_otp()
    login_page.expect_resend_otp_success_message()
    login_page.expect_resend_otp_countdown()


def test_login_13_verify_email_field_required(page: Page):
    """Test login with email required error."""
    login_page = do_login(page, "", "password123")
    login_page.expect_email_required_error()


def test_login_14_verify_password_field_required(page: Page):
    """Test login with password required error."""
    login_page = do_login(page, "50st3o@mepost.pw", "")
    login_page.expect_password_required_error()


def test_login_15_verify_public_domain_warning(page: Page):
    """Test login with public domain email warning."""
    login_page = do_login(page, "kabirwiit@gmail.com", "")
    login_page.expect_public_domain_warning()


def test_login_16_verify_fields_are_required_with_empty_values(page: Page):
    """Test login with empty email and password fields."""
    login_page = do_login(page, "", "")
    login_page.expect_email_required_error()
    login_page.expect_password_required_error()


def test_login_17_verify_invalid_email(page: Page):
    """Test login with invalid email format."""
    login_page = do_login(page, "invalid-email", "Kabir123#")
    login_page.expect_invalid_email_error()


def test_login_18_verify_invalid_credentials(page: Page):
    """Test login with invalid credentials."""
    login_page = do_login(page, "50st3o@mepost.pw", "wrong-password")
    page.screenshot(path="./screenshots/login_screenshot/ss_invalid_credentials.png")
    login_page.expect_invalid_credentials_error()


def test_login_19_verify_show_hide_mask_password_field(page: Page):
    """Test show/hide password functionality."""
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

def test_login_20_verify_forgot_password_link_visibility(page: Page):
    login_page = do_login(page, None, None)
    login_page.expect_forgot_password_link()

def test_login_21_verify_sign_in_heading_visibility(page: Page):
    login_page = do_login(page, None, None)
    login_page.expect_sign_in_heading()

def test_login_22_verify_black_pigeon_heading_visibility(page: Page):
    login_page = do_login(page, None, None)
    login_page.expect_black_pigeon_link()


def test_login_23_verify_sign_in_button_visibility(page: Page):
    login_page = do_login(page, None, None)
    login_page.expect_sign_in_button_visible()


def test_login_24_verify_email_label_visibility(page: Page):
    login_page = do_login(page, None, None)
    login_page.expect_email_label()


def test_login_25_verify_password_label_visibility(page: Page):
    login_page = do_login(page, None, None)
    login_page.expect_password_label()


def test_login_26_verify_unregistered_email_error(page: Page):
    login_page = do_login(page, "unregistered@example.com", "Kabir123#")
    login_page.expect_unregistered_email_error()


def test_login_27_verify_dont_have_account_text_visibility(page: Page):
    login_page = do_login(page, None, None)
    login_page.expect_dont_have_account_text()
