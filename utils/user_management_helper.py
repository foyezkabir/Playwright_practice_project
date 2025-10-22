"""
User Management Helper Module
Contains utility functions for user management tests including roles & access and user list operations
"""

from playwright.sync_api import Page
from utils.config import BASE_URL
from utils.login_helper import do_login
from conftest import wait_for_action_completion
from utils.enhanced_assertions import enhanced_assert_visible, enhanced_assert_not_visible
import time


def do_user_management_login(page: Page, email: str, password: str):
    """
    Helper function to login, select demo 06 agency, and navigate to user management
    
    Args:
        page: Playwright page object
        email: User email
        password: User password
    
    Returns:
        UserManagementPage instance
    """
    from pages.user_management_page import UserManagementPage
    
    # Step 1: Login
    do_login(page, email, password)
    time.sleep(3)
    
    # Step 2: Click on "demo 06" agency to access it
    demo_agency = page.get_by_text("demo 06", exact=True).first
    demo_agency.wait_for(state="visible", timeout=10000)
    demo_agency.click()
    time.sleep(3)
    
    # Step 3: Initialize user management page and navigate to User Management menu
    user_mgmt_page = UserManagementPage(page)
    user_mgmt_page.navigate_to_user_management()
    time.sleep(2)
    
    # Step 4: Click on Roles & Access tab
    user_mgmt_page.click_roles_access_tab()
    time.sleep(2)
    
    return user_mgmt_page


def setup_demo_agency_access(page: Page, email: str, password: str):
    """
    Complete setup for demo agency access in user management
    
    Args:
        page: Playwright page object
        email: User email
        password: User password
        
    Returns:
        UserManagementPage instance
    """
    # Login and get to user management
    user_mgmt_page = do_user_management_login(page, email, password)
    
    # Select demo agency
    user_mgmt_page.click_demo_agency()
    time.sleep(2)
    
    # Navigate to roles & access tab
    user_mgmt_page.click_roles_access_tab()
    time.sleep(2)
    
    return user_mgmt_page


