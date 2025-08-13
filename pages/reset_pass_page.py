from playwright.sync_api import Page, expect
import re
from locators.loc_reset_pass import ResetPasswordLocators

class ResetPasswordPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = ResetPasswordLocators(page)

    def navigate_to_landing_page(self, url: str):
        self.page.goto(url)

    def navigate_to_reset_password(self, url: str):
        self.page.goto(url)

    def expect_forgot_password_link_visibility(self):
        assert self.locators.go_to_forgot_password_link.is_visible(), "Forgot password link should be visible"

    def click_forgot_password_link(self):
        self.locators.go_to_forgot_password_link.click()

    def click_get_started_button(self):
        self.locators.get_started_button.click()

    def enter_email(self, email: str):
        self.locators.email_input_box.fill(email)

    def click_next(self):
        self.locators.next_button.click()

    def click_back_button(self):
        self.locators.back_button.click()

    def verify_reset_password_heading(self):
        assert self.locators.reset_password_heading.is_visible(), "Reset password heading should be visible"

    def enter_otp(self, otp: str):
        self.locators.otp_input.fill(otp)

    def enter_new_password(self, password: str):
        self.locators.new_password_input.fill(password)

    def enter_confirm_password(self, password: str):
        self.locators.confirm_password_input.fill(password)

    def click_set_password(self):
        self.locators.set_password_button.click()

    def click_resend_otp(self):
        self.locators.resend_otp_button.click()

    def click_back_final_page(self):
        self.locators.back_button.click()

    def expect_attempt_limit_error(self):
        assert self.locators.error_reset_pass_attempt_limit.is_visible(), "Attempt limit error should be visible"

    def expect_invalid_email_error(self):
        assert self.locators.error_invalid_email.is_visible(), "Invalid email error should be visible"
    
    def expect_email_required_error(self):
        assert self.locators.error_email_required.is_visible(), "Email required error should be visible"
    
    def expect_public_domain_email_error(self):
        assert self.locators.error_public_domain_email.is_visible(), "Public domain email error should be visible"
    
    def expect_unregistered_email_error(self):
        assert self.locators.error_unregistered_email.is_visible(), "Unregistered email error should be visible"

    def expect_nonverified_email_error(self):
        assert self.locators.error_nonverified_email.is_visible(), "Non-verified email error should be visible"

    def expect_invalid_otp_error(self):
        assert self.locators.error_invalid_otp.is_visible(), "Invalid OTP error should be visible"
    
    def expect_otp_input_limit_error(self):
        assert self.locators.error_otp_input_limit.is_visible(), "OTP input limit error should be visible"
    
    def expect_otp_required_error(self):
        assert self.locators.error_otp_required.is_visible(), "OTP required error should be visible"
    
    def expect_otp_accept_numbers_only_error(self):
        assert self.locators.error_otp_accept_numbers_only.is_visible(), "OTP accept numbers only error should be visible"
    
    def expect_new_password_required_error(self):
        assert self.locators.error_new_password_required.is_visible(), "New password required error should be visible"
    
    def expect_password_complexity_error(self):
        assert self.locators.error_password_complexity.is_visible(), "Password complexity error should be visible"
    
    def expect_confirm_password_required_error(self):
        assert self.locators.error_confirm_password_required.is_visible(), "Confirm password required error should be visible"
    
    def expect_password_mismatch_error(self):
        assert self.locators.error_password_mismatch.is_visible(), "Password mismatch error should be visible"
    
    def expect_otp_sent_toast(self):
        assert self.locators.toast_email_with_otp_sent.is_visible(), "OTP sent toast should be visible"
    
    def expect_otp_resent_toast(self):
        assert self.locators.toast_otp_resent.is_visible(), "OTP resent toast should be visible"

    def expect_password_reset_success_toast(self):
        assert self.locators.toast_password_reset_success.is_visible(), "Password reset success toast should be visible"

    def expect_otp_expired_toast(self):
        assert self.locators.toast_otp_expired.is_visible(), "OTP expired toast should be visible"

    def expect_countdown_timer_visible(self):
        assert self.locators.countdown_timer.is_visible(), "Countdown timer should be visible"
    
    def expect_back_button_visible(self):
        assert self.locators.back_button.is_visible(), "Back button should be visible"

    def show_new_password(self):
        self.locators.show_new_password_button.click()

    def hide_new_password(self):
        self.locators.hide_new_password_button.click()

    def show_confirm_password(self):
        self.locators.show_confirm_password_button.click()

    def hide_confirm_password(self):
        self.locators.hide_confirm_password_button.click()

    def get_resend_otp_countdown_text(self):
        return self.locators.resend_otp_countdown.text_content()
    
    def get_otp_label(self):
        return self.locators.otp_label.text_content()
    
    def get_new_password_label(self):
        return self.locators.new_password_label.text_content()
    
    def get_confirm_password_label(self):
        return self.locators.confirm_password_label.text_content()
    
    def get_instruction_text(self):
        return self.locators.instruction_text.text_content()

    def expect_forgot_password_heading_visible(self):
        assert self.locators.forgot_password_heading.is_visible(), "Forgot password heading should be visible"

    def expect_email_input_visible(self):
        assert self.locators.email_input_box.is_visible(), "Email input should be visible"

    def expect_next_button_visible(self):
        assert self.locators.next_button.is_visible(), "Next button should be visible"

    def expect_otp_input_visible(self):
        assert self.locators.otp_input.is_visible(), "OTP input should be visible"

    def expect_new_password_input_visible(self):
        assert self.locators.new_password_input.is_visible(), "New password input should be visible"

    def expect_confirm_password_input_visible(self):
        assert self.locators.confirm_password_input.is_visible(), "Confirm password input should be visible"

    def expect_set_password_button_visible(self):
        assert self.locators.set_password_button.is_visible(), "Set password button should be visible"

    def expect_resend_otp_button_visible(self):
        assert self.locators.resend_otp_button.is_visible(), "Resend OTP button should be visible"