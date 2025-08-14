from playwright.sync_api import Page,expect
from locators.loc_signup import SignupLocators
import utils.signup_helper as signup_helper

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
        signup_helper.assert_full_name_required_error(self.page, self.locators.error_full_name_required, "Full name required error should be visible")

    def expect_email_required_error(self):
        signup_helper.assert_email_required_error(self.page, self.locators.error_email_required, "Email required error should be visible")

    def expect_password_required_error(self):
        signup_helper.assert_password_required_error(self.page, self.locators.error_password_required, "Password required error should be visible")

    def expect_confirm_password_required_error(self):
        signup_helper.assert_confirm_password_required_error(self.page, self.locators.error_confirm_password_required, "Confirm password required error should be visible")

    def expect_password_mismatch_error(self):
        signup_helper.assert_password_mismatch_error(self.page, self.locators.error_password_mismatch, "Password mismatch error should be visible")

    def expect_invalid_email_error(self):
        signup_helper.assert_invalid_email_error(self.page, self.locators.error_invalid_email, "Invalid email error should be visible")

    def expect_email_exists_error(self):
        signup_helper.assert_email_exists_error(self.page, self.locators.error_email_exists, "Email exists error should be visible")

    def expect_public_domain_warning(self):
        signup_helper.assert_public_domain_warning(self.page, self.locators.public_domain_warning, "Public domain warning should be visible")

    def expect_password_strength_warning(self):
        signup_helper.assert_password_strength_warning(self.page, self.locators.password_strength_warning, "Password strength warning should be visible")

    def expect_signup_success_message(self):
        # Wait for the success message to appear with a reasonable timeout
        # Toast messages typically appear within 1-2 seconds after form submission
        try:
            self.locators.signup_success_message.wait_for(state="visible", timeout=5000)
            signup_helper.assert_signup_success_message(self.page, self.locators.signup_success_message, "Signup success message should be visible")
        except Exception as e:
            # If the success message doesn't appear, provide more context
            assert False, f"Signup success message 'Registered successfully' was not found within 5 seconds. Error: {str(e)}"

    def expect_full_name_min_limit(self):
        signup_helper.assert_full_name_min_limit(self.page, self.locators.full_name_min_limit, "Full name min limit message should be visible")

    def expect_full_name_max_limit(self):
        signup_helper.assert_full_name_max_limit(self.page, self.locators.full_name_max_limit, "Full name max limit message should be visible")

    def expect_full_name_contains_special_characters(self):
        signup_helper.assert_full_name_contains_special_characters(self.page, self.locators.full_name_contains_special_characters, "Full name contains special characters message should be visible")

    def expect_full_name_contains_numbers(self):
        signup_helper.assert_full_name_contains_numbers(self.page, self.locators.full_name_contains_numbers, "Full name contains numbers message should be visible")

    def expect_full_name_label(self):
        signup_helper.assert_full_name_label(self.page, self.locators.full_name_label, "Full name label should be visible")

    def expect_email_label(self):
        signup_helper.assert_email_label(self.page, self.locators.email_label, "Email label should be visible")

    def expect_password_label(self):
        signup_helper.assert_password_label(self.page, self.locators.password_label, "Password label should be visible")

    def expect_confirm_password_label(self):
        signup_helper.assert_confirm_password_label(self.page, self.locators.confirm_password_label, "Confirm password label should be visible")

    def expect_show_password_button(self):
        signup_helper.assert_show_password_button(self.page, self.locators.show_password_button, "Show password button should be visible")

    def expect_hide_password_button(self):
        signup_helper.assert_hide_password_button(self.page, self.locators.hide_password_button, "Hide password button should be visible")

    def expect_signup_page_heading(self):
        signup_helper.assert_signup_page_heading(self.page, self.locators.Signup_page_Heading, "Signup page heading should be visible")

    def expect_by_clicking_sign_up_button(self):
        signup_helper.assert_by_clicking_sign_up_button(self.page, self.locators.By_clicking_sign_up_button, "By clicking sign up button text should be visible")

    def click_policy_link(self):
        self.locators.Policy_link.click()

    def expect_policy_link(self):
        signup_helper.assert_policy_link(self.page, self.locators.Policy_link, "Policy link should be visible")

    def click_user_agreement_link(self):
        self.locators.User_Agreement_link.click()

    def expect_user_agreement_link(self):
        signup_helper.assert_user_agreement_link(self.page, self.locators.User_Agreement_link, "User agreement link should be visible")

    def expect_email_verification_page(self):
        signup_helper.assert_email_verification_page(self.page, self.locators.email_verification_page, "Email verification page should be visible")

    def expect_verification_page_heading(self):
        signup_helper.assert_verification_page_heading(self.page, self.locators.Verification_page_Heading, "Verification page heading should be visible")

    def expect_otp_input_box(self):
        signup_helper.assert_otp_input_box(self.page, self.locators.otp_input_box, "OTP input box should be visible")

    def expect_input_box_title(self):
        signup_helper.assert_input_box_title(self.page, self.locators.input_box_title, "Input box title should be visible")

    def expect_verify_button(self):
        signup_helper.assert_verify_button(self.page, self.locators.verify_button, "Verify button should be visible")

    def expect_resend_otp_button(self):
        signup_helper.assert_resend_otp_button(self.page, self.locators.resend_otp_button, "Resend OTP button should be visible")

    def expect_resend_otp_countdown(self):
        signup_helper.assert_resend_otp_countdown(self.page, self.locators.resend_otp_countdown, "Resend OTP countdown should be visible")

    def expect_verification_success_message(self):
        signup_helper.assert_verification_success_message(self.page, self.locators.verification_success_message, "Verification success message should be visible")

    def expect_verification_error_message(self):
        signup_helper.assert_verification_error_message(self.page, self.locators.verification_error_message, "Verification error message should be visible")

    def expect_back_button(self):
        signup_helper.assert_back_button(self.page, self.locators.back_button, "Back button should be visible")

    def click_back_button(self):
        self.locators.back_button.click()

    def expect_resend_otp_success_message(self):
        signup_helper.assert_resend_otp_success_message(self.page, self.locators.resend_otp_success_message, "Resend OTP success message should be visible")

    def click_resend_otp_button(self):
        self.locators.resend_otp_button.click() 

    def click_verify_email_button(self, otp: str):
        self.locators.otp_input_box.fill(otp)
        self.locators.verify_button.click()

    def expect_mail_image_visible(self):
        signup_helper.assert_mail_image_visible(self.page, self.locators.mailbox_image, "Mail image should be visible")

    def expect_verification_instructions(self):
        signup_helper.assert_verification_instructions(self.page, self.locators.verification_instructions, "Verification instructions should be visible")

    def expect_back_to_sign_in_page(self):
        signup_helper.assert_back_to_sign_in_page(self.page, self.locators.back_to_sign_in_page, "Back to sign in page should be visible")
