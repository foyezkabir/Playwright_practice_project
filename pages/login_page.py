from playwright.sync_api import Page, expect
from locators.loc_login import LoginLocators
from utils.enhanced_assertions import enhanced_assert_visible, enhanced_assert_not_visible
import utils.login_helper as login_helper

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = LoginLocators(page)

    def navigate_to_landing_page(self, url: str):
        self.page.goto(url)

    def click_get_started(self):
        self.locators.get_started_button.click()

    def fill_email(self, email: str):
        self.locators.email_input.fill(email)

    def fill_password(self, password: str):
        self.locators.password_input.fill(password)

    def click_sign_in(self):
        self.locators.sign_in_button.click()

    def expect_verification_required_for_login(self):
        enhanced_assert_visible(self.page, self.locators.verification_required_for_login, "Verification required for login should be visible")

    def expect_system_shows_email_verification_page(self):
        enhanced_assert_visible(self.page, self.locators.system_shows_verification_page,"System shows verification page should be visible")

    def expect_verification_page_heading(self):
        enhanced_assert_visible(self.page, self.locators.verification_page_heading, "Verification page heading should be visible")

    def expect_mailbox_image(self):
        enhanced_assert_visible(self.page, self.locators.mailbox_image, "Mailbox image should be visible")

    def expect_verification_instructions(self):
        enhanced_assert_visible(self.page, self.locators.verification_instructions, "Verification instructions should be visible")

    def expect_otp_input_box(self):
        enhanced_assert_visible(self.page, self.locators.otp_input_box, "OTP input box should be visible")
    
    def expect_input_box_title(self):
        enhanced_assert_visible(self.page, self.locators.input_box_title, "Input box title should be visible")

    def expect_resend_otp_countdown(self):
        enhanced_assert_visible(self.page, self.locators.resend_otp_countdown, "Resend OTP countdown should be visible")

    def expect_verify_button(self):
        enhanced_assert_visible(self.page, self.locators.verify_button, "Verify button should be visible")

    def expect_resend_otp_button(self):
        enhanced_assert_visible(self.page, self.locators.resend_otp_button, "Resend OTP button should be visible")

    def click_resend_otp(self):
        self.locators.resend_otp_button.click()

    def expect_resend_otp_success_message(self):
        login_helper.assert_resend_otp_success_message(self.page, self.locators.resend_otp_success_message, "Resend OTP success message should be visible")

    def expect_email_required_error(self):
        login_helper.assert_email_required_error(self.page, self.locators.error_email_required, "Email required error should be visible")

    def expect_password_required_error(self):
        login_helper.assert_password_required_error(self.page, self.locators.error_password_required, "Password required error should be visible")

    def expect_public_domain_warning(self):
        login_helper.assert_public_domain_warning(self.page, self.locators.public_domain_warning, "Public domain warning should be visible")

    def expect_invalid_email_error(self):
        login_helper.assert_invalid_email_error(self.page, self.locators.error_invalid_email, "Invalid email error should be visible")

    def expect_invalid_credentials_error(self):
        login_helper.assert_invalid_credentials_error(self.page, self.locators.error_invalid_credentials, "Invalid credentials error should be visible")

    def expect_show_password_button(self):
        login_helper.assert_show_password_button(self.page, self.locators.show_password_button, "Show password button should be visible")

    def expect_hide_password_button(self):
        login_helper.assert_hide_password_button(self.page, self.locators.hide_password_button, "Hide password button should be visible")

    def expect_forgot_password_link(self):
        login_helper.assert_forgot_password_link(self.page, self.locators.forgot_password_link, "Forgot password link should be visible")

    def expect_sign_in_heading(self):
        login_helper.assert_sign_in_heading(self.page, self.locators.sign_in_heading, "Sign in heading should be visible")

    def expect_black_pigeon_link(self):
        login_helper.assert_black_pigeon_link(self.page, self.locators.black_pigeon_link, "Black pigeon link should be visible")

    def expect_sign_in_button_visible(self):
        login_helper.assert_sign_in_button_visible(self.page, self.locators.sign_in_button_visible, "Sign in button should be visible")

    def expect_email_label(self):
        login_helper.assert_email_label(self.page, self.locators.email_label, "Email label should be visible")

    def expect_password_label(self):
        login_helper.assert_password_label(self.page, self.locators.password_label, "Password label should be visible")

    def expect_unregistered_email_error(self):
        login_helper.assert_unregistered_email_error(self.page, self.locators.unregistered_email_error, "Unregistered email error should be visible")

    def expect_dont_have_account_text(self):
        login_helper.assert_dont_have_account_text(self.page, self.locators.dont_have_account_text, "Don't have account text should be visible")

    def expect_nonverified_email_error(self):
        login_helper.assert_nonverified_email_error(self.page, self.locators.nonverified_email_error, "Non-verified email error should be visible")