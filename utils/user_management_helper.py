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
    Helper function to login and navigate to user management page
    
    Args:
        page: Playwright page object
        email: User email
        password: User password
    
    Returns:
        UserManagementPage instance
    """
    from pages.user_management_page import UserManagementPage
    
    # Login first
    do_login(page, email, password)
    time.sleep(2)
    
    # Navigate to user management
    user_mgmt_page = UserManagementPage(page)
    user_mgmt_page.navigate_to_user_management()
    
    return user_mgmt_page


def setup_demo_agency_access(page: Page, email: str = "mi003b@onemail.host", password: str = "Kabir123#", 
                           agency_name: str = "demo 06"):
    """
    Helper function to login and access specific demo agency for user management testing
    
    Args:
        page: Playwright page object
        email: User email (default: demo account)
        password: User password
        agency_name: Name of the demo agency to access
    
    Returns:
        UserManagementPage instance
    """
    from pages.user_management_page import UserManagementPage
    
    # Login and navigate
    user_mgmt_page = do_user_management_login(page, email, password)
    
    # Select demo agency
    user_mgmt_page.select_demo_agency(agency_name)
    
    return user_mgmt_page


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
