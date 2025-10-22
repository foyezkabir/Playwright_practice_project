# JD (Job Description) Test Execution Guide

This guide provides detailed instructions for executing JD automation tests in the Black Pigeon system.

## Prerequisites

1. **Environment Setup**: Ensure virtual environment is activated and dependencies installed
2. **Browser Installation**: Playwright browsers must be installed (`python -m playwright install`)
3. **Test Data**: JD test files should be available in `images_for_test/jd_files/`
4. **Credentials**: Valid login credentials with agency access permissions

## Test Execution Commands

### Complete JD Test Suite

Execute all JD tests with detailed output:
```powershell
pytest tests/test_jd.py -v --html=jd_report.html --self-contained-html
```

### Test Categories

#### 1. JD CRUD Operations (TC_01-TC_15)
```powershell
# All CRUD tests
pytest tests/test_jd.py -k "TC_01 or TC_02 or TC_03 or TC_04 or TC_05 or TC_06 or TC_07 or TC_08 or TC_09 or TC_10 or TC_11 or TC_12 or TC_13 or TC_14 or TC_15" -v

# JD Creation tests only
pytest tests/test_jd.py -k "create" -v

# JD Edit tests only  
pytest tests/test_jd.py -k "edit" -v

# JD Delete tests only
pytest tests/test_jd.py -k "delete" -v
```

#### 2. Search Functionality (TC_16-TC_25)
```powershell
# All search tests
pytest tests/test_jd.py -k "TC_16 or TC_17 or TC_18 or TC_19 or TC_20 or TC_21 or TC_22 or TC_23 or TC_24 or TC_25" -v

# Search functionality only
pytest tests/test_jd.py -k "search" -v

# Search validation tests
pytest tests/test_jd.py -k "search and validation" -v
```

#### 3. Filter Functionality (TC_26-TC_35)
```powershell
# All filter tests
pytest tests/test_jd.py -k "TC_26 or TC_27 or TC_28 or TC_29 or TC_30 or TC_31 or TC_32 or TC_33 or TC_34 or TC_35" -v

# Filter functionality only
pytest tests/test_jd.py -k "filter" -v

# Filter clearing tests
pytest tests/test_jd.py -k "filter and clear" -v
```

#### 4. Validation Testing (TC_36-TC_45)
```powershell
# All validation tests
pytest tests/test_jd.py -k "validation" -v

# Mandatory field validation
pytest tests/test_jd.py -k "required" -v

# Format validation tests
pytest tests/test_jd.py -k "format" -v
```

#### 5. File Upload Testing (TC_46-TC_55)
```powershell
# All file upload tests
pytest tests/test_jd.py -k "upload" -v

# File format validation
pytest tests/test_jd.py -k "file and format" -v

# File size validation
pytest tests/test_jd.py -k "file and size" -v
```

#### 6. Pagination Testing (TC_56-TC_65)
```powershell
# All pagination tests
pytest tests/test_jd.py -k "pagination" -v

# Page navigation tests
pytest tests/test_jd.py -k "page and navigation" -v
```

#### 7. Bulk Operations (TC_66-TC_75)
```powershell
# All bulk operation tests
pytest tests/test_jd.py -k "bulk" -v

# Bulk selection tests
pytest tests/test_jd.py -k "bulk and select" -v

# Bulk deletion tests
pytest tests/test_jd.py -k "bulk and delete" -v
```

### Individual Test Cases

#### Critical JD Creation Tests
```powershell
# Test JD creation with valid data
pytest tests/test_jd.py::test_TC_01_create_jd_with_valid_data -v

# Test mandatory field validation
pytest tests/test_jd.py::test_TC_05_position_title_required_validation -v
pytest tests/test_jd.py::test_TC_06_company_required_validation -v
pytest tests/test_jd.py::test_TC_07_work_style_required_validation -v
pytest tests/test_jd.py::test_TC_08_workplace_required_validation -v
```

#### Key Search and Filter Tests
```powershell
# Test search by position title
pytest tests/test_jd.py::test_TC_16_search_jd_by_position_title -v

# Test company filter
pytest tests/test_jd.py::test_TC_26_filter_jd_by_company -v

# Test filter clearing
pytest tests/test_jd.py::test_TC_35_clear_all_filters -v
```

#### Important File Upload Tests
```powershell
# Test valid file upload
pytest tests/test_jd.py::test_TC_46_upload_valid_jd_file -v

# Test invalid file format
pytest tests/test_jd.py::test_TC_48_upload_invalid_file_format -v
```

## Test Execution Options

