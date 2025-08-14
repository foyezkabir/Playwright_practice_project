import time
import email
import sys
import os
from turtle import reset
import pytest
from playwright.sync_api import Page, expect
from utils.config import BASE_URL
from pages.login_page import LoginPage
from utils.login_helper import do_login
from utils.signup_helper import do_signup
from pages.agency_page import AgencyPage   
from pages.reset_pass_page import ResetPasswordPage
from random_values_generator.random_agency_name import generate_agency_name
from pages.signup_page import SignupPage
from random_values_generator.random_email import RandomEmail
from utils.signup_helper import do_signup, fill_valid_signup_form, navigate_to_signup_page, navigate_to_landing_and_signup
from conftest import wait_for_action_completion
from utils.enhanced_assertions import enhanced_assert_visible

random_email = RandomEmail()

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import Page
from pages.signup_page import SignupPage
from pages.email_verify_page import EmailVerifyPage, EmailService

email_service = EmailService("5uH0ULA52vndQ2PKYKhEavj7G1ISTKB1", "lgb6k58k")

#For agency
@pytest.fixture(scope="module")
def created_agency_name():
    return generate_agency_name()

# Signup tests

def test_TC_01(page: Page):
    """Verify successful signup message."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="Kabir123#", confirm_password="Kabir123#")
    # Wait is now handled in the helper function
    signup_page.expect_signup_success_message()

def test_TC_02(page: Page):
    """Verify full name maximum character limit."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="A" * 81, email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_full_name_max_limit()

