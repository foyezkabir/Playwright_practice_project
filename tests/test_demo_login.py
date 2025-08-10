import time
import pytest
from playwright.sync_api import Page, expect
from utils.config import BASE_URL
from pages.reset_pass_page import ResetPasswordPage

def test_reset_pass_01_verify_unregistered_email_validation(page: Page):
    """Verify unregistered email validation."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("nonexistent@example.com")
    reset_page.click_next()
    reset_page.expect_unregistered_email_error()

def test_reset_pass_02_verify_attempt_limit_exceeded(page: Page):
    """Verify attempt limit exceeded error."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("nua26i@onemail.host")  # EMAIL 1 - Attempt 5 (LAST ATTEMPT)
    reset_page.click_next()
    reset_page.expect_attempt_limit_error()

def test_reset_pass_3_verify_reset_password_page(page: Page):
    """Verify reset password page elements."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL)
    reset_page.click_get_started_button()
    reset_page.expect_forgot_password_link_visibility()
    reset_page.click_forgot_password_link()
    reset_page.expect_forgot_password_heading_visible()