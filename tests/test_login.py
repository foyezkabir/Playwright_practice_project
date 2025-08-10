import time
from playwright.sync_api import Page, expect
from utils.config import BASE_URL
from pages.login_page import LoginPage

def test_login_01_successful_login(page: Page):
    """Test successful login."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50st3o@mepost.pw")
    login_page.fill_password("Kabir123#")
    login_page.click_sign_in()
    expect(page.get_by_text("Logged in successfully")).to_be_visible()

def test_login_02_verify_nonverified_email_instruction_message(page: Page):
    """Test login with non-verified email error."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50df@mailtor.com")
    login_page.fill_password("Kabir123#")
    login_page.click_sign_in()
    login_page.expect_nonverified_email_error()

def test_login_03_system_shows_verification_page(page: Page):
    """Test system shows verification page after login."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50so@mepost.pw")
    login_page.fill_password("Kabir123#")
    login_page.click_sign_in()
    login_page.expect_system_shows_email_verification_page()

def test_login_04_email_verification_page_heading(page: Page):
    """Test visibility of verification page heading."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50so@mepost.pw")
    login_page.fill_password("Kabir123#")
    login_page.click_sign_in()
    login_page.expect_verification_page_heading()

def test_login_05_verification_page_has_mailbox_image(page: Page):
    """Test visibility of mailbox image on verification page."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50so@mepost.pw")
    login_page.fill_password("Kabir123#")
    login_page.click_sign_in()
    login_page.expect_mailbox_image()

def test_login_06_email_verification_page_instructions_visibility(page: Page):
    """Test visibility of verification instructions on verification page."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50so@mepost.pw")
    login_page.fill_password("Kabir123#")
    login_page.click_sign_in()
    login_page.expect_verification_instructions()

def test_login_07_Verification_page_has_otp_input_box(page: Page):
    """Test visibility of OTP input box on verification page."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50so@mepost.pw")
    login_page.fill_password("Kabir123#")
    login_page.click_sign_in()
    login_page.expect_otp_input_box()

def test_login_08_Verification_page_has_input_box_title(page: Page):
    """Test visibility of input box title on verification page."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50so@mepost.pw")
    login_page.fill_password("Kabir123#")
    login_page.click_sign_in()
    login_page.expect_input_box_title()

def test_login_09_Verification_page_has_verify_button(page: Page):
    """Test visibility of verify button on verification page."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50so@mepost.pw")
    login_page.fill_password("Kabir123#")
    login_page.click_sign_in()
    login_page.expect_verify_button()

def test_login_10_Verification_page_has_resend_otp_countdown_text(page: Page):
    """Test visibility of resend OTP countdown text on verification page."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50so@mepost.pw")
    login_page.fill_password("Kabir123#")
    login_page.click_sign_in()
    login_page.expect_resend_otp_countdown()  # Ensure the countdown text is visible

def test_login_11_Verification_page_has_resend_otp_button(page: Page):
    """Test visibility of resend OTP button on verification page."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50so@mepost.pw")
    login_page.fill_password("Kabir123#")
    login_page.click_sign_in()
    time.sleep(60)  # Wait for the OTP countdown to appear
    login_page.expect_resend_otp_button()

def test_login_12_resend_otp_shows_success_message(page: Page):
    """Test visibility of verification success message."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50so@mepost.pw")
    login_page.fill_password("Kabir123#")
    login_page.click_sign_in()
    time.sleep(60)  # Wait for the OTP countdown to appear
    login_page.click_resend_otp()
    login_page.expect_resend_otp_success_message()
    login_page.expect_resend_otp_countdown()

def test_login_13_verify_email_field_required(page: Page):
    """Test login with email required error."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_password("password123")
    login_page.click_sign_in()
    login_page.expect_email_required_error()

def test_login_14_verify_password_field_required(page: Page):
    """Test login with password required error."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50st3o@mepost.pw")
    login_page.click_sign_in()
    login_page.expect_password_required_error()

def test_login_15_verify_public_domain_warning(page: Page):
    """Test login with public domain email warning."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("kabirwiit@gmail.com")
    login_page.click_sign_in()  # Added missing () to call method
    login_page.expect_public_domain_warning()

def test_login_16_verify_fields_are_required_with_empty_values(page: Page):
    """Test login with empty email and password fields."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.click_sign_in()
    login_page.expect_email_required_error()
    login_page.expect_password_required_error()

def test_login_17_verify_invalid_email(page: Page):
    """Test login with invalid email format."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("invalid-email")
    login_page.fill_password("Kabir123#")
    login_page.click_sign_in()
    login_page.expect_invalid_email_error()

def test_login_18_verify_invalid_credentials(page: Page):
    """Test login with invalid credentials."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("50st3o@mepost.pw")
    login_page.fill_password("wrong-password")
    login_page.click_sign_in()
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
    """Test visibility of forgot password link."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.expect_forgot_password_link()

def test_login_21_verify_sign_in_heading_visibility(page: Page):
    """Test visibility of sign in heading."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.expect_sign_in_heading()

def test_login_22_verify_black_pigeon_heading_visibility(page: Page):
    """Test visibility of Black Pigeon heading."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.expect_black_pigeon_link()

def test_login_23_verify_sign_in_button_visibility(page: Page):
    """Test visibility of sign in button."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.expect_sign_in_button_visible()

def test_login_24_verify_email_label_visibility(page: Page):
    """Test visibility of email label."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.expect_email_label()

def test_login_25_verify_password_label_visibility(page: Page):
    """Test visibility of password label."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.expect_password_label()

def test_login_26_verify_unregistered_email_error(page: Page):
    """Test login with unregistered email error."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.fill_email("unregistered@example.com")
    login_page.fill_password("Kabir123#")
    login_page.click_sign_in()
    login_page.expect_unregistered_email_error()

def test_login_27_verify_dont_have_account_text_visibility(page: Page):
    """Test visibility of 'Don't you have an account?' text."""
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL)
    login_page.click_get_started()
    login_page.expect_dont_have_account_text()