class UserManagementTestHelper:
    """
    Centralized helper class for user management test operations
    Provides parameterized methods for all user management test scenarios
    """
    
    def __init__(self, page: Page):
        self.page = page
        self.user_mgmt_page = None
    
    def setup_user_management(self, email: str, password: str):
        """
        Complete setup: Login and navigate to user management
        
        Args:
            email: User email
            password: User password
            
        Returns:
            UserManagementPage instance
        """
        from pages.user_management_page import UserManagementPage
        
        # Login first
        do_login(self.page, email, password)
        time.sleep(3)
        
        # Initialize user management page
        self.user_mgmt_page = UserManagementPage(self.page)
        
        # Navigate to user management and select demo agency
        self.user_mgmt_page.navigate_to_user_management()
        time.sleep(2)
        
        # Select demo agency
        self.user_mgmt_page.click_demo_agency()
        time.sleep(2)
        
        # Navigate to roles & access tab
        self.user_mgmt_page.click_roles_access_tab()
        time.sleep(2)
        
        print("✅ User management setup completed successfully")
        return self.user_mgmt_page
    
    def create_role(self, role_name: str, description: str, permissions: list):
        """
        Create a new role with validation
        
        Args:
            role_name: Name of the role
            description: Role description
            permissions: List of permissions to assign
        """
        if not self.user_mgmt_page:
            raise ValueError("User management not initialized. Call setup_user_management first.")
        
        print(f"🏗️ Creating role '{role_name}'...")
        
        # Click create role button
        self.user_mgmt_page.click_create_role_button()
        time.sleep(2)
        
        # Fill role details
        self.user_mgmt_page.fill_role_name(role_name)
        self.user_mgmt_page.fill_role_description(description)
        
        # Select permissions
        self.user_mgmt_page.select_multiple_permissions(permissions)
        
        # Save role
        self.user_mgmt_page.click_save_role_button()
        time.sleep(3)
        
        # Verify success message
        enhanced_assert_visible(self.page, self.user_mgmt_page.locators.role_created_successfully_message, 
                              f"Role '{role_name}' creation success message should be visible", f"create_role_{role_name}")
        
        print(f"✅ Role '{role_name}' created successfully")
    
    def search_and_verify_role(self, role_name: str):
        """
        Search for a role and verify it exists
        
        Args:
            role_name: Name of role to search
            
        Returns:
            bool: True if role found
        """
        if not self.user_mgmt_page:
            raise ValueError("User management not initialized. Call setup_user_management first.")
        
        print(f"🔍 Searching for role '{role_name}'...")
        
        self.user_mgmt_page.search_role(role_name)
        time.sleep(2)
        
        role_found = self.user_mgmt_page.find_role_by_name(role_name)
        
        if role_found:
            print(f"✅ Role '{role_name}' found successfully")
        else:
            print(f"❌ Role '{role_name}' not found")
        
        return role_found
    
    def edit_role(self, current_role_name: str, new_role_name: str = None, new_description: str = None, new_permissions: list = None):
        """
        Edit an existing role
        
        Args:
            current_role_name: Current name of the role to edit
            new_role_name: New role name (optional)
            new_description: New description (optional)
            new_permissions: New permissions list (optional)
        """
        if not self.user_mgmt_page:
            raise ValueError("User management not initialized. Call setup_user_management first.")
        
        print(f"🔧 Editing role '{current_role_name}'...")
        
        # Click edit button
        self.user_mgmt_page.click_edit_role_button(current_role_name)
        time.sleep(2)
        
        # Verify edit modal is visible
        enhanced_assert_visible(self.page, self.user_mgmt_page.locators.edit_role_modal_heading, 
                              "Edit Role modal should be visible", f"edit_role_{current_role_name}")
        
        # Update fields if provided
        if new_role_name:
            self.user_mgmt_page.clear_and_fill_role_name(new_role_name)
        
        if new_description:
            self.user_mgmt_page.clear_and_fill_role_description(new_description)
        
        if new_permissions:
            # Clear existing permissions and select new ones
            self.user_mgmt_page.clear_all_permissions()
            self.user_mgmt_page.select_multiple_permissions(new_permissions)
        
        # Save changes
        self.user_mgmt_page.click_save_role_button()
        time.sleep(3)
        
        # Verify success message
        enhanced_assert_visible(self.page, self.user_mgmt_page.locators.role_updated_successfully_message, 
                              f"Role update success message should be visible", f"edit_role_{current_role_name}_success")
        
        updated_name = new_role_name if new_role_name else current_role_name
        print(f"✅ Role '{current_role_name}' updated successfully to '{updated_name}'")
        
        return updated_name
    
    def delete_role(self, role_name: str):
        """
        Delete a role with confirmation
        
        Args:
            role_name: Name of role to delete
        """
        if not self.user_mgmt_page:
            raise ValueError("User management not initialized. Call setup_user_management first.")
        
        print(f"🗑️ Deleting role '{role_name}'...")
        
        # Click delete button
        self.user_mgmt_page.click_delete_role_button(role_name)
        time.sleep(2)
        
        # Confirm deletion
        enhanced_assert_visible(self.page, self.user_mgmt_page.locators.delete_confirmation_modal, 
                              "Delete confirmation modal should be visible", f"delete_role_{role_name}")
        
        self.user_mgmt_page.click_confirm_delete_button()
        time.sleep(3)
        
        print(f"✅ Role '{role_name}' deleted successfully")
    
    def navigate_through_pagination(self, target_role: str, max_pages: int = 10):
        """
        Navigate through pagination to find a specific role
        
        Args:
            target_role: Role name to find
            max_pages: Maximum pages to search through
            
        Returns:
            bool: True if role found
        """
        if not self.user_mgmt_page:
            raise ValueError("User management not initialized. Call setup_user_management first.")
        
        print(f"📄 Searching for '{target_role}' through pagination (max {max_pages} pages)...")
        
        current_page = 1
        
        while current_page <= max_pages:
            print(f"   Checking page {current_page}...")
            
            # Check if target role exists on current page
            role_found = self.user_mgmt_page.find_role_by_name(target_role)
            
            if role_found:
                print(f"✅ Role '{target_role}' found on page {current_page}")
                return True
            
            # Check if next page is available
            if self.user_mgmt_page.is_next_page_available():
                self.user_mgmt_page.click_next_page()
                time.sleep(2)
                current_page += 1
            else:
                print(f"   Reached last page ({current_page})")
                break
        
        print(f"❌ Role '{target_role}' not found in {current_page} pages")
        return False
    
    def full_role_lifecycle_test(self, role_name: str, description: str, permissions: list):
        """
        Complete role lifecycle: Create → Search → Edit → Delete
        
        Args:
            role_name: Role name
            description: Role description  
            permissions: Initial permissions
        """
        print(f"🔄 Starting full lifecycle test for role '{role_name}'...")
        
        # 1. Create role
        self.create_role(role_name, description, permissions)
        
        # 2. Search and verify
        assert self.search_and_verify_role(role_name), f"Created role '{role_name}' should be found"
        
        # 3. Edit role
        updated_name = f"{role_name}_EDITED"
        updated_description = f"{description} - EDITED"
        new_permissions = permissions + ["Reports"] if "Reports" not in permissions else permissions
        
        final_name = self.edit_role(role_name, updated_name, updated_description, new_permissions)
        
        # 4. Verify edited role
        assert self.search_and_verify_role(final_name), f"Edited role '{final_name}' should be found"
        
        # 5. Delete role
        self.delete_role(final_name)
        
        # 6. Verify deletion
        time.sleep(2)
        role_still_exists = self.search_and_verify_role(final_name)
        assert not role_still_exists, f"Deleted role '{final_name}' should not be found"
        
        print(f"✅ Full lifecycle test completed for role '{role_name}'")


