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
        expect(self.locators.go_to_forgot_password_link).to_be_visible()

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
        expect(self.locators.reset_password_heading).to_be_visible()

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
        expect(self.locators.error_reset_pass_attempt_limit).to_be_visible()

    def expect_invalid_email_error(self):
        expect(self.locators.error_invalid_email).to_be_visible()
    
    def expect_email_required_error(self):
        expect(self.locators.error_email_required).to_be_visible()
    
    def expect_public_domain_email_error(self):
        expect(self.locators.error_public_domain_email).to_be_visible()
    
    def expect_unregistered_email_error(self):
        expect(self.locators.error_unregistered_email).to_be_visible()

    def expect_nonverified_email_error(self):
        expect(self.locators.error_nonverified_email).to_be_visible()

    def expect_invalid_otp_error(self):
        expect(self.locators.error_invalid_otp).to_be_visible()
    
    def expect_otp_input_limit_error(self):
        expect(self.locators.error_otp_input_limit).to_be_visible()
    
    def expect_otp_required_error(self):
        expect(self.locators.error_otp_required).to_be_visible()
    
    def expect_otp_accept_numbers_only_error(self):
        expect(self.locators.error_otp_accept_numbers_only).to_be_visible()
    
    def expect_new_password_required_error(self):
        expect(self.locators.error_new_password_required).to_be_visible()
    
    def expect_password_complexity_error(self):
        expect(self.locators.error_password_complexity).to_be_visible()
    
    def expect_confirm_password_required_error(self):
        expect(self.locators.error_confirm_password_required).to_be_visible()
    
    def expect_password_mismatch_error(self):
        expect(self.locators.error_password_mismatch).to_be_visible()
    
    def expect_otp_sent_toast(self):
        expect(self.locators.toast_email_with_otp_sent).to_be_visible()
    
    def expect_otp_resent_toast(self):
        expect(self.locators.toast_otp_resent).to_be_visible()

    def expect_password_reset_success_toast(self):
        expect(self.locators.toast_password_reset_success).to_be_visible()

    def expect_otp_expired_toast(self):
        expect(self.locators.toast_otp_expired).to_be_visible()

    def expect_countdown_timer_visible(self):
        expect(self.locators.countdown_timer).to_be_visible()
    
    def expect_back_button_visible(self):
        expect(self.locators.back_button).to_be_visible()

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
        expect(self.locators.forgot_password_heading).to_be_visible()

    def expect_email_input_visible(self):
        expect(self.locators.email_input_box).to_be_visible()

    def expect_next_button_visible(self):
        expect(self.locators.next_button).to_be_visible()

    def expect_otp_input_visible(self):
        expect(self.locators.otp_input).to_be_visible()

    def expect_new_password_input_visible(self):
        expect(self.locators.new_password_input).to_be_visible()

    def expect_confirm_password_input_visible(self):
        expect(self.locators.confirm_password_input).to_be_visible()

    def expect_set_password_button_visible(self):
        expect(self.locators.set_password_button).to_be_visible()

    def expect_resend_otp_button_visible(self):
        expect(self.locators.resend_otp_button).to_be_visible()