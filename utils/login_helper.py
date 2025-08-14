from playwright.sync_api import Page, expect
from utils.config import BASE_URL
from conftest import wait_for_action_completion
from utils.enhanced_assertions import enhanced_assert_visible, enhanced_assert_not_visible

def do_login(page: Page, email: str, password: str):
    from pages.login_page import LoginPage
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL + "/login")
    # login_page.click_get_started()
    if email:
        login_page.fill_email(email)
    if password:
        login_page.fill_password(password)
    login_page.click_sign_in()
    wait_for_action_completion(page, "login")  # Just wait for login action to complete
    return login_page

# Enhanced assertion functions for login
def assert_verification_required_for_login(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_system_shows_email_verification_page(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_verification_page_heading(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_mailbox_image(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_verification_instructions(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_otp_input_box(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_input_box_title(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_resend_otp_countdown(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_verify_button(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_resend_otp_button(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_resend_otp_success_message(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_email_required_error(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_password_required_error(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_public_domain_warning(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_invalid_email_error(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_invalid_credentials_error(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_show_password_button(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_hide_password_button(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_forgot_password_link(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_sign_in_heading(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_black_pigeon_link(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_sign_in_button_visible(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_email_label(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_password_label(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_unregistered_email_error(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_dont_have_account_text(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_nonverified_email_error(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)