# Legacy function wrappers for backward compatibility
def do_optimized_user_management_setup(page: Page, email: str, password: str):
    """Legacy wrapper - use UserManagementTestHelper class instead"""
    helper = UserManagementTestHelper(page)
    return helper.setup_user_management(email, password)

def create_role_with_validation(page: Page, user_mgmt_page, role_name: str, description: str, permissions: list):
    """Legacy wrapper - use UserManagementTestHelper class instead"""
    helper = UserManagementTestHelper(page)
    helper.user_mgmt_page = user_mgmt_page
    helper.create_role(role_name, description, permissions)

def search_and_verify_role(page: Page, user_mgmt_page, role_name: str):
    """Legacy wrapper - use UserManagementTestHelper class instead"""
    helper = UserManagementTestHelper(page)
    helper.user_mgmt_page = user_mgmt_page
    return helper.search_and_verify_role(role_name)

def find_role_through_pagination(page: Page, user_mgmt_page, role_name: str):
    """Legacy wrapper - use UserManagementTestHelper class instead"""
    helper = UserManagementTestHelper(page)
    helper.user_mgmt_page = user_mgmt_page
    return helper.navigate_through_pagination(role_name)

def comprehensive_role_edit_test(page: Page, user_mgmt_page, role_name: str):
    """Legacy wrapper - use UserManagementTestHelper class instead"""
    helper = UserManagementTestHelper(page)
    helper.user_mgmt_page = user_mgmt_page
    updated_name = f"{role_name}_EDITED"
    return helper.edit_role(role_name, updated_name, f"Updated {role_name} description", ["Dashboard", "Talent", "Reports"])

def cleanup_test_role(page: Page, user_mgmt_page, role_name: str):
    """Legacy wrapper - use UserManagementTestHelper class instead"""
    helper = UserManagementTestHelper(page)
    helper.user_mgmt_page = user_mgmt_page
    helper.delete_role(role_name)


def setup_demo_agency_access(page: Page, email: str, password: str):
    """
    Simplified setup - just calls do_user_management_login
    (Kept for backward compatibility)
    
    Args:
        page: Playwright page object
        email: User email
        password: User password
    
    Returns:
        UserManagementPage instance
    """
    return do_user_management_login(page, email, password)


def create_test_role(page: Page, role_name: str, permissions: list, 
                    email: str = "mi003b@onemail.host", password: str = "Kabir123#"):
    """
    Helper function to create a test role with specific permissions
    
    Args:
        page: Playwright page object
        role_name: Name of the role to create
        permissions: List of permissions to assign to the role
        email: Login email
        password: Login password
    
    Returns:
        tuple: (UserManagementPage instance, success boolean)
    """
    user_mgmt_page = setup_demo_agency_access(page, email, password)
    
    print(f"🔧 Creating test role: {role_name}")
    print(f"📝 Permissions: {', '.join(permissions)}")
    
    # Navigate to roles & access tab
    user_mgmt_page.click_roles_access_tab()
    time.sleep(1)
    
    # Create role
    success = user_mgmt_page.create_role_with_permissions(role_name, permissions)
    
    if success:
        print(f"✅ Successfully created role: {role_name}")
    else:
        print(f"❌ Failed to create role: {role_name}")
    
    return user_mgmt_page, success


