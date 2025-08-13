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
        assert self.locators.error_full_name_required.is_visible(), "Full name required error should be visible"

    def expect_email_required_error(self):
        assert self.locators.error_email_required.is_visible(), "Email required error should be visible"

    def expect_password_required_error(self):
        assert self.locators.error_password_required.is_visible(), "Password required error should be visible"

    def expect_confirm_password_required_error(self):
        assert self.locators.error_confirm_password_required.is_visible(), "Confirm password required error should be visible"

    def expect_password_mismatch_error(self):
        assert self.locators.error_password_mismatch.is_visible(), "Password mismatch error should be visible"

    def expect_invalid_email_error(self):
        assert self.locators.error_invalid_email.is_visible(), "Invalid email error should be visible"

    def expect_email_exists_error(self):
        assert self.locators.error_email_exists.is_visible(), "Email exists error should be visible"

    def expect_public_domain_warning(self):
        assert self.locators.public_domain_warning.is_visible(), "Public domain warning should be visible"

    def expect_password_strength_warning(self):
        assert self.locators.password_strength_warning.is_visible(), "Password strength warning should be visible"

    def expect_signup_success_message(self):
        assert self.locators.signup_success_message.is_visible(), "Signup success message should be visible"

    def expect_full_name_min_limit(self):
        assert self.locators.full_name_min_limit.is_visible(), "Full name min limit message should be visible"

    def expect_full_name_max_limit(self):
        assert self.locators.full_name_max_limit.is_visible(), "Full name max limit message should be visible"

    def expect_full_name_contains_special_characters(self):
        assert self.locators.full_name_contains_special_characters.is_visible(), "Full name contains special characters message should be visible"

    def expect_full_name_contains_numbers(self):
        assert self.locators.full_name_contains_numbers.is_visible(), "Full name contains numbers message should be visible"

    def expect_full_name_label(self):
        assert self.locators.full_name_label.is_visible(), "Full name label should be visible"

    def expect_email_label(self):
        assert self.locators.email_label.is_visible(), "Email label should be visible"

    def expect_password_label(self):
        assert self.locators.password_label.is_visible(), "Password label should be visible"

    def expect_confirm_password_label(self):
        assert self.locators.confirm_password_label.is_visible(), "Confirm password label should be visible"

    def expect_show_password_button(self):
        assert self.locators.show_password_button.is_visible(), "Show password button should be visible"

    def expect_hide_password_button(self):
        assert self.locators.hide_password_button.is_visible(), "Hide password button should be visible"

    def expect_signup_page_heading(self):
        assert self.locators.Signup_page_Heading.is_visible(), "Signup page heading should be visible"

    def expect_by_clicking_sign_up_button(self):
        assert self.locators.By_clicking_sign_up_button.is_visible(), "By clicking sign up button text should be visible"

    def click_policy_link(self):
        self.locators.Policy_link.click()

    def expect_policy_link(self):
        assert self.locators.Policy_link.is_visible(), "Policy link should be visible"

    def click_user_agreement_link(self):
        self.locators.User_Agreement_link.click()

    def expect_user_agreement_link(self):
        assert self.locators.User_Agreement_link.is_visible(), "User agreement link should be visible"

    def expect_email_verification_page(self):
        assert self.locators.email_verification_page.is_visible(), "Email verification page should be visible"

    def expect_verification_page_heading(self):
        assert self.locators.Verification_page_Heading.is_visible(), "Verification page heading should be visible"

    def expect_otp_input_box(self):
        assert self.locators.otp_input_box.is_visible(), "OTP input box should be visible"

    def expect_input_box_title(self):
        assert self.locators.input_box_title.is_visible(), "Input box title should be visible"

    def expect_verify_button(self):
        assert self.locators.verify_button.is_visible(), "Verify button should be visible"

    def expect_resend_otp_button(self):
        assert self.locators.resend_otp_button.is_visible(), "Resend OTP button should be visible"

    def expect_resend_otp_countdown(self):
        assert self.locators.resend_otp_countdown.is_visible(), "Resend OTP countdown should be visible"

    def expect_verification_success_message(self):
        assert self.locators.verification_success_message.is_visible(), "Verification success message should be visible"

    def expect_verification_error_message(self):
        assert self.locators.verification_error_message.is_visible(), "Verification error message should be visible"

    def expect_back_button(self):
        assert self.locators.back_button.is_visible(), "Back button should be visible"

    def click_back_button(self):
        self.locators.back_button.click()

    def expect_resend_otp_success_message(self):
        assert self.locators.resend_otp_success_message.is_visible(), "Resend OTP success message should be visible"

    def click_resend_otp_button(self):
        self.locators.resend_otp_button.click() 

    def click_verify_email_button(self, otp: str):
        self.locators.otp_input_box.fill(otp)
        self.locators.verify_button.click()

    def expect_mail_image_visible(self):
        assert self.locators.mailbox_image.is_visible(), "Mail image should be visible"

    def expect_verification_instructions(self):
        assert self.locators.verification_instructions.is_visible(), "Verification instructions should be visible"

    def expect_back_to_sign_in_page(self):
        assert self.locators.back_to_sign_in_page.is_visible(), "Back to sign in page should be visible"
