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
from pages.reset_pass_page import ResetPasswordPage
import pytest

email_service = EmailService("74A19fEsjeBBQZ1lFT7rmm0KfvEvUWnw", "lgb6k58k")

# Shared fixture to store verified email from TC_01
@pytest.fixture(scope="module")
def verified_email_data():
    return {"email": None, "password": "TestPass123!"}


#Email veriification for SignUp tests

def test_TC_01(page: Page, verified_email_data):
    """Verify user can successfully complete sign-up email verification with valid OTP."""

    signup_page = SignupPage(page)
    email_verify_page = EmailVerifyPage(page)
    
    # Precondition: Complete signup and get valid OTP
    email_service.clear_inbox()
    test_email = email_service.generate_random_email()
    
    # Store email for later reset password tests
    verified_email_data["email"] = test_email
    
    print(f"🔍 Using test email: {test_email}")
    
    # Complete signup to get to verification page
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("Test User")
    signup_page.fill_email(test_email)
    signup_page.fill_password("TestPass123!")
    signup_page.fill_confirm_password("TestPass123!")
    signup_page.click_sign_up_button()
    
    print("⏳ Waiting for OTP verification page...")
    page.wait_for_url("**/otp-verification", timeout=15000)
    print("✅ Reached OTP verification page")
    
    # Get valid OTP from email
    otp_code = email_service.wait_for_verification_email(test_email, max_attempts=20)
    assert otp_code is not None, "No verification email with OTP received"
    
    # Action: Fill in valid OTP and submit
    email_verify_page.enter_otp_code(otp_code)
    email_verify_page.wait_for_verify_button_enabled()
    email_verify_page.click_verify_button()
    time.sleep(2)
    email_verify_page.expect_verification_success()
    email_verify_page.expect_sign_in_heading_visible()

def test_TC_02(page: Page):
    """Verify user can not verify sign-up email with invalid OTP."""

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

def test_TC_03(page: Page):
    """Verify user verifies sign-up email after initial OTP expires, by resending and using new OTP."""

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
    time.sleep(2)
    email_verify_page.expect_verification_error()
    
    # Step 6: Clear OTP input (simulate clearing fields)
    email_verify_page.clear_otp_fields_by_backspace()
    
    # Step 7: Get and enter the resent OTP
    resent_otp = email_service.wait_for_verification_email(test_email, max_attempts=10)
    assert resent_otp is not None, "No resent verification email received"
    assert resent_otp != initial_otp, "Resent OTP should be different from initial OTP"
    
    email_verify_page.enter_otp_code(resent_otp)
    email_verify_page.wait_for_verify_button_enabled()
    email_verify_page.click_verify_button()
    email_verify_page.expect_verification_success()
    email_verify_page.expect_sign_in_heading_visible()


#Email veriification for Reset Password tests

def test_TC_04(page: Page, verified_email_data):
    """Verify user can successfully reset password with valid OTP."""
    
    reset_pass_page = ResetPasswordPage(page)
    
    # Precondition: Use verified email from TC_01
    test_email = verified_email_data["email"]
    assert test_email is not None, "TC_01 must run first to create verified email"
    
    print(f"🔍 Resetting password for: {test_email}")
    
    # Navigate to login page
    reset_pass_page.navigate_to_landing_page("https://bprp-qa.shadhinlab.xyz/login")
    time.sleep(2)
    
    # Click forgot password link
    reset_pass_page.click_forgot_password_link()
    
    # Request password reset OTP
    email_service.clear_inbox()
    time.sleep(2)
    reset_pass_page.enter_email(test_email)
    reset_pass_page.click_next()
    
    time.sleep(3)  # Wait for OTP email to be sent
    
    # Get reset password OTP from email
    reset_otp = email_service.wait_for_verification_email(test_email, max_attempts=20)
    assert reset_otp is not None, "No reset password OTP received"
    
    # Enter OTP and new password
    reset_pass_page.enter_otp(reset_otp)
    new_password = "NewTestPass123!"
    reset_pass_page.enter_new_password(new_password)
    reset_pass_page.enter_confirm_password(new_password)
    reset_pass_page.click_set_password()
    
    # Verify success
    time.sleep(2)
    reset_pass_page.expect_password_reset_success_toast()

def test_TC_05(page: Page, verified_email_data):
    """Verify user cannot reset password with invalid OTP."""
    
    reset_pass_page = ResetPasswordPage(page)
    
    # Precondition: Use verified email from TC_01
    test_email = verified_email_data["email"]
    assert test_email is not None, "TC_01 must run first to create verified email"
    
    # Navigate to login page
    reset_pass_page.navigate_to_landing_page("https://bprp-qa.shadhinlab.xyz/login")
    time.sleep(2)
    
    # Click forgot password link
    reset_pass_page.click_forgot_password_link()
    
    # Request password reset OTP
    email_service.clear_inbox()
    reset_pass_page.enter_email(test_email)
    reset_pass_page.click_next()
    
    time.sleep(3)  # Wait for page to load
    
    # Enter invalid OTP
    invalid_otp = "123456"
    reset_pass_page.enter_otp(invalid_otp)
    reset_pass_page.enter_new_password("NewTestPass123!")
    reset_pass_page.enter_confirm_password("NewTestPass123!")
    reset_pass_page.click_set_password()
    
    # Verify error message
    time.sleep(2)
    reset_pass_page.expect_invalid_otp_error()