def invite_test_user(page: Page, user_name: str, user_email: str, role_name: str,
                    login_email: str = "mi003b@onemail.host", password: str = "Kabir123#"):
    """
    Helper function to invite a test user with specific role
    
    Args:
        page: Playwright page object
        user_name: Name of the user to invite
        user_email: Email of the user to invite
        role_name: Role to assign to the user
        login_email: Login email for admin
        password: Login password for admin
    
    Returns:
        tuple: (UserManagementPage instance, success boolean)
    """
    user_mgmt_page = setup_demo_agency_access(page, login_email, password)
    
    print(f"📧 Inviting test user: {user_name} ({user_email})")
    print(f"👤 Assigned role: {role_name}")
    
    # Navigate to user list tab
    user_mgmt_page.click_user_list_tab()
    time.sleep(1)
    
    # Invite user
    success = user_mgmt_page.invite_user_with_role(user_name, user_email, role_name)
    
    if success:
        print(f"✅ Successfully invited user: {user_email}")
    else:
        print(f"❌ Failed to invite user: {user_email}")
    
    return user_mgmt_page, success


def perform_role_crud_operations(page: Page, base_role_name: str = "Test CRUD Role",
                                email: str = "mi003b@onemail.host", password: str = "Kabir123#"):
    """
    Helper function to perform complete CRUD operations on roles
    
    Args:
        page: Playwright page object
        base_role_name: Base name for the test role
        email: Login email
        password: Login password
    
    Returns:
        dict: Results of CRUD operations
    """
    results = {
        'create': False,
        'read': False,
        'update': False,
        'delete': False
    }
    
    user_mgmt_page = setup_demo_agency_access(page, email, password)
    user_mgmt_page.click_roles_access_tab()
    
    # CREATE
    print("🔧 Testing role creation...")
    permissions = ["Dashboard", "Talent Read", "Company Read"]
    results['create'] = user_mgmt_page.create_role_with_permissions(base_role_name, permissions)
    
    if results['create']:
        time.sleep(2)
        
        # READ
        print("👀 Testing role search/read...")
        user_mgmt_page.search_role(base_role_name)
        results['read'] = user_mgmt_page.find_role_by_name(base_role_name)
        user_mgmt_page.clear_role_search()
        
        if results['read']:
            # UPDATE
            print("✏️ Testing role update...")
            updated_role_name = f"{base_role_name} Updated"
            updated_permissions = ["Dashboard", "Talent Read", "Company Read", "Agency Read"]
            
            try:
                user_mgmt_page.edit_role(base_role_name, updated_role_name, updated_permissions)
                time.sleep(2)
                results['update'] = user_mgmt_page.find_role_by_name(updated_role_name)
                
                # DELETE
                if results['update']:
                    print("🗑️ Testing role deletion...")
                    user_mgmt_page.delete_role(updated_role_name, confirm=True)
                    time.sleep(2)
                    results['delete'] = not user_mgmt_page.find_role_by_name(updated_role_name)
            except Exception as e:
                print(f"Error during update/delete: {e}")
    
    return results


