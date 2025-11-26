import re
from playwright.sync_api import Page

class EmailVerifyLocators:
    
    def __init__(self, page: Page):
        self.page = page
        
        # Page elements
        self.verification_page_heading = page.get_by_role("heading", name="OTP Verification")
        self.mailbox_image = page.get_by_role("img", name="Mail Inbox")
        self.verification_instructions = page.get_by_text("We just sent a verification")
        self.input_box_title = page.get_by_text("Enter the OTP below to verify")
        
        # OTP input container and fields
        self.otp_input_container = page.locator(".flex.justify-center.gap-2")
        
        # Multiple OTP input selectors for different implementations
        self.otp_spinbuttons = page.locator('spinbutton')
        self.otp_digit_inputs = page.locator('input[maxlength="1"]')
        self.otp_number_inputs = page.locator('input[type="number"]')
        
        # Action buttons
        self.verify_button = page.get_by_role("button", name="Verify OTP")
        self.resend_otp_button = page.get_by_role("button", name="Resend OTP")
        self.back_button = page.get_by_role("button").filter(has_text=re.compile(r"^$"))
        
        # Status and feedback messages
        self.resend_otp_countdown = page.get_by_text("Resend OTP in")
        self.verification_success_message = page.get_by_text("OTP verified successfully")
        self.verification_error_message = page.get_by_text("Invalid verification code provided, please try again.")
        self.resend_otp_success_message = page.get_by_text("OTP resent successfully")
        
        # Navigation elements
        self.sign_in_heading = page.get_by_role("heading", name="Sign in")
        
        # Email display (shows which email verification was sent to)
        self.email_display = page.locator("[data-testid='verification-email']")
        
    def get_otp_input_fields(self):

        if self.otp_spinbuttons.count() >= 6:
            return self.otp_spinbuttons
        elif self.otp_digit_inputs.count() >= 6:
            return self.otp_digit_inputs
        elif self.otp_number_inputs.count() >= 6:
            return self.otp_number_inputs
        else:
            return None