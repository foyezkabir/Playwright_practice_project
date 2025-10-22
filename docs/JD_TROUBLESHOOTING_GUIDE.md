# JD Automation Troubleshooting Guide

This guide helps resolve common issues encountered during JD (Job Description) automation testing.

## Common Test Failures and Solutions

### 1. JD Modal Issues

#### Problem: JD Creation Modal Not Opening
**Symptoms:**
- "Add JD" button click doesn't open modal
- Modal heading not visible
- Timeout waiting for modal

**Solutions:**
```python
# Check if button is visible and enabled
enhanced_assert_visible(page, jd_page.locators.add_jd_button, 
                       "Add JD button should be visible", "add_jd_button_check")

# Verify page is fully loaded
page.wait_for_load_state("networkidle")
time.sleep(2)

# Try alternative click method
jd_page.locators.add_jd_button.click(force=True)
```

#### Problem: Modal Closes Unexpectedly
**Symptoms:**
- Modal closes during form filling
- Form data is lost
- Validation errors not visible

**Solutions:**
- Ensure modal remains open during validation
- Check for JavaScript errors in console
- Verify form submission doesn't auto-close modal on errors

### 2. Form Filling Issues

#### Problem: Dropdown Selection Fails
**Symptoms:**
- Dropdown doesn't open when clicked
- Options not visible or selectable
- Selected value not retained

**Solutions:**
```python
# Wait for dropdown to be ready
jd_page.locators.company_dropdown.wait_for(state="visible")
time.sleep(1)

# Click dropdown to open
jd_page.locators.company_dropdown.click()
time.sleep(1)

# Verify options are visible before selecting
jd_page.locators.company_option("Test Company").wait_for(state="visible")
jd_page.locators.company_option("Test Company").click()
```

#### Problem: Input Fields Not Accepting Text
**Symptoms:**
- Text not appearing in input fields
- Fields appear disabled
- Validation errors for filled fields

**Solutions:**
```python
# Clear field before filling
jd_page.locators.position_job_title_input.clear()
jd_page.locators.position_job_title_input.fill(title)

# Verify text was entered
actual_value = jd_page.locators.position_job_title_input.input_value()
assert actual_value == title, f"Expected '{title}' but got '{actual_value}'"
```

### 3. Validation Error Issues

#### Problem: Expected Validation Errors Not Appearing
**Symptoms:**
- Required field errors not shown
- Form submits with invalid data
- Validation messages have wrong text

**Solutions:**
```python
# Trigger validation explicitly
jd_page.attempt_save_with_validation_errors()

# Wait for validation messages to appear
time.sleep(2)

# Check for specific error messages
enhanced_assert_visible(page, jd_page.locators.position_title_required_error,
                       "Position title required error should be visible", 
                       "validation_error_check")
```

#### Problem: Validation Errors Persist After Correction
**Symptoms:**
- Error messages remain after fixing issues
- Form won't submit even with valid data
- Validation state not updating

**Solutions:**
- Clear and refill problematic fields
- Trigger field blur events to update validation
- Refresh form state by closing and reopening modal

### 4. Search Functionality Issues

#### Problem: Search Not Returning Expected Results
**Symptoms:**
- Search returns no results for existing JDs
- Search results don't match search term
- Search input not accepting text

**Solutions:**
```python
# Verify search input is focused and ready
jd_page.locators.search_input.click()
jd_page.locators.search_input.clear()
jd_page.locators.search_input.fill(search_term)

# Submit search explicitly
page.keyboard.press("Enter")
time.sleep(2)

# Verify search was executed
current_url = page.url
assert search_term in current_url or "search" in current_url
```

#### Problem: Search Results Not Loading
**Symptoms:**
- Search executes but results don't update
- Loading indicators persist
- Page appears frozen

**Solutions:**
- Wait for network requests to complete
- Check for JavaScript errors
- Verify search API endpoints are responding

### 5. Filter Functionality Issues

#### Problem: Filter Panel Not Opening
**Symptoms:**
- Filter button click has no effect
- Filter panel not visible
- Filter options not accessible

**Solutions:**
```python
# Ensure filter button is clickable
enhanced_assert_visible(page, jd_page.locators.filters_button,
                       "Filters button should be visible", "filters_button_check")

# Click with explicit wait
jd_page.locators.filters_button.click()
time.sleep(2)

# Verify panel opened
enhanced_assert_visible(page, jd_page.locators.filter_panel,
                       "Filter panel should be visible", "filter_panel_check")
```

#### Problem: Filter Options Not Selectable
**Symptoms:**
- Filter checkboxes/dropdowns not responding
- Selected filters not applying
- Filter state not updating

**Solutions:**
- Verify filter options are enabled
- Check for overlapping elements blocking clicks
- Use force clicks if necessary

### 6. File Upload Issues

#### Problem: File Upload Dialog Not Opening
**Symptoms:**
- Upload button click has no effect
- File chooser dialog doesn't appear
- Upload area not responsive

**Solutions:**
```python
# Use file chooser expectation
with page.expect_file_chooser() as fc_info:
    jd_page.locators.upload_file_button.click()
file_chooser = fc_info.value
file_chooser.set_files(file_path)
```

#### Problem: File Upload Validation Errors
**Symptoms:**
- Valid files rejected as invalid format
- File size errors for small files
- Upload process hangs

