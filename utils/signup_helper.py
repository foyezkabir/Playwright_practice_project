"""
Signup Helper Module
Contains utility functions for signup tests
"""

import pytest
from playwright.sync_api import Page
from utils.config import BASE_URL
from random_values_generator.random_email import RandomEmail
from conftest import wait_for_action_completion
from utils.enhanced_assertions import enhanced_assert_visible, enhanced_assert_not_visible

# Initialize random email generator
random_email = RandomEmail()

def do_signup(page: Page, full_name: str = None, email: str = None, password: str = None, confirm_password: str = None):
    """
    Helper function to fill signup form with specified data and click signup button
    Similar to do_login helper for login tests
    
    Args:
        page: Playwright page object
        full_name: Full name to fill (optional)
        email: Email to fill (optional) 
        password: Password to fill (optional)
        confirm_password: Confirm password to fill (optional)
    
    Returns:
        SignupPage instance
    """
    from pages.signup_page import SignupPage
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    
    if full_name:
        signup_page.fill_full_name(full_name)
    if email:
        signup_page.fill_email(email)
    if password:
        signup_page.fill_password(password)
    if confirm_password:
        signup_page.fill_confirm_password(confirm_password)
    
    signup_page.click_sign_up_button()
    wait_for_action_completion(page, "signup")  # Use global wait function
    return signup_page

def fill_valid_signup_form(signup_page, email=None):
    """
    Helper function to fill signup form with valid data (without clicking signup button)
    """
    if email is None:
        email = random_email.generate_email()
    
    signup_page.fill_full_name("John Doe")
    signup_page.fill_email(email)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    return email

def navigate_to_signup_page(signup_page):
    """
    Helper function to navigate to signup page
    """
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")

def navigate_to_landing_and_signup(signup_page):
    """
    Helper function to navigate from landing page to signup
    """
    signup_page.navigate_to_landing_page(BASE_URL)
    signup_page.click_get_started()
    signup_page.click_sign_in_link()

# Enhanced assertion functions for signup
def assert_full_name_required_error(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_email_required_error(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_password_required_error(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_confirm_password_required_error(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_password_mismatch_error(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_invalid_email_error(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_email_exists_error(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_public_domain_warning(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_password_strength_warning(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_signup_success_message(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_full_name_min_limit(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_full_name_max_limit(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_full_name_contains_special_characters(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_full_name_contains_numbers(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_full_name_label(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_email_label(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_password_label(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_confirm_password_label(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_show_password_button(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_hide_password_button(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_signup_page_heading(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_by_clicking_sign_up_button(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_policy_link(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_user_agreement_link(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_email_verification_page(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_verification_page_heading(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_otp_input_box(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_input_box_title(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_verify_button(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_resend_otp_button(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_resend_otp_countdown(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_verification_success_message(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_verification_error_message(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_back_button(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_resend_otp_success_message(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_mail_image_visible(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_verification_instructions(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)

def assert_back_to_sign_in_page(page: Page, locator, message: str):
    enhanced_assert_visible(page, locator, message)
