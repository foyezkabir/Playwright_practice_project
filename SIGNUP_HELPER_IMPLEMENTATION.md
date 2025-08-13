# Signup Helper Function - do_signup()

## Overview
Created a new `do_signup()` helper function in `utils/signup_helper.py` similar to the existing `do_login()` helper in `utils/login_helper.py`. This function simplifies signup test cases by providing a single function to fill form fields and submit.

## Function Signature

```python
def do_signup(page: Page, full_name: str = None, email: str = None, password: str = None, confirm_password: str = None):
    """
    Helper function to fill signup form with specified data and click signup button
    Similar to do_login helper for login tests
    
    Args:
        page: Playwright page object
        full_name: Full name to fill (optional)
        email: Email to fill (optional) 
        password: Password to fill (optional)
        confirm_password: Confirm password to fill (optional)
    
    Returns:
        SignupPage instance
    """
```

## Usage Examples

### Basic Field Validation Tests
```python
def test_TC_03(page: Page):
    """Verify full name required error."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_full_name_required_error()

def test_TC_04(page: Page):
    """Verify email required error."""
    signup_page = do_signup(page, full_name="John Doe", email="", password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_email_required_error()
```

### Successful Signup Tests
```python
def test_TC_12(page: Page):
    """Verify successful signup message."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="John Doe", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_signup_success_message()
```

### Validation Error Tests
```python
def test_TC_13(page: Page):
    """Verify full name minimum character limit."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="Jo", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_full_name_min_limit()
```

## Before vs After Comparison

### Before (Verbose)
```python
def test_TC_03(navigate_to_signup):
    """Verify full name required error."""
    signup_page = navigate_to_signup
    email = random_email.generate_email()
    
    signup_page.fill_email(email)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    signup_page.click_sign_up_button()
    signup_page.expect_full_name_required_error()
```

### After (Concise)
```python
def test_TC_03(page: Page):
    """Verify full name required error."""
    email = random_email.generate_email()
    signup_page = do_signup(page, full_name="", email=email, password="Kabir123#", confirm_password="Kabir123#")
    signup_page.expect_full_name_required_error()
```

## Benefits

1. **Consistency**: Similar to `do_login()` helper pattern
2. **Conciseness**: Reduces test code from 8+ lines to 3 lines
3. **Clarity**: Clear function signature with optional parameters
4. **Maintainability**: Changes to signup flow only need updates in one place
5. **Flexibility**: Can skip any field by not providing it (useful for error testing)

## Test Cases Updated

The following test cases now use the `do_signup()` helper:
- **Form validation tests**: TC_03 through TC_17 (15 tests)
- **Verification page tests**: TC_26 through TC_34 (9 tests)
- **Total**: 24 out of 34 tests now use the helper

## Test Cases Not Using Helper

The following test cases use different approaches:
- **TC_01**: Uses `navigate_to_landing_and_signup()` for heading test
- **TC_02**: Uses `fill_valid_signup_form()` for comprehensive signup flow
- **TC_18-TC_25**: Simple visibility tests that only check page elements

## Code Reduction

- **Before**: ~200 lines of test code
- **After**: ~140 lines of test code  
- **Reduction**: ~30% less code while maintaining the same functionality

## Maintained Functionality

✅ All 34 test cases preserved  
✅ Exact same test behavior  
✅ Excel report generation works correctly  
✅ Test naming convention maintained (`test_TC_XX`)  
✅ All error validations intact  

The `do_signup()` helper makes the signup tests much more readable and maintainable while following the same pattern as the login helper function.
