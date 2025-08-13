import email
import time
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import Page
from utils.config import BASE_URL
from pages.signup_page import SignupPage
from pages.email_verify_page import EmailVerifyPage, EmailService

email_service = EmailService("5uH0ULA52vndQ2PKYKhEavj7G1ISTKB1", "lgb6k58k")

def test_01_verify_successful_email_verification_with_valid_otp(page: Page):
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
    email_verify_page.expect_verification_success()
    email_verify_page.expect_sign_in_heading_visible()

def test_02_verify_email_verification_with_invalid_otp(page: Page):
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


def test_03_verify_email_verification_with_resend_otp_flow(page: Page):
    """user can verify email with resend OTP flow."""

    signup_page = SignupPage(page)
    email_verify_page = EmailVerifyPage(page)
    
    # Step 1: Complete signup to trigger sending the OTP email
    email_service.clear_inbox()
    test_email = email_service.generate_random_email()
    
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("Test User")
    signup_page.fill_email(test_email)
    signup_page.fill_password("TestPass123!")
    signup_page.fill_confirm_password("TestPass123!")
    signup_page.click_sign_up_button()
    
    page.wait_for_url("**/otp-verification", timeout=15000)
    
    # Step 2: Store the initial OTP
    initial_otp = email_service.wait_for_verification_email(test_email, max_attempts=10)
    assert initial_otp is not None, "No initial verification email received"
    
    # Step 3: Wait for 60 seconds (simulate wait time for OTP expiry)
    print("⏳ Waiting 60 seconds to simulate OTP expiry...")
    time.sleep(60)
    
    # Step 4: Click Resend OTP button
    email_verify_page.expect_resend_otp_button_visible()
    email_verify_page.click_resend_otp_button()
    
    # Step 5: Enter the first (expired) OTP and verify error
    email_verify_page.enter_otp_code(initial_otp)
    email_verify_page.wait_for_verify_button_enabled()
    email_verify_page.click_verify_button()
    
    # Verify error message appears
    time.sleep(1)
    email_verify_page.expect_verification_error()
    
    # Step 6: Clear OTP input (simulate clearing fields)
    email_verify_page.clear_otp_fields_by_backspace()

    # page.reload()  # Reload to clear fields
    # page.wait_for_url("**/otp-verification", timeout=15000)
    
    # Step 7: Get and enter the resent OTP
    resent_otp = email_service.wait_for_verification_email(test_email, max_attempts=10)
    assert resent_otp is not None, "No resent verification email received"
    assert resent_otp != initial_otp, "Resent OTP should be different from initial OTP"
    
    email_verify_page.enter_otp_code(resent_otp)
    email_verify_page.wait_for_verify_button_enabled()
    email_verify_page.click_verify_button()
    email_verify_page.expect_verification_success()
    email_verify_page.expect_sign_in_heading_visible()