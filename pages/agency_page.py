from playwright.sync_api import Page, expect
from locators.loc_agency import AgencyLocators
from utils.config import BASE_URL
import time

class AgencyPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = AgencyLocators(page)

    def navigate_to_login_page(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        self.locators.email_input.wait_for()
        self.locators.password_input.wait_for()

    def navigate_to_agency_page(self):
        self.page.goto(self.locators.agency_page_url)

    def fill_email(self, email: str):
        self.locators.email_input.fill(email)

    def fill_password(self, password: str):
        self.locators.password_input.fill(password)

    def click_sign_in(self):
        self.locators.sign_in_button.click()

    def expect_agency_modal_heading(self):
        expect(self.locators.agency_create_modal_heading).to_be_visible()

    def expect_agency_modal_body(self):
        expect(self.locators.create_modal_body).to_be_visible()

    def expect_no_agency_modal(self):
        try:
            time.sleep(3)
            expect(self.locators.agency_create_modal_heading).not_to_be_visible(timeout=2000)
            expect(self.locators.create_modal_body).not_to_be_visible(timeout=2000)
            print("✅ No agency creation modal appeared (as expected for account which has at least single agency)")
        except Exception as e:
            raise AssertionError(f"Agency creation modal appeared when it shouldn't have: {str(e)}")

    def verify_agency_page_url(self):
        current_url = self.page.url
        expected_url = self.locators.agency_page_url
        assert expected_url in current_url, f"Expected to be on agency page {expected_url}, but was on {current_url}"

    def click_create_new_agency(self):
        self.locators.create_new_agency_button.click()

    def click_agency_create_modal_heading(self):
        self.locators.agency_create_modal_heading.click()

    def click_close_modal_button(self):
        self.locators.close_modal_button.click()

    def expect_all_agencies_message(self):
        expect(self.locators.all_agencies_message).to_be_visible()

    def expect_all_agencies_list(self):
        expect(self.locators.all_agencies_list).to_be_visible()

    def fill_agency_name(self, agency_name: str):
        self.locators.agency_name_input.fill(agency_name)

    def select_industry_IT(self):
        self.locators.information_technology_option.click()

    def select_industry_finance(self):
        self.locators.finance_option.click()

    # def select_industry(self, industry: str):
    #     if industry == "Information Technology":
    #         self.locators.information_technology_option.click()
    #     elif industry == "Finance":
    #         self.locators.finance_option.click()
    #     elif industry == "Healthcare":
    #         self.locators.healthcare_option.click()
    #     elif industry == "Education":
    #         self.locators.education_option.click()

    def fill_website(self, website: str):
        self.locators.website_input.fill(website)

    def fill_address(self, address: str):
        self.locators.address_input.fill(address)

    def fill_description(self, description: str):
        self.locators.description_input.fill(description)

    def upload_logo(self):
        self.locators.upload_logo_button.click()

    def click_agency_save_button(self):
        self.locators.agency_save_button.click()

    def verify_agency_created_successfully(self):
        expect(self.locators.agency_created_successfully_message).to_be_visible()

    def verify_created_agency_appears(self):
        expect(self.locators.created_agency_appear).to_be_visible()

    def verify_created_agency_appears_in_list(self, agency_name: str):
        """Verify that the created agency appears in the agencies list with the correct name"""
        try:
            # Wait for the agencies list to load
            time.sleep(2)
            
            # Look for the agency name in the page content
            agency_locator = self.page.locator(f"text={agency_name}")
            expect(agency_locator).to_be_visible(timeout=10000)
            print(f"✅ Agency '{agency_name}' found in the agencies list")
            
        except Exception as e:
            # Take screenshot for debugging
            self.page.screenshot(path=f"debug_agency_list_{agency_name.replace(' ', '_')}.png")
            
            # Also try alternative locators
            try:
                # Try case-insensitive search
                agency_locator_alt = self.page.locator(f"text={agency_name}", has_text=agency_name)
                expect(agency_locator_alt).to_be_visible(timeout=5000)
                print(f"✅ Agency '{agency_name}' found with alternative locator")
            except:
                raise AssertionError(f"Agency '{agency_name}' not found in the agencies list: {str(e)}")

    def click_industry_dropdown(self):
        self.locators.industry_dropdown.click()

    def click_healthcare_option(self):
        self.locators.healthcare_option.click()

    def click_edit_button(self):
        self.locators.edit_button.click()

    def click_delete_button(self):
        self.locators.delete_button.click()

    def verify_update_agency_modal(self):
        expect(self.locators.update_agency_modal).to_be_visible()

    def verify_delete_confirmation_modal(self):
        expect(self.locators.delete_confirmation_modal).to_be_visible()

    def click_cancel_button(self):
        self.locators.cancel_button.click()

    def click_confirm_button(self):
        self.locators.confirm_button.click()

    def verify_agency_deleted_successfully(self):
        expect(self.locators.agency_deleted_successfully_message).to_be_visible()

    def click_agency_list_item(self):
        self.locators.agency_list_item.click()

    def verify_main_content(self):
        expect(self.locators.main_content).to_be_visible()

    def go_back_to_all_agencies(self):
        """Navigate back to All Agencies page using browser back"""
        self.page.go_back()
        self.page.wait_for_load_state("networkidle")

    # =====================
    # Custom helpers for test_agency_04
    # =====================


    def delete_all_agencies_if_exist(self):
        """
        Delete all agencies if any exist (for cleanup before test).
        Returns True if any agencies were deleted, False otherwise.
        """
        try:
            self.expect_all_agencies_list()
            time.sleep(2)
            agencies = self.locators.agency_list_item_data_testid
            count = agencies.count()
            deleted = False
            while count > 0:
                agencies.nth(0).click()
                time.sleep(1)
                self.click_delete_button()
                time.sleep(1)
                self.verify_delete_confirmation_modal()
                self.click_confirm_button()
                time.sleep(2)
                self.verify_agency_deleted_successfully()
                time.sleep(1)
                self.page.reload()
                self.expect_all_agencies_list()
                agencies = self.locators.agency_list_item_data_testid
                count = agencies.count()
                deleted = True
        except Exception as e:
            print(f"No agencies to delete or error occurred: {e}")
            return False
        return deleted

    def delete_agency_by_name(self, agency_name: str):
        """
        Delete only the agency with the given name.
        Returns True if deleted, False if not found.
        """
        try:
            self.expect_all_agencies_list()
            time.sleep(2)
            agency_locator = self.page.get_by_text(f"{agency_name}")
            print(agency_locator)
            if agency_locator.count() == 0:
                print(f"Agency '{agency_name}' not found for deletion.")
                return False
            agency_locator.first.click()
            time.sleep(1)
            self.click_delete_button()
            time.sleep(1)
            self.verify_delete_confirmation_modal()
            self.click_confirm_button()
            time.sleep(2)
            self.verify_agency_deleted_successfully()
            print(f"Agency '{agency_name}' deleted successfully.")
            return True
        except Exception as e:
            print(f"Error deleting agency '{agency_name}': {e}")
            return False

    def logout(self):
        """Logout from the current session."""
        try:
            self.locators.user_menu_data_testid.click()
            time.sleep(1)
            self.locators.logout_button_data_testid.click()
            time.sleep(2)
        except Exception as e:
            print(f"Logout failed or already logged out: {e}")
