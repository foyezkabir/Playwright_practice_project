# Client Test Helper - Login Decorator Guide

## Overview
The `client_helper.py` module provides decorators and helper functions to eliminate repetitive login code in client module tests.

## Available Tools

### 1. `@with_client_login()` Decorator (Recommended)

**Purpose:** Automatically handles login and navigation, making tests cleaner and more focused.

**Default Behavior:**
- Email: `mi003b@onemail.host`
- Password: `Kabir123#`
- Agency ID: `173`
- Auto-navigates to client page: `True`

#### Basic Usage (Most Common)

```python
from utils.client_helper import with_client_login

@with_client_login()
def test_TC_01(page: Page):
    """Already logged in and on client page."""
    client_page = page._client_page  # Access the ClientPage instance
    client_page.expect_client_page_heading()
    client_page.click_add_client_button()
```

**Before (Old Way):**
```python
def test_TC_01(page: Page):
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.expect_client_page_heading()
```

**After (With Decorator):**
```python
@with_client_login()
def test_TC_01(page: Page):
    client_page = page._client_page
    client_page.expect_client_page_heading()
```

**Benefits:**
- ✅ Reduces 3 lines of boilerplate to 1 decorator + 1 line to get client_page
- ✅ Parameter stays as `page: Page` (pytest fixture compatible)
- ✅ Access ClientPage via `page._client_page`
- ✅ More readable and maintainable
- ✅ Consistent login handling across tests

#### Advanced Usage

**Different Agency ID:**
```python
@with_client_login(agency_id="174")
def test_TC_07(page: Page):
    """Test with agency ID 174."""
    client_page = page._client_page
    client_page.create_client_with_all_fields(...)
```

**Login Without Auto-Navigation:**
```python
@with_client_login(navigate_to_client_page=False)
def test_custom(page: Page):
    """Need to manually navigate for specific test flow."""
    client_page = page._client_page
    # Already logged in to agency dashboard
    # Custom navigation logic here
    client_page.navigate_to_client_page()
```

**Different User:**
```python
@with_client_login(email="other@email.com", password="Pass123#")
def test_different_user(page: Page):
    """Test with different user credentials."""
    client_page = page._client_page
    client_page.expect_client_page_heading()
```

### 2. Helper Functions (Alternative Approach)

If you prefer not to use decorators, use these helper functions:

#### `do_client_login_and_navigate()`
```python
from utils.client_helper import do_client_login_and_navigate

def test_TC_01(page: Page):
    client_page = do_client_login_and_navigate(page)
    # Already on client page
    client_page.expect_client_page_heading()
```

#### `do_client_login()`
```python
from utils.client_helper import do_client_login

def test_TC_01(page: Page):
    client_page = do_client_login(page)
    # On agency dashboard, need to navigate
    client_page.navigate_to_client_page()
    client_page.expect_client_page_heading()
```

#### With Custom Parameters:
```python
def test_TC_07(page: Page):
    client_page = do_client_login_and_navigate(page, agency_id="174")
    client_page.create_client_with_all_fields(...)
```

## Migration Examples

### Example 1: Simple Test
**Before:**
```python
def test_TC_02(page: Page):
    """Verify 'No clients found' message."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.expect_no_clients_found_message()
    client_page.expect_add_client_button()
```

**After:**
```python
@with_client_login()
def test_TC_02(page: Page):
    """Verify 'No clients found' message."""
    client_page = page._client_page
    client_page.expect_no_clients_found_message()
    client_page.expect_add_client_button()
```

### Example 2: Different Agency
**Before:**
```python
def test_TC_07(page: Page):
    """Create client with all fields."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "174")
    client_page.navigate_to_client_page()
    email = random_email.generate_email()
    client_page.create_client_with_all_fields(...)
```

**After:**
```python
@with_client_login(agency_id="174")
def test_TC_07(page: Page):
    """Create client with all fields."""
    client_page = page._client_page
    email = random_email.generate_email()
    client_page.create_client_with_all_fields(...)
```

### Example 3: Modal Opening
**Before:**
```python
def test_TC_03(page: Page):
    """Verify modal fields."""
    client_page = ClientPage(page)
    client_page.login_and_navigate_to_agency_dashboard("mi003b@onemail.host", "Kabir123#", "173")
    client_page.navigate_to_client_page()
    client_page.click_add_client_button()
    client_page.expect_add_new_client_modal_heading()
```

**After:**
```python
@with_client_login()
def test_TC_03(page: Page):
    """Verify modal fields."""
    client_page = page._client_page
    client_page.click_add_client_button()
    client_page.expect_add_new_client_modal_heading()
```

## Best Practices

1. **Use the decorator for most tests** - It's cleaner and more maintainable
2. **Keep parameter as `page: Page`** when using decorator (pytest fixture compatibility)
3. **Access ClientPage via `page._client_page`** in the test body
4. **Specify `agency_id` when different from default 173**
5. **Use helper functions when you need more control** over the login flow
6. **Keep credentials in constants** in `client_helper.py` for easy updates

## Summary

| Approach | Use When | Lines of Code |
|----------|----------|---------------|
| `@with_client_login()` | Standard tests (default agency 173) | 2 lines (decorator + get client_page) |
| `@with_client_login(agency_id="174")` | Different agency needed | 2 lines (decorator + get client_page) |
| `do_client_login_and_navigate()` | Prefer functions over decorators | 1 line |
| `do_client_login()` | Need custom navigation logic | 2 lines |
| Original way | Not recommended | 3 lines |

## Impact
- **Before:** 21+ tests × 3 lines = 63+ lines of repetitive code
- **After:** 21+ tests × 2 lines (decorator + get client_page) = **42 lines total (21 lines saved!)**
- **Maintenance:** Update credentials in one place instead of 21+ places
- **Consistency:** All tests use the same login pattern
