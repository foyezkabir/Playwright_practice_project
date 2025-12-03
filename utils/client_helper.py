"""
Client Helper Functions
Contains helper functions and decorators for client module tests
"""
import functools
from playwright.sync_api import Page
from pages.client_page import ClientPage


# Default login credentials for client tests
DEFAULT_EMAIL = "mi003b@onemail.host"
DEFAULT_PASSWORD = "Kabir123#"
DEFAULT_AGENCY_ID = "173"


def with_client_login(email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD, agency_id=DEFAULT_AGENCY_ID, navigate_to_client_page=True):
    """
    Decorator that automatically handles login and navigation to client page for test functions.
    
    Args:
        email (str): Email for login (default: mi003b@onemail.host)
        password (str): Password for login (default: Kabir123#)
        agency_id (str): Agency ID to navigate to (default: 173)
        navigate_to_client_page (bool): Whether to navigate to client page after login (default: True)
    
    Usage:
        @with_client_login()
        def test_TC_01(page: Page):
            # Test code here - page is automatically logged in and on client page
            # Access ClientPage through page._client_page if needed
            pass
        
        # With custom agency_id
        @with_client_login(agency_id="174")
        def test_TC_02(page: Page):
            # Test code here
            pass
        
        # Without auto-navigation to client page
        @with_client_login(navigate_to_client_page=False)
        def test_TC_03(page: Page):
            # Test code here - logged in but not on client page yet
            pass
    """
    def decorator(test_func):
        @functools.wraps(test_func)
        def wrapper(page: Page, *args, **kwargs):
            # Initialize ClientPage
            client_page = ClientPage(page)
            
            # Perform login and navigation
            client_page.login_and_navigate_to_agency_dashboard(email, password, agency_id)
            
            # Navigate to client page if requested
            if navigate_to_client_page:
                client_page.navigate_to_client_page()
            
            # Store client_page instance in page object for access in test
            page._client_page = client_page
            
            # Call the test function with page (which now has _client_page attached)
            return test_func(page, *args, **kwargs)
        
        return wrapper
    return decorator


def do_client_login(page: Page, email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD, agency_id=DEFAULT_AGENCY_ID):
    """
    Helper function to perform client login and navigation.
    Returns ClientPage instance.
    
    Args:
        page (Page): Playwright Page object
        email (str): Email for login
        password (str): Password for login
        agency_id (str): Agency ID to navigate to
    
    Returns:
        ClientPage: Initialized and logged-in ClientPage instance
    
    Usage:
        def test_example(page: Page):
            client_page = do_client_login(page)
            client_page.navigate_to_client_page()
            # Test code here
    """
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard(email, password, agency_id)
    return client_page


def do_client_login_and_navigate(page: Page, email=DEFAULT_EMAIL, password=DEFAULT_PASSWORD, agency_id=DEFAULT_AGENCY_ID):
    """
    Helper function to perform client login, navigate to agency dashboard, and then to client page.
    Returns ClientPage instance.
    
    Args:
        page (Page): Playwright Page object
        email (str): Email for login
        password (str): Password for login
        agency_id (str): Agency ID to navigate to
    
    Returns:
        ClientPage: Initialized ClientPage instance on client page
    
    Usage:
        def test_example(page: Page):
            client_page = do_client_login_and_navigate(page)
            # Already on client page - test code here
            client_page.expect_client_page_heading()
    """
    client_page = do_client_login(page, email, password, agency_id)
    client_page.navigate_to_client_page()
    return client_page


