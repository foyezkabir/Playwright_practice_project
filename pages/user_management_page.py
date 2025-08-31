"""
User Management Page Object Model
Handles all user management operations including roles & access and user list functionality
"""

from playwright.sync_api import Page, expect
from locators.loc_user_management import UserManagementLocators
from utils.config import BASE_URL
import time


class UserManagementPage:
    def __init__(self, page: Page):
        self.page = page
        self.locators = UserManagementLocators(page)

    # ===== NAVIGATION METHODS =====
    def navigate_to_user_management(self):
        """Navigate to user management page"""
        self.locators.user_management_menu.click()
        self.page.wait_for_load_state("networkidle")

    def click_roles_access_tab(self):
        """Switch to Roles & Access tab"""
        self.locators.roles_access_tab.click()
        time.sleep(1)

    def click_user_list_tab(self):
        """Switch to User List tab"""
        self.locators.user_list_tab.click()
        time.sleep(1)

    def select_demo_agency(self, agency_name: str = "demo 06"):
        """Select a specific demo agency"""
        self.locators.agency_card(agency_name).click()
        self.page.wait_for_load_state("networkidle")

    # ===== ROLES & ACCESS METHODS =====
    def click_create_role_button(self):
        """Click the Create Role button to open modal"""
        self.locators.create_role_button.click()
        time.sleep(1)

    def fill_role_name(self, role_name: str):
        """Fill the role name input field"""
        self.locators.role_name_input.wait_for(state="visible")
        self.locators.role_name_input.fill(role_name)

    def select_permission(self, permission_name: str):
        """Select a specific permission checkbox"""
        self.locators.permission_checkbox(permission_name).check()

    def select_multiple_permissions(self, permissions_list: list):
        """Select multiple permissions from a list"""
        for permission in permissions_list:
            try:
                self.select_permission(permission)
                time.sleep(0.5)  # Brief pause between selections
            except Exception as e:
                print(f"Could not select permission '{permission}': {e}")

    def select_module_permissions(self, module: str, actions: list):
        """Select specific actions for a module (create, read, update, delete)"""
        for action in actions:
            try:
                permission_locator = self.locators.permission_checkbox(f"{module} {action}")
                if permission_locator.count() > 0:
                    permission_locator.check()
            except Exception as e:
                print(f"Could not select {action} permission for {module}: {e}")

    def click_save_role_button(self):
        """Save the role after filling details"""
        self.locators.save_role_button.click()
        time.sleep(2)  # Wait for save operation

    def click_cancel_role_button(self):
        """Cancel role creation/editing"""
        self.locators.cancel_role_button.click()

    def close_role_modal(self):
        """Close the role modal using X button"""
        self.locators.close_role_modal.click()

    # ===== ROLE MANAGEMENT METHODS =====
    def search_role(self, role_name: str):
        """Search for a specific role"""
        if self.locators.role_search_input.count() > 0:
            self.locators.role_search_input.fill(role_name)
            if self.locators.search_role_button.count() > 0:
                self.locators.search_role_button.click()
            time.sleep(2)

    def clear_role_search(self):
        """Clear the role search"""
        if self.locators.clear_search_button.count() > 0:
            self.locators.clear_search_button.click()
        time.sleep(1)

    def find_role_by_name(self, role_name: str) -> bool:
        """Check if a role exists in the current view"""
        return self.locators.role_item_by_name(role_name).count() > 0

    def click_role_actions_menu(self, role_name: str):
        """Click the actions menu (three dots) for a specific role"""
        try:
            self.locators.three_dots_menu(role_name).click()
            time.sleep(1)
        except:
            # Fallback to row-level actions
            self.locators.role_actions_dropdown(role_name).click()
            time.sleep(1)

    def edit_role(self, role_name: str, new_role_name: str = None, new_permissions: list = None):
        """Edit an existing role"""
        self.click_role_actions_menu(role_name)
        self.locators.edit_role_button.click()
        time.sleep(1)
        
        if new_role_name:
            self.locators.role_name_input.fill(new_role_name)
        
        if new_permissions:
            self.select_multiple_permissions(new_permissions)
        
        self.locators.update_role_button.click()
        time.sleep(2)

    def delete_role(self, role_name: str, confirm: bool = True):
        """Delete a specific role"""
        self.click_role_actions_menu(role_name)
        self.locators.delete_role_button.click()
        time.sleep(1)
        
        if confirm:
            self.locators.confirm_delete_button.click()
        else:
            self.locators.cancel_delete_button.click()
        time.sleep(2)

    # ===== USER LIST METHODS =====
    def click_invite_user_button(self):
        """Click the Invite User button to open modal"""
        self.locators.invite_user_button.click()
        time.sleep(1)

    def fill_user_name(self, user_name: str):
        """Fill the user name input field"""
        self.locators.user_name_input.wait_for(state="visible")
        self.locators.user_name_input.fill(user_name)

    def fill_user_email(self, user_email: str):
        """Fill the user email input field"""
        self.locators.user_email_input.wait_for(state="visible")
        self.locators.user_email_input.fill(user_email)

    def select_user_role(self, role_name: str):
        """Select a role for the user from dropdown"""
        try:
            self.locators.user_role_dropdown.click()
            time.sleep(1)
            self.locators.role_option(role_name).click()
        except:
            # Alternative approach for different dropdown implementations
            self.locators.user_role_dropdown.select_option(label=role_name)

    def click_send_invite_button(self):
        """Send the user invitation"""
        self.locators.send_invite_button.click()
        time.sleep(2)

    def click_cancel_invite_button(self):
        """Cancel user invitation"""
        self.locators.cancel_invite_button.click()

    def close_invite_modal(self):
        """Close the invite user modal using X button"""
        self.locators.close_invite_modal.click()

    # ===== USER MANAGEMENT METHODS =====
    def search_user(self, user_email: str):
        """Search for a specific user by email"""
        if self.locators.user_search_input.count() > 0:
            self.locators.user_search_input.fill(user_email)
            if self.locators.search_user_button.count() > 0:
                self.locators.search_user_button.click()
            time.sleep(2)

    def clear_user_search(self):
        """Clear the user search"""
        if self.locators.clear_user_search_button.count() > 0:
            self.locators.clear_user_search_button.click()
        time.sleep(1)

    def find_user_by_email(self, user_email: str) -> bool:
        """Check if a user exists in the current view"""
        return self.locators.user_item_by_email(user_email).count() > 0

    def click_user_actions_menu(self, user_email: str):
        """Click the actions menu (three dots) for a specific user"""
        try:
            self.locators.user_three_dots_menu(user_email).click()
            time.sleep(1)
        except:
            # Fallback to row-level actions
            self.locators.user_actions_dropdown(user_email).click()
            time.sleep(1)

    def edit_user_role(self, user_email: str, new_role: str):
        """Edit a user's role"""
        self.click_user_actions_menu(user_email)
        self.locators.edit_user_role_button.click()
        time.sleep(1)
        
        try:
            self.locators.new_role_dropdown.click()
            self.locators.role_option(new_role).click()
        except:
            self.locators.new_role_dropdown.select_option(label=new_role)
        
        self.locators.save_role_change_button.click()
        time.sleep(2)

    def delete_user(self, user_email: str, confirm: bool = True):
        """Delete a specific user"""
        self.click_user_actions_menu(user_email)
        self.locators.delete_user_button.click()
        time.sleep(1)
        
        if confirm:
            self.locators.confirm_delete_user_button.click()
        else:
            self.locators.cancel_delete_user_button.click()
        time.sleep(2)

    # ===== VALIDATION HELPER METHODS =====
    def wait_for_toast_message(self, timeout: int = 5000) -> bool:
        """Wait for any toast message to appear"""
        try:
            self.locators.toast_message.first.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    def get_toast_message_text(self) -> str:
        """Get the text of the current toast message"""
        if self.locators.toast_message.count() > 0:
            return self.locators.toast_message.first.text_content()
        return ""

    def check_success_toast_visible(self) -> bool:
        """Check if success toast is visible"""
        return self.locators.success_toast.count() > 0

    def check_error_toast_visible(self) -> bool:
        """Check if error toast is visible"""
        return self.locators.error_toast.count() > 0

    def check_validation_error_visible(self) -> bool:
        """Check if form validation error is visible"""
        return self.locators.form_validation_error.count() > 0

    # ===== COMPREHENSIVE WORKFLOW METHODS =====
    def create_role_with_permissions(self, role_name: str, permissions: list) -> bool:
        """Complete workflow to create a role with specific permissions"""
        try:
            self.click_create_role_button()
            self.fill_role_name(role_name)
            self.select_multiple_permissions(permissions)
            self.click_save_role_button()
            
            # Wait for success message
            success = self.wait_for_toast_message()
            return success and self.check_success_toast_visible()
        except Exception as e:
            print(f"Error creating role: {e}")
            return False

    def invite_user_with_role(self, user_name: str, user_email: str, role_name: str) -> bool:
        """Complete workflow to invite a user with specific role"""
        try:
            self.click_invite_user_button()
            self.fill_user_name(user_name)
            self.fill_user_email(user_email)
            self.select_user_role(role_name)
            self.click_send_invite_button()
            
            # Wait for success message
            success = self.wait_for_toast_message()
            return success and self.check_success_toast_visible()
        except Exception as e:
            print(f"Error inviting user: {e}")
            return False

    def get_roles_list(self) -> list:
        """Get list of all visible roles"""
        roles = []
        try:
            role_elements = self.page.locator("tbody tr td:first-child, .role-name")
            count = role_elements.count()
            for i in range(count):
                role_name = role_elements.nth(i).text_content()
                if role_name and role_name.strip():
                    roles.append(role_name.strip())
        except Exception as e:
            print(f"Error getting roles list: {e}")
        return roles

    def get_users_list(self) -> list:
        """Get list of all visible users"""
        users = []
        try:
            user_elements = self.page.locator("tbody tr")
            count = user_elements.count()
            for i in range(count):
                row = user_elements.nth(i)
                # Extract user info (name, email, role, status)
                cells = row.locator("td")
                if cells.count() >= 3:
                    user_info = {
                        'name': cells.nth(0).text_content().strip() if cells.nth(0).text_content() else '',
                        'email': cells.nth(1).text_content().strip() if cells.nth(1).text_content() else '',
                        'role': cells.nth(2).text_content().strip() if cells.nth(2).text_content() else ''
                    }
                    if cells.count() >= 4:
                        user_info['status'] = cells.nth(3).text_content().strip()
                    users.append(user_info)
        except Exception as e:
            print(f"Error getting users list: {e}")
        return users

    # ===== PAGINATION HELPER METHODS =====
    def navigate_to_next_page(self) -> bool:
        """Navigate to next page if available"""
        if self.locators.next_page_button.count() > 0 and self.locators.next_page_button.is_enabled():
            self.locators.next_page_button.click()
            time.sleep(2)
            return True
        return False

    def navigate_to_previous_page(self) -> bool:
        """Navigate to previous page if available"""
        if self.locators.previous_page_button.count() > 0 and self.locators.previous_page_button.is_enabled():
            self.locators.previous_page_button.click()
            time.sleep(2)
            return True
        return False

    def find_item_in_paginated_list(self, item_name: str, search_type: str = "role") -> bool:
        """
        Find an item (role or user) across paginated results
        
        Args:
            item_name: Name of the role or email of the user to find
            search_type: Either "role" or "user"
        
        Returns:
            True if item found, False otherwise
        """
        max_pages = 10
        current_page = 0
        
        while current_page < max_pages:
            current_page += 1
            
            # Search in current page
            if search_type == "role":
                found = self.find_role_by_name(item_name)
            else:
                found = self.find_user_by_email(item_name)
                
            if found:
                print(f"✅ Found {search_type} '{item_name}' on page {current_page}")
                return True
            
            # Try to go to next page
            if not self.navigate_to_next_page():
                break
                
        print(f"❌ {search_type.title()} '{item_name}' not found after searching {current_page} pages")
        return False

    # ===== CLEANUP METHODS =====
    def cleanup_test_roles(self, test_role_prefix: str = "Test Role"):
        """Clean up test roles that start with specific prefix"""
        roles_to_delete = []
        
        # Get all roles
        roles = self.get_roles_list()
        
        # Find test roles
        for role in roles:
            if role.startswith(test_role_prefix):
                roles_to_delete.append(role)
        
        # Delete test roles
        for role in roles_to_delete:
            try:
                self.delete_role(role, confirm=True)
                print(f"🗑️ Cleaned up test role: {role}")
            except Exception as e:
                print(f"❌ Failed to cleanup role {role}: {e}")

    def cleanup_test_users(self, test_email_domain: str = "test"):
        """Clean up test users with specific email domain"""
        users_to_delete = []
        
        # Get all users
        users = self.get_users_list()
        
        # Find test users
        for user in users:
            if test_email_domain in user.get('email', ''):
                users_to_delete.append(user['email'])
        
        # Delete test users
        for user_email in users_to_delete:
            try:
                self.delete_user(user_email, confirm=True)
                print(f"🗑️ Cleaned up test user: {user_email}")
            except Exception as e:
                print(f"❌ Failed to cleanup user {user_email}: {e}")

    # ===== VERIFICATION METHODS =====
    def verify_role_exists(self, role_name: str) -> bool:
        """Verify that a role exists in the system"""
        return self.find_item_in_paginated_list(role_name, "role")

    def verify_user_exists(self, user_email: str) -> bool:
        """Verify that a user exists in the system"""
        return self.find_item_in_paginated_list(user_email, "user")

    def verify_user_role_assignment(self, user_email: str, expected_role: str) -> bool:
        """Verify that a user has the expected role assigned"""
        users = self.get_users_list()
        for user in users:
            if user.get('email') == user_email:
                return user.get('role') == expected_role
        return False

    def verify_user_status(self, user_email: str, expected_status: str) -> bool:
        """Verify that a user has the expected status"""
        users = self.get_users_list()
        for user in users:
            if user.get('email') == user_email:
                return user.get('status') == expected_status
        return False