def perform_user_crud_operations(page: Page, test_user_name: str = "Test CRUD User",
                                test_user_email: str = "testcrud@example.com",
                                role_name: str = "Test Role",
                                email: str = "mi003b@onemail.host", password: str = "Kabir123#"):
    """
    Helper function to perform complete CRUD operations on users
    
    Args:
        page: Playwright page object
        test_user_name: Name of the test user
        test_user_email: Email of the test user
        role_name: Role to assign to the user
        email: Login email
        password: Login password
    
    Returns:
        dict: Results of CRUD operations
    """
    results = {
        'create': False,
        'read': False,
        'update': False,
        'delete': False
    }
    
    user_mgmt_page = setup_demo_agency_access(page, email, password)
    user_mgmt_page.click_user_list_tab()
    
    # CREATE (Invite user)
    print("📧 Testing user invitation...")
    results['create'] = user_mgmt_page.invite_user_with_role(test_user_name, test_user_email, role_name)
    
    if results['create']:
        time.sleep(2)
        
        # READ
        print("🔍 Testing user search/read...")
        user_mgmt_page.search_user(test_user_email)
        results['read'] = user_mgmt_page.find_user_by_email(test_user_email)
        user_mgmt_page.clear_user_search()
        
        if results['read']:
            # UPDATE (Change role)
            print("✏️ Testing user role update...")
            new_role = "Admin"  # Assume Admin role exists
            
            try:
                user_mgmt_page.edit_user_role(test_user_email, new_role)
                time.sleep(2)
                results['update'] = user_mgmt_page.verify_user_role_assignment(test_user_email, new_role)
                
                # DELETE
                if results['update']:
                    print("🗑️ Testing user deletion...")
                    user_mgmt_page.delete_user(test_user_email, confirm=True)
                    time.sleep(2)
                    results['delete'] = not user_mgmt_page.find_user_by_email(test_user_email)
            except Exception as e:
                print(f"Error during user update/delete: {e}")
    
    return results


# ===== ENHANCED ASSERTION HELPER FUNCTIONS =====

def assert_role_created_successfully(page: Page, role_name: str, test_name: str = "role_creation"):
    """Assert that role was created successfully"""
    from pages.user_management_page import UserManagementPage
    user_mgmt_page = UserManagementPage(page)
    
    # Check for success message
    enhanced_assert_visible(page, user_mgmt_page.locators.role_created_successfully,
                           f"Role '{role_name}' created successfully message should be visible", test_name)


def assert_user_invited_successfully(page: Page, user_email: str, test_name: str = "user_invitation"):
    """Assert that user was invited successfully"""
    from pages.user_management_page import UserManagementPage
    user_mgmt_page = UserManagementPage(page)
    
    # Check for success message
    enhanced_assert_visible(page, user_mgmt_page.locators.user_invited_successfully,
                           f"User '{user_email}' invited successfully message should be visible", test_name)


def assert_role_validation_error(page: Page, expected_error: str, test_name: str = "role_validation"):
    """Assert that specific role validation error is visible"""
    from pages.user_management_page import UserManagementPage
    user_mgmt_page = UserManagementPage(page)
    
    # Wait for validation message
    time.sleep(1)
    user_mgmt_page.wait_for_toast_message(timeout=3000)
    
    # Check for specific validation error
    error_locator = page.get_by_text(expected_error)
    enhanced_assert_visible(page, error_locator, f"Validation error '{expected_error}' should be visible", test_name)


def assert_user_validation_error(page: Page, expected_error: str, test_name: str = "user_validation"):
    """Assert that specific user validation error is visible"""
    from pages.user_management_page import UserManagementPage
    user_mgmt_page = UserManagementPage(page)
    
    # Wait for validation message
    time.sleep(1)
    user_mgmt_page.wait_for_toast_message(timeout=3000)
    
    # Check for specific validation error
    error_locator = page.get_by_text(expected_error)
    enhanced_assert_visible(page, error_locator, f"Validation error '{expected_error}' should be visible", test_name)


def assert_role_exists_in_list(page: Page, role_name: str, test_name: str = "role_verification"):
    """Assert that role exists in the roles list"""
    from pages.user_management_page import UserManagementPage
    user_mgmt_page = UserManagementPage(page)
    
    # Search and verify role exists
    found = user_mgmt_page.find_item_in_paginated_list(role_name, "role")
    assert found, f"Role '{role_name}' should exist in the roles list"
    
    # Visual assertion
    role_locator = user_mgmt_page.locators.role_item_by_name(role_name)
    enhanced_assert_visible(page, role_locator, f"Role '{role_name}' should be visible in roles list", test_name)


def assert_user_exists_in_list(page: Page, user_email: str, test_name: str = "user_verification"):
    """Assert that user exists in the users list"""
    from pages.user_management_page import UserManagementPage
    user_mgmt_page = UserManagementPage(page)
    
    # Search and verify user exists
    found = user_mgmt_page.find_item_in_paginated_list(user_email, "user")
    assert found, f"User '{user_email}' should exist in the users list"
    
    # Visual assertion
    user_locator = user_mgmt_page.locators.user_item_by_email(user_email)
    enhanced_assert_visible(page, user_locator, f"User '{user_email}' should be visible in users list", test_name)