def verify_bulk_actions(page: Page, client_page):
    """
    Verify bulk action functionality after clicking bulk select checkbox.
    Tests Delete and Add Notes buttons, their modals, and navigation display.
    
    Args:
        page: Playwright Page object
        client_page: ClientPage instance
    
    Usage:
        def test_TC_22(page: Page):
            client_page: ClientPage = page._client_page
            client_page.click_bulk_select_checkbox()
            time.sleep(1)
            verify_bulk_actions(page, client_page)
    """
    import re
    import time
    from utils.enhanced_assertions import enhanced_assert_visible
    
    # Dynamically detect the count from the Delete button text
    # The button format is "Delete (X)" where X is the count
    delete_button = page.get_by_role("button", name=re.compile(r"Delete \(\d+\)"))
    delete_button.wait_for(state="visible", timeout=5000)
    button_text = delete_button.inner_text()
    # Extract count from "Delete (3)" format
    count = int(button_text.split("(")[1].split(")")[0])
    print(f"ℹ️ Detected {count} clients selected for bulk actions")
    
    # Assert Delete and Add Notes buttons with correct count are visible
    enhanced_assert_visible(page, client_page.locators.bulk_delete_button(count), f"Bulk Delete button ({count}) should be visible", "test_TC_22_bulk_delete_visible")
    enhanced_assert_visible(page, client_page.locators.bulk_add_notes_button(count), f"Bulk Add Notes button ({count}) should be visible", "test_TC_22_bulk_add_notes_visible")
    
    # Click Delete and assert modal opens
    client_page.click_bulk_delete_button(count)
    enhanced_assert_visible(page, client_page.locators.bulk_delete_modal_text, "Bulk Delete modal text should be visible", "test_TC_22_bulk_delete_modal_text")
    enhanced_assert_visible(page, client_page.locators.bulk_delete_modal_cancel, "Bulk Delete Cancel button should be visible", "test_TC_22_bulk_delete_cancel")
    enhanced_assert_visible(page, client_page.locators.bulk_delete_modal_confirm, "Bulk Delete Confirm button should be visible", "test_TC_22_bulk_delete_confirm")
    client_page.click_bulk_delete_modal_cancel()
    time.sleep(1)
    
    # Click Add Notes and assert modal opens
    client_page.click_bulk_add_notes_button(count)
    enhanced_assert_visible(page, client_page.locators.bulk_add_notes_modal_heading(count), f"Bulk Add Notes modal heading ({count}) should be visible", "test_TC_22_bulk_add_notes_modal_heading")
    enhanced_assert_visible(page, client_page.locators.bulk_add_notes_modal_cancel, "Bulk Add Notes Cancel button should be visible", "test_TC_22_bulk_add_notes_cancel")
    enhanced_assert_visible(page, client_page.locators.bulk_add_notes_modal_save_next, "Bulk Add Notes Save & Next button should be visible", "test_TC_22_bulk_add_notes_save_next")
    
    # Verify note navigation display is visible (showing "1 of 10" format)
    enhanced_assert_visible(page, client_page.locators.note_nav(1, count), f"Note navigation display (1 of {count}) should be visible", "test_TC_22_note_nav_display")
    client_page.click_bulk_add_notes_modal_cancel()
    time.sleep(1)


def verify_pagination_navigation(page: Page, client_page, total_pages: int):
    """
    Verify pagination navigation based on total page count.
    
    Args:
        page (Page): Playwright page object
        client_page: ClientPage instance
        total_pages (int): Total number of pages
    """
    import time
    
    # If only one page exists, verify buttons are disabled
    if total_pages == 1:
        print(f"ℹ️ Only 1 page exists - verifying buttons are disabled")
        client_page.expect_previous_page_button_disabled()
        client_page.expect_next_page_button_disabled()
    else:
        # Multiple pages exist - test navigation
        print(f"ℹ️ Multiple pages exist ({total_pages}) - testing navigation")
        
        # Verify previous button is disabled on first page
        client_page.expect_previous_page_button_disabled()
        
        # Click next page button to go to next page
        client_page.click_next_page()
        time.sleep(2)
        
        # Get current page number after navigation
        current_page = client_page.get_current_page_number()
        
        # Verify now on next page
        client_page.expect_page_number(current_page)
        time.sleep(2)
        
        # If on last page, verify forward button is disabled
        if current_page == total_pages:
            client_page.expect_next_page_button_disabled()
        
        # Click previous page button to go back
        client_page.click_previous_page()
        time.sleep(2)
        
        # Verify back on previous page
        client_page.expect_page_number(current_page - 1)


def select_random_clients_from_first_four(page: Page, count: int = 2):
    """
    Randomly select specified number of clients from the first 4 in the list.
    
    Args:
        page (Page): Playwright page object
        count (int): Number of clients to select (default: 2)
    
    Returns:
        list: List of selected indices
    """
    import random
    import time
    
    all_labels = page.locator("label[for^='select-']").all()
    
    if len(all_labels) >= 4:
        selected_indices = random.sample(range(4), count)
        selected_indices.sort()
        
        for idx in selected_indices:
            all_labels[idx].click()
            time.sleep(0.5)
        
        time.sleep(1)
        print(f"✅ Selected {count} random clients at indices: {selected_indices}")
        return selected_indices
    else:
        print(f"⚠️ Not enough clients to select {count} from first 4")
        return []


def wait_for_modal_backdrop_hidden(page: Page, timeout: int = 5000):
    """Wait for any modal backdrop to disappear."""
    import time
    time.sleep(1)
    try:
        page.wait_for_selector(".modal-backdrop", state="hidden", timeout=timeout)
    except:
        pass  # Backdrop might not exist


def wait_for_bulk_delete_success(page: Page, timeout: int = 10000):
    """Wait for bulk delete success toast message to appear."""
    success_message = page.get_by_text("Clients deleted successfully")
    success_message.wait_for(state="visible", timeout=timeout)
    return success_message


def select_remaining_clients_from_first_four(page: Page, already_selected_indices: list):
    """
    Select remaining clients from first 4 that weren't already selected.
    
    Args:
        page (Page): Playwright page object
        already_selected_indices (list): List of indices already selected
    """
    import time
    
    all_labels = page.locator("label[for^='select-']").all()
    remaining_indices = [i for i in range(4) if i not in already_selected_indices]
    
    for idx in remaining_indices:
        all_labels[idx].click()
        time.sleep(0.5)
    
    time.sleep(1)
    print(f"✅ Selected remaining clients at indices: {remaining_indices}")
