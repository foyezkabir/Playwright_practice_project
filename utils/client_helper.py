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