def test_TC_06(page: Page, verified_email_data):
    """Verify user resets password after initial OTP expires, using resent OTP."""
    
    reset_pass_page = ResetPasswordPage(page)
    
    # Precondition: Use verified email from TC_01
    test_email = verified_email_data["email"]
    assert test_email is not None, "TC_01 must run first to create verified email"
    
    print(f"🔍 Testing resend OTP flow for: {test_email}")
    
    # Navigate to login page
    reset_pass_page.navigate_to_landing_page("https://bprp-qa.shadhinlab.xyz/login")
    time.sleep(2)
    
    # Click forgot password link
    reset_pass_page.click_forgot_password_link()
    
    # Request password reset OTP
    email_service.clear_inbox()
    reset_pass_page.enter_email(test_email)
    reset_pass_page.click_next()
    
    time.sleep(3)
    
    # Get initial OTP
    initial_otp = email_service.wait_for_verification_email(test_email, max_attempts=20)
    assert initial_otp is not None, "No initial reset password OTP received"
    
    # Wait for OTP to expire
    print("⏳ Waiting 60 seconds to simulate OTP expiry...")
    time.sleep(60)
    
    # Click resend OTP
    reset_pass_page.click_resend_otp()
    time.sleep(3)
    
    # Try with expired OTP first
    reset_pass_page.enter_otp(initial_otp)
    reset_pass_page.enter_new_password("NewTestPass123!")
    reset_pass_page.enter_confirm_password("NewTestPass123!")
    reset_pass_page.click_set_password()
    
    # Verify error message for expired OTP
    time.sleep(2)
    reset_pass_page.expect_invalid_otp_error()
    
    # Clear only the OTP input field
    reset_pass_page.locators.otp_input.clear()
    time.sleep(1)
    
    # Get and use resent OTP
    resent_otp = email_service.wait_for_verification_email(test_email, max_attempts=20)
    assert resent_otp is not None, "No resent reset password OTP received"
    assert resent_otp != initial_otp, "Resent OTP should be different from initial OTP"
    
    reset_pass_page.enter_otp(resent_otp)
    # new_password = "FinalTestPass123!"
    # reset_pass_page.enter_new_password(new_password)
    # reset_pass_page.enter_confirm_password(new_password)
    reset_pass_page.click_set_password()
    
    # Verify success
    time.sleep(2)
    reset_pass_page.expect_password_reset_success_toast()

#Email verification for Login tests with non-verified users

