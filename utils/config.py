BASE_URL = "https://bprp-qa.shadhinlab.xyz"
BROWSER_NAME = "chromium"  # chromium, firefox, webkit
HEADLESS = False
DEFAULT_TIMEOUT = 15000  # in milliseconds

# Screenshot configuration
SCREENSHOT_ON_FAILURE = True
SCREENSHOT_DELAY = 1  # Wait 1ms before taking screenshot
FULL_PAGE_SCREENSHOT = True

# Toast/Error message timing
TOAST_WAIT_TIME = 1500  # Wait 3 seconds for toasts to appear
TOAST_TIMEOUT = 5000   # Wait up to 10 seconds for toast visibility
ERROR_MESSAGE_WAIT = 2000  # Wait 2 seconds for error messages

# Screenshot naming configuration
SCREENSHOT_DATE_FORMAT = "%d-%m-%Y"
SCREENSHOT_TIME_FORMAT = "%H.%M.%S"  # Fixed Windows compatibility
INCLUDE_TEST_FILE_PREFIX = False  # Don't include "reset_pass" etc.
INCLUDE_VERIFY_WORD = False       # Don't include "verify"

# Screenshot directories
SCREENSHOT_BASE_DIR = "screenshots"
FAILURE_SCREENSHOT_DIR = "failures"

# Network and loading configuration
NETWORK_IDLE_TIMEOUT = 5000  # Wait for network idle
PAGE_LOAD_STRATEGY = "networkidle"  # or "domcontentloaded" or "load"
SLOW_MO = 1000  # Slow down operations by 1000ms