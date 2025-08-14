from playwright.sync_api import Page, expect
import re
from locators.loc_reset_pass import ResetPasswordLocators
from utils.enhanced_assertions import enhanced_assert_visible, enhanced_assert_not_visible
import utils.reset_pass_helper as reset_pass_helper

class ResetPasswordPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = ResetPasswordLocators(page)

    def navigate_to_landing_page(self, url: str):
        self.page.goto(url)

    def navigate_to_reset_password(self, url: str):
        self.page.goto(url)

    def expect_forgot_password_link_visibility(self):
        reset_pass_helper.assert_go_to_forgot_password_link(self.page)

    def click_forgot_password_link(self):
        self.locators.go_to_forgot_password_link.click()

    def click_forgot_password_heading(self):
        self.locators.forgot_password_heading.click()

    def click_get_started_button(self):
        self.locators.get_started_button.click()

    def click_on_email_input_box(self):
        self.locators.email_input_box.click()

    def enter_email(self, email: str):
        self.locators.email_input_box.fill(email)

    def click_next(self):
        self.locators.next_button.click()

    def expect_next_button_disabled(self):
        assert self.locators.next_button.is_disabled(), "Next button should be disabled"

    def click_back_button(self):
        self.locators.back_button.click()

    def verify_reset_password_heading(self):
        reset_pass_helper.assert_reset_password_heading(self.page)

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
        reset_pass_helper.assert_error_reset_pass_attempt_limit(self.page)

    def expect_invalid_email_error(self):
        reset_pass_helper.assert_error_invalid_email(self.page)
    
    def expect_email_required_error(self):
        reset_pass_helper.assert_error_email_required(self.page)
    
    def expect_public_domain_email_error(self):
        reset_pass_helper.assert_error_public_domain_email(self.page)
    
    def expect_unregistered_email_error(self):
        reset_pass_helper.assert_error_unregistered_email(self.page)

    def expect_nonverified_email_error(self):
        reset_pass_helper.assert_error_nonverified_email(self.page)

    def expect_invalid_otp_error(self):
        reset_pass_helper.assert_error_invalid_otp(self.page)
    
    def expect_otp_input_limit_error(self):
        reset_pass_helper.assert_error_otp_input_limit(self.page)
    
    def expect_otp_required_error(self):
        reset_pass_helper.assert_error_otp_required(self.page)
    
    def expect_otp_accept_numbers_only_error(self):
        reset_pass_helper.assert_error_otp_accept_numbers_only(self.page)
    
    def expect_new_password_required_error(self):
        reset_pass_helper.assert_error_new_password_required(self.page)
    
    def expect_password_complexity_error(self):
        reset_pass_helper.assert_error_password_complexity(self.page)
    
    def expect_confirm_password_required_error(self):
        reset_pass_helper.assert_error_confirm_password_required(self.page)
    
    def expect_password_mismatch_error(self):
        reset_pass_helper.assert_error_password_mismatch(self.page)
    
    def expect_otp_sent_toast(self):
        reset_pass_helper.assert_toast_email_with_otp_sent(self.page)
    
    def expect_otp_resent_toast(self):
        reset_pass_helper.assert_toast_otp_resent(self.page)

    def expect_password_reset_success_toast(self):
        enhanced_assert_visible(self.page, self.locators.toast_password_reset_success, "Password reset success toast should be visible")

    def expect_otp_expired_toast(self):
        enhanced_assert_visible(self.page, self.locators.toast_otp_expired, "OTP expired toast should be visible")

    def expect_countdown_timer_visible(self):
        enhanced_assert_visible(self.page, self.locators.countdown_timer, "Countdown timer should be visible")
    
    def expect_back_button_visible(self):
        enhanced_assert_visible(self.page, self.locators.back_button, "Back button should be visible")

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
        enhanced_assert_visible(self.page, self.locators.forgot_password_heading, "Forgot password heading should be visible")

    def expect_email_input_visible(self):
        enhanced_assert_visible(self.page, self.locators.email_input_box, "Email input should be visible")

    def expect_next_button_visible(self):
        enhanced_assert_visible(self.page, self.locators.next_button, "Next button should be visible")

    def expect_otp_input_visible(self):
        enhanced_assert_visible(self.page, self.locators.otp_input, "OTP input should be visible")

    def expect_new_password_input_visible(self):
        enhanced_assert_visible(self.page, self.locators.new_password_input, "New password input should be visible")

    def expect_confirm_password_input_visible(self):
        enhanced_assert_visible(self.page, self.locators.confirm_password_input, "Confirm password input should be visible")

    def expect_set_password_button_visible(self):
        enhanced_assert_visible(self.page, self.locators.set_password_button, "Set password button should be visible")

    def expect_resend_otp_button_visible(self):
        enhanced_assert_visible(self.page, self.locators.resend_otp_button, "Resend OTP button should be visible")