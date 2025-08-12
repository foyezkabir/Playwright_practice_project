import time
from playwright.sync_api import Page, expect
from pages.signup_page import SignupPage
from utils.config import BASE_URL
from random_values_generator.random_email import RandomEmail

random_email = RandomEmail() #Create an instance of RandomEmail to generate random email addresses
email_address = random_email.generate_email() # generate random email here

def test_01_signup_heading_visibility(page: Page):
    """Test visibility of signup heading."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL)
    signup_page.click_get_started()
    signup_page.click_sign_in_link()
    signup_page.expect_signup_page_heading()

def test_02_signup_success(page: Page):
    """Test successful signup."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up") 
    signup_page.fill_full_name("John Doe")
    signup_page.fill_email(email_address)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
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

def test_03_signup_full_name_required(page: Page):
    """Test signup with full name required error."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    email2 = random_email.generate_email()
    signup_page.fill_email(email2)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_full_name_required_error()

def test_04_signup_email_required(page: Page):
    """Test signup with email required error."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_email_required_error()  

def test_05_signup_password_required(page: Page):
    """Test signup with password required error."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    email3 = random_email.generate_email()
    signup_page.fill_email(email3)
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_password_required_error()

def test_06_signup_confirm_password_required(page: Page):
    """Test signup with confirm password required error."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    email4 = random_email.generate_email()
    signup_page.fill_email(email4)
    signup_page.fill_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_confirm_password_required_error()

def test_07_signup_password_mismatch(page: Page):
    """Test signup with password mismatch error."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL  + "/sign-up")
    signup_page.fill_full_name("John Doe")
    email5 = random_email.generate_email()
    signup_page.fill_email(email5)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir1234#")
    signup_page.click_sign_up_button()
    signup_page.expect_password_mismatch_error()

def test_08_signup_invalid_email(page: Page):
    """Test signup with invalid email format."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    signup_page.fill_email("invalid-email.com")
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_invalid_email_error()

def test_09_signup_email_exists(page: Page):
    """Test signup with existing email."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    signup_page.fill_email("50st3o@mepost.pw")
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    page.screenshot(path="signup_email_exists.png")

    # Wait for toast message to appear
    # page.wait_for_selector(".toast-message")
    # toast_message = page.query_selector(".toast-message").text_content()
    # print(f"Toast message: {toast_message}")
    signup_page.expect_email_exists_error()

def test_10_signup_public_domain_warning(page: Page):
    """Test signup with public domain email warning."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    signup_page.fill_email("50st3of@hotmail.com")
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_public_domain_warning()

def test_11_signup_password_strength_warning(page: Page):
    """Test signup with weak password warning."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    email6 = random_email.generate_email()
    signup_page.fill_email(email6)
    signup_page.fill_password("weakpassword")
    signup_page.fill_confirm_password("weakpassword")
    signup_page.click_sign_up_button()
    signup_page.expect_password_strength_warning()

def test_12_signup_success_message(page: Page):
    """Test successful signup message."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    email7 = random_email.generate_email()
    signup_page.fill_email(email7)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_signup_success_message()

def test_13_signup_full_name_min_limit(page: Page):
    """Test full name minimum character limit."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("Jo")
    email8 = random_email.generate_email()
    signup_page.fill_email(email8)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_full_name_min_limit()

def test_14_signup_full_name_max_limit(page: Page):
    """Test full name maximum character limit."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("A" * 81)  # Assuming max limit is 80 characters
    email9 = random_email.generate_email()
    signup_page.fill_email(email9)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_full_name_max_limit()

def test_15_signup_full_name_special_characters(page: Page):
    """full name can contain special characters."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John@Doe")
    email10 = random_email.generate_email()
    signup_page.fill_email(email10)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_signup_success_message()
    # signup_page.expect_full_name_contains_special_characters()

def test_16_signup_full_name_only_contains_numbers(page: Page):
    """full name can only contain numbers."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("123")
    email11 = random_email.generate_email()  # Generate a new random email for this test
    signup_page.fill_email(email11)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_signup_success_message()
    # signup_page.expect_full_name_contains_numbers()