def test_TC_03(page: Page):
    """Verify existing email error."""
    signup_page = do_signup(page, full_name="John Doe", email="50st3o@mepost.pw", password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_email_exists_error()

# Email verification tests

def test_TC_04(page: Page):
    """user can successfully complete email verification with valid OTP."""
    signup_page = SignupPage(page)
    email_verify_page = EmailVerifyPage(page)
    
    # Precondition: Complete signup and get valid OTP
    email_service.clear_inbox()
    test_email = email_service.generate_random_email()
    
    # Complete signup to get to verification page
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("Test User")
    signup_page.fill_email(test_email)
    signup_page.fill_password("TestPass123!")
    signup_page.fill_confirm_password("TestPass123!")
    signup_page.click_sign_up_button()
    
    page.wait_for_url("**/otp-verification", timeout=15000)
    
    # Get valid OTP from email
    otp_code = email_service.wait_for_verification_email(test_email, max_attempts=10)
    assert otp_code is not None, "No verification email with OTP received"
    
    # Action: Fill in valid OTP and submit
    email_verify_page.enter_otp_code(otp_code)
    email_verify_page.wait_for_verify_button_enabled()
    email_verify_page.click_verify_button()
    
    # Wait for verification to complete using global wait function
    wait_for_action_completion(page, "verify")
    
    email_verify_page.expect_verification_success()
    email_verify_page.expect_sign_in_heading_visible()

def test_TC_05(page: Page):
    """user can not verify email with invalid OTP."""
    signup_page = SignupPage(page)
    email_verify_page = EmailVerifyPage(page)
    
    # Setup: Complete signup to get to verification page
    email_service.clear_inbox()
    test_email = email_service.generate_random_email()
    
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("Test User")
    signup_page.fill_email(test_email)
    signup_page.fill_password("TestPass123!")
    signup_page.fill_confirm_password("TestPass123!")
    signup_page.click_sign_up_button()
    
    page.wait_for_url("**/otp-verification", timeout=15000)
    
    # Action: Fill in invalid OTP "123456" and submit
    invalid_otp = "123456"
    email_verify_page.enter_otp_code(invalid_otp)
    email_verify_page.wait_for_verify_button_enabled()
    email_verify_page.click_verify_button()
    
    # Assertion: Verify error message is displayed
    time.sleep(2)
    email_verify_page.expect_verification_error()

# Login tests

def test_TC_06(page: Page):
    """Verify user can do successful login with valid credentials."""
    do_login(page, "50st3o@mepost.pw", "Kabir123#")
    expect(page.get_by_text("Logged in successfully")).to_be_visible()

def test_TC_07(page: Page):
    """Verify visibility of email field required error."""
    login_page = do_login(page, "", "password123")
    login_page.expect_email_required_error()

def test_TC_08(page: Page):
    """Verify visibility of public domain email warning."""
    login_page = do_login(page, "kabirwiit@gmail.com", "")
    login_page.expect_public_domain_warning()

# Reset password tests
def test_TC_09(page: Page):
    """non-verified email validation is visible."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("ja2768@mepost.pw") #This email is non verified
    reset_page.click_next()
    reset_page.expect_nonverified_email_error()

def test_TC_10(page: Page):
    """OTP input accepts only numbers."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("50st3o@mepost.pw")  # Email 1 - Attempt 5
    reset_page.click_next()
    reset_page.enter_otp("OTP!@#")
    reset_page.click_set_password()
    reset_page.expect_otp_accept_numbers_only_error()

def test_TC_11(page: Page):
    """email required validation is visible & Next button in disabled."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.expect_next_button_disabled()
    reset_page.click_on_email_input_box()
    reset_page.click_forgot_password_heading()

def test_TC_12(page: Page):
    """unregistered email validation is visible."""
    reset_page = ResetPasswordPage(page)
    reset_page.navigate_to_reset_password(BASE_URL + "/forgot-password")
    reset_page.enter_email("nonexistent@example.com")
    reset_page.click_next()
    reset_page.expect_unregistered_email_error()

# Agency tests

def test_TC_13(page: Page):
    """Verify agency modal appears on first time login."""
    agency_page = AgencyPage(page)
    do_login(page, "867da9@onemail.host", "Kabir123#")
    # Wait is now handled in login helper
    agency_page.expect_agency_modal_body()
    time.sleep(1)
    agency_page.click_cancel_button()
    time.sleep(1)
    agency_page.expect_all_agencies_message()

def test_TC_14(page: Page):
    """agency create modal appears or not with existing agencies."""
    agency_page = AgencyPage(page)
    do_login(page, "50st3o@mepost.pw", "Kabir123#")
    # Wait is now handled in login helper - no manual sleep needed
    agency_page.expect_no_agency_modal()
    agency_page.verify_agency_page_url()
    agency_page.verify_agency_page_url()

def test_TC_15(page: Page, created_agency_name):
    """user can edit the agency user created"""
    agency_name = created_agency_name
    agency_page = AgencyPage(page)
    do_login(page, "gi7j8d@mepost.pw", "Kabir123#")
    # Wait is now handled in login helper - reduced sleep
    time.sleep(2)
    agency_page.click_create_new_agency()
    agency_page.fill_agency_name(agency_name)
    agency_page.click_industry_dropdown()
    agency_page.click_healthcare_option()
    agency_page.fill_website("https://testagency123.com")
    agency_page.fill_address("123 Test Agency St")
    agency_page.fill_description("This is a test agency for automation.")
    agency_page.click_agency_save_button()
    time.sleep(10)
    agency_page.find_agency_in_paginated_list(page, agency_name)
    agency_page.get_agency_actions(agency_name)
    agency_page.click_edit_button_for_agency(agency_name)
    time.sleep(2)
    agency_page.locators.agency_name_input.wait_for(timeout=10000)
    updated_name = agency_name + " - Edited"
    agency_page.locators.agency_name_input.fill(updated_name)
    time.sleep(1)
    agency_page.locators.agency_update_button.click()
    # Use enhanced assertion to capture screenshot immediately if message doesn't appear
    wait_for_action_completion(page, "update")  # Wait for update to complete
    enhanced_assert_visible(page, agency_page.locators.update_confirm_message, 
                           "Update confirmation message should be visible", "test_TC_15")
    agency_page.get_agency_by_name(updated_name)




