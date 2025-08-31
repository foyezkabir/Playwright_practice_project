# User Management Test Suite

## Overview
Comprehensive automated test suite for BPRP user management functionality, including roles & access and user list operations. Built using Playwright + Pytest with Page Object Model architecture.

## 🏗️ Architecture

### File Structure
```
├── locators/
│   └── loc_user_management.py          # Centralized locators for user management
├── pages/
│   └── user_management_page.py         # Page Object Model implementation
├── utils/
│   └── user_management_helper.py       # Helper functions and assertions
├── random_values_generator/
│   ├── random_role_name.py            # Role name generation
│   └── random_user_data.py            # User data generation
├── tests/
│   └── test_user_management.py        # Comprehensive test cases
└── screenshots/
    └── user_management_screenshots/    # Auto-generated test artifacts
```

### Key Components
- **UserManagementLocators**: 200+ locators for all UI elements
- **UserManagementPage**: 50+ methods for user management operations
- **Helper Functions**: CRUD operations, validations, cleanup utilities
- **Random Data Generators**: Unique test data creation
- **Enhanced Assertions**: Automatic screenshot capture on failures

## 🚀 Quick Start

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt
python -m playwright install
```

### Run Tests
```bash
# Run all user management tests
pytest tests/test_user_management.py -v

# Run specific test cases
pytest tests/test_user_management.py::test_TC_02_create_role_with_permissions -v

# Run with cleanup
pytest tests/test_user_management.py -v -m cleanup

# Run without cleanup (faster)
pytest tests/test_user_management.py -v -m "not cleanup"
```

## 📋 Test Cases

### Roles & Access (TC_01-TC_07)
| Test Case | Description | Validation |
|-----------|-------------|------------|
| TC_01 | Navigate to user management | ✅ Page loads, tabs visible |
| TC_02 | Create role with permissions | ✅ Role created successfully |
| TC_03 | Search existing role | ✅ Role found in search |
| TC_04 | Edit existing role | ✅ Role updated with new permissions |
| TC_05 | Delete role with confirmation | ✅ Role deleted successfully |
| TC_06 | Role validation - empty name | ✅ Error: "Role name is required" |
| TC_07 | Role validation - no permissions | ✅ Error: "At least one permission is required" |

### User List (TC_08-TC_14)
| Test Case | Description | Validation |
|-----------|-------------|------------|
| TC_08 | Invite user with valid details | ✅ User invited successfully |
| TC_09 | Search invited user | ✅ User found in search |
| TC_10 | Edit user role | ✅ Role updated (or 404 for pending users) |
| TC_11 | Delete user with confirmation | ✅ User deleted successfully |
| TC_12 | User validation - empty email | ✅ Error: "Email is required" |
| TC_13 | User validation - invalid email | ✅ Error: "Please enter a valid email" |
| TC_14 | Host email protection | ✅ Error: "Cannot invite host email" |

### Comprehensive Workflows (TC_15-TC_20)
| Test Case | Description | Validation |
|-----------|-------------|------------|
| TC_15 | Complete role lifecycle | ✅ Create → Read → Update → Delete |
| TC_16 | Complete user lifecycle | ✅ Invite → Search → Edit → Delete |
| TC_17 | Pagination functionality | ✅ Next/Previous page navigation |
| TC_18 | Search edge cases | ✅ Empty, non-existent, whitespace |
| TC_19 | Cleanup test data | ✅ Remove all test roles/users |
| TC_20 | Performance testing | ✅ Multiple operations efficiently |

## 🧪 Test Data Management

### Dynamic Data Generation
```python
# Role data
role_data = generate_test_role_data_set()
# Output: {'role_name': 'Test Manager Role 1234', 'permissions': ['Dashboard', 'Talent Read']}

# User data  
user_data = generate_test_user_data()
# Output: {'user_name': 'John Smith', 'user_email': 'john.smith.567890@test.com'}
```

### Edge Case Testing
- **Invalid Emails**: Missing @, empty domain, special characters
- **Role Names**: Empty, duplicate, special characters
- **Host Protection**: Prevents inviting admin@onemail.host variants
- **Permissions**: Empty sets, invalid combinations

## 🎯 Key Features

### Enhanced Assertions
```python
# Automatic screenshot on failure
enhanced_assert_visible(page, locator, "Error message should appear", "test_name")

# Result: screenshots/user_management_screenshots/test_name_timestamp.png
```

### Comprehensive Locators
- **Role-based selectors**: `page.get_by_role("button", name="Create Role")`
- **Text-based selectors**: `page.get_by_text("Role created successfully")`
- **Dynamic selectors**: `role_item_by_name(role_name)`
- **Validation messages**: Specific locators for each error type

### Robust Error Handling
- **Network wait strategies**: Wait for API calls to complete
- **Toast message detection**: Automatic wait for success/error messages
- **Pagination support**: Find items across multiple pages
- **Retry mechanisms**: Handle intermittent failures

## 🔧 Configuration

### Login Credentials
```python
ADMIN_CREDENTIALS = {
    'email': 'mi003b@onemail.host',
    'password': 'Kabir123#'
}
```

### Test Environment
- **Target**: https://bprp-qa.shadhinlab.xyz
- **Agency**: demo 06
- **Browser**: Chromium (configurable)
- **Screenshots**: Enabled on failures

## 📊 Test Execution Patterns

### Parallel Execution
```bash
# Run tests in parallel (requires pytest-xdist)
pytest tests/test_user_management.py -n 2
```

### Selective Execution
```bash
# Run only role tests
pytest tests/test_user_management.py -k "role" -v

# Run only validation tests  
pytest tests/test_user_management.py -k "validation" -v

# Skip cleanup
pytest tests/test_user_management.py -m "not cleanup" -v
```

### Debug Mode
```bash
# Run with debug info
pytest tests/test_user_management.py -v -s --tb=long
```

## 🛠️ Maintenance

### Adding New Tests
1. **Add locators** in `loc_user_management.py`
2. **Add page methods** in `user_management_page.py`  
3. **Add helpers** in `user_management_helper.py`
4. **Create test case** in `test_user_management.py`

### Updating Selectors
- Check `locators/loc_user_management.py` for element changes
- Use browser dev tools to verify selector accuracy
- Update both primary and fallback selectors

### Test Data Cleanup
```python
# Manual cleanup
cleanup_test_data(page, email, password)

# Automatic cleanup (runs after all tests)
pytest tests/test_user_management.py -v -m cleanup
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: Role/User not found after creation
```bash
Solution: Check for success toast messages, verify pagination
```

**Issue**: API 404 errors during role edit
```bash
Solution: Expected for pending users, check business logic
```

**Issue**: Toast messages not detected
```bash
Solution: Increase TOAST_WAIT_TIME in config.py
```

**Issue**: Locators not finding elements
```bash
Solution: Check if UI structure changed, update locators
```

### Debug Screenshots
All test failures automatically capture screenshots with:
- **Location**: `screenshots/user_management_screenshots/`
- **Naming**: `{test_name}_{timestamp}.png`
- **Content**: Full page with element highlighting

## 📈 Reporting

### HTML Reports
```bash
# Generate detailed HTML report
pytest tests/test_user_management.py --html=report.html --self-contained-html
```

### Coverage Reports
```bash
# Run with coverage
pytest tests/test_user_management.py --cov=pages --cov=utils --cov-report=html
```

## 🔒 Security Testing

### Host Email Protection
- Tests prevent inviting admin emails
- Validates case sensitivity protection
- Checks whitespace handling

### Permission Validation
- Ensures roles require at least one permission
- Tests permission inheritance
- Validates role hierarchy

## ⚡ Performance Considerations

### Optimizations
- **Fixture scoping**: Module-level fixtures for shared data
- **Wait strategies**: Network idle vs DOM content loaded
- **Batch operations**: Multiple role/user creation
- **Cleanup batching**: Efficient test data removal

### Timing Configuration
```python
TOAST_WAIT_TIME = 1500      # Toast appearance
NETWORK_IDLE_TIMEOUT = 5000 # API call completion
PAGE_LOAD_STRATEGY = "networkidle"
```

## 📝 Best Practices

### Test Writing
1. **Use descriptive test names**: `test_TC_##_descriptive_functionality`
2. **Include docstrings**: Explain what each test verifies
3. **Generate unique data**: Avoid conflicts between test runs
4. **Clean up test data**: Use fixtures and cleanup methods
5. **Assert with context**: Provide meaningful error messages

### Page Objects
1. **Single responsibility**: One method per action
2. **Return meaningful data**: Page objects return useful information
3. **Handle exceptions**: Graceful error handling with alternatives
4. **Use waiting strategies**: Built-in waits for reliability
5. **Document complex methods**: Explain business logic

---

**For questions or contributions, refer to the main project documentation or create an issue.**