### Browser Selection
```powershell
# Run with specific browser
pytest tests/test_jd.py --browser=chromium -v
pytest tests/test_jd.py --browser=firefox -v
pytest tests/test_jd.py --browser=webkit -v
```

### Execution Speed
```powershell
# Fast execution (no slowmo)
pytest tests/test_jd.py --slowmo=0 -v

# Slow execution for debugging
pytest tests/test_jd.py --slowmo=2000 -v
```

### Headless vs Headed
```powershell
# Headless execution (faster)
pytest tests/test_jd.py --headed=false -v

# Headed execution (visible browser)
pytest tests/test_jd.py --headed=true -v
```

### Parallel Execution
```powershell
# Run tests in parallel (requires pytest-xdist)
pytest tests/test_jd.py -n 2 -v
```

## Test Data Management

### Using Different Test Data Sets
```powershell
# Tests with fresh data (function-scoped)
pytest tests/test_jd.py -k "fresh_data" -v

# Tests with bulk data
pytest tests/test_jd.py -k "bulk_data" -v

# Tests with validation data
pytest tests/test_jd.py -k "validation_data" -v
```

### Test Data Cleanup
```powershell
# Run tests with cleanup tracking
pytest tests/test_jd.py --cleanup -v
```

## Debugging and Troubleshooting

### Debug Mode Execution
```powershell
# Run with maximum verbosity and debugging
pytest tests/test_jd.py -vvv --tb=long --capture=no
```

### Screenshot Capture
```powershell
# Force screenshot capture on all tests
pytest tests/test_jd.py --screenshot=always -v

# Screenshots only on failures (default)
pytest tests/test_jd.py --screenshot=failure -v
```

### Trace Generation
```powershell
# Generate Playwright traces for debugging
pytest tests/test_jd.py --tracing=on -v
```

### Specific Test Debugging
```powershell
# Debug specific failing test with full output
pytest tests/test_jd.py::test_TC_01_create_jd_with_valid_data -vvv --tb=long --capture=no --slowmo=2000
```

## Test Reports

### HTML Reports
```powershell
# Generate detailed HTML report
pytest tests/test_jd.py --html=reports/jd_test_report.html --self-contained-html -v
```

### Excel Reports
Excel reports are automatically generated in the `reports/` directory after test execution:
- `test_jd_report.xlsx` - Detailed test results with test steps and outcomes

### Screenshot Reports
Failure screenshots are saved in `screenshots/jd_screenshots/` with naming pattern:
- `TC_XX_failure_DD-MM-YYYY_HH.MM.SS.png`

## Performance Testing

### Large Dataset Testing
```powershell
# Test with large JD datasets
pytest tests/test_jd.py -k "bulk or pagination" --dataset-size=100 -v
```

### Load Testing
```powershell
# Simulate multiple concurrent users
pytest tests/test_jd.py -n 4 --dist=loadscope -v
```

## Continuous Integration

### CI/CD Pipeline Commands
```powershell
# CI-friendly execution
pytest tests/test_jd.py --browser=chromium --headed=false --html=reports/ci_jd_report.html --junit-xml=reports/jd_junit.xml -v
```

### Environment-Specific Testing
```powershell
# QA Environment
pytest tests/test_jd.py --base-url=https://bprp-qa.shadhinlab.xyz -v

# Staging Environment  
pytest tests/test_jd.py --base-url=https://bprp-staging.shadhinlab.xyz -v
```

## Best Practices

### Test Execution Order
1. **Smoke Tests**: Run critical JD creation and basic functionality tests first
2. **Core Features**: Execute CRUD operations and search functionality
3. **Advanced Features**: Run filter, pagination, and bulk operations
4. **Edge Cases**: Execute validation and error handling tests
5. **Performance**: Run bulk data and performance tests last

### Test Data Strategy
- Use `fresh_jd_data` fixture for tests requiring unique data
- Use `jd_test_data` fixture for consistent test data across module
- Clean up test data after execution to prevent conflicts

### Error Handling
- Review screenshots immediately after test failures
- Check console logs for detailed error information
- Verify test data and page state before reporting issues

### Maintenance
- Update locators in `loc_jd.py` when UI changes
- Refresh test data generators when business rules change
- Review and update test cases when new JD features are added

## Support and Contact

For issues with JD test execution:
1. Check this guide for common solutions
2. Review test failure screenshots and logs
3. Verify test environment and data setup
4. Contact the automation team for complex issues

---

**Last Updated**: December 2024  
**Version**: 1.0  
**Maintainer**: Black Pigeon Automation Team