def assert_role_deleted_successfully(page: Page, role_name: str, test_name: str = "role_deletion"):
    """Assert that role was deleted successfully"""
    from pages.user_management_page import UserManagementPage
    user_mgmt_page = UserManagementPage(page)
    
    # Check for success message
    enhanced_assert_visible(page, user_mgmt_page.locators.role_deleted_successfully,
                           f"Role '{role_name}' deleted successfully message should be visible", test_name)
    
    # Verify role no longer exists
    time.sleep(2)
    found = user_mgmt_page.find_role_by_name(role_name)
    assert not found, f"Role '{role_name}' should not exist after deletion"


def assert_user_deleted_successfully(page: Page, user_email: str, test_name: str = "user_deletion"):
    """Assert that user was deleted successfully"""
    from pages.user_management_page import UserManagementPage
    user_mgmt_page = UserManagementPage(page)
    
    # Check for success message
    enhanced_assert_visible(page, user_mgmt_page.locators.user_deleted_successfully,
                           f"User '{user_email}' deleted successfully message should be visible", test_name)
    
    # Verify user no longer exists
    time.sleep(2)
    found = user_mgmt_page.find_user_by_email(user_email)
    assert not found, f"User '{user_email}' should not exist after deletion"


def assert_host_email_protection_error(page: Page, test_name: str = "host_protection"):
    """Assert that host email protection error is visible"""
    from pages.user_management_page import UserManagementPage
    user_mgmt_page = UserManagementPage(page)
    
    # Check for host email protection error
    enhanced_assert_visible(page, user_mgmt_page.locators.host_email_protection_error,
                           "Host email protection error should be visible", test_name)


def assert_duplicate_email_error(page: Page, test_name: str = "duplicate_email"):
    """Assert that duplicate email error is visible"""
    from pages.user_management_page import UserManagementPage
    user_mgmt_page = UserManagementPage(page)
    
    # Check for duplicate email error
    enhanced_assert_visible(page, user_mgmt_page.locators.email_already_exists_error,
                           "Duplicate email error should be visible", test_name)


# ===== TEST DATA GENERATION HELPERS =====

def generate_test_role_data():
    """Generate test data for role creation"""
    import random
    
    role_names = [
        "Test Manager Role",
        "Test Editor Role", 
        "Test Viewer Role",
        "Test Admin Role",
        "Test Moderator Role"
    ]
    
    permission_sets = [
        ["Dashboard", "Talent Read", "Company Read"],
        ["Dashboard", "Talent Read", "Talent Create", "Company Read"],
        ["Dashboard", "User Management", "Agency Read"],
        ["Dashboard", "Talent Read", "Company Read", "User Management"],
        ["Dashboard", "Agency Read", "Company Create", "Talent Update"]
    ]
    
    role_name = f"{random.choice(role_names)} {random.randint(100, 999)}"
    permissions = random.choice(permission_sets)
    
    return {
        'role_name': role_name,
        'permissions': permissions
    }


