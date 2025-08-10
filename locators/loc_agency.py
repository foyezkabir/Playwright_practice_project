from playwright.sync_api import Page, Locator
import re

class AgencyLocators:
    def __init__(self, page: Page):
        self.page = page

        # Login page locators
        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.sign_in_button = page.get_by_role("button", name="Sign in")
        
        # Agency modal locators (primary and fallbacks)
        self.agency_create_modal_heading = page.locator("div").filter(has_text=re.compile(r"^Create Agency$"))
        self.agency_modal_heading_alt = page.locator("text=Create Agency")
        self.agency_modal_heading_alt2 = page.locator("h2:has-text('Create Agency')")
        self.create_modal_body = page.locator(".modal-body")
        self.close_modal_button = page.get_by_role("button", name="Close modal")
        self.all_agencies_message = page.locator("div").filter(has_text="All AgenciesNo Agency found").nth(3)
        self.all_agencies_list = page.locator("div").filter(has_text="All Agencies Create new agencyAasd sdfdEditDeleteAasdjafsh gjhEditDeleteBbh").nth(3)
        self.create_new_agency_button = page.get_by_role("button", name="Create new agency")
        self.agency_name_input = page.get_by_role("textbox", name="Agency name")
        self.select_trigger = page.locator(".select-trigger")
        self.industry_dropdown = self.select_trigger
        self.information_technology_option = page.get_by_text("Information Technology")
        self.finance_option = page.get_by_text("Finance")
        self.healthcare_option = page.locator("div").filter(has_text=re.compile(r"^Healthcare$"))
        self.education_option = page.get_by_text("Education")
        self.website_input = page.get_by_role("textbox", name="Website (optional)")
        self.address_input = page.get_by_role("textbox", name="Address (optional)")
        self.description_input = page.get_by_role("textbox", name="Description (optional)")
        self.upload_logo_button = page.locator("div").filter(has_text=re.compile(r"^Upload Logo$"))
        self.agency_save_button = page.get_by_role("button", name="Save")
        self.agency_created_successfully_message = page.get_by_text("Agency created successfully")
        self.edit_button = page.locator("div").filter(has_text=re.compile(r"^asd sdfdEditDelete$")).get_by_role("button").first
        self.delete_button = page.locator("div").filter(has_text=re.compile(r"^asd sdfdEditDelete$")).get_by_role("button").nth(2)
        self.update_agency_modal = page.locator("div").filter(has_text=re.compile(r"^Update Agency$"))
        self.delete_confirmation_modal = page.get_by_text("Are you sure you want to delete this agency?This action cannot be undone. All")
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.confirm_button = page.get_by_role("button", name="Confirm")
        self.agency_deleted_successfully_message = page.get_by_text("Agency deleted successfully")
        self.agency_list_item = page.locator("div").filter(has_text=re.compile(r"^A$")).nth(1)
        self.main_content = page.get_by_role("main")
        self.agency_page_url = "https://bprp-qa.shadhinlab.xyz/agency"
        self.agency_list_item_data_testid = page.locator("[data-testid='agency-list-item']")
        self.user_menu_data_testid = page.locator("[data-testid='user-menu']")
        self.logout_button_data_testid = page.locator("[data-testid='logout-button']")
