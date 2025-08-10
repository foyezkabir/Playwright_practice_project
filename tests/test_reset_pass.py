import time
from playwright.sync_api import Page, expect
from utils.config import BASE_URL
from pages.reset_pass_page import ResetPasswordPage

# UI VISIBILITY TESTS (Tests 01-05).
# 4 Emails are ready for testing.
# ============================================================================

def test_reset_pass_01_verify_forgot_password_link_visibility(page: Page):
    """Verify forgot password link is visible on login page."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_landing_page(BASE_URL)
    reset_page.click_get_started_button()
    reset_page.expect_forgot_password_link_visibility()

def test_reset_pass_02_verify_forgot_password_page_visibility(page: Page):
    """Verify forgot password page is visible after clicking link."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_landing_page(BASE_URL)
    reset_page.click_get_started_button()
    reset_page.click_forgot_password_link()
    reset_page.expect_forgot_password_heading_visible()

def test_reset_pass_03_verify_forgot_password_page_elements(page: Page):
    """Verify forgot password page elements are visible."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.expect_forgot_password_heading_visible()
    reset_page.expect_email_input_visible()
    reset_page.expect_next_button_visible()
    reset_page.expect_back_button_visible()

def test_reset_pass_04_verify_reset_password_page_elements(page: Page):
    """Verify reset password page elements are visible."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("50st3o@mepost.pw")  # Email 1 - Attempt 1
    reset_page.click_next()
    reset_page.verify_reset_password_heading()
    reset_page.expect_otp_input_visible()
    reset_page.expect_new_password_input_visible()
    reset_page.expect_confirm_password_input_visible()
    reset_page.expect_set_password_button_visible()

def test_reset_pass_05_verify_resend_otp_countdown_visibility(page: Page):
    """Verify resend OTP countdown visibility."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("50st3o@mepost.pw")  # Email 1 - Attempt 2
    reset_page.click_next()
    reset_page.expect_countdown_timer_visible()

# EMAIL VALIDATION TESTS (Tests 06-10)
# ============================================================================

def test_reset_pass_06_verify_email_required_validation(page: Page):
    """Verify email required validation."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.click_next()
    # Note: Button might be disabled for empty email

def test_reset_pass_07_verify_invalid_email_validation(page: Page):
    """Verify invalid email format validation."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("invalidemail.com")
    reset_page.click_next()
    reset_page.expect_invalid_email_error()

def test_reset_pass_08_verify_unregistered_email_validation(page: Page):
    """Verify unregistered email validation."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("nonexistent@example.com")
    reset_page.click_next()
    reset_page.expect_unregistered_email_error()

def test_reset_pass_09_verify_public_domain_email_validation(page: Page):
    """Verify public domain email validation."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("kabir@gmail.com")
    reset_page.click_next()
    reset_page.expect_public_domain_email_error()

def test_reset_pass_10_verify_nonverified_email_validation(page: Page):
    """Verify non-verified email validation."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("ja2768@mepost.pw") #This email is non verified
    reset_page.click_next()
    reset_page.expect_nonverified_email_error()

def test_reset_pass_11_verify_valid_email_navigation_to_reset_page(page: Page):
    """Verify valid email navigation to reset password page."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("50st3o@mepost.pw")  # Email 1 - Attempt 3
    reset_page.click_next()
    reset_page.expect_otp_sent_toast()
    reset_page.verify_reset_password_heading()

# OTP VALIDATION TESTS (Tests 11-15)
# ============================================================================

def test_reset_pass_12_verify_empty_fields_validation(page: Page):
    """Verify validation when all fields are empty."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("50st3o@mepost.pw")  # Email 1 - Attempt 4
    reset_page.click_next()
    reset_page.click_set_password()
    reset_page.expect_otp_required_error()
    reset_page.expect_new_password_required_error()
    reset_page.expect_confirm_password_required_error()

def test_reset_pass_13_verify_otp_accepts_numbers_only(page: Page):
    """Verify OTP input accepts only numbers."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("50st3o@mepost.pw")  # Email 1 - Attempt 5
    reset_page.click_next()
    reset_page.enter_otp("OTP!@#")
    reset_page.expect_otp_accept_numbers_only_error()

def test_reset_pass_14_verify_attempt_limit_exceeded(page: Page):
    """Verify attempt limit exceeded error."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("50st3o@mepost.pw")  # EMAIL 1 - LAST ATTEMPT
    reset_page.click_next()
    reset_page.expect_attempt_limit_error()

