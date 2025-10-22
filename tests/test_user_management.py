import pytest
import time
import random
from playwright.sync_api import Page
from utils.user_management_helper import do_user_management_login
from utils.enhanced_assertions import enhanced_assert_visible
from random_values_generator.random_role_name import generate_role_name


@pytest.fixture(scope="module")
def test_role_name():
    return f"Test Role {generate_role_name()}"


@pytest.fixture(scope="module")
def admin_credentials():
    return {"email": "mi003b@onemail.host", "password": "Kabir123#"}


def test_TC_01(page: Page, admin_credentials):
    """Verify successful navigation to user management."""
    user_mgmt_page = do_user_management_login(page, admin_credentials["email"], admin_credentials["password"])
    enhanced_assert_visible(page, user_mgmt_page.locators.roles_access_tab, "Roles & Access tab visible", "test_TC_01")
    enhanced_assert_visible(page, user_mgmt_page.locators.user_list_tab, "User List tab visible", "test_TC_01")


def test_TC_02(page: Page, admin_credentials, test_role_name):
    """Verify role creation and search."""
    user_mgmt_page = do_user_management_login(page, admin_credentials["email"], admin_credentials["password"])
    
    # Create role
    user_mgmt_page.click_create_role_button()
    time.sleep(1)
    user_mgmt_page.fill_role_name(test_role_name)
    user_mgmt_page.fill_role_description(f"Test: {test_role_name}")
    user_mgmt_page.click_save_role_button()
    time.sleep(3)
    
    # Refresh roles list to see the newly created role
    user_mgmt_page.click_roles_access_tab()
    time.sleep(2)
    
    # Search for the created role
    user_mgmt_page.search_role(test_role_name)
    time.sleep(2)
    
    # Verify exact role name exists
    found = user_mgmt_page.find_role_by_name(test_role_name)
    assert found, f"Role '{test_role_name}' not found in search results"
    enhanced_assert_visible(page, page.get_by_text(test_role_name, exact=True).first, f"Role '{test_role_name}' visible", "test_TC_02")


def test_TC_03(page: Page, admin_credentials):
    """Verify finding role through pagination."""
    user_mgmt_page = do_user_management_login(page, admin_credentials["email"], admin_credentials["password"])
    target_role = "Test Supervisor"
    
    print(f"🔍 Starting search for role: '{target_role}'")
    found = False
    max_pages = 100  # Search up to 100 pages
    current_page = 0
    
    while current_page < max_pages:
        current_page += 1
        print(f"🔍 Searching page {current_page}...")
        time.sleep(1)
        
        # Check if role exists on current page
        if user_mgmt_page.find_role_by_name(target_role):
            print(f"✅ Found '{target_role}' on page {current_page}")
            found = True
            break
        
        print(f"   Not found on page {current_page}, trying next page...")
        
        # Try to click next button
        next_button = page.locator("ul.pagination-container > li:last-child:not(.disabled)")
        if next_button.count() > 0:
            print(f"   -> Clicking next button...")
            next_button.click()
            print(f"   -> Waiting 2 seconds for page to load...")
            time.sleep(2)
        else:
            print(f"❌ No more pages available. '{target_role}' not found after {current_page} pages.")
            break
    
    assert found, f"Role '{target_role}' not found through pagination"
    enhanced_assert_visible(page, page.get_by_text(target_role, exact=True).first, f"Role '{target_role}' visible", "test_TC_03")


def test_TC_04(page: Page, admin_credentials):
    """Verify role edit with validation."""
    user_mgmt_page = do_user_management_login(page, admin_credentials["email"], admin_credentials["password"])
    
    # Create test role
    original = f"TC04 Edit {random.randint(10000, 99999)}"
    user_mgmt_page.click_create_role_button()
    time.sleep(1)
    user_mgmt_page.fill_role_name(original)
    user_mgmt_page.fill_role_description(f"Desc: {original}")
    user_mgmt_page.click_save_role_button()
    time.sleep(3)
    
    # Search and edit
    user_mgmt_page.search_role(original)
    time.sleep(2)
    user_mgmt_page.click_edit_role_button(original)
    time.sleep(2)
    
    # Validate modal
    enhanced_assert_visible(page, user_mgmt_page.locators.edit_role_modal_heading, "Edit modal visible", "test_TC_04")
    
    # Test validation
    user_mgmt_page.locators.role_name_input.clear()
    user_mgmt_page.locators.update_role_button.click()
    time.sleep(2)
    enhanced_assert_visible(page, user_mgmt_page.locators.role_name_required_error, "Validation error visible", "test_TC_04")
    
    # Update role
    updated = f"{original} - EDITED"
    user_mgmt_page.locators.role_name_input.fill(updated)
    time.sleep(1)
    user_mgmt_page.locators.update_role_button.click()
    time.sleep(3)
    
    # Verify update
    user_mgmt_page.click_roles_access_tab()
    time.sleep(2)
    user_mgmt_page.search_role(updated)
    time.sleep(2)
    assert user_mgmt_page.find_role_by_name(updated), f"Updated role {updated} not found"
    
    # Cleanup
    user_mgmt_page.delete_role(updated, confirm=True)
    time.sleep(2)
