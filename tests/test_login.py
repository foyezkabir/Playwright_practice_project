import time
import pytest
from playwright.sync_api import Page, expect
from utils.config import BASE_URL
from pages.login_page import LoginPage
from utils.login_helper import do_login

def test_TC_01(page: Page):
    """Verify user can do successful login with valid credentials."""
    do_login(page, "50st3o@mepost.pw", "Kabir123#")
    expect(page.get_by_text("Logged in successfully")).to_be_visible()

def test_TC_02(page: Page):
    """Verify user can not login with non-verified email."""
    login_page = do_login(page, "50df@mailtor.com", "Kabir123#")
    login_page.expect_nonverified_email_error()

def test_TC_03(page: Page):
    """Verify system shows email verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_system_shows_email_verification_page()

def test_TC_04(page: Page):
    """Verify verification page heading visibility."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_verification_page_heading()

def test_TC_05(page: Page):
    """Verify mailbox image visibility on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_mailbox_image()

def test_TC_06(page: Page):
    """Verify verification instructions visibility on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_verification_instructions()

def test_TC_07(page: Page):
    """Verify OTP input box visibility on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_otp_input_box()

def test_TC_08(page: Page):
    """Verify input box title visibility on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_input_box_title()

def test_TC_09(page: Page):
    """Verify verify button visibility on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_verify_button()

def test_TC_10(page: Page):
    """Verify resend OTP countdown visibility on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_resend_otp_countdown()

def test_TC_11(page: Page):
    """Verify visibility of resend OTP button on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    time.sleep(60)
    login_page.expect_resend_otp_button()

def test_TC_12(page: Page):
    """Verify visibility of verification success message."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    time.sleep(60)
    login_page.click_resend_otp()
    login_page.expect_resend_otp_success_message()
    login_page.expect_resend_otp_countdown()

def test_TC_13(page: Page):
    """Verify visibility of email field required error."""
    login_page = do_login(page, "", "password123")
    login_page.expect_email_required_error()

def test_TC_14(page: Page):
    """Verify visibility of password field required error."""
    login_page = do_login(page, "50st3o@mepost.pw", "")
    login_page.expect_password_required_error()

def test_TC_15(page: Page):
    """Verify visibility of public domain email warning."""
    login_page = do_login(page, "kabirwiit@gmail.com", "")
    login_page.expect_public_domain_warning()

def test_TC_16(page: Page):
    """Verify visibility of email and password fields required error."""
    login_page = do_login(page, "", "")
    login_page.expect_email_required_error()
    login_page.expect_password_required_error()

def test_TC_17(page: Page):
    """Verify user can not login with invalid email format."""
    login_page = do_login(page, "invalid-email", "Kabir123#")
    login_page.expect_invalid_email_error()

def test_TC_18(page: Page):
    """Verify user can not login with invalid credentials."""
    login_page = do_login(page, "50st3o@mepost.pw", "wrong-password")
    login_page.expect_invalid_credentials_error()

def test_TC_19(page: Page):
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

def test_TC_20(page: Page):
    """Verify forgot password link is visible on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_forgot_password_link()

def test_TC_21(page: Page):
    """Verify visibility of sign in heading on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_sign_in_heading()

def test_TC_22(page: Page):
    """Verify visibility of Black Pigeon heading on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_black_pigeon_link()

def test_TC_23(page: Page):
    """Verify visibility of sign in button on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_sign_in_button_visible()

def test_TC_24(page: Page):
    """Verify visibility of email label on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_email_label()

def test_TC_25(page: Page):
    """Verify visibility of password label on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_password_label()

def test_TC_26(page: Page):
    """Verify user can not login with unregistered email."""
    login_page = do_login(page, "unregistered@example.com", "Kabir123#")
    login_page.expect_unregistered_email_error()

def test_TC_27(page: Page):
    """Verify visibility of "Don't have an account?" text on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_dont_have_account_text()
