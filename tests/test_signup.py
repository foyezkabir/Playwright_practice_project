import time
import pytest
import allure
from playwright.sync_api import Page, expect
from pages.signup_page import SignupPage
from utils.config import BASE_URL
from random_values_generator.random_email import RandomEmail
from utils.signup_helper import do_signup, fill_valid_signup_form, navigate_to_signup_page, navigate_to_landing_and_signup

random_email = RandomEmail()

@allure.title("TC_01 - visibility of signup heading.")
def test_TC_01(page: Page):
    """Verify visibility of signup heading."""
    signup_page = SignupPage(page)
    navigate_to_landing_and_signup(signup_page)
    signup_page.expect_signup_page_heading()

@allure.title("TC_02 - successful signup with valid data.")
def test_TC_02(page: Page):
    """Verify successful signup with valid data."""
    signup_page = SignupPage(page)
    navigate_to_signup_page(signup_page)
    
    email_address = fill_valid_signup_form(signup_page)
    signup_page.click_sign_up_button()
    signup_page.expect_signup_success_message()
    time.sleep(2)  # Wait for the success message to appear
    signup_page.expect_email_verification_page()
    signup_page.expect_verification_page_heading()

    signup_page.expect_mail_image_visible()
    signup_page.expect_verification_instructions()
    signup_page.expect_otp_input_box()
    signup_page.expect_verify_button()
    signup_page.expect_input_box_title()
    signup_page.expect_back_button()

@allure.title("TC_03 - full name required error.")
def test_TC_03(page: Page):
    """Verify full name required error."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_full_name_required_error()

@allure.title("TC_04 - email required error.")
def test_TC_04(page: Page):
    """Verify email required error."""
    signup_page = do_signup(page, full_name="John Doe", email="", password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_email_required_error()

@allure.title("TC_05 - password required error.")
def test_TC_05(page: Page):
    """Verify password required error."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="", confirm_password="Kabir123#")
    signup_page.expect_password_required_error()

@allure.title("TC_06 - confirm password required error.")
def test_TC_06(page: Page):
    """Verify confirm password required error."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="Kabir123#", confirm_password="")
    signup_page.expect_confirm_password_required_error()

@allure.title("TC_07 - password mismatch error.")
def test_TC_07(page: Page):
    """Verify password mismatch error."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="Kabir123#", confirm_password="DifferentPass123#")
    signup_page.expect_password_mismatch_error()

