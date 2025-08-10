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
        expect(self.locators.verification_required_for_login).to_be_visible()

    def expect_system_shows_email_verification_page(self):
        expect(self.locators.system_shows_verification_page).to_be_visible()

    def expect_verification_page_heading(self):
        expect(self.locators.verification_page_heading).to_be_visible()

    def expect_mailbox_image(self):
        expect(self.locators.mailbox_image).to_be_visible()

    def expect_verification_instructions(self):
        expect(self.locators.verification_instructions).to_be_visible()

    def expect_otp_input_box(self):
        expect(self.locators.otp_input_box).to_be_visible()
    
    def expect_input_box_title(self):
        expect(self.locators.input_box_title).to_be_visible()

    def expect_resend_otp_countdown(self):
        expect(self.locators.resend_otp_countdown).to_be_visible()

    def expect_verify_button(self):
        expect(self.locators.verify_button).to_be_visible()

    def expect_resend_otp_button(self):
        expect(self.locators.resend_otp_button).to_be_visible()

    def click_resend_otp(self):
        self.locators.resend_otp_button.click()

    def expect_resend_otp_success_message(self):
        expect(self.locators.resend_otp_success_message).to_be_visible()

    def expect_email_required_error(self):
        expect(self.locators.error_email_required).to_be_visible()

    def expect_password_required_error(self):
        expect(self.locators.error_password_required).to_be_visible()

    def expect_public_domain_warning(self):
        expect(self.locators.public_domain_warning).to_be_visible()

    def expect_invalid_email_error(self):
        expect(self.locators.error_invalid_email).to_be_visible()

    def expect_invalid_credentials_error(self):
        expect(self.locators.error_invalid_credentials).to_be_visible()

    def expect_show_password_button(self):
        expect(self.locators.show_password_button).to_be_visible()

    def expect_hide_password_button(self):
        expect(self.locators.hide_password_button).to_be_visible()

    def expect_forgot_password_link(self):
        expect(self.locators.forgot_password_link).to_be_visible()

    def expect_sign_in_heading(self):
        expect(self.locators.sign_in_heading).to_be_visible()

    def expect_black_pigeon_link(self):
        expect(self.locators.black_pigeon_link).to_be_visible()

    def expect_sign_in_button_visible(self):
        expect(self.locators.sign_in_button_visible).to_be_visible()

    def expect_email_label(self):
        expect(self.locators.email_label).to_be_visible()

    def expect_password_label(self):
        expect(self.locators.password_label).to_be_visible()

    def expect_unregistered_email_error(self):
        expect(self.locators.unregistered_email_error).to_be_visible()

    def expect_dont_have_account_text(self):
        expect(self.locators.dont_have_account_text).to_be_visible()

    def expect_nonverified_email_error(self):
        expect(self.locators.nonverified_email_error).to_be_visible()