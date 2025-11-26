from playwright.sync_api import Page

class ResetPasswordLocators:
    def __init__(self, page: Page):
        self.page = page
        
        # Navigation elements
        self.get_started_button = page.get_by_role("button", name="Get Started")
        self.go_to_forgot_password_link = page.get_by_role("link", name="Forgot password?")
        self.back_button = page.get_by_role("link", name="Back")
        self.black_pigeon_link = page.get_by_role("link", name="Black Pigeon HR")
        
        # Forgot password page elements
        self.email_input_box = page.get_by_role("textbox", name="Email")
        self.next_button = page.get_by_role("button", name="Next")
        self.forgot_password_heading = page.get_by_role("heading", name="Forgot password")
        
        # Reset password page elements
        self.reset_password_heading = page.get_by_role("heading", name="Reset Password")
        self.otp_input = page.get_by_role("textbox", name="OTP")
        self.new_password_input = page.get_by_role("textbox", name="New Password")
        self.confirm_password_input = page.get_by_role("textbox", name="Confirm Password")
        self.set_password_button = page.get_by_role("button", name="Set new password")
        self.resend_otp_button = page.get_by_role("button", name="Resend OTP")
        
        # Labels
        self.otp_label = page.get_by_text("OTP", exact=True)
        self.new_password_label = page.get_by_text("New Password", exact=True)
        self.confirm_password_label = page.get_by_text("Confirm Password", exact=True)
        self.instruction_text = page.get_by_text("Please enter the OTP sent to your email and your new password.")
        
        # Show/Hide password buttons
        self.show_new_password_button = page.locator('#newPassword + .password-visiablity')
        self.hide_new_password_button = page.locator('#newPassword + .password-visiablity')
        self.show_confirm_password_button = page.locator('#confirmPassword + .password-visiablity')
        self.hide_confirm_password_button = page.locator('#confirmPassword + .password-visiablity')
        
        # Error messages - Forgot password page
        self.error_email_required = page.get_by_text("Email is required")
        self.error_invalid_email = page.get_by_text("Invalid email address")
        self.error_public_domain_email = page.get_by_text("Please use your official work email")
        self.error_unregistered_email = page.get_by_text("User not found")
        
        # Error messages - Reset password page
        self.error_nonverified_email = page.get_by_text("You must have a verified email before resetting your password.")
        self.error_otp_required = page.get_by_text("OTP is required")
        self.error_invalid_otp = page.get_by_text("Invalid verification code provided, please try again.")
        self.error_otp_input_limit = page.get_by_text("OTP must be 6 digits")
        self.error_otp_accept_numbers_only = page.get_by_text("OTP accept only number")
        self.error_new_password_required = page.get_by_text("New password is required")
        self.error_password_complexity = page.get_by_text("Password must contain an uppercase, lowercase, number and special character")
        self.error_confirm_password_required = page.get_by_text("Confirm password is required")
        self.error_password_mismatch = page.get_by_text("Passwords do not match")
        self.error_reset_pass_attempt_limit = page.get_by_text("Attempt limit exceeded, please try after some time.")
        
        # Toast messages
        self.toast_email_with_otp_sent = page.get_by_text("OTP has been sent to your email for password reset.")
        self.toast_otp_resent = page.get_by_text("OTP resent successfully")
        self.toast_password_reset_success = page.get_by_text("Password reset successfully")
        self.toast_otp_expired = page.get_by_text("OTP has expired")
        
        # Timer elements
        self.countdown_timer = page.get_by_text("Resend OTP in")
        self.resend_otp_countdown = page.locator("text=/\\d{2}:\\d{2}/")