@allure.title("TC_08 - invalid email format error.")
def test_TC_08(page: Page):
    """Verify invalid email format error."""
    signup_page = do_signup(page, full_name="John Doe", email="invalid-email.com", password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_invalid_email_error()

@allure.title("TC_09 - existing email error.")
def test_TC_09(page: Page):
    """Verify existing email error."""
    signup_page = do_signup(page, full_name="John Doe", email="50st3o@mepost.pw", password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_email_exists_error()

@allure.title("TC_10 - public domain email warning.")
def test_TC_10(page: Page):
    """Verify public domain email warning."""
    signup_page = do_signup(page, full_name="John Doe", email="test@hotmail.com", password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_public_domain_warning()

@allure.title("TC_11 - weak password warning.")
def test_TC_11(page: Page):
    """Verify weak password warning."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="weakpassword", confirm_password="weakpassword")
    signup_page.expect_password_strength_warning()

@allure.title("TC_12 - successful signup message.")
def test_TC_12(page: Page):
    """Verify successful signup message."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_signup_success_message()

@allure.title("TC_13 - full name minimum character limit.")
def test_TC_13(page: Page):
    """Verify full name minimum character limit."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="Jo", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_full_name_min_limit()

@allure.title("TC_14 - full name maximum character limit.")
def test_TC_14(page: Page):
    """Verify full name maximum character limit."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="A" * 81, email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_full_name_max_limit()

@allure.title("TC_15 - full name can contain special characters.")
def test_TC_15(page: Page):
    """Verify full name can contain special characters."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John@Doe", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_full_name_contains_numbers()

@allure.title("TC_16 - full name can only contain numbers.")
def test_TC_16(page: Page):
    """Verify full name can only contain numbers."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="123", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_full_name_contains_numbers()

@allure.title("TC_17 - full name cannot start or end with special characters.")
def test_TC_17(page: Page):
    """Verify full name cannot start or end with special characters."""
    email = random_email.generate_email()
    
    # Test name starting with space
    signup_page = do_signup(page, full_name=" John Doe", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_full_name_contains_special_characters()
    
    # Test name ending with space
    signup_page.fill_full_name("John Doe ")
    signup_page.click_sign_up_button()
    signup_page.expect_full_name_contains_special_characters()

@allure.title("TC_18 - visibility of full name label.")
def test_TC_18(page: Page):
    """Verify visibility of full name label."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.expect_full_name_label()

@allure.title("TC_19 - visibility of email label.")
def test_TC_19(page: Page):
    """Verify visibility of email label."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.expect_email_label()

@allure.title("TC_20 - visibility of password label.")
def test_TC_20(page: Page):
    """Verify visibility of password label."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.expect_password_label()

@allure.title("TC_21 - visibility of confirm password label.")
def test_TC_21(page: Page):
    """Verify visibility of confirm password label."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.expect_confirm_password_label()

@allure.title("TC_22 - show/hide password functionality.")
def test_TC_22(page: Page):
    """Verify show/hide password functionality."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    email_address = random_email.generate_email()
    
    signup_page.fill_full_name("John Doe")
    signup_page.fill_email(email_address)
    signup_page.fill_password("Kabir123#")
    expect(signup_page.locators.show_password_button).to_be_visible()
    signup_page.locators.show_password_button.click()
    expect(signup_page.locators.hide_password_button).to_be_visible()
    signup_page.locators.hide_password_button.click()
    expect(signup_page.locators.show_password_button).to_be_visible()

@allure.title("TC_23 - visibility of 'By clicking Agree & Join or' text.")
def test_TC_23(page: Page):
    """Verify visibility of 'By clicking Agree & Join or' text."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.expect_by_clicking_sign_up_button()

@allure.title("TC_24 - visibility of Privacy Policy link.")
def test_TC_24(page: Page):
    """Verify visibility of Privacy Policy link."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.expect_policy_link()

@allure.title("TC_25 - visibility of User Agreement link.")
def test_TC_25(page: Page):
    """Verify visibility of User Agreement link."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.expect_user_agreement_link()

@allure.title("TC_26 - email verification page visibility.")
def test_TC_26(page: Page):
    """Verify email verification page visibility."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_email_verification_page()

@allure.title("TC_27 - OTP verification page heading visibility.")
def test_TC_27(page: Page):
    """Verify OTP verification page heading visibility."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_verification_page_heading()

@allure.title("TC_28 - mailbox image visibility on verification page.")
def test_TC_28(page: Page):
    """Verify mailbox image visibility on verification page."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_mail_image_visible()

@allure.title("TC_29 - verification instructions visibility on verification page.")
def test_TC_29(page: Page):
    """Verify verification instructions visibility on verification page."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_verification_instructions()

@allure.title("TC_30 - OTP input box visibility on verification page.")
def test_TC_30(page: Page):
    """Verify OTP input box visibility on verification page."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_otp_input_box()

@allure.title("TC_31 - input box title visibility on verification page.")
def test_TC_31(page: Page):
    """Verify input box title visibility on verification page."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_input_box_title()

@allure.title("TC_32 - verify button visibility on verification page.")
def test_TC_32(page: Page):
    """Verify verify button visibility on verification page."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_verify_button()

@allure.title("TC_33 - visibility of resend OTP button on verification page.")
def test_TC_33(page: Page):
    """Verify visibility of resend OTP button on verification page."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="Kabir123#", confirm_password="Kabir123#")
    time.sleep(60)  # Wait for the OTP input box to appear
    signup_page.expect_resend_otp_button()

@allure.title("TC_34 - resend OTP countdown visibility on verification page.")
def test_TC_34(page: Page):
    """Verify resend OTP countdown visibility on verification page."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_resend_otp_countdown()