def test_17_signup_full_name_contains_special_characters(page: Page):
    """full name can not start or end with special characters."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name(" John Doe")

    email12 = random_email.generate_email()
    signup_page.fill_email(email12)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_full_name_contains_special_characters()
    signup_page.fill_full_name("John Doe ")
    signup_page.click_sign_up_button()
    signup_page.expect_full_name_contains_special_characters()

def test_18_signup_full_name_label_visibility(page: Page):
    """Test visibility of full name label."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.expect_full_name_label()

def test_19_signup_email_label_visibility(page: Page):
    """Test visibility of email label."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.expect_email_label()

def test_20_signup_password_label_visibility(page: Page):
    """Test visibility of password label."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.expect_password_label()

def test_21_signup_confirm_password_label_visibility(page: Page):
    """Test visibility of confirm password label."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.expect_confirm_password_label()

def test_22_signup_show_hide_password_button(page: Page):
    """Test show/hide password functionality."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")

    signup_page.fill_email(email_address)
    signup_page.fill_password("Kabir123#")
    expect(signup_page.locators.show_password_button).to_be_visible()
    signup_page.locators.show_password_button.click()
    expect(signup_page.locators.hide_password_button).to_be_visible()
    signup_page.locators.hide_password_button.click()
    expect(signup_page.locators.show_password_button).to_be_visible()

def test_23_signup_by_clicking_sign_up_text(page: Page):
    """Test visibility of 'By clicking Agree & Join or' text."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.expect_by_clicking_sign_up_button()

def test_24_signup_policy_link_visibility(page: Page):
    """Test visibility of Privacy Policy link."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.expect_policy_link()

def test_25_signup_user_agreement_link_visibility(page: Page):
    """Test visibility of User Agreement link."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.expect_user_agreement_link()

def test_26_signup_email_verification_page_visibility(page: Page):
    """Test visibility of email verification page."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    email13 = random_email.generate_email()
    signup_page.fill_email(email13)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_email_verification_page()

def test_27_signup_verification_page_heading_visibility(page: Page):
    """Test visibility of OTP verification page heading."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    email14 = random_email.generate_email()
    signup_page.fill_email(email14)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_verification_page_heading()

def test_28_signup_mailbox_image_visibility(page: Page):
    """Test visibility of mailbox image on verification page."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    email15 = random_email.generate_email()
    signup_page.fill_email(email15)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_mail_image_visible()

def test_29_signup_verification_instructions_visibility(page: Page):
    """Test visibility of verification instructions on verification page."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    email16 = random_email.generate_email()
    signup_page.fill_email(email16)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_verification_instructions()

def test_30_signup_otp_input_box_visibility(page: Page):
    """Test visibility of OTP input box on verification page."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    email17 = random_email.generate_email()
    signup_page.fill_email(email17)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_otp_input_box()

def test_31_signup_input_box_title_visibility(page: Page):
    """Test visibility of input box title on verification page."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    email18 = random_email.generate_email()
    signup_page.fill_email(email18)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_input_box_title()

def test_32_signup_verify_button_visibility(page: Page):
    """Test visibility of verify button on verification page."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    email19 = random_email.generate_email()
    signup_page.fill_email(email19)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()  # Wait for the OTP input box to appear
    signup_page.expect_verify_button()

def test_33_signup_resend_otp_button_visibility(page: Page):
    """Test visibility of resend OTP button on verification page."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    email20 = random_email.generate_email()
    signup_page.fill_email(email20)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    time.sleep(60)  # Wait for the OTP input box to appear
    signup_page.expect_resend_otp_button()

def test_34_signup_resend_otp_countdown_visibility(page: Page):
    """Test visibility of resend OTP countdown on verification page."""
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    signup_page.fill_full_name("John Doe")
    email21 = random_email.generate_email()
    signup_page.fill_email(email21)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_resend_otp_countdown()