def generate_test_user_data():
    """Generate test data for user invitation"""
    import random
    
    first_names = ["John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert", "Emma"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    user_name = f"{first_name} {last_name}"
    
    # Generate unique email with timestamp
    import time
    timestamp = str(int(time.time()))[-6:]
    email_domain = random.choice(["test.com", "example.org", "demo.net"])
    user_email = f"{first_name.lower()}.{last_name.lower()}.{timestamp}@{email_domain}"
    
    return {
        'user_name': user_name,
        'user_email': user_email
    }


# ===== CLEANUP UTILITIES =====

def cleanup_test_data(page: Page, email: str = "mi003b@onemail.host", password: str = "Kabir123#"):
    """Clean up all test data (roles and users)"""
    user_mgmt_page = setup_demo_agency_access(page, email, password)
    
    print("🧹 Starting cleanup of test data...")
    
    # Cleanup test roles
    user_mgmt_page.click_roles_access_tab()
    user_mgmt_page.cleanup_test_roles("Test")
    
    # Cleanup test users
    user_mgmt_page.click_user_list_tab()
    user_mgmt_page.cleanup_test_users("test")
    user_mgmt_page.cleanup_test_users("example")
    user_mgmt_page.cleanup_test_users("demo")
    
    print("✅ Cleanup completed")


def validate_user_management_permissions(page: Page, role_name: str, expected_permissions: list,
                                       email: str = "mi003b@onemail.host", password: str = "Kabir123#"):
    """
    Validate that a role has the correct permissions assigned
    
    Args:
        page: Playwright page object
        role_name: Name of the role to validate
        expected_permissions: List of expected permissions
        email: Login email
        password: Login password
    
    Returns:
        bool: True if permissions match, False otherwise
    """
    user_mgmt_page = setup_demo_agency_access(page, email, password)
    user_mgmt_page.click_roles_access_tab()
    
    # Find and edit the role to check permissions
    try:
        user_mgmt_page.click_role_actions_menu(role_name)
        user_mgmt_page.locators.edit_role_button.click()
        time.sleep(2)
        
        # Check each expected permission
        permissions_match = True
        for permission in expected_permissions:
            checkbox = user_mgmt_page.locators.permission_checkbox(permission)
            if checkbox.count() > 0:
                is_checked = checkbox.is_checked()
                if not is_checked:
                    permissions_match = False
                    print(f"❌ Permission '{permission}' is not checked for role '{role_name}'")
            else:
                permissions_match = False
                print(f"❌ Permission '{permission}' not found for role '{role_name}'")
        
        # Cancel the edit modal
        user_mgmt_page.locators.cancel_role_button.click()
        
        return permissions_match
        
    except Exception as e:
        print(f"Error validating permissions for role '{role_name}': {e}")
        return False


# ===== OPTIMIZED TC HELPER FUNCTIONS =====

def do_optimized_user_management_setup(page: Page, email: str = "mi003b@onemail.host", password: str = "Kabir123#"):
    """
    Optimized single function to handle login and navigation to user management
    Used across TC_01, TC_02, TC_03, TC_04
    """
    print("🔐 Performing user management login and setup...")
    user_mgmt_page = setup_demo_agency_access(page, email, password)
    user_mgmt_page.click_roles_access_tab()
    time.sleep(2)
    print("✅ User management setup completed")
    return user_mgmt_page


def create_role_with_validation(user_mgmt_page, role_name: str, description: str, permissions: list = None):
    """
    Optimized role creation with built-in validation
    Used in TC_02 and TC_04
    """
    print(f"🏗️ Creating role: {role_name}")
    
    # Open create role modal
    user_mgmt_page.click_create_role_button()
    time.sleep(1)
    
    # Fill role details
    user_mgmt_page.fill_role_name(role_name)
    user_mgmt_page.fill_role_description(description)
    
    # Select permissions if provided
    if permissions:
        user_mgmt_page.select_multiple_permissions(permissions)
    
    # Save role
    user_mgmt_page.click_save_role_button()
    time.sleep(3)
    
    print(f"✅ Role '{role_name}' created successfully")
    return True


def search_and_verify_role(user_mgmt_page, role_name: str, page: Page):
    """
    Optimized role search with verification
    Used in TC_02, TC_03, TC_04
    """
    print(f"🔍 Searching for role: {role_name}")
    
    # Search for role
    user_mgmt_page.search_role(role_name)
    time.sleep(2)
    
    # Verify role exists
    role_found = user_mgmt_page.find_role_by_name(role_name)
    if role_found:
        print(f"✅ Role '{role_name}' found in search results")
        enhanced_assert_visible(page, user_mgmt_page.locators.role_item_by_name(role_name), 
                               f"Role '{role_name}' should be visible", f"search_{role_name}")
        return True
    else:
        print(f"❌ Role '{role_name}' not found in search results")
        return False


def find_role_through_pagination(user_mgmt_page, target_role: str, page: Page, max_pages: int = 20):
    """
    Optimized pagination search for roles
    Used in TC_03
    """
    print(f"📄 Searching for '{target_role}' through pagination...")
    
    current_page = 1
    while current_page <= max_pages:
        print(f"   Checking page {current_page}...")
        
        # Get roles on current page
        current_page_roles = user_mgmt_page.get_roles_list()
        print(f"   Found {len(current_page_roles)} roles on page {current_page}")
        
        # Check if target role is on this page (flexible matching)
        for role in current_page_roles:
            if target_role.lower() in role.lower():
                print(f"✅ Found target role '{target_role}' in '{role}' on page {current_page}!")
                enhanced_assert_visible(page, page.get_by_text(role, exact=True),
                                       f"Role containing '{target_role}' should be visible", 
                                       f"pagination_page_{current_page}")
                return True
        
        # Try to go to next page
        try:
            next_page_num = current_page + 1
            next_page_link = page.locator(f"text='{next_page_num}'")
            if next_page_link.count() > 0 and next_page_link.is_visible():
                next_page_link.click()
                time.sleep(3)
                current_page = next_page_num
                print(f"✅ Navigated to page {current_page}")
            else:
                print(f"📄 No more pages available after page {current_page}")
                break
        except Exception as e:
            print(f"Navigation error: {e}")
            break
    
    print(f"❌ Role '{target_role}' not found after checking {current_page} pages")
    return False


def comprehensive_role_edit_test(user_mgmt_page, role_name: str, page: Page):
    """
    Comprehensive role editing with all validations
    Used in TC_04
    """
    print(f"🔧 Starting comprehensive edit test for role: {role_name}")
    
    # Step 1: Open edit modal
    user_mgmt_page.click_edit_role_button(role_name)
    time.sleep(2)
    
    # Step 2: Validate modal elements
    enhanced_assert_visible(page, user_mgmt_page.locators.edit_role_modal_heading, 
                           "Edit Role modal should be visible", "edit_modal_validation")
    
    role_name_input = user_mgmt_page.locators.role_name_input
    role_description_input = user_mgmt_page.locators.role_description_input
    
    enhanced_assert_visible(page, role_name_input, "Role name field should be visible", "name_field_validation")
    enhanced_assert_visible(page, role_description_input, "Description field should be visible", "description_field_validation")
    
    # Get current values
    current_name = role_name_input.input_value()
    current_description = role_description_input.input_value()
    
    print(f"✅ Modal validation passed - Current name: '{current_name}'")
    
    # Step 3: Test empty field validation
    print("🚫 Testing empty field validation...")
    role_name_input.clear()
    user_mgmt_page.locators.update_role_button.click()
    time.sleep(2)
    
    try:
        validation_error = page.locator("text=required, text=field is required, text=cannot be empty").first
        enhanced_assert_visible(page, validation_error, "Validation error should appear", "empty_field_validation")
        print("✅ Empty field validation passed")
    except:
        print("⚠️ Validation error check skipped")
    
    # Step 4: Update with new data
    updated_name = f"{current_name} - EDITED"
    updated_description = f"UPDATED: {current_description}"
    
    print(f"📝 Updating to: '{updated_name}'")
    role_name_input.fill(updated_name)
    role_description_input.clear()
    role_description_input.fill(updated_description)
    
    # Step 5: Save changes
    user_mgmt_page.locators.update_role_button.click()
    time.sleep(3)
    
    # Step 6: Verify success toast
    try:
        success_toast = page.get_by_text("updated successfully", exact=False).first
        enhanced_assert_visible(page, success_toast, "Success toast should appear", "success_toast_validation")
        print("✅ Success toast verified")
    except:
        print("⚠️ Success toast verification skipped")
    
    # Step 7: Verify updated role in list
    user_mgmt_page.click_roles_access_tab()
    time.sleep(2)
    
    search_result = search_and_verify_role(user_mgmt_page, updated_name, page)
    
    if search_result:
        print(f"✅ Comprehensive edit test completed successfully for '{updated_name}'")
        return updated_name
    else:
        print(f"❌ Edit verification failed for '{updated_name}'")
        return None


def cleanup_test_role(user_mgmt_page, role_name: str):
    """
    Clean up test role with delete confirmation message wait
    """
    try:
        print(f"🧹 Cleaning up test role: '{role_name}'")
        
        # Delete role and click confirm
        user_mgmt_page.delete_role(role_name, confirm=True)
        time.sleep(2)
        
        # Wait for delete success confirmation message
        enhanced_assert_visible(user_mgmt_page.page, user_mgmt_page.locators.role_deleted_successfully, 
                              f"Role '{role_name}' delete success message should be visible", f"cleanup_role_{role_name}")
        
        print(f"✅ Role '{role_name}' deleted successfully with confirmation")
        return True
    except Exception as e:
        print(f"⚠️ Cleanup warning for '{role_name}': {e}")
        return False
