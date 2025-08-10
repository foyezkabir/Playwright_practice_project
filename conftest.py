import pytest
from playwright.sync_api import sync_playwright, Page
from utils.config import BROWSER_NAME, HEADLESS, DEFAULT_TIMEOUT, SLOW_MO, SCREENSHOT_DELAY
from utils.screenshot_helper import capture_failure_screenshot

# BROWSER AND PAGE FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def browser():
    """Session-scoped browser fixture with configuration from config.py"""
    with sync_playwright() as p:
        if BROWSER_NAME == "chromium":
            browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        elif BROWSER_NAME == "firefox":
            browser = p.firefox.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        elif BROWSER_NAME == "webkit":
            browser = p.webkit.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        else:
            browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
            
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    """Page fixture with configured timeout"""
    page = browser.new_page()
    page.set_default_timeout(DEFAULT_TIMEOUT)
    yield page
    page.close()

@pytest.fixture
def context(browser):
    """Browser context fixture for tests requiring context"""
    context = browser.new_context()
    yield context
    context.close()

# SCREENSHOT HOOKS AND FIXTURES
# ============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook to capture test execution results."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(autouse=True)
def auto_screenshot_on_failure(request, page: Page):
    """Automatic screenshot capture fixture for failed tests."""
    yield
    
    # Check if test failed
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        test_name = request.node.name
        test_file = request.node.fspath.strpath
        capture_failure_screenshot(page, test_name, test_file)

@pytest.fixture
def screenshot_on_failure(request, page: Page):
    """Manual screenshot fixture for tests marked with @pytest.mark.screenshot"""
    def _capture_screenshot():
        test_name = request.node.name
        test_file = request.node.fspath.strpath
        capture_failure_screenshot(page, test_name, test_file)
    
    yield _capture_screenshot
    
    # Auto-capture on failure if marked with @pytest.mark.screenshot
    if request.node.get_closest_marker("screenshot"):
        if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            test_name = request.node.name
            test_file = request.node.fspath.strpath
            capture_failure_screenshot(page, test_name, test_file)