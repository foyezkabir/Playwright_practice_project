"""
User Management Loc        # Create Role Modal
        self.create_role_button = page.get_by_role("button", name="Add Role")
        self.role_modal_heading = page.get_by_role("heading", name="Add Role")
        self.role_name_input = page.locator("input[name='name']")
        self.role_description_input = page.locator("input[name='description']") for BPRP Web Application
Contains all locators for user management features including roles & access and user list functionality
"""

from playwright.sync_api import Page, Locator
import re


class UserManagementLocators:
    def __init__(self, page: Page):
        self.page = page
        
        # ===== NAVIGATION & MAIN PAGE ELEMENTS =====
        self.user_management_menu = page.get_by_text("User Management")
        self.user_management_heading = page.get_by_text("User Management")
        self.roles_access_tab = page.get_by_role("link", name="Roles & Access")
        self.user_list_tab = page.get_by_role("link", name="User list")
        
        # Demo agency selection
        self.demo_06_agency = page.get_by_text("demo 06")
        self.agency_card = lambda agency_name: page.get_by_text(agency_name)
        
        # ===== ROLES & ACCESS TAB LOCATORS =====
        # Create Role Modal
        self.create_role_button = page.get_by_text("Add Role")
        self.role_modal_heading = page.get_by_role("heading", name="Add Role")
        self.role_name_input = page.locator("input[name='name']")
        self.role_description_input = page.locator("input[name='description']")
        
        # Permissions section
        self.permissions_heading = page.get_by_role("heading", name="Permissions")
        self.permissions_section = page.locator(".permissions-section, [class*='permission']")
        
        # Permission checkboxes - dynamic based on available permissions
        self.dashboard_permission = page.get_by_label("Dashboard")
        self.talent_permission = page.get_by_label("Talent")
        self.company_permission = page.get_by_label("Company")
        self.user_management_permission = page.get_by_label("User Management")
        self.agency_permission = page.get_by_label("Agency")
        
        # Permission actions for each module
        self.create_permission = lambda module: page.get_by_label(f"{module} Create")
        self.read_permission = lambda module: page.get_by_label(f"{module} Read")
        self.update_permission = lambda module: page.get_by_label(f"{module} Update") 
        self.delete_permission = lambda module: page.get_by_label(f"{module} Delete")
        
        # Generic permission checkbox locator
        self.permission_checkbox = lambda permission_name: page.get_by_label(permission_name)
        self.all_permission_checkboxes = page.locator("input[type='checkbox'][name*='permission'], .permission-checkbox input")
        
        # Role modal buttons
        self.save_role_button = page.locator("form button[type='submit']:has-text('Add Role')")
        self.cancel_role_button = page.get_by_role("button", name="Cancel")
        self.close_role_modal = page.get_by_role("button", name="×")
        
        # ===== ROLES LIST MANAGEMENT =====
        # Roles table/list
        self.roles_table = page.locator("table, .roles-list, [data-testid*='role']")
        self.role_row = lambda role_name: page.locator(f"tr:has-text('{role_name}'), .role-item:has-text('{role_name}')")
        self.role_item_by_name = lambda role_name: page.get_by_text(role_name, exact=True)
        
        # Role actions - Direct access to Edit/Delete buttons (no dropdown)
        self.edit_role_button_by_name = lambda role_name: page.get_by_role("row", name=f"{role_name} View Policies").get_by_role("button", name="Edit")
        self.delete_role_button_by_name = lambda role_name: page.get_by_role("row", name=f"{role_name} View Policies").get_by_role("button", name="Delete")
        
        # Edit role modal elements
        self.edit_role_button = page.get_by_role("button", name="Edit")
        self.edit_role_modal_heading = page.get_by_role("heading", name="Edit Role")
        self.update_role_button = page.get_by_role("button", name="Update Role")
        
        # Delete role confirmation
        self.delete_role_button = page.get_by_role("button", name="Delete")
        self.delete_confirmation_modal = page.get_by_role("dialog")
        self.delete_confirmation_heading = page.get_by_role("heading", name="Delete Role")
        self.confirm_delete_button = page.get_by_role("button", name="Yes, Delete")
        self.cancel_delete_button = page.get_by_role("button", name="Cancel")
        
        # Role search functionality
        self.role_search_input = page.locator("input[placeholder*='search'], input[placeholder*='Search'], .search-input")
        self.search_role_button = page.get_by_role("button", name="Search")
        self.clear_search_button = page.get_by_role("button", name="Clear")
        
        # ===== USER LIST TAB LOCATORS =====
        # Invite User Modal
        self.invite_user_button = page.get_by_role("button", name="Invite User")
        self.invite_user_modal_heading = page.get_by_role("heading", name="Invite User")
        
        # User invitation form fields
        self.user_name_input = page.locator("input[name='userName'], input[placeholder*='name'], input[placeholder*='Name']")
        self.user_email_input = page.locator("input[name='email'], input[type='email'], input[placeholder*='email']")
        self.user_role_dropdown = page.locator("select[name='role'], .role-select, [class*='role-dropdown']")
        self.role_option = lambda role_name: page.get_by_role("option", name=role_name)
        
        # Invite modal buttons
        self.send_invite_button = page.get_by_role("button", name="Invite")
        self.cancel_invite_button = page.get_by_role("button", name="Cancel")
        self.close_invite_modal = page.get_by_role("button", name="×")
        
        # ===== USERS LIST MANAGEMENT =====
        # Users table/list
        self.users_table = page.locator("table, .users-list, [data-testid*='user']")
        self.user_row = lambda user_email: page.locator(f"tr:has-text('{user_email}'), .user-item:has-text('{user_email}')")
        self.user_item_by_email = lambda user_email: page.get_by_text(user_email, exact=True)
        
        # User status indicators
        self.pending_status = page.get_by_text("Pending")
        self.active_status = page.get_by_text("Active")
        self.inactive_status = page.get_by_text("Inactive")
        
        # User actions
        self.user_actions_dropdown = lambda user_email: page.locator(f"tr:has-text('{user_email}') .dropdown, .user-item:has-text('{user_email}') .actions")
        self.user_three_dots_menu = lambda user_email: page.locator(f"tr:has-text('{user_email}') button[aria-label*='menu'], tr:has-text('{user_email}') .dropdown-toggle")
        
        # Edit user role
        self.edit_user_role_button = page.get_by_role("button", name="Edit Role")
        self.edit_role_modal = page.get_by_role("dialog")
        self.new_role_dropdown = page.locator("select[name='newRole'], .new-role-select")
        self.save_role_change_button = page.get_by_role("button", name="Save")
        
        # Delete user
        self.delete_user_button = page.get_by_role("button", name="Delete")
        self.delete_user_confirmation_modal = page.get_by_role("dialog")
        self.delete_user_confirmation_heading = page.get_by_role("heading", name="Delete User")
        self.confirm_delete_user_button = page.get_by_role("button", name="Yes, Delete")
        self.cancel_delete_user_button = page.get_by_role("button", name="Cancel")
        
        # User search functionality
        self.user_search_input = page.locator("input[placeholder*='search'], input[placeholder*='Search'], .search-input")
        self.search_user_button = page.get_by_role("button", name="Search")
        self.clear_user_search_button = page.get_by_role("button", name="Clear")
        
        # ===== VALIDATION & ERROR MESSAGES =====
        # Role validation messages
        self.role_name_required_error = page.get_by_text("Role name is required")
        self.role_name_exists_error = page.get_by_text("Role name already exists")
        self.permissions_required_error = page.get_by_text("At least one permission is required")
        
        # User invitation validation messages
        self.user_name_required_error = page.get_by_text("Name is required")
        self.user_email_required_error = page.get_by_text("Email is required")
        self.invalid_email_format_error = page.get_by_text("Please enter a valid email address")
        self.email_already_exists_error = page.get_by_text("User with this email already exists")
        self.role_selection_required_error = page.get_by_text("Role is required")
        self.host_email_protection_error = page.get_by_text("Cannot invite host email")
        
        # ===== SUCCESS MESSAGES =====
        self.role_created_success_message = page.get_by_text("Role added successfully")
        self.role_updated_successfully = page.get_by_text("Role updated successfully") 
        self.role_deleted_successfully = page.get_by_text("Role deleted successfully")
        self.user_invited_successfully = page.get_by_text("User invited successfully")
        self.user_role_updated_successfully = page.get_by_text("User role updated successfully")
        self.user_deleted_successfully = page.get_by_text("User deleted successfully")
        
        # Generic success/error toast messages
        self.success_toast = page.locator(".toast-success, .alert-success, [class*='success']")
        self.error_toast = page.locator(".toast-error, .alert-error, [class*='error']")
        self.toast_message = page.locator(".toast, .alert, [class*='toast'], [class*='alert']")
        
        # ===== PAGINATION & LOADING =====
        self.pagination_container = page.locator("ul.pagination-container")
        self.next_page_button = page.locator("ul.pagination-container > li:last-child:not(.disabled)")
        self.previous_page_button = page.locator("ul.pagination-container > li:first-child:not(.disabled)")
        self.page_number = lambda page_num: page.get_by_role("button", name=str(page_num))
        
        self.loading_spinner = page.locator(".loading, .spinner, [class*='loading']")
        self.no_data_message = page.get_by_text("No data available")
        
        # ===== ADDITIONAL UTILITY LOCATORS =====
        # General form elements
        self.required_field_indicator = page.locator(".required, [class*='required'], .mandatory")
        self.form_validation_error = page.locator(".error, .validation-error, [class*='error']")
        self.modal_overlay = page.locator(".modal-overlay, .backdrop")
        
        # Specific validation error messages
        self.role_name_required_error = page.get_by_text("Role name is required")
        self.role_name_validation_error = page.locator("[data-testid='role-name-error'], .role-name-error")
        self.description_validation_error = page.locator("[data-testid='description-error'], .description-error")
        
        # Table headers for sorting
        self.role_name_header = page.get_by_role("columnheader", name="Role Name")
        self.permissions_header = page.get_by_role("columnheader", name="Permissions")
        self.user_name_header = page.get_by_role("columnheader", name="Name")
        self.user_email_header = page.get_by_role("columnheader", name="Email")
        self.user_role_header = page.get_by_role("columnheader", name="Role")
        self.user_status_header = page.get_by_role("columnheader", name="Status")
        
        # Action buttons in table rows
        self.table_action_button = page.locator("tbody tr button, .table-row button")
        self.dropdown_menu = page.locator(".dropdown-menu, [class*='dropdown']")
        
        # ===== RESPONSIVE & ACCESSIBILITY =====
        # Mobile menu toggles
        self.mobile_menu_toggle = page.locator(".mobile-menu, [class*='mobile']")
        self.hamburger_menu = page.locator(".hamburger, [class*='hamburger']")
        
        # Accessibility landmarks
        self.main_content = page.locator("main, [role='main']")
        self.navigation_menu = page.locator("nav, [role='navigation']")
        
        # ===== BREADCRUMB & NAVIGATION =====
        self.breadcrumb = page.locator(".breadcrumb, [class*='breadcrumb']")
        self.back_button = page.get_by_role("button", name="Back")
        self.home_link = page.get_by_role("link", name="Home")
        
        # ===== FILTERS & SORTING =====
        self.filter_dropdown = page.locator("select[name*='filter'], .filter-select")
        self.sort_dropdown = page.locator("select[name*='sort'], .sort-select")
        self.status_filter = page.locator("select[name='status'], .status-filter")
        self.role_filter = page.locator("select[name='roleFilter'], .role-filter")
        
        # Date range filters
        self.date_from_input = page.locator("input[type='date'][name*='from']")
        self.date_to_input = page.locator("input[type='date'][name*='to']")
        self.apply_filter_button = page.get_by_role("button", name="Apply Filter")
        self.reset_filter_button = page.get_by_role("button", name="Reset")
