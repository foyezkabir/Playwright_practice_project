"""
Email Verification Helper Functions
Provides centralized assertion functions for email verification tests with enhanced screenshot capabilities.
"""

from playwright.sync_api import Page
from utils.enhanced_assertions import enhanced_assert_visible, enhanced_assert_not_visible

def assert_verification_success_message(page: Page, locator, message: str):
    """Assert that verification success message is visible"""
    enhanced_assert_visible(page, locator, message)

def assert_verification_error_message(page: Page, locator, message: str):
    """Assert that verification error message is visible"""
    enhanced_assert_visible(page, locator, message)

def assert_resend_otp_success_message(page: Page, locator, message: str):
    """Assert that resend OTP success message is visible"""
    enhanced_assert_visible(page, locator, message)

def assert_sign_in_heading_visible(page: Page, locator, message: str):
    """Assert that sign in heading is visible after successful verification"""
    enhanced_assert_visible(page, locator, message)

def assert_resend_otp_button_visible(page: Page, locator, message: str):
    """Assert that resend OTP button is visible"""
    enhanced_assert_visible(page, locator, message)

def assert_verification_page_heading_visible(page: Page, locator, message: str):
    """Assert that OTP verification page heading is visible"""
    enhanced_assert_visible(page, locator, message)

def assert_resend_otp_countdown_visible(page: Page, locator, message: str):
    """Assert that resend OTP countdown is visible"""
    enhanced_assert_visible(page, locator, message)

def assert_verification_instructions_visible(page: Page, locator, message: str):
    """Assert that verification instructions are visible"""
    enhanced_assert_visible(page, locator, message)

def assert_otp_input_container_visible(page: Page, locator, message: str):
    """Assert that OTP input container is visible"""
    enhanced_assert_visible(page, locator, message)

def assert_verify_button_visible(page: Page, locator, message: str):
    """Assert that verify button is visible"""
    enhanced_assert_visible(page, locator, message)
