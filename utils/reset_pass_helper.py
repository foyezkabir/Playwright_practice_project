"""
Reset Password Helper Module
Contains utility functions for reset password tests
"""

from playwright.sync_api import Page
from utils.config import BASE_URL
from conftest import wait_for_action_completion
from utils.enhanced_assertions import enhanced_assert_visible, enhanced_assert_not_visible

def do_reset_password_navigation(page: Page, url: str = None):
    """
    Helper function to navigate to reset password page
    
    Args:
        page: Playwright page object
        url: URL to navigate (optional, defaults to forgot-password page)
    
    Returns:
        ResetPasswordPage instance
    """
    from pages.reset_pass_page import ResetPasswordPage
    reset_page = ResetPasswordPage(page)
    if url:
        reset_page.navigate_to_reset_password(url)
    else:
        reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    return reset_page

def do_reset_password_flow(page: Page, email: str = None, otp: str = None, 
                          new_password: str = None, confirm_password: str = None,
                          submit: bool = False):
    """
    Helper function to perform reset password flow with given data
    
    Args:
        page: Playwright page object
        email: Email to enter (optional)
        otp: OTP to enter (optional)
        new_password: New password to enter (optional)
        confirm_password: Confirm password to enter (optional)
        submit: Whether to click submit buttons (optional)
    
    Returns:
        ResetPasswordPage instance
    """
    from pages.reset_pass_page import ResetPasswordPage
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    
    if email:
        reset_page.enter_email(email)
        if submit:
            reset_page.click_next()
            wait_for_action_completion(page, "navigation")
    
    if otp:
        reset_page.enter_otp(otp)
    
    if new_password:
        reset_page.enter_new_password(new_password)
    
    if confirm_password:
        reset_page.enter_confirm_password(confirm_password)
    
    if submit and (otp or new_password or confirm_password):
        reset_page.click_set_password()
        # Don't wait - let the test immediately check for toast messages
        # wait_for_action_completion(page, "save")
    
    return reset_page

def navigate_to_forgot_password_via_login(page: Page):
    """
    Helper function to navigate to forgot password from login page
    
    Args:
        page: Playwright page object
    
    Returns:
        ResetPasswordPage instance
    """
    from pages.reset_pass_page import ResetPasswordPage
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_landing_page(BASE_URL)
    reset_page.click_get_started_button()
    reset_page.click_forgot_password_link()
    return reset_page

# Enhanced assertion helper functions for reset password tests
def assert_reset_password_heading(page: Page):
    """Assert reset password heading is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.reset_password_heading, "Reset password heading should be visible")

def assert_error_reset_pass_attempt_limit(page: Page):
    """Assert reset password attempt limit error is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.error_reset_pass_attempt_limit, "Reset password attempt limit error should be visible")

def assert_error_invalid_email(page: Page):
    """Assert invalid email error is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.error_invalid_email, "Invalid email error should be visible")

def assert_error_email_required(page: Page):
    """Assert email required error is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.error_email_required, "Email required error should be visible")

def assert_error_public_domain_email(page: Page):
    """Assert public domain email error is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.error_public_domain_email, "Public domain email error should be visible")

def assert_error_unregistered_email(page: Page):
    """Assert unregistered email error is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.error_unregistered_email, "Unregistered email error should be visible")

def assert_error_nonverified_email(page: Page):
    """Assert non-verified email error is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.error_nonverified_email, "Non-verified email error should be visible")

def assert_error_invalid_otp(page: Page):
    """Assert invalid OTP error is visible - Toast message appears immediately"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    # Toast appears immediately, no need for extra wait - check right away
    enhanced_assert_visible(page, reset_pass_page.locators.error_invalid_otp, "Invalid OTP error should be visible", timeout=3000)

def assert_error_otp_input_limit(page: Page):
    """Assert OTP input limit error is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.error_otp_input_limit, "OTP input limit error should be visible")

def assert_error_otp_required(page: Page):
    """Assert OTP required error is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.error_otp_required, "OTP required error should be visible")

def assert_error_otp_accept_numbers_only(page: Page):
    """Assert OTP accepts numbers only error is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.error_otp_accept_numbers_only, "OTP accepts numbers only error should be visible")

def assert_error_new_password_required(page: Page):
    """Assert new password required error is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.error_new_password_required, "New password required error should be visible")

def assert_error_password_complexity(page: Page):
    """Assert password complexity error is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.error_password_complexity, "Password complexity error should be visible")

def assert_error_confirm_password_required(page: Page):
    """Assert confirm password required error is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.error_confirm_password_required, "Confirm password required error should be visible")

def assert_error_password_mismatch(page: Page):
    """Assert password mismatch error is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.error_password_mismatch, 
                          "Password mismatch error should be visible")

def assert_toast_email_with_otp_sent(page: Page):
    """Assert email with OTP sent toast is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.toast_email_with_otp_sent, 
                          "Email with OTP sent toast should be visible")

def assert_toast_otp_resent(page: Page):
    """Assert OTP resent toast is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.toast_otp_resent, 
                          "OTP resent toast should be visible")

def assert_go_to_forgot_password_link(page: Page):
    """Assert go to forgot password link is visible"""
    from pages.reset_pass_page import ResetPasswordPage
    reset_pass_page = ResetPasswordPage(page)
    enhanced_assert_visible(page, reset_pass_page.locators.go_to_forgot_password_link, 
                          "Go to forgot password link should be visible")
