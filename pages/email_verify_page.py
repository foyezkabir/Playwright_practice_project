import time
import re
from typing import Optional
from playwright.sync_api import Page, expect
from mailosaur import MailosaurClient

from locators.loc_email_verify import EmailVerifyLocators

class EmailVerifyPage:
    
    def __init__(self, page: Page):
        self.page = page
        self.locators = EmailVerifyLocators(page)
    
    # Navigation and Page Verification
    def expect_verification_page_visible(self):
        assert self.locators.verification_page_heading.is_visible(), "Verification page heading should be visible"
    
    def expect_verification_instructions_visible(self):
        assert self.locators.verification_instructions.is_visible(), "Verification instructions should be visible"
    
    def expect_otp_input_container_visible(self):
        assert self.locators.otp_input_container.is_visible(), "OTP input container should be visible"
    
    def expect_verify_button_visible(self):
        assert self.locators.verify_button.is_visible(), "Verify button should be visible"
    
    def expect_resend_otp_button_visible(self):
        assert self.locators.resend_otp_button.is_visible(), "Resend OTP button should be visible"
    
    def expect_resend_countdown_visible(self):
        assert self.locators.resend_otp_countdown.is_visible(), "Resend countdown should be visible"
    
    # OTP Input Operations
    def enter_otp_code(self, otp_code: str):
        time.sleep(2)  # Wait for page to fully load
        
        # Method 1: Try spinbutton inputs
        try:
            self.page.wait_for_selector('spinbutton', timeout=5000)
            if self.locators.otp_spinbuttons.count() >= 6:
                for i, digit in enumerate(otp_code[:6]):
                    self.locators.otp_spinbuttons.nth(i).fill(digit)
                    time.sleep(0.2)
                return
        except Exception:
            pass
        
        # Method 2: Try digit input fields
        try:
            if self.locators.otp_digit_inputs.count() >= 6:
                for i, digit in enumerate(otp_code[:6]):
                    self.locators.otp_digit_inputs.nth(i).fill(digit)
                    time.sleep(0.2)
                return
        except Exception:
            pass
        
        # Method 3: Try number input fields
        try:
            if self.locators.otp_number_inputs.count() >= 6:
                for i, digit in enumerate(otp_code[:6]):
                    self.locators.otp_number_inputs.nth(i).fill(digit)
                    time.sleep(0.2)
                return
        except Exception:
            pass
    
    def clear_otp_fields_by_backspace(self):
        time.sleep(1)
        
        # Method 1: Try spinbutton inputs
        try:
            if self.locators.otp_spinbuttons.count() >= 6:
                # Click the 6th (last) box
                self.locators.otp_spinbuttons.nth(5).click()
                # Press backspace multiple times to clear all fields
                for i in range(6):
                    self.page.keyboard.press("Backspace")
                    time.sleep(0.05)
                return True
        except Exception:
            pass
        
        # Method 2: Try digit input fields
        try:
            if self.locators.otp_digit_inputs.count() >= 6:
                self.locators.otp_digit_inputs.nth(5).click()
                for i in range(6):
                    self.page.keyboard.press("Backspace")
                    time.sleep(0.05)
                return True
        except Exception:
            pass
        
        # Method 3: Try number input fields
        try:
            if self.locators.otp_number_inputs.count() >= 6:
                self.locators.otp_number_inputs.nth(5).click()
                for i in range(6):
                    self.page.keyboard.press("Backspace")
                    time.sleep(0.05)
                return True
        except Exception:
            pass
        
        return False

    # Button Actions
    def click_verify_button(self):
        """Click the verify OTP button"""
        self.locators.verify_button.click()
    
    def click_resend_otp_button(self):
        """Click the resend OTP button"""
        self.locators.resend_otp_button.click()
    
    # Verification and Validation
    def expect_verification_success(self):
        assert self.locators.verification_success_message.is_visible(), "Verification success message should be visible"
    
    def expect_verification_error(self):
        assert self.locators.verification_error_message.is_visible(), "Verification error message should be visible"
    
    def expect_resend_success(self):
        assert self.locators.resend_otp_success_message.is_visible(), "Resend OTP success message should be visible"
    
    def expect_sign_in_heading_visible(self):
        assert self.locators.sign_in_heading.is_visible(), "Sign in heading should be visible"
    
    def is_verify_button_enabled(self):
        return self.locators.verify_button.is_enabled()
    
    def wait_for_verify_button_enabled(self):
        assert self.locators.verify_button.is_enabled(timeout=2000), "Verify button should be enabled"

class EmailService:
    
    def __init__(self, api_key: str, server_id: str):
        self.api_key = api_key
        self.server_id = server_id
        self.client = MailosaurClient(api_key)
    
    def generate_random_email(self):
        import random
        import string
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test_{random_string}@{self.server_id}.mailosaur.net"
    
    def clear_inbox(self):
        try:
            self.client.messages.delete_all(self.server_id)
            return True
        except Exception as e:
            return False
    
    def extract_otp_from_content(self, email_content: str):
        patterns = [
            r'Your verification code is:\s*(\d{6})',  # Primary pattern
            r'verification code is:\s*(\d{6})',      # Fallback 1
            r'code is:\s*(\d{6})',                   # Fallback 2
            r'\b(\d{6})\b'                           # Any 6-digit number
        ]
        
        for pattern in patterns:
            match = re.search(pattern, email_content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def wait_for_verification_email(self, email_address: str, max_attempts: int = 20):
        for attempt in range(1, max_attempts + 1):
            time.sleep(3)
            
            try:
                messages = self.client.messages.list(self.server_id)
                
                for message in messages.items:
                    if (message.to and 
                        any(addr.email == email_address for addr in message.to)):
                        
                        # Get full email content
                        full_message = self.client.messages.get_by_id(message.id)
                        email_content = ""
                        if full_message.text and full_message.text.body:
                            email_content = full_message.text.body
                        
                        # Extract OTP
                        otp_code = self.extract_otp_from_content(email_content)
                        if otp_code:
                            return otp_code
                        
            except Exception as e:
                continue
        
        return None