# NOTE: SWITCH TO NEW EMAIL STARTING FROM TEST 13
# ============================================================================

def test_reset_pass_15_verify_otp_input_limit_with_less_than_6(page: Page):
    """Verify OTP input limit validation with less than 6 digits."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("gi7j8d@mepost.pw")  # EMAIL 2 - Attempt 1
    reset_page.click_next()
    reset_page.enter_otp("123")
    reset_page.click_set_password()
    reset_page.expect_otp_input_limit_error()

def test_reset_pass_16_verify_otp_input_limit_with_more_than_6(page: Page):
    """Verify OTP input limit validation with more than 6 digits."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("gi7j8d@mepost.pw")  # EMAIL 2 - Attempt 2
    reset_page.click_next()
    reset_page.enter_otp("12345678901")
    reset_page.click_set_password()
    reset_page.expect_otp_input_limit_error()

def test_reset_pass_17_verify_invalid_otp_validation(page: Page):
    """Verify invalid OTP validation."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("gi7j8d@mepost.pw")  # EMAIL 2 - Attempt 3
    reset_page.click_next()
    reset_page.enter_otp("123456")
    reset_page.enter_new_password("SecurePass123!")
    reset_page.enter_confirm_password("SecurePass123!")
    reset_page.click_set_password()
    reset_page.expect_invalid_otp_error()

# PASSWORD VALIDATION TESTS (Tests 16-18)
# ============================================================================

def test_reset_pass_18_verify_password_complexity_validation(page: Page):
    """Verify password complexity validation."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("t66468@mepost.pw")  # EMAIL 3 - Attempt 1
    reset_page.click_next()
    reset_page.enter_otp("123456")
    reset_page.enter_new_password("weak")
    reset_page.enter_confirm_password("weak")
    reset_page.click_set_password()
    reset_page.expect_password_complexity_error()

def test_reset_pass_19_verify_password_mismatch_validation(page: Page):
    """Verify password mismatch validation."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("t66468@mepost.pw")  # EMAIL 3 - Attempt 2
    reset_page.click_next()
    reset_page.enter_otp("123456")
    reset_page.enter_new_password("SecurePass123!")
    reset_page.enter_confirm_password("DifferentPass456@")
    reset_page.click_set_password()
    reset_page.expect_password_mismatch_error()


# FUNCTIONALITY TESTS (Tests 19-22)
# ============================================================================

def test_reset_pass_20_verify_show_hide_password_functionality(page: Page):
    """Verify show/hide password functionality."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("t66468@mepost.pw")  # EMAIL 3 - Attempt 3
    reset_page.click_next()
    reset_page.enter_new_password("SecurePass123!")
    reset_page.show_new_password()
    reset_page.hide_new_password()
    reset_page.enter_confirm_password("SecurePass123!")
    reset_page.show_confirm_password()
    reset_page.hide_confirm_password()

def test_reset_pass_21_verify_resend_otp_functionality(page: Page):
    """Verify resend OTP functionality."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("t66468@mepost.pw")  # EMAIL 3 - Attempt 4
    reset_page.click_next()
    reset_page.expect_countdown_timer_visible()
    time.sleep(60)  # Wait for countdown to finish
    reset_page.expect_resend_otp_button_visible()
    reset_page.click_resend_otp()
    reset_page.expect_otp_resent_toast()

def test_reset_pass_22_verify_back_button_functionality_from_reset_page(page: Page):
    """Verify back button functionality on reset password page."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("867da9@onemail.host")  # EMAIL 4 - Attempt 1
    reset_page.click_next()
    reset_page.click_back_button()
    reset_page.expect_forgot_password_heading_visible()

def test_reset_pass_23_verify_back_button_functionality_from_email_input_page(page: Page):
    """Verify back button functionality on email input page."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.click_back_button()
    expect(reset_page.page.get_by_role("heading", name="Sign in")).to_be_visible()