def test_TC_07(page: Page):
    """Verify unverified user can verify email during login with invalid OTP, resend OTP, then valid OTP."""
    
    from pages.login_page import LoginPage
    
    signup_page = SignupPage(page)
    login_page = LoginPage(page)
    email_verify_page = EmailVerifyPage(page)
    
    # Step 1: Sign up but don't verify email
    email_service.clear_inbox()
    test_email = email_service.generate_random_email()
    test_password = "TestPass123!"
    
    print(f"🔍 Signing up with unverified email: {test_email}")
    
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("Unverified User")
    signup_page.fill_email(test_email)
    signup_page.fill_password(test_password)
    signup_page.fill_confirm_password(test_password)
    signup_page.click_sign_up_button()
    
    # Wait for OTP page
    page.wait_for_url("**/otp-verification", timeout=15000)
    print("✅ Reached OTP verification page but not verifying...")
    time.sleep(1)
    
    # Step 2: Navigate to login and try to login with unverified account
    print("🔑 Attempting to login with unverified account...")
    login_page.navigate_to_landing_page("https://bprp-qa.shadhinlab.xyz/login")
    time.sleep(2)
    
    login_page.fill_email(test_email)
    login_page.fill_password(test_password)
    login_page.click_sign_in()
    
    # Should show verification required message
    time.sleep(2)
    login_page.expect_verification_required_for_login()
    print("✅ Verification required message shown")
    
    # Should redirect to verification page
    time.sleep(3)
    page.wait_for_url("**/otp-verification", timeout=15000)
    print("✅ Redirected to OTP verification page")
    
    # Step 3: Try with invalid OTP
    print("❌ Testing with invalid OTP...")
    invalid_otp = "123456"
    email_verify_page.enter_otp_code(invalid_otp)
    email_verify_page.wait_for_verify_button_enabled()
    email_verify_page.click_verify_button()
    
    time.sleep(2)
    email_verify_page.expect_verification_error()
    print("✅ Invalid OTP error shown correctly")
    
    # Step 4: Click resend OTP
    print("🔄 Resending OTP...")
    time.sleep(60)  # Wait for resend button to be enabled
    email_verify_page.expect_resend_otp_button_visible()
    email_verify_page.click_resend_otp_button()
    time.sleep(1)
    
    # Step 5: Get initial OTP and try it (should fail since time has passed)
    print("📧 Getting initial OTP from email...")
    initial_otp = email_service.wait_for_verification_email(test_email, max_attempts=20)
    assert initial_otp is not None, "No initial verification OTP received"
    
    print("⏳ Testing with initial OTP after resend...")
    # email_verify_page.clear_otp_fields_by_backspace()
    # time.sleep(1)
    
    email_verify_page.enter_otp_code(initial_otp)
    email_verify_page.wait_for_verify_button_enabled()
    email_verify_page.click_verify_button()
    
    time.sleep(1.5)
    email_verify_page.expect_verification_error()
    print("✅ Initial OTP correctly shows error after resend")
    
    # Step 6: Get the valid (resent) OTP and verify
    print("📧 Getting resent OTP from email...")
    resent_otp = email_service.wait_for_verification_email(test_email, max_attempts=20)
    assert resent_otp is not None, "No resent verification OTP received"
    assert resent_otp != initial_otp, "Resent OTP should be different from initial OTP"
    
    # Clear previous OTP and enter new one
    email_verify_page.clear_otp_fields_by_backspace()
    time.sleep(1)
    
    email_verify_page.enter_otp_code(resent_otp)
    email_verify_page.wait_for_verify_button_enabled()
    email_verify_page.click_verify_button()
    
    # Verify success
    time.sleep(1.5)
    email_verify_page.expect_verification_success()
    print("✅ Email verified successfully!")
    
    # Step 7: Should be redirected to sign-in, now login with verified account
    email_verify_page.expect_sign_in_heading_visible()
    print("🔑 Now logging in with verified account...")
    
    login_page.fill_email(test_email)
    login_page.fill_password(test_password)
    login_page.click_sign_in()
    page.wait_for_url("**/agency?page=1", timeout=15000)
    
    # Verify successful login - check for dashboard or success indicator
    time.sleep(1.5)
    # Assuming successful login redirects to dashboard or shows success
    print("✅ Login successful with verified account!")

def test_TC_08(page: Page):
    """Verify unverified user can verify email during login with valid OTP directly."""
    
    from pages.login_page import LoginPage
    
    signup_page = SignupPage(page)
    login_page = LoginPage(page)
    email_verify_page = EmailVerifyPage(page)
    
    # Step 1: Sign up but don't verify email
    email_service.clear_inbox()
    test_email = email_service.generate_random_email()
    test_password = "TestPass123!"
    
    print(f"🔍 Signing up with unverified email: {test_email}")
    
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("Unverified User Direct")
    signup_page.fill_email(test_email)
    signup_page.fill_password(test_password)
    signup_page.fill_confirm_password(test_password)
    signup_page.click_sign_up_button()
    
    # Wait for OTP page
    page.wait_for_url("**/otp-verification", timeout=15000)
    print("✅ Reached OTP verification page but not verifying...")
    time.sleep(1.5)
    
    # Step 2: Navigate to login and try to login with unverified account
    print("🔑 Attempting to login with unverified account...")
    login_page.navigate_to_landing_page("https://bprp-qa.shadhinlab.xyz/login")
    time.sleep(1.5)
    
    login_page.fill_email(test_email)
    login_page.fill_password(test_password)
    login_page.click_sign_in()
    
    # Should show verification required message
    time.sleep(1.5)
    login_page.expect_verification_required_for_login()
    print("✅ Verification required message shown")
    
    # Should redirect to verification page
    time.sleep(1.5)
    page.wait_for_url("**/otp-verification", timeout=15000)
    print("✅ Redirected to OTP verification page")
    
    # Step 3: Get valid OTP and verify directly
    print("📧 Getting valid OTP from email...")
    valid_otp = email_service.wait_for_verification_email(test_email, max_attempts=20)
    assert valid_otp is not None, "No verification OTP received"
    
    print("✅ Entering valid OTP directly...")
    email_verify_page.enter_otp_code(valid_otp)
    email_verify_page.wait_for_verify_button_enabled()
    email_verify_page.click_verify_button()
    
    # Verify success
    time.sleep(2)
    email_verify_page.expect_verification_success()
    print("✅ Email verified successfully!")
    
    # Step 4: Should be redirected to sign-in, now login with verified account
    email_verify_page.expect_sign_in_heading_visible()
    print("🔑 Now logging in with verified account...")
    
    login_page.fill_email(test_email)
    login_page.fill_password(test_password)
    login_page.click_sign_in()
    page.wait_for_url("**/agency?page=1", timeout=15000)
    
    # Verify successful login
    time.sleep(1.5)
    print("✅ Login successful with verified account!")