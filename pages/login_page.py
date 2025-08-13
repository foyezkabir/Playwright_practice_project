from playwright.sync_api import Page, expect
from locators.loc_login import LoginLocators

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
        assert self.locators.verification_required_for_login.is_visible(), "Verification required for login should be visible"

    def expect_system_shows_email_verification_page(self):
        assert self.locators.system_shows_verification_page.is_visible(), "System shows verification page should be visible"

    def expect_verification_page_heading(self):
        assert self.locators.verification_page_heading.is_visible(), "Verification page heading should be visible"

    def expect_mailbox_image(self):
        assert self.locators.mailbox_image.is_visible(), "Mailbox image should be visible"

    def expect_verification_instructions(self):
        assert self.locators.verification_instructions.is_visible(), "Verification instructions should be visible"

    def expect_otp_input_box(self):
        assert self.locators.otp_input_box.is_visible(), "OTP input box should be visible"
    
    def expect_input_box_title(self):
        assert self.locators.input_box_title.is_visible(), "Input box title should be visible"

    def expect_resend_otp_countdown(self):
        assert self.locators.resend_otp_countdown.is_visible(), "Resend OTP countdown should be visible"

    def expect_verify_button(self):
        assert self.locators.verify_button.is_visible(), "Verify button should be visible"

    def expect_resend_otp_button(self):
        assert self.locators.resend_otp_button.is_visible(), "Resend OTP button should be visible"

    def click_resend_otp(self):
        self.locators.resend_otp_button.click()

    def expect_resend_otp_success_message(self):
        assert self.locators.resend_otp_success_message.is_visible(), "Resend OTP success message should be visible"

    def expect_email_required_error(self):
        assert self.locators.error_email_required.is_visible(), "Email required error should be visible"

    def expect_password_required_error(self):
        assert self.locators.error_password_required.is_visible(), "Password required error should be visible"

    def expect_public_domain_warning(self):
        assert self.locators.public_domain_warning.is_visible(), "Public domain warning should be visible"

    def expect_invalid_email_error(self):
        assert self.locators.error_invalid_email.is_visible(), "Invalid email error should be visible"

    def expect_invalid_credentials_error(self):
        assert self.locators.error_invalid_credentials.is_visible(), "Invalid credentials error should be visible"

    def expect_show_password_button(self):
        assert self.locators.show_password_button.is_visible(), "Show password button should be visible"

    def expect_hide_password_button(self):
        assert self.locators.hide_password_button.is_visible(), "Hide password button should be visible"

    def expect_forgot_password_link(self):
        assert self.locators.forgot_password_link.is_visible(), "Forgot password link should be visible"

    def expect_sign_in_heading(self):
        assert self.locators.sign_in_heading.is_visible(), "Sign in heading should be visible"

    def expect_black_pigeon_link(self):
        assert self.locators.black_pigeon_link.is_visible(), "Black pigeon link should be visible"

    def expect_sign_in_button_visible(self):
        assert self.locators.sign_in_button_visible.is_visible(), "Sign in button should be visible"

    def expect_email_label(self):
        assert self.locators.email_label.is_visible(), "Email label should be visible"

    def expect_password_label(self):
        assert self.locators.password_label.is_visible(), "Password label should be visible"

    def expect_unregistered_email_error(self):
        assert self.locators.unregistered_email_error.is_visible(), "Unregistered email error should be visible"

    def expect_dont_have_account_text(self):
        assert self.locators.dont_have_account_text.is_visible(), "Don't have account text should be visible"

    def expect_nonverified_email_error(self):
        assert self.locators.nonverified_email_error.is_visible(), "Non-verified email error should be visible"