**Solutions:**
- Verify test files exist and are accessible
- Check file permissions and paths
- Ensure file formats match expected validation rules

### 7. Pagination Issues

#### Problem: Pagination Controls Not Working
**Symptoms:**
- Next/Previous buttons not clickable
- Page numbers not responding
- URL not updating on navigation

**Solutions:**
```python
# Verify pagination is needed (more items than page size)
total_items = jd_page.get_total_jd_count()
page_size = jd_page.get_page_size()
assert total_items > page_size, "Pagination should be available"

# Check if controls are enabled
next_button_enabled = not jd_page.locators.next_page_button.is_disabled()
assert next_button_enabled, "Next button should be enabled"
```

### 8. Data-Related Issues

#### Problem: Test Data Conflicts
**Symptoms:**
- Tests fail due to existing data
- Unique constraint violations
- Inconsistent test results

**Solutions:**
```python
# Use fresh data for each test
@pytest.fixture
def unique_jd_data():
    return generate_complete_jd_data()

# Add timestamp to ensure uniqueness
timestamp = str(int(time.time()))
jd_data.position_title = f"Test Position {timestamp}"
```

#### Problem: Test Data Cleanup Issues
**Symptoms:**
- Test data accumulates over time
- Database performance degrades
- Tests become unreliable

**Solutions:**
- Implement proper cleanup in fixtures
- Use test-specific data prefixes
- Clean up data in teardown methods

### 9. Performance Issues

#### Problem: Tests Running Too Slowly
**Symptoms:**
- Individual tests take too long
- Timeouts occurring frequently
- Browser appears sluggish

**Solutions:**
```python
# Reduce slowmo setting
# In pytest.ini: --slowmo=0

# Optimize waits
page.wait_for_load_state("networkidle", timeout=10000)
time.sleep(1)  # Reduce unnecessary sleeps

# Use more specific locators
page.get_by_role("button", name="Save").click()  # Better than generic selectors
```

#### Problem: Memory Issues During Bulk Testing
**Symptoms:**
- Browser crashes during large dataset tests
- System becomes unresponsive
- Out of memory errors

**Solutions:**
- Reduce bulk test dataset sizes
- Close browser contexts between tests
- Use headless mode for bulk testing

### 10. Environment-Specific Issues

#### Problem: Tests Pass Locally But Fail in CI
**Symptoms:**
- Different behavior in CI environment
- Timing-related failures
- Resource constraints

**Solutions:**
```python
# Add CI-specific configurations
if os.getenv("CI"):
    # Increase timeouts for CI
    DEFAULT_TIMEOUT = 30000
    # Use headless mode
    HEADLESS = True
```

#### Problem: Cross-Browser Compatibility Issues
**Symptoms:**
- Tests pass in Chrome but fail in Firefox
- Different element behavior across browsers
- Browser-specific bugs

**Solutions:**
- Use browser-agnostic locators
- Add browser-specific handling where needed
- Test critical paths across all browsers

## Debugging Strategies

### 1. Screenshot Analysis
```python
# Capture debug screenshots at key points
page.screenshot(path=f"debug_screenshots/debug_{test_name}_{step}.png")

# Use enhanced assertions for automatic screenshots
enhanced_assert_visible(page, element, message, screenshot_name)
```

### 2. Console Log Analysis
```python
# Check for JavaScript errors
console_messages = page.evaluate("() => console.messages")
for message in console_messages:
    if message.type == "error":
        print(f"Console error: {message.text}")
```

### 3. Network Request Monitoring
```python
# Monitor network requests
def handle_request(request):
    print(f"Request: {request.method} {request.url}")

def handle_response(response):
    print(f"Response: {response.status} {response.url}")

page.on("request", handle_request)
page.on("response", handle_response)
```

### 4. Element State Verification
```python
# Check element state before interactions
element = jd_page.locators.save_button
print(f"Visible: {element.is_visible()}")
print(f"Enabled: {element.is_enabled()}")
print(f"Editable: {element.is_editable()}")
```

## Prevention Best Practices

### 1. Robust Locator Strategies
- Use semantic locators (role, text) over CSS selectors
- Implement fallback locator strategies
- Regularly review and update locators

### 2. Proper Wait Strategies
- Use explicit waits instead of fixed sleeps
- Wait for specific conditions, not just time
- Implement retry mechanisms for flaky operations

### 3. Test Data Management
- Generate unique test data for each test run
- Implement proper cleanup mechanisms
- Use test-specific data isolation

### 4. Error Handling
- Implement comprehensive error handling
- Provide meaningful error messages
- Capture diagnostic information on failures

## Getting Help

### 1. Log Analysis
- Check test execution logs for detailed error information
- Review browser console logs for JavaScript errors
- Analyze network requests for API failures

### 2. Screenshot Review
- Examine failure screenshots for visual clues
- Compare with expected page states
- Look for UI changes or unexpected elements

### 3. Test Environment Verification
- Verify test environment is properly configured
- Check browser versions and compatibility
- Ensure test data and files are available

### 4. Escalation Process
1. Try solutions from this guide
2. Review recent code changes for potential impacts
3. Check with team members for similar issues
4. Create detailed bug reports with reproduction steps

---

**Last Updated**: December 2024  
**Version**: 1.0  
**Maintainer**: Black Pigeon Automation Team