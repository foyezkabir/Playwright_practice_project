from os import name
import re
from unicodedata import normalize
from playwright.sync_api import Page, expect
from locators.loc_login import LoginLocators

class SignupLocators:
    def __init__(self, page: Page):
        self.page = page

        # Locators for the signup page
        self.get_started_button = page.get_by_role("button", name="Get Started")
        self.sign_in_link = page.get_by_role("link", name="Sign Up")
        self.Signup_page_Heading = page.get_by_role("heading", name="Sign up")

        # Locators for the signup form fields and buttons
        self.full_name_input = page.get_by_role("textbox", name="Full Name")
        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_role("textbox", name="Password", exact=True)
        self.confirm_password_input = page.get_by_role("textbox", name="Confirm Password")
        self.sign_up_button = page.get_by_role("button", name="Sign Up")
        self.By_clicking_sign_up_button = page.get_by_text("By clicking Agree & Join or")
        self.Policy_link = page.get_by_role("link", name="Privacy Policy")
        self.User_Agreement_link = page.get_by_role("link", name="User Agreement")

        # Locators for validation messages
        self.error_full_name_required = page.get_by_text("Name is required")
        self.full_name_min_limit = page.get_by_text("Name must be at least 3 characters")
        self.full_name_max_limit = page.get_by_text("Name must not exceed 80 characters")
        self.full_name_contains_special_characters = page.get_by_text("Name must not start or end with special characters.")
        self.full_name_contains_numbers = page.get_by_text("Name not allow any number")
        self.error_email_required = page.get_by_text("Email is required")
        self.error_password_required = page.get_by_text("Password is required")
        self.error_confirm_password_required = page.get_by_text("Confirm Password is required")
        self.error_password_mismatch = page.get_by_text("Passwords do not match")
        self.error_invalid_email = page.get_by_text("Invalid email address")
        self.error_email_exists = page.get_by_text("This email is already registered. Please log in or reset your password.")
        self.public_domain_warning = page.get_by_text("Please use your official work email address. Public domains are not allowed.")
        self.password_strength_warning = page.get_by_text("Password must contain an uppercase, lowercase, number and special character")

        # Locators for success message
        self.signup_success_message = page.get_by_text("Registered successfully")

        # Locators for verifcation page
        self.email_verification_page = page.locator("div").filter(has_text="OTP VerificationWe just sent").nth(2)
        self.Verification_page_Heading = page.get_by_role("heading", name="OTP Verification")
        self.mailbox_image = page.get_by_role("img", name="Mail Inbox")
        self.verification_instructions = page.get_by_text("We just sent a verification")
        self.otp_input_box = page.locator(".flex.justify-center.gap-2")
        self.input_box_title = page.get_by_text("Enter the OTP below to verify")
        self.verify_button = page.get_by_role("button", name="Verify OTP")
        self.resend_otp_countdown = page.get_by_text("Resend OTP in")
        self.resend_otp_button = page.get_by_role("button", name="Resend OTP")
        self.verification_success_message = page.get_by_text("Email verified successfully")
        self.verification_error_message = page.get_by_text("Invalid code")
        self.back_button = page.locator('svg.heading-color')
        self.resend_otp_success_message = page.get_by_text("OTP resent successfully")
        self.back_to_sign_in_page = page.get_by_role("heading", name="Sign in")

        # Locators for additional elements
        self.full_name_label = page.get_by_text("Full Name", exact=True)
        self.email_label = page.get_by_text("Email", exact=True)
        self.password_label = page.get_by_text("Password", exact=True)
        self.confirm_password_label = page.get_by_text("Confirm Password", exact=True)
        self.show_password_button = page.get_by_text("Show")
        self.hide_password_button = page.get_by_text("Hide")
