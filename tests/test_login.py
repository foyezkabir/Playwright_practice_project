import time
import pytest
import allure
from playwright.sync_api import Page, expect
from utils.config import BASE_URL
from pages.login_page import LoginPage
from utils.login_helper import do_login

@allure.title("TC_01 - Verify user can do successful login with valid credentials.")
def test_TC_01(page: Page):
    """Verify user can do successful login with valid credentials."""
    do_login(page, "50st3o@mepost.pw", "Kabir123#")
    expect(page.get_by_text("Logged in successfully")).to_be_visible()

@allure.title("TC_02 - Verify user can not login with non-verified email.")
def test_TC_02(page: Page):
    """Verify user can not login with non-verified email."""
    login_page = do_login(page, "50df@mailtor.com", "Kabir123#")
    login_page.expect_nonverified_email_error()

@allure.title("TC_03 - Verify system shows email verification page.")
def test_TC_03(page: Page):
    """Verify system shows email verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_system_shows_email_verification_page()

@allure.title("TC_04 - Verify verification page heading visibility.")
def test_TC_04(page: Page):
    """Verify verification page heading visibility."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_verification_page_heading()

@allure.title("TC_05 - Verify mailbox image visibility on verification page.")
def test_TC_05(page: Page):
    """Verify mailbox image visibility on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_mailbox_image()

@allure.title("TC_06 - Verify verification instructions visibility on verification page.")
def test_TC_06(page: Page):
    """Verify verification instructions visibility on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_verification_instructions()

@allure.title("TC_07 - Verify OTP input box visibility on verification page.")
def test_TC_07(page: Page):
    """Verify OTP input box visibility on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_otp_input_box()

@allure.title("TC_08 - Verify input box title visibility on verification page.")
def test_TC_08(page: Page):
    """Verify input box title visibility on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_input_box_title()

@allure.title("TC_09 - Verify verify button visibility on verification page.")
def test_TC_09(page: Page):
    """Verify verify button visibility on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_verify_button()

@allure.title("TC_10 - Verify resend OTP countdown visibility on verification page.")
def test_TC_10(page: Page):
    """Verify resend OTP countdown visibility on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    login_page.expect_resend_otp_countdown()

@allure.title("TC_11 - Verify visibility of resend OTP button on verification page.")
def test_TC_11(page: Page):
    """Verify visibility of resend OTP button on verification page."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    time.sleep(60)
    login_page.expect_resend_otp_button()

@allure.title("TC_12 - Verify visibility of OTP resent success message.")
def test_TC_12(page: Page):
    """Verify visibility of OTP resent success message."""
    login_page = do_login(page, "50so@mepost.pw", "Kabir123#")
    time.sleep(60)
    login_page.click_resend_otp()
    login_page.expect_resend_otp_success_message()
    login_page.expect_resend_otp_countdown()

@allure.title("TC_13 - Verify visibility of email field required error.")
def test_TC_13(page: Page):
    """Verify visibility of email field required error."""
    login_page = do_login(page, "", "password123")
    login_page.expect_email_required_error()

@allure.title("TC_14 - Verify visibility of password field required error.")
def test_TC_14(page: Page):
    """Verify visibility of password field required error."""
    login_page = do_login(page, "50st3o@mepost.pw", "")
    login_page.expect_password_required_error()

@allure.title("TC_15 - Verify visibility of public domain email warning.")
def test_TC_15(page: Page):
    """Verify visibility of public domain email warning."""
    login_page = do_login(page, "kabirwiit@gmail.com", "")
    login_page.expect_public_domain_warning()

@allure.title("TC_16 - Verify visibility of email and password fields required error.")
def test_TC_16(page: Page):
    """Verify visibility of email and password fields required error."""
    login_page = do_login(page, "", "")
    login_page.expect_email_required_error()
    login_page.expect_password_required_error()

@allure.title("TC_17 - Verify user can not login with invalid email format.")
def test_TC_17(page: Page):
    """Verify user can not login with invalid email format."""
    login_page = do_login(page, "invalid-email", "Kabir123#")
    login_page.expect_invalid_email_error()

@allure.title("TC_18 - Verify user can not login with invalid credentials.")
def test_TC_18(page: Page):
    """Verify user can not login with invalid credentials."""
    login_page = do_login(page, "50st3o@mepost.pw", "wrong-password")
    login_page.expect_invalid_credentials_error()

@allure.title("TC_19 - Verify show/hide password functionality works.")
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

@allure.title("TC_20 - Verify forgot password link is visible on login page.")
def test_TC_20(page: Page):
    """Verify forgot password link is visible on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_forgot_password_link()

@allure.title("TC_21 - Verify visibility of sign in heading on login page.")
def test_TC_21(page: Page):
    """Verify visibility of sign in heading on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_sign_in_heading()

@allure.title("TC_22 - Verify visibility of Black Pigeon heading on login page.")
def test_TC_22(page: Page):
    """Verify visibility of Black Pigeon heading on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_black_pigeon_link()

@allure.title("TC_23 - Verify visibility of sign in button on login page.")
def test_TC_23(page: Page):
    """Verify visibility of sign in button on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_sign_in_button_visible()

@allure.title("TC_24 - Verify visibility of email label on login page.")
def test_TC_24(page: Page):
    """Verify visibility of email label on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_email_label()

@allure.title("TC_25 - Verify visibility of password label on login page.")
def test_TC_25(page: Page):
    """Verify visibility of password label on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_password_label()

@allure.title("TC_26 - Verify user can not login with unregistered email.")
def test_TC_26(page: Page):
    """Verify user can not login with unregistered email."""
    login_page = do_login(page, "unregistered@example.com", "Kabir123#")
    login_page.expect_unregistered_email_error()

@allure.title("TC_27 - Verify visibility of 'Don't have an account?' text on login page.")
def test_TC_27(page: Page):
    """Verify visibility of 'Don't have an account?' text on login page."""
    login_page = do_login(page, None, None)
    login_page.expect_dont_have_account_text()
