import time
from turtle import reset
import pytest
from playwright.sync_api import Page, expect
from utils.config import BASE_URL
from pages.reset_pass_page import ResetPasswordPage
from utils.reset_pass_helper import (do_reset_password_navigation, do_reset_password_flow, navigate_to_forgot_password_via_login, assert_reset_password_heading, assert_go_to_forgot_password_link)

def test_TC_01(page: Page):
    """Verify forgot password link is visible on login page."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_landing_page(BASE_URL)
    reset_page.click_get_started_button()
    assert_go_to_forgot_password_link(page)

def test_TC_02(page: Page):
    """Verify forgot password page is visible after clicking the link."""
    reset_page = navigate_to_forgot_password_via_login(page)
    reset_page.expect_forgot_password_heading_visible()

def test_TC_03(page: Page):
    """Verify email required validation is visible."""
    reset_page = do_reset_password_navigation(page)
    reset_page.click_on_email_input_box()
    reset_page.click_forgot_password_heading()

def test_TC_04(page: Page):
    """Verify email input section's Next button is disabled."""
    reset_page = do_reset_password_navigation(page)
    reset_page.expect_next_button_disabled()

def test_TC_05(page: Page):
    """Verify invalid email format validation is visible."""
    reset_page = do_reset_password_flow(page, email="invalidemail.com", submit=True)
    reset_page.expect_invalid_email_error()

def test_TC_06(page: Page):
    """Verify unregistered email validation is visible."""
    reset_page = do_reset_password_flow(page, email="nonexistent@example.com", submit=True)
    reset_page.expect_unregistered_email_error()

def test_TC_07(page: Page):
    """Verify public domain email validation is visible."""
    reset_page = do_reset_password_flow(page, email="kabir@gmail.com", submit=True)
    reset_page.expect_public_domain_email_error()

def test_TC_08(page: Page):
    """Verify non-verified email validation is visible."""
    reset_page = do_reset_password_flow(page, email="ja2768@mepost.pw", submit=True)
    reset_page.expect_nonverified_email_error()

def test_TC_09(page: Page):
    """Verify forgot password page's elements are visible."""
    reset_page = do_reset_password_navigation(page)
    reset_page.expect_forgot_password_heading_visible()
    reset_page.expect_email_input_visible()
    reset_page.expect_next_button_visible()
    reset_page.expect_back_button_visible()

def test_TC_10(page: Page):
    """Verify reset password page's elements are visible."""
    reset_page = do_reset_password_flow(page, email="t631iv@givememail.club", submit=True) # email 1 = attempt 1
    reset_page.verify_reset_password_heading()
    reset_page.expect_otp_input_visible()
    reset_page.expect_new_password_input_visible()
    reset_page.expect_confirm_password_input_visible()
    reset_page.expect_set_password_button_visible()

def test_TC_11(page: Page):
    """Verify resend OTP countdown is visible."""
    reset_page = do_reset_password_flow(page, email="t631iv@givememail.club", submit=True) # email 1 = attempt 2
    reset_page.expect_countdown_timer_visible()

def test_TC_12(page: Page):
    """Verify valid email navigation to reset password page."""
    reset_page = do_reset_password_flow(page, email="t631iv@givememail.club", submit=True) # email 1 = attempt 3
    reset_page.expect_otp_sent_toast()
    reset_page.verify_reset_password_heading()

def test_TC_13(page: Page):
    """Verify empty fields validation message is visible."""
    reset_page = do_reset_password_flow(page, email="t631iv@givememail.club", submit=True) # email 1 = attempt 4
    reset_page.click_set_password()
    reset_page.expect_otp_required_error()
    reset_page.expect_new_password_required_error()
    reset_page.expect_confirm_password_required_error()

def test_TC_14(page: Page):
    """Verify OTP input accepts only numbers."""
    reset_page = do_reset_password_flow(page, email="t631iv@givememail.club", otp="OTP!@#", submit=True) # email 1 = attempt 5
    reset_page.expect_otp_accept_numbers_only_error()

def test_TC_15(page: Page):
    """Verify max attempt limit exceeded error is visible."""
    reset_page = do_reset_password_flow(page, email="t631iv@givememail.club", submit=True) # email 1 = Final attempt
    reset_page.expect_attempt_limit_error()

def test_TC_16(page: Page):
    """Verify OTP input limit validation with less than 6 digits."""
    reset_page = do_reset_password_flow(page, email="gi7j8d@mepost.pw", otp="123", submit=True)
    reset_page.expect_otp_input_limit_error()

def test_TC_17(page: Page):
    """Verify OTP input limit validation with more than 6 digits."""
    reset_page = do_reset_password_flow(page, email="gi7j8d@mepost.pw", otp="12345678901", submit=True)
    reset_page.expect_otp_input_limit_error()

def test_TC_18(page: Page):
    """Verify invalid OTP validation is visible."""
    reset_page = do_reset_password_flow(page, email="gi7j8d@mepost.pw", otp="123456", new_password="SecurePass123!", confirm_password="SecurePass123!", submit=True)
    reset_page.expect_invalid_otp_error()

def test_TC_19(page: Page):
    """Verify password complexity validation is visible."""
    reset_page = do_reset_password_flow(page, email="t66468@mepost.pw", otp="123456", new_password="weak", confirm_password="weak", submit=True)
    reset_page.expect_password_complexity_error()

def test_TC_20(page: Page):
    """Verify password mismatch validation is visible."""
    reset_page = do_reset_password_flow(page, email="t66468@mepost.pw", otp="123456", new_password="SecurePass123!", confirm_password="DifferentPass456@", submit=True)
    reset_page.expect_password_mismatch_error()

def test_TC_21(page: Page):
    """Verify show/hide password functionality works."""
    reset_page = do_reset_password_flow(page, email="t66468@mepost.pw", submit=True)
    reset_page.enter_new_password("SecurePass123!")
    reset_page.show_new_password()
    reset_page.hide_new_password()
    reset_page.enter_confirm_password("SecurePass123!")
    reset_page.show_confirm_password()
    reset_page.hide_confirm_password()

def test_TC_22(page: Page):
    """Verify resend OTP functionality works."""
    reset_page = do_reset_password_flow(page, email="t66468@mepost.pw", submit=True)
    reset_page.expect_countdown_timer_visible()
    time.sleep(60)  # Wait for countdown to finish
    reset_page.expect_resend_otp_button_visible()
    reset_page.click_resend_otp()
    reset_page.expect_otp_resent_toast()

def test_TC_23(page: Page):
    """Verify back button functionality on reset password page."""
    reset_page = do_reset_password_flow(page, email="867da9@onemail.host", submit=True)
    reset_page.click_back_button()
    reset_page.expect_forgot_password_heading_visible()

def test_TC_24(page: Page):
    """Verify back button functionality on email input page."""
    reset_page = do_reset_password_navigation(page)
    reset_page.click_back_button()
    expect(reset_page.page.get_by_role("heading", name="Sign in")).to_be_visible()