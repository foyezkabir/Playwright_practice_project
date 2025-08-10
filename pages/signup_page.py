from playwright.sync_api import Page,expect
from locators.loc_signup import SignupLocators

class SignupPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = SignupLocators(page)

    def navigate_to_landing_page(self, url: str):
        self.page.goto(url)

    def click_get_started(self):
        self.locators.get_started_button.click()

    def click_sign_in_link(self):
        self.locators.sign_in_link.click()

    def fill_full_name(self, full_name: str):
        self.locators.full_name_input.fill(full_name)

    def fill_email(self, email: str):
        self.locators.email_input.fill(email)

    def fill_password(self, password: str):
        self.locators.password_input.fill(password)

    def fill_confirm_password(self, confirm_password: str):
        self.locators.confirm_password_input.fill(confirm_password)

    def click_sign_up_button(self):
        self.locators.sign_up_button.click()

    def expect_full_name_required_error(self):
        expect(self.locators.error_full_name_required).to_be_visible()

    def expect_email_required_error(self):
        expect(self.locators.error_email_required).to_be_visible()

    def expect_password_required_error(self):
        expect(self.locators.error_password_required).to_be_visible()

    def expect_confirm_password_required_error(self):
        expect(self.locators.error_confirm_password_required).to_be_visible()

    def expect_password_mismatch_error(self):
        expect(self.locators.error_password_mismatch).to_be_visible()

    def expect_invalid_email_error(self):
        expect(self.locators.error_invalid_email).to_be_visible()

    def expect_email_exists_error(self):
        expect(self.locators.error_email_exists).to_be_visible()

    def expect_public_domain_warning(self):
        expect(self.locators.public_domain_warning).to_be_visible()

    def expect_password_strength_warning(self):
        expect(self.locators.password_strength_warning).to_be_visible()

    def expect_signup_success_message(self):
        expect(self.locators.signup_success_message).to_be_visible()

    def expect_full_name_min_limit(self):
        expect(self.locators.full_name_min_limit).to_be_visible()

    def expect_full_name_max_limit(self):
        expect(self.locators.full_name_max_limit).to_be_visible()

    def expect_full_name_contains_special_characters(self):
        expect(self.locators.full_name_contains_special_characters).to_be_visible()

    def expect_full_name_contains_numbers(self):
        expect(self.locators.full_name_contains_numbers).to_be_visible()

    def expect_full_name_label(self):
        expect(self.locators.full_name_label).to_be_visible()

    def expect_email_label(self):
        expect(self.locators.email_label).to_be_visible()

    def expect_password_label(self):
        expect(self.locators.password_label).to_be_visible()

    def expect_confirm_password_label(self):
        expect(self.locators.confirm_password_label).to_be_visible()

    def expect_show_password_button(self):
        expect(self.locators.show_password_button).to_be_visible()

    def expect_hide_password_button(self):
        expect(self.locators.hide_password_button).to_be_visible()

    def expect_signup_page_heading(self):
        expect(self.locators.Signup_page_Heading).to_be_visible()

    def expect_by_clicking_sign_up_button(self):
        expect(self.locators.By_clicking_sign_up_button).to_be_visible()

    def click_policy_link(self):
        self.locators.Policy_link.click()

    def expect_policy_link(self):
        expect(self.locators.Policy_link).to_be_visible()

    def click_user_agreement_link(self):
        self.locators.User_Agreement_link.click()

    def expect_user_agreement_link(self):
        expect(self.locators.User_Agreement_link).to_be_visible()

    def expect_email_verification_page(self):
        expect(self.locators.email_verification_page).to_be_visible()

    def expect_verification_page_heading(self):
        expect(self.locators.Verification_page_Heading).to_be_visible()

    def expect_otp_input_box(self):
        expect(self.locators.otp_input_box).to_be_visible()

    def expect_input_box_title(self):
        expect(self.locators.input_box_title).to_be_visible()

    def expect_verify_button(self):
        expect(self.locators.verify_button).to_be_visible()

    def expect_resend_otp_button(self):
        expect(self.locators.resend_otp_button).to_be_visible()

    def expect_resend_otp_countdown(self):
        expect(self.locators.resend_otp_countdown).to_be_visible()

    def expect_verification_success_message(self):
        expect(self.locators.verification_success_message).to_be_visible()

    def expect_verification_error_message(self):
        expect(self.locators.verification_error_message).to_be_visible()

    def expect_back_button(self):
        expect(self.locators.back_button).to_be_visible()

    def click_back_button(self):
        self.locators.back_button.click()

    def expect_resend_otp_success_message(self):
        expect(self.locators.resend_otp_success_message).to_be_visible()

    def click_resend_otp_button(self):
        self.locators.resend_otp_button.click() 

    def click_verify_email_button(self, otp: str):
        self.locators.otp_input_box.fill(otp)
        self.locators.verify_button.click()

    def expect_mail_image_visible(self):
        expect(self.locators.mailbox_image).to_be_visible()

    def expect_verification_instructions(self):
        expect(self.locators.verification_instructions).to_be_visible()

    def expect_back_to_sign_in_page(self):
        expect(self.locators.back_to_sign_in_page).to_be_visible()
