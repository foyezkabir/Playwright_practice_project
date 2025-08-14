from encodings.punycode import T
from playwright.sync_api import Page, expect
from locators.loc_agency import AgencyLocators
from utils.config import BASE_URL
import utils.agency_helper as agency_helper
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
        agency_helper.assert_agency_create_modal_heading(self.page)

    def expect_agency_modal_body(self):
        agency_helper.assert_create_modal_body(self.page)

    def expect_no_agency_modal(self):
        try:
            time.sleep(3)
            # Use enhanced assertions for better screenshot timing
            agency_helper.assert_agency_create_modal_not_visible(self.page)
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
        agency_helper.assert_all_agencies_message(self.page)

    def expect_all_agencies_list(self):
        agency_helper.assert_all_agencies_list(self.page)

    def fill_agency_name(self, agency_name: str):
        self.locators.agency_name_input.fill(agency_name)

    def select_industry_IT(self):
        self.locators.information_technology_option.click()

    def select_industry_finance(self):
        self.locators.finance_option.click()

    def fill_website(self, website: str):
        self.locators.website_input.fill(website)

    def fill_website_alt(self, website: str):
        """Alternative website input method using backup locator"""
        self.locators.website_input_alt.first.fill(website)

    def check_validation_error(self):
        """Check if validation error is visible"""
        # Check multiple error sources
        form_errors = self.locators.validation_error.count() > 0
        toast_errors = self.locators.error_toast.count() > 0
        toast_messages = self.locators.toast_message.count() > 0
        return form_errors or toast_errors or toast_messages

    def check_file_format_error(self):
        """Check if file format validation error is visible"""
        # Check both form errors and toast messages
        format_errors = self.locators.file_format_error.count() > 0
        toast_errors = self.locators.error_toast.count() > 0
        return format_errors or toast_errors

    def check_file_size_error(self):
        """Check if file size validation error is visible"""
        # Check both form errors and toast messages
        size_errors = self.locators.file_size_error.count() > 0
        toast_errors = self.locators.error_toast.count() > 0
        return size_errors or toast_errors

    def get_validation_error_message(self) -> str:
        """Get the text of any validation error or toast message."""
        # Try different error sources
        if self.locators.validation_error.count() > 0:
            return self.locators.validation_error.first.text_content()
        elif self.locators.error_toast.count() > 0:
            return self.locators.error_toast.first.text_content()
        elif self.locators.toast_message.count() > 0:
            return self.locators.toast_message.first.text_content()
        return ""

    def wait_for_toast_message(self, timeout=5000):
        """Wait for any toast message to appear"""
        try:
            self.locators.toast_message.first.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    def upload_file(self, file_path: str):
        """Upload file using file input - handles hidden inputs"""
        try:
            # Try to use the first file input (even if hidden)
            self.locators.file_upload_input.first.set_input_files(file_path)
        except Exception as e:
            # If first method fails, try clicking the upload area first
            try:
                self.locators.upload_logo_button.first.click()
                time.sleep(1)
                self.locators.file_upload_input.first.set_input_files(file_path)
            except Exception as e2:
                print(f"File upload failed: {e2}")
                raise e2

    def check_all_agencies_heading(self):
        """Check if we're on the all agencies page"""
        return self.locators.all_agencies_heading.count() > 0

    def fill_address(self, address: str):
        self.locators.address_input.fill(address)

    def fill_description(self, description: str):
        self.locators.description_input.fill(description)

    def upload_logo(self):
        self.locators.upload_logo_button.click()

    def click_agency_save_button(self):
        self.locators.agency_save_button.click()

    def verify_agency_created_successfully(self):
        agency_helper.assert_agency_created_successfully_message(self.page)

    def verify_created_agency_appears(self):
        agency_helper.assert_created_agency_appear(self.page)

    def verify_created_agency_appears_in_list(self, agency_name: str):
        """Verify that the created agency appears in the agencies list with the correct name"""
        try:
            # Wait for the agencies list to load
            time.sleep(2)
            
            # Look for the agency name in the page content
            agency_locator = self.page.locator(f"text={agency_name}")
            assert agency_locator.is_visible(timeout=10000), f"Agency '{agency_name}' should be visible in list"
            print(f"✅ Agency '{agency_name}' found in the agencies list")
            
        except Exception as e:
            # Take screenshot for debugging
            self.page.screenshot(path=f"debug_agency_list_{agency_name.replace(' ', '_')}.png")
            
            # Also try alternative locators
            try:
                # Try case-insensitive search
                agency_locator_alt = self.page.locator(f"text={agency_name}", has_text=agency_name)
                assert agency_locator_alt.is_visible(timeout=5000), f"Agency '{agency_name}' should be visible with alternative locator"
                print(f"✅ Agency '{agency_name}' found with alternative locator")
            except:
                raise AssertionError(f"Agency '{agency_name}' not found in the agencies list: {str(e)}")

    def click_industry_dropdown(self):
        self.locators.industry_dropdown.click()

    def click_healthcare_option(self):
        self.locators.healthcare_option.click()

    def click_edit_button(self):
        self.locators.edit_button.click()

    def click_update_button(self):
        self.locators.agency_update_button.click()

    def verify_update_confirm_message(self):
        agency_helper.assert_update_confirm_message(self.page)

    def click_delete_button(self):
        self.locators.delete_button.click()

    def verify_update_agency_modal(self):
        agency_helper.assert_update_agency_modal(self.page)

    def verify_delete_confirmation_modal(self):
        agency_helper.assert_delete_confirmation_modal(self.page)

    def click_cancel_button(self):
        self.locators.cancel_button.click()

    def click_confirm_button(self):
        self.locators.confirm_button.click()

    def verify_agency_deleted_successfully(self):
        agency_helper.assert_agency_deleted_successfully_message(self.page)

    def click_agency_list_item(self):
        self.locators.agency_list_item.click()

    def verify_main_content(self):
        agency_helper.assert_main_content(self.page)

    def go_back_to_all_agencies(self):
        self.page.go_back()
        self.page.wait_for_load_state("networkidle")

    def get_three_dot_icon_and_click(self):
        self.locators.Three_dot_icon.click()

    def get_edit_icon_and_click(self):
        self.locators.edit_button.click()

    def get_agency_by_name(self, agency_name: str):
        return self.locators.locate_agency_card(agency_name)

    def get_agency_actions(self, agency_name: str):
        agency_card = self.get_agency_by_name(agency_name)
        return agency_card.locator("//following-sibling::div/button").click(force=True)

    def delete_all_agencies_if_exist(self):
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
        try:
            agency_locator = self.get_agency_by_name(agency_name)
            print(agency_locator)
            if agency_locator.count() == 0:
                print(f"Agency '{agency_name}' not found for deletion.")
                return False
            agency_locator.locator("//following-sibling::div/button").click(force=True)
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

    def edit_agency_by_name(self, agency_name: str, new_name: str):
        try:
            
            self.fill_agency_name(new_name)
            self.click_update_button()
            time.sleep(2)
            print(f"Agency '{agency_name}' updated successfully to {new_name}.")
            return True
        except Exception as e:
            print(f"Error updating agency '{agency_name}': {e}")
            return False

    def find_agency_in_paginated_list(self, page: Page, agency_name: str):
        """
        Loops through a paginated list to find specific text.

        This function checks the current page for the agency_name. If the name is not found,
        it looks for a clickable 'next' button and clicks it, repeating the process
        until the agency is found or the last page is reached.
        """
        # Wait for page to load initially
        time.sleep(2)
        
        print(f"🔍 Starting search for agency: '{agency_name}'")
        print(f"📍 Current URL: {page.url}")
        
        # This locator targets the 'next' button, which is the last list item (`li:last-child`)
        # in the pagination container. The `:not(.disabled)` part ensures we only select it
        # when it's clickable.
        next_button = page.locator("ul.pagination-container > li:last-child:not(.disabled)")
        max_pages = 10  # Prevent infinite loops
        current_page = 0

        while current_page < max_pages:
            current_page += 1
            
            # Wait for content to load and be stable
            try:
                page.wait_for_load_state("domcontentloaded", timeout=5000)
                time.sleep(1)  # Small wait for content to stabilize
            except:
                pass
            
            print(f"🔍 Searching page {current_page} for '{agency_name}'...")
            
            # Debug: print all agency names on current page
            all_agencies = page.locator("[data-testid='agency-name'], .agency-name, .agency-list-item")
            agency_count = all_agencies.count()
            print(f"📊 Found {agency_count} agencies on page {current_page}")
            
            # Print visible agencies for debugging
            for i in range(min(agency_count, 5)):  # Limit to first 5 for debugging
                try:
                    agency_text = all_agencies.nth(i).text_content()
                    print(f"  - Agency {i+1}: '{agency_text}'")
                except:
                    pass
            
            # Check if the agency name is visible on the current page.
            agency_element = page.get_by_text(agency_name, exact=True)
            if agency_element.count() > 0:
                print(f"✅ Found agency '{agency_name}' on page {current_page}.")
                # Check if there are multiple elements with same name (duplicates)
                if agency_element.count() > 1:
                    print(f"⚠️ Warning: Found {agency_element.count()} duplicate agencies with name '{agency_name}'")
                return True  # Return success
                
            # If the agency is not on this page, check if a 'next' button is available.
            if next_button.count() == 0:
               print(f"❌ Reached the end of pagination after {current_page} pages. Agency '{agency_name}' was not found.")
               return False  # Return failure

            # If we are here, it means the agency wasn't found AND there's a next page.
            print(f"-> Agency not found on page {current_page}, navigating to the next page...")
            
            try:
                next_button.click()
                # Wait for the network to be idle with shorter timeout
                page.wait_for_load_state("networkidle", timeout=8000)
                time.sleep(2)  # Shorter wait than before
            except Exception as e:
                print(f"Error clicking next button: {e}")
                return False
                
        print(f"❌ Searched {max_pages} pages but couldn't find agency '{agency_name}'")
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

    def click_edit_button_for_agency(self, agency_name: str):
        """Find the agency card by name and click its edit button reliably."""
        agency_card = self.page.get_by_text(agency_name, exact=True)
        agency_card.wait_for()
        # Try common edit button selectors within the card's parent/container
        parent = agency_card.locator('xpath=..')
        # Try several possible selectors for the edit button
        edit_btn = parent.locator("button[title='Edit'], .edit-icon, [aria-label='Edit']")
        if edit_btn.count() == 0:
            # Fallback to the original locator if needed
            edit_btn = self.locators.edit_button(agency_name)
        edit_btn.wait_for()
        edit_btn.click(force=True)

    # ===== NEW VALIDATION HELPER METHODS =====
    
    def fill_website_field(self, website_url: str):
        """Fill the website field with the given URL."""
        try:
            self.locators.website_input.fill(website_url)
        except:
            # Fallback to alternative locator
            self.locators.website_input_alt.first.fill(website_url)
    
    def upload_logo_file(self, file_path: str):
        """Upload a logo file."""
        try:
            self.locators.file_upload_input.set_input_files(file_path)
        except:
            # Alternative approach
            upload_area = self.page.locator("input[type='file'], .upload, [class*='upload']")
            if upload_area.count() > 0:
                upload_area.first.set_input_files(file_path)
    
    def check_validation_error_exists(self) -> bool:
        """Check if any validation error is visible."""
        return self.locators.validation_error.count() > 0
    
    def check_success_message_exists(self) -> bool:
        """Check if any success message is visible."""
        return self.locators.success_message.count() > 0
    
    def get_validation_error_message(self) -> str:
        """Get the text of the first validation error."""
        if self.check_validation_error_exists():
            return self.locators.validation_error.first.text_content()
        return ""
    
    def verify_field_labels_present(self, expected_labels: list) -> bool:
        """Verify that all expected field labels are present."""
        for label_text in expected_labels:
            label_element = self.page.locator(f"text='{label_text}'")
            if label_element.count() == 0:
                return False
        return True
    
    def count_form_labels(self) -> int:
        """Count the number of form labels present."""
        return self.locators.form_labels.count()
