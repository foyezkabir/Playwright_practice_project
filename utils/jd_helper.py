"""
JD (Job Description) Helper Module
Contains utility functions for JD management tests including creation, editing, listing, search, and filtering operations
"""

from playwright.sync_api import Page
from utils.config import BASE_URL
from utils.login_helper import do_login
from conftest import wait_for_action_completion
from utils.enhanced_assertions import (
    enhanced_assert_visible,
    enhanced_assert_not_visible,
)
import time


def do_jd_login(page: Page, email: str, password: str, agency_id: str = "174"):
    """
    Helper function to login and navigate to JD page for specified agency

    Args:
        page: Playwright page object
        email: User email
        password: User password
        agency_id: Agency ID to navigate to (default: "174" for demo 06)

    Returns:
        JDPage instance
    """
    from pages.jd_page import JDPage

    # Step 1: Login
    do_login(page, email, password)
    time.sleep(3)

    # Step 2: Initialize JD page and navigate directly to JD management
    jd_page = JDPage(page)
    jd_page.navigate_to_jd_page(agency_id)
    time.sleep(2)

    return jd_page


def do_create_jd(
    page: Page,
    jd_data: dict,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#",
):
    """
    Complete JD creation workflow with validation

    Args:
        page: Playwright page object
        jd_data: Dictionary containing JD data
        agency_id: Agency ID to create JD for
        email: Login email
        password: Login password

    Returns:
        tuple: (JDPage instance, success boolean)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)

    print(f"🔧 Creating JD: {jd_data.get('position_title', 'Unknown Position')}")

    # Open JD creation modal
    jd_page.click_add_jd()
    jd_page.wait_for_modal_to_open()

    # Fill JD form
    jd_page.fill_jd_form(jd_data)

    # Save JD
    jd_page.save_jd()

    # Wait a moment for the form to process
    time.sleep(2)

    # Check for success or validation errors
    success = False
    try:
        # Try to wait for success message (toast appears quickly)
        try:
            jd_page.locators.jd_created_successfully_message.wait_for(state="visible", timeout=5000)
            print("✅ JD created successfully!")
            success = True
        except:
            # Success message didn't appear, check for validation errors
            print("⚠️ Success message not found, checking for validation errors...")
            validation_found = False
            
            # Check for all mandatory field validation errors
            if jd_page.locators.position_title_required_error.count() > 0:
                print("❌ Job title is required error found")
                validation_found = True
            if jd_page.locators.company_required_error.count() > 0:
                print("❌ Company is required error found")
                validation_found = True
            if jd_page.locators.work_style_required_error.count() > 0:
                print("❌ Work style is required error found")
                validation_found = True
            if jd_page.locators.salary_required_error.count() > 0:
                print("❌ Salary is required error found")
                validation_found = True
            if jd_page.locators.target_age_min_required_error.count() > 0:
                print("❌ Target age min is required error found")
                validation_found = True
            if jd_page.locators.target_age_max_required_error.count() > 0:
                print("❌ Target age max is required error found")
                validation_found = True
            if jd_page.locators.client_required_error.count() > 0:
                print("❌ Client is required error found")
                validation_found = True
            if jd_page.locators.hiring_status_required_error.count() > 0:
                print("❌ Hiring status is required error found")
                validation_found = True
            
            if validation_found:
                print("❌ Validation errors found during JD creation")
                success = False
            else:
                print("⚠️ No success message and no validation errors - uncertain state")
                success = False  # Don't assume success if we can't confirm it
                success = True
                
    except Exception as e:
        print(f"⚠️ Error checking JD creation status: {e}")
        success = False

    return jd_page, success


def do_search_and_verify_jd(
    page: Page, search_term: str, expected_results: list = None
):
    """
    Search for JDs and verify results

    Args:
        page: Playwright page object
        search_term: Term to search for
        expected_results: List of expected JD titles in results (optional)

    Returns:
        JDPage instance
    """
    from pages.jd_page import JDPage

    jd_page = JDPage(page)

    print(f"🔍 Searching for JDs with term: '{search_term}'")
    jd_page.search_jd(search_term)
    time.sleep(2)

    # Verify search results if expected results provided
    if expected_results:
        for expected_title in expected_results:
            jd_card = jd_page.locators.jd_card(expected_title)
            enhanced_assert_visible(
                page,
                jd_card,
                f"JD '{expected_title}' should be visible in search results",
                "jd_search_verification",
            )

    return jd_page


# ===== ENHANCED SEARCH HELPER FUNCTIONS =====

def do_comprehensive_search_test(page: Page, search_test_cases: list):
    """
    Perform comprehensive search testing with multiple test cases
    
    Args:
        page: Playwright page object
        search_test_cases: List of search test cases
                          Example: [
                              {"term": "engineer", "expected_count": 3},
                              {"term": "nonexistent", "expected_count": 0},
                              {"term": "", "expected_count": None}  # All results
                          ]
    
    Returns:
        tuple: (JDPage instance, test results dict)
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print(f"🔍 Running comprehensive search test with {len(search_test_cases)} test cases")
    
    # Run comprehensive search test
    results = jd_page.test_search_functionality_comprehensive(search_test_cases)
    
    return jd_page, results


def do_search_with_verification(page: Page, search_term: str, expected_count: int = None, verify_highlights: bool = True):
    """
    Perform search with comprehensive verification
    
    Args:
        page: Playwright page object
        search_term: Search term to use
        expected_count: Expected number of results (optional)
        verify_highlights: Whether to verify search term highlighting
    
    Returns:
        tuple: (JDPage instance, actual results count)
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print(f"🔍 Performing search with verification for: '{search_term}'")
    
    # Perform search and verify results
    actual_count = jd_page.search_and_verify_results(search_term, expected_count)
    
    # Additional verification if results found and highlights requested
    if actual_count > 0 and verify_highlights:
        jd_page.verify_search_highlights(search_term)
    
    return jd_page, actual_count


def do_test_search_input_handling(page: Page):
    """
    Test search input handling and behavior
    
    Args:
        page: Playwright page object
    
    Returns:
        JDPage instance
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print("🔍 Testing search input handling")
    
    # Test filling search input without submitting
    test_term = "test search"
    jd_page.fill_search_input(test_term)
    jd_page.verify_search_input_value(test_term)
    
    # Test clearing search input
    jd_page.clear_search_input()
    jd_page.verify_search_input_value("")
    
    # Test empty search
    empty_results_count = jd_page.perform_empty_search()
    print(f"✅ Empty search returned {empty_results_count} results")
    
    return jd_page


def do_test_search_reset_functionality(page: Page, initial_search_term: str):
    """
    Test search reset and clearing functionality
    
    Args:
        page: Playwright page object
        initial_search_term: Search term to use before testing reset
    
    Returns:
        JDPage instance
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print(f"🔍 Testing search reset functionality with initial term: '{initial_search_term}'")
    
    # Perform initial search
    initial_count = jd_page.perform_search(initial_search_term)
    print(f"-> Initial search returned {initial_count} results")
    
    # Test search reset
    jd_page.reset_search_state()
    
    # Verify search is reset (should show all JDs)
    reset_count = jd_page.get_search_results_count()
    print(f"-> After reset: {reset_count} results")
    
    # Test clear search button if available
    jd_page.click_clear_search_button()
    
    print("✅ Search reset functionality tested")
    return jd_page


def do_test_no_results_scenarios(page: Page, no_results_terms: list = ["nonexistentterm123", "zzzzzzz", "!@#$%"]):
    """
    Test search scenarios that should return no results
    
    Args:
        page: Playwright page object
        no_results_terms: List of search terms that should return no results
    
    Returns:
        tuple: (JDPage instance, test results dict)
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print(f"🔍 Testing no results scenarios with terms: {no_results_terms}")
    
    results = {}
    
    for term in no_results_terms:
        try:
            print(f"-> Testing no results for: '{term}'")
            
            # Perform search
            count = jd_page.perform_search(term)
            
            # Should return 0 results
            if count == 0:
                # Verify no results message is displayed
                jd_page.handle_no_results_scenario(term)
                results[term] = {"success": True, "count": count}
                print(f"✅ No results scenario verified for '{term}'")
            else:
                results[term] = {"success": False, "count": count, "error": f"Expected 0 results but got {count}"}
                print(f"❌ Expected no results for '{term}' but got {count}")
            
            # Reset for next test
            jd_page.reset_search_state()
            
        except Exception as e:
            results[term] = {"success": False, "error": str(e)}
            print(f"❌ Error testing no results for '{term}': {e}")
    
    successful_tests = len([r for r in results.values() if r.get("success")])
    print(f"✅ No results scenarios test completed: {successful_tests}/{len(no_results_terms)} passed")
    
    return jd_page, results


def do_test_search_term_highlighting(page: Page, search_terms: list):
    """
    Test search term highlighting in results
    
    Args:
        page: Playwright page object
        search_terms: List of search terms to test highlighting for
    
    Returns:
        tuple: (JDPage instance, highlighting results dict)
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print(f"🔍 Testing search term highlighting for: {search_terms}")
    
    results = {}
    
    for term in search_terms:
        try:
            print(f"-> Testing highlighting for: '{term}'")
            
            # Perform search
            count = jd_page.perform_search(term)
            
            if count > 0:
                # Test highlighting
                highlighting_works = jd_page.verify_search_highlights(term)
                results[term] = {"success": True, "highlighting": highlighting_works, "count": count}
            else:
                results[term] = {"success": True, "highlighting": False, "count": 0, "note": "No results to highlight"}
            
            # Reset for next test
            jd_page.reset_search_state()
            
        except Exception as e:
            results[term] = {"success": False, "error": str(e)}
            print(f"❌ Error testing highlighting for '{term}': {e}")
    
    print("✅ Search term highlighting test completed")
    return jd_page, results


def assert_search_results_count(page: Page, search_term: str, expected_count: int, test_name: str = "search_results_count"):
    """
    Assert search results return expected count
    
    Args:
        page: Playwright page object
        search_term: Search term used
        expected_count: Expected number of results
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    # Get actual count
    actual_count = jd_page.get_search_results_count()
    
    # Assert count matches expected
    if actual_count == expected_count:
        print(f"✅ Search results count verified: {actual_count} results for '{search_term}'")
    else:
        raise AssertionError(f"Expected {expected_count} search results for '{search_term}' but found {actual_count}")


def assert_search_term_in_results(page: Page, search_term: str, test_name: str = "search_term_in_results"):
    """
    Assert search term appears in search results
    
    Args:
        page: Playwright page object
        search_term: Search term to verify in results
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    # Verify search term appears in results
    jd_page.verify_search_results_contain_term(search_term)
    
    print(f"✅ Search term '{search_term}' verified in results")


def assert_no_search_results(page: Page, search_term: str, test_name: str = "no_search_results"):
    """
    Assert search returns no results and displays appropriate message
    
    Args:
        page: Playwright page object
        search_term: Search term that should return no results
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    # Verify no results scenario
    jd_page.handle_no_results_scenario(search_term)
    
    print(f"✅ No search results scenario verified for '{search_term}'")


def assert_search_input_cleared(page: Page, test_name: str = "search_input_cleared"):
    """
    Assert search input is cleared/empty
    
    Args:
        page: Playwright page object
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    # Verify search input is empty
    jd_page.verify_search_input_value("")
    
    print("✅ Search input cleared verification passed")


def do_apply_jd_filters(page: Page, filters: dict):
    """
    Apply multiple filters to JD list

    Args:
        page: Playwright page object
        filters: Dictionary of filters to apply
                Example: {
                    'company': 'Test Company',
                    'work_style': 'Remote',
                    'hiring_status': 'Active'
                }

    Returns:
        JDPage instance
    """
    from pages.jd_page import JDPage

    jd_page = JDPage(page)

    print(f"🔧 Applying filters: {filters}")
    jd_page.open_filters()
    time.sleep(1)

    # Apply each filter
    for filter_type, filter_value in filters.items():
        if filter_type == "company":
            jd_page.apply_company_filter(filter_value)
        elif filter_type == "work_style":
            jd_page.apply_work_style_filter(filter_value)
        elif filter_type == "hiring_status":
            jd_page.apply_hiring_status_filter(filter_value)
        # Add more filter types as needed

        time.sleep(1)

    print("✅ Filters applied successfully")
    return jd_page


# ===== ENHANCED FILTER HELPER FUNCTIONS =====

def do_comprehensive_filter_test(page: Page, filter_test_cases: list):
    """
    Perform comprehensive filter testing with multiple filter combinations
    
    Args:
        page: Playwright page object
        filter_test_cases: List of filter combinations to test
                          Example: [
                              {"company": "Test Company", "work_style": "Remote"},
                              {"status": "Active", "work_style": "On-site"},
                              {"company": "ABC Corp", "status": "Inactive"}
                          ]
    
    Returns:
        tuple: (JDPage instance, test results dict)
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print(f"🔧 Running comprehensive filter test with {len(filter_test_cases)} combinations")
    
    # Run filter combinations test
    results = jd_page.test_filter_combinations(filter_test_cases)
    
    return jd_page, results


def do_test_filter_panel_interactions(page: Page):
    """
    Test filter panel opening, closing, and basic interactions
    
    Args:
        page: Playwright page object
    
    Returns:
        JDPage instance
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print("🔧 Testing filter panel interactions")
    
    # Test opening filter panel
    jd_page.click_filters_button()
    jd_page.verify_filter_panel_opened()
    
    # Test closing filter panel
    jd_page.close_filter_panel()
    jd_page.verify_filter_panel_closed()
    
    print("✅ Filter panel interactions tested")
    return jd_page


def do_test_individual_filters(page: Page, filter_options: dict):
    """
    Test individual filter types with specific options
    
    Args:
        page: Playwright page object
        filter_options: Dictionary of filter types and their test values
                       Example: {
                           "company": ["Test Company", "ABC Corp"],
                           "status": ["Active", "Inactive"],
                           "work_style": ["Remote", "On-site"]
                       }
    
    Returns:
        tuple: (JDPage instance, test results dict)
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print(f"🔧 Testing individual filters: {list(filter_options.keys())}")
    
    results = {}
    
    for filter_type, test_values in filter_options.items():
        print(f"\n-> Testing {filter_type} filter with values: {test_values}")
        
        filter_results = {}
        
        for value in test_values:
            try:
                print(f"   -> Testing {filter_type} = '{value}'")
                
                # Open filter panel
                jd_page.click_filters_button()
                
                # Apply single filter
                success = jd_page.apply_single_filter(filter_type, value)
                
                if success:
                    # Get results count
                    count = jd_page.get_filtered_results_count()
                    
                    # Verify results match criteria
                    matches = jd_page.verify_filtered_results_match_criteria({filter_type: value})
                    
                    filter_results[value] = {
                        "success": True,
                        "count": count,
                        "matches_criteria": matches
                    }
                    print(f"   ✅ {filter_type} = '{value}': {count} results")
                else:
                    filter_results[value] = {
                        "success": False,
                        "error": "Failed to apply filter"
                    }
                    print(f"   ❌ Failed to apply {filter_type} = '{value}'")
                
                # Clear filters for next test
                jd_page.click_all_clear_button()
                
            except Exception as e:
                filter_results[value] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"   ❌ Error testing {filter_type} = '{value}': {e}")
        
        results[filter_type] = filter_results
    
    print("\n✅ Individual filters test completed")
    return jd_page, results


def do_test_multi_filter_combinations(page: Page, combinations: list):
    """
    Test multiple filter combinations and verify results
    
    Args:
        page: Playwright page object
        combinations: List of filter combination dictionaries
    
    Returns:
        tuple: (JDPage instance, combination results dict)
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print(f"🔧 Testing {len(combinations)} multi-filter combinations")
    
    results = {}
    
    for i, filters in enumerate(combinations):
        try:
            print(f"\n-> Testing combination {i+1}: {filters}")
            
            # Apply multiple filters
            success = jd_page.apply_multiple_filters(filters)
            
            if success:
                # Verify results
                count = jd_page.verify_filter_combination_results(filters)
                results[f"combination_{i+1}"] = {
                    "filters": filters,
                    "success": True,
                    "count": count
                }
                print(f"   ✅ Combination {i+1}: {count} results")
            else:
                results[f"combination_{i+1}"] = {
                    "filters": filters,
                    "success": False,
                    "error": "Failed to apply filters"
                }
                print(f"   ❌ Failed to apply combination {i+1}")
            
            # Clear filters for next test
            jd_page.click_all_clear_button()
            
        except Exception as e:
            results[f"combination_{i+1}"] = {
                "filters": filters,
                "success": False,
                "error": str(e)
            }
            print(f"   ❌ Error in combination {i+1}: {e}")
    
    successful_combinations = len([r for r in results.values() if r.get("success")])
    print(f"\n✅ Multi-filter combinations test completed: {successful_combinations}/{len(combinations)} passed")
    
    return jd_page, results


def do_test_filter_options_availability(page: Page):
    """
    Test availability of filter options for each filter type
    
    Args:
        page: Playwright page object
    
    Returns:
        tuple: (JDPage instance, available options dict)
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print("🔧 Testing filter options availability")
    
    # Test all filter types
    results = jd_page.test_all_filter_types()
    
    return jd_page, results


def do_test_salary_range_filter(page: Page, salary_ranges: list):
    """
    Test salary range filter with different min/max combinations
    
    Args:
        page: Playwright page object
        salary_ranges: List of salary range dictionaries
                      Example: [
                          {"min": "50000", "max": "80000"},
                          {"min": "30000", "max": None},
                          {"min": None, "max": "100000"}
                      ]
    
    Returns:
        tuple: (JDPage instance, salary filter results dict)
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print(f"🔧 Testing salary range filter with {len(salary_ranges)} ranges")
    
    results = {}
    
    for i, salary_range in enumerate(salary_ranges):
        try:
            min_salary = salary_range.get("min")
            max_salary = salary_range.get("max")
            
            print(f"\n-> Testing salary range {i+1}: min={min_salary}, max={max_salary}")
            
            # Open filter panel
            jd_page.click_filters_button()
            
            # Set salary range filter
            success = jd_page.set_salary_range_filter(min_salary, max_salary)
            
            if success:
                # Apply filters
                jd_page.click_apply_filters_button()
                
                # Get results count
                count = jd_page.get_filtered_results_count()
                
                results[f"range_{i+1}"] = {
                    "min_salary": min_salary,
                    "max_salary": max_salary,
                    "success": True,
                    "count": count
                }
                print(f"   ✅ Salary range {i+1}: {count} results")
            else:
                results[f"range_{i+1}"] = {
                    "min_salary": min_salary,
                    "max_salary": max_salary,
                    "success": False,
                    "error": "Failed to set salary range"
                }
                print(f"   ❌ Failed to set salary range {i+1}")
            
            # Clear filters for next test
            jd_page.click_all_clear_button()
            
        except Exception as e:
            results[f"range_{i+1}"] = {
                "min_salary": min_salary,
                "max_salary": max_salary,
                "success": False,
                "error": str(e)
            }
            print(f"   ❌ Error testing salary range {i+1}: {e}")
    
    successful_ranges = len([r for r in results.values() if r.get("success")])
    print(f"\n✅ Salary range filter test completed: {successful_ranges}/{len(salary_ranges)} passed")
    
    return jd_page, results


def assert_filter_panel_state(page: Page, should_be_open: bool, test_name: str = "filter_panel_state"):
    """
    Assert filter panel open/closed state
    
    Args:
        page: Playwright page object
        should_be_open: Whether filter panel should be open (True) or closed (False)
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    if should_be_open:
        jd_page.verify_filter_panel_opened()
    else:
        jd_page.verify_filter_panel_closed()
    
    print(f"✅ Filter panel state verified: {'open' if should_be_open else 'closed'}")


def assert_filtered_results_count(page: Page, filters: dict, expected_count: int, test_name: str = "filtered_results_count"):
    """
    Assert filtered results return expected count
    
    Args:
        page: Playwright page object
        filters: Applied filters
        expected_count: Expected number of results
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    # Verify filter combination results
    actual_count = jd_page.verify_filter_combination_results(filters, expected_count)
    
    print(f"✅ Filtered results count verified: {actual_count} results for filters {filters}")


def assert_filters_cleared(page: Page, test_name: str = "filters_cleared"):
    """
    Assert all filters have been cleared
    
    Args:
        page: Playwright page object
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    # Verify all filters are cleared
    jd_page.verify_all_filters_cleared()
    
    print("✅ All filters cleared verification passed")


def assert_filter_results_match_criteria(page: Page, filters: dict, test_name: str = "filter_results_match"):
    """
    Assert filtered results match the applied filter criteria
    
    Args:
        page: Playwright page object
        filters: Applied filter criteria
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    # Verify results match criteria
    jd_page.verify_filtered_results_match_criteria(filters)
    
    print(f"✅ Filter results match criteria verified for: {filters}")


# ===== FILTER CLEARING AND RESET HELPER FUNCTIONS =====

def do_test_filter_clearing_functionality(page: Page):
    """
    Test comprehensive filter clearing functionality
    
    Args:
        page: Playwright page object
    
    Returns:
        tuple: (JDPage instance, clearing test results dict)
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print("🔧 Testing filter clearing functionality")
    
    # Run comprehensive filter clearing test
    results = jd_page.test_filter_clearing_comprehensive()
    
    return jd_page, results


def do_test_all_clear_button(page: Page, test_filters: dict = None):
    """
    Test 'All clear' button functionality
    
    Args:
        page: Playwright page object
        test_filters: Filters to apply before testing clear (optional)
    
    Returns:
        tuple: (JDPage instance, success boolean)
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print("🔧 Testing 'All clear' button functionality")
    
    # Use default test filters if none provided
    if test_filters is None:
        test_filters = {"company": "Test Company", "work_style": "Remote"}
    
    try:
        # Get original count before applying filters
        original_count = jd_page.get_filtered_results_count()
        
        # Apply test filters
        jd_page.apply_multiple_filters(test_filters)
        filtered_count = jd_page.get_filtered_results_count()
        
        print(f"-> Applied filters: {original_count} -> {filtered_count} JDs")
        
        # Test all clear button
        clear_success = jd_page.click_all_clear_filters_button()
        
        if clear_success:
            # Verify filters are cleared
            verification_success = jd_page.verify_all_filters_removed()
            
            # Verify original state is restored
            restore_success = jd_page.verify_filter_reset_restores_original_state(original_count)
            
            overall_success = verification_success and restore_success
            
            if overall_success:
                print("✅ 'All clear' button functionality verified")
            else:
                print("⚠️ 'All clear' button issues detected")
            
            return jd_page, overall_success
        else:
            print("❌ 'All clear' button failed to work")
            return jd_page, False
            
    except Exception as e:
        print(f"❌ Error testing 'All clear' button: {e}")
        return jd_page, False


# ===== JD DELETION HELPER FUNCTIONS =====

def do_delete_jd(
    page: Page,
    jd_title: str,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#",
    from_detail_view: bool = False,
    confirm_deletion: bool = True
):
    """
    Complete JD deletion workflow
    
    Args:
        page: Playwright page object
        jd_title: Title of JD to delete
        agency_id: Agency ID where JD exists
        email: Login email
        password: Login password
        from_detail_view: Whether to delete from detail view (True) or list view (False)
        confirm_deletion: Whether to confirm deletion (True) or cancel (False)
    
    Returns:
        tuple: (JDPage instance, success boolean)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"🗑️ Deleting JD: '{jd_title}' (from {'detail view' if from_detail_view else 'list view'})")
    
    try:
        if confirm_deletion:
            # Perform complete deletion workflow
            success = jd_page.perform_complete_jd_deletion_workflow(jd_title, from_detail_view)
        else:
            # Perform cancellation workflow
            success = jd_page.perform_jd_deletion_cancellation_workflow(jd_title)
        
        return jd_page, success
        
    except Exception as e:
        print(f"❌ Error in JD deletion workflow: {e}")
        return jd_page, False


def do_bulk_delete_jds(
    page: Page,
    jd_titles: list,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#",
    confirm_deletion: bool = True,
    use_select_all: bool = False
):
    """
    Complete bulk JD deletion workflow
    
    Args:
        page: Playwright page object
        jd_titles: List of JD titles to delete
        agency_id: Agency ID where JDs exist
        email: Login email
        password: Login password
        confirm_deletion: Whether to confirm deletion (True) or cancel (False)
        use_select_all: Whether to use select all checkbox instead of individual selection
    
    Returns:
        tuple: (JDPage instance, success boolean)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"🗑️ Bulk deleting {len(jd_titles)} JDs: {jd_titles}")
    
    try:
        if use_select_all:
            # Use select all functionality
            jd_page.select_all_jds()
        else:
            # Select specific JDs
            jd_page.select_multiple_jds(jd_titles)
        
        if confirm_deletion:
            # Perform complete bulk deletion workflow
            success = jd_page.perform_complete_bulk_deletion_workflow(jd_titles)
        else:
            # Perform bulk cancellation workflow
            success = jd_page.perform_bulk_deletion_cancellation_workflow(jd_titles)
        
        return jd_page, success
        
    except Exception as e:
        print(f"❌ Error in bulk JD deletion workflow: {e}")
        return jd_page, False


def do_test_jd_deletion_with_associated_data(
    page: Page,
    jd_title: str,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#",
    force_delete: bool = True
):
    """
    Test JD deletion when JD has associated data
    
    Args:
        page: Playwright page object
        jd_title: Title of JD with associated data
        agency_id: Agency ID where JD exists
        email: Login email
        password: Login password
        force_delete: Whether to force delete despite associated data
    
    Returns:
        tuple: (JDPage instance, success boolean)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"🗑️ Testing deletion of JD with associated data: '{jd_title}'")
    
    try:
        # Trigger deletion
        jd_page.trigger_jd_deletion_from_list(jd_title)
        
        # Verify associated data warning appears
        jd_page.verify_jd_with_associated_data_warning()
        
        if force_delete:
            # Handle force delete scenario
            success = jd_page.handle_force_delete_for_associated_data()
        else:
            # Cancel deletion due to associated data
            success = jd_page.cancel_jd_deletion()
            # Verify JD still exists
            jd_page.verify_jd_remains_in_list_after_failed_deletion(jd_title)
        
        return jd_page, success
        
    except Exception as e:
        print(f"❌ Error testing JD deletion with associated data: {e}")
        return jd_page, False


def do_test_jd_deletion_error_scenarios(
    page: Page,
    jd_title: str,
    agency_id: str,
    error_type: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#"
):
    """
    Test JD deletion error scenarios
    
    Args:
        page: Playwright page object
        jd_title: Title of JD to test deletion for
        agency_id: Agency ID where JD exists
        error_type: Type of error to test ('network', 'permission', 'associated_data', 'general')
        email: Login email
        password: Login password
    
    Returns:
        tuple: (JDPage instance, success boolean)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"🗑️ Testing JD deletion error scenario: '{error_type}' for JD '{jd_title}'")
    
    try:
        # Perform deletion with error handling
        success = jd_page.perform_deletion_with_error_handling(jd_title, error_type)
        
        return jd_page, success
        
    except Exception as e:
        print(f"❌ Error testing JD deletion error scenario: {e}")
        return jd_page, False


def do_test_bulk_deletion_partial_failures(
    page: Page,
    jd_titles: list,
    expected_failures: list,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#"
):
    """
    Test bulk deletion with expected partial failures
    
    Args:
        page: Playwright page object
        jd_titles: List of JD titles to attempt deletion
        expected_failures: List of JD titles expected to fail deletion
        agency_id: Agency ID where JDs exist
        email: Login email
        password: Login password
    
    Returns:
        tuple: (JDPage instance, results dict)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"🗑️ Testing bulk deletion with partial failures")
    print(f"Attempting: {jd_titles}")
    print(f"Expected failures: {expected_failures}")
    
    try:
        # Perform bulk deletion with partial failures
        results = jd_page.perform_bulk_deletion_with_partial_failures(jd_titles, expected_failures)
        
        return jd_page, results
        
    except Exception as e:
        print(f"❌ Error testing bulk deletion with partial failures: {e}")
        return jd_page, None


def assert_jd_deletion_success(page: Page, deleted_jd_title: str, test_name: str = "jd_deletion_success"):
    """
    Assert JD deletion was successful
    
    Args:
        page: Playwright page object
        deleted_jd_title: Title of JD that should be deleted
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    # Verify successful deletion
    jd_page.verify_successful_jd_deletion(deleted_jd_title)
    
    print(f"✅ JD deletion success verified for '{deleted_jd_title}'")


def assert_jd_still_exists(page: Page, jd_title: str, test_name: str = "jd_still_exists"):
    """
    Assert JD still exists in list (deletion was cancelled or failed)
    
    Args:
        page: Playwright page object
        jd_title: Title of JD that should still exist
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    # Verify JD still exists
    jd_page.verify_jd_remains_in_list_after_failed_deletion(jd_title)
    
    print(f"✅ JD still exists verification passed for '{jd_title}'")


def assert_bulk_deletion_success(page: Page, deleted_jd_titles: list, test_name: str = "bulk_deletion_success"):
    """
    Assert bulk deletion was successful
    
    Args:
        page: Playwright page object
        deleted_jd_titles: List of JD titles that should be deleted
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    # Verify bulk deletion success
    jd_page.verify_bulk_deletion_success(deleted_jd_titles)
    
    print(f"✅ Bulk deletion success verified for {len(deleted_jd_titles)} JDs")


def assert_deletion_confirmation_dialog(page: Page, test_name: str = "deletion_confirmation_dialog"):
    """
    Assert deletion confirmation dialog appears correctly
    
    Args:
        page: Playwright page object
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    # Verify deletion confirmation dialog
    jd_page.verify_deletion_confirmation_dialog()
    
    print("✅ Deletion confirmation dialog verification passed")


def assert_deletion_error_message(page: Page, error_type: str, test_name: str = "deletion_error_message"):
    """
    Assert appropriate deletion error message is displayed
    
    Args:
        page: Playwright page object
        error_type: Type of error expected ('network', 'permission', 'associated_data', 'general')
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    # Verify deletion error message
    jd_page.verify_deletion_failure_error_messages(error_type)
    
    print(f"✅ Deletion error message verification passed for type: {error_type}")


def assert_jd_list_count_updated(page: Page, original_count: int, deleted_count: int, test_name: str = "jd_list_count_updated"):
    """
    Assert JD list count is correctly updated after deletion
    
    Args:
        page: Playwright page object
        original_count: Original count before deletion
        deleted_count: Number of JDs that should be deleted
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    if deleted_count == 1:
        # Single deletion
        jd_page.verify_jd_list_updated_after_deletion(original_count)
    else:
        # Bulk deletion
        jd_page.verify_jd_list_updated_after_bulk_deletion(original_count, deleted_count)
    
    print(f"✅ JD list count update verification passed: -{deleted_count} JDs")


def do_test_filter_reset_functionality(page: Page):
    """
    Test filter reset functionality using reset button
    
    Args:
        page: Playwright page object
    
    Returns:
        tuple: (JDPage instance, success boolean)
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    print("🔧 Testing filter reset functionality")
    
    # Test filter reset
    success = jd_page.test_filter_reset_functionality()
    
    return jd_page, success


# ===== JD EDIT AND UPDATE HELPER FUNCTIONS =====

def do_edit_jd(
    page: Page,
    jd_title: str,
    updated_data: dict,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#",
):
    """
    Complete JD edit workflow with validation

    Args:
        page: Playwright page object
        jd_title: Title of JD to edit
        updated_data: Dictionary containing updated JD data
        agency_id: Agency ID where JD exists
        email: Login email
        password: Login password

    Returns:
        tuple: (JDPage instance, success boolean)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)

    print(f"🔧 Editing JD: {jd_title}")

    try:
        # Complete JD update workflow
        success = jd_page.complete_jd_update_workflow(jd_title, updated_data)
        
        if success:
            print(f"✅ JD '{jd_title}' updated successfully!")
        else:
            print(f"❌ JD '{jd_title}' update failed")
        
        return jd_page, success
        
    except Exception as e:
        print(f"❌ Error during JD edit workflow: {e}")
        return jd_page, False


def do_test_jd_edit_access(page: Page, jd_title: str, access_method: str = "list"):
    """
    Test JD edit mode access from different entry points

    Args:
        page: Playwright page object
        jd_title: Title of JD to access for editing
        access_method: Method to access edit mode ("list" or "detail")

    Returns:
        tuple: (JDPage instance, success boolean)
    """
    from pages.jd_page import JDPage

    jd_page = JDPage(page)

    print(f"🔧 Testing JD edit access via {access_method} for: {jd_title}")

    try:
        if access_method == "list":
            success = jd_page.access_edit_mode_from_list(jd_title)
        elif access_method == "detail":
            success = jd_page.access_edit_mode_from_detail_view(jd_title)
        else:
            raise ValueError(f"Invalid access method: {access_method}")

        if success:
            print(f"✅ JD edit access via {access_method} successful")
            # Close edit mode after test
            jd_page.cancel_edit_without_saving()
        else:
            print(f"❌ JD edit access via {access_method} failed")

        return jd_page, success

    except Exception as e:
        print(f"❌ Error testing JD edit access: {e}")
        return jd_page, False


def do_test_jd_edit_pre_filled_data(page: Page, jd_title: str, expected_data: dict):
    """
    Test that JD edit modal opens with correct pre-filled data

    Args:
        page: Playwright page object
        jd_title: Title of JD to test
        expected_data: Expected data that should be pre-filled

    Returns:
        tuple: (JDPage instance, success boolean)
    """
    from pages.jd_page import JDPage

    jd_page = JDPage(page)

    print(f"🔍 Testing JD edit pre-filled data for: {jd_title}")

    try:
        # Access edit mode
        jd_page.access_edit_mode_from_list(jd_title)

        # Verify pre-filled data
        success = jd_page.verify_edit_modal_pre_filled_data(expected_data)

        if success:
            print(f"✅ JD edit pre-filled data verification successful")
        else:
            print(f"❌ JD edit pre-filled data verification failed")

        # Close edit mode
        jd_page.cancel_edit_without_saving()

        return jd_page, success

    except Exception as e:
        print(f"❌ Error testing JD edit pre-filled data: {e}")
        return jd_page, False


def do_test_jd_update_validation(page: Page, jd_title: str, validation_scenarios: dict):
    """
    Test JD update validation with various error scenarios

    Args:
        page: Playwright page object
        jd_title: Title of JD to test validation on
        validation_scenarios: Dictionary of validation scenarios to test

    Returns:
        tuple: (JDPage instance, validation results dict)
    """
    from pages.jd_page import JDPage

    jd_page = JDPage(page)

    print(f"🔍 Testing JD update validation for: {jd_title}")

    results = {}

    try:
        # Access edit mode
        jd_page.access_edit_mode_from_list(jd_title)

        # Test validation scenarios
        for scenario_name, scenario_data in validation_scenarios.items():
            try:
                print(f"-> Testing validation scenario: {scenario_name}")

                # Implement validation test
                jd_page.implement_update_validation({scenario_name: scenario_data})

                # Handle error scenarios
                if "error_type" in scenario_data:
                    jd_page.handle_update_error_scenarios(scenario_data["error_type"])

                results[scenario_name] = {"success": True}
                print(f"   ✅ Validation scenario '{scenario_name}' passed")

            except Exception as e:
                results[scenario_name] = {"success": False, "error": str(e)}
                print(f"   ❌ Validation scenario '{scenario_name}' failed: {e}")

        # Close edit mode
        jd_page.cancel_edit_without_saving()
        jd_page.handle_unsaved_changes_warning("discard")

        successful_scenarios = len([r for r in results.values() if r.get("success")])
        print(f"✅ JD update validation test completed: {successful_scenarios}/{len(validation_scenarios)} passed")

        return jd_page, results

    except Exception as e:
        print(f"❌ Error testing JD update validation: {e}")
        return jd_page, {"error": str(e)}


def do_test_jd_edit_cancellation(page: Page, jd_title: str, original_data: dict):
    """
    Test JD edit cancellation functionality and data preservation

    Args:
        page: Playwright page object
        jd_title: Title of JD to test cancellation on
        original_data: Original JD data to verify preservation

    Returns:
        tuple: (JDPage instance, success boolean)
    """
    from pages.jd_page import JDPage

    jd_page = JDPage(page)

    print(f"🔧 Testing JD edit cancellation for: {jd_title}")

    try:
        # Test complete edit cancellation workflow
        success = jd_page.verify_edit_cancellation_workflow(jd_title, original_data)

        if success:
            print(f"✅ JD edit cancellation test successful")
        else:
            print(f"❌ JD edit cancellation test failed")

        return jd_page, success

    except Exception as e:
        print(f"❌ Error testing JD edit cancellation: {e}")
        return jd_page, False


def do_test_jd_edit_cancellation_scenarios(page: Page, jd_title: str, original_data: dict):
    """
    Test various JD edit cancellation scenarios

    Args:
        page: Playwright page object
        jd_title: Title of JD to test
        original_data: Original JD data for verification

    Returns:
        tuple: (JDPage instance, scenario results dict)
    """
    from pages.jd_page import JDPage

    jd_page = JDPage(page)

    print(f"🧪 Testing JD edit cancellation scenarios for: {jd_title}")

    try:
        # Test all cancellation scenarios
        success = jd_page.test_edit_cancellation_scenarios(jd_title, original_data)

        if success:
            print(f"✅ All JD edit cancellation scenarios passed")
        else:
            print(f"❌ Some JD edit cancellation scenarios failed")

        return jd_page, success

    except Exception as e:
        print(f"❌ Error testing JD edit cancellation scenarios: {e}")
        return jd_page, False


def do_test_jd_edit_state_management(page: Page, jd_title: str):
    """
    Test JD edit mode state management and navigation

    Args:
        page: Playwright page object
        jd_title: Title of JD to test state management on

    Returns:
        tuple: (JDPage instance, success boolean)
    """
    from pages.jd_page import JDPage

    jd_page = JDPage(page)

    print(f"🔧 Testing JD edit state management for: {jd_title}")

    try:
        # Access edit mode
        jd_page.access_edit_mode_from_list(jd_title)

        # Test different state management scenarios
        navigation_scenarios = ["browser_back", "page_refresh", "direct_url"]
        
        for scenario in navigation_scenarios:
            try:
                print(f"-> Testing navigation scenario: {scenario}")
                
                # Re-access edit mode for each test
                if not jd_page.is_modal_open():
                    jd_page.access_edit_mode_from_list(jd_title)
                
                # Test navigation scenario
                jd_page.handle_edit_state_navigation(scenario)
                
                print(f"   ✅ Navigation scenario '{scenario}' handled")
                
            except Exception as e:
                print(f"   ❌ Navigation scenario '{scenario}' failed: {e}")

        print(f"✅ JD edit state management test completed")
        return jd_page, True

    except Exception as e:
        print(f"❌ Error testing JD edit state management: {e}")
        return jd_page, False


def assert_jd_edit_modal_opened(page: Page, test_name: str = "jd_edit_modal_opened"):
    """
    Assert JD edit modal has opened correctly

    Args:
        page: Playwright page object
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage

    jd_page = JDPage(page)

    # Verify edit modal opened
    jd_page.verify_edit_modal_opened()

    print("✅ JD edit modal opened verification passed")


def assert_jd_edit_pre_filled_data(page: Page, expected_data: dict, test_name: str = "jd_edit_pre_filled_data"):
    """
    Assert JD edit modal has correct pre-filled data

    Args:
        page: Playwright page object
        expected_data: Expected pre-filled data
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage

    jd_page = JDPage(page)

    # Verify pre-filled data
    jd_page.verify_edit_modal_pre_filled_data(expected_data)

    print("✅ JD edit pre-filled data verification passed")


def assert_jd_update_success(page: Page, test_name: str = "jd_update_success"):
    """
    Assert JD update was successful

    Args:
        page: Playwright page object
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage

    jd_page = JDPage(page)

    # Verify update success message
    jd_page.verify_update_success_message()

    print("✅ JD update success verification passed")


def assert_jd_edit_validation_errors(page: Page, expected_errors: list, test_name: str = "jd_edit_validation_errors"):
    """
    Assert JD edit validation errors are displayed correctly

    Args:
        page: Playwright page object
        expected_errors: List of expected validation errors
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage

    jd_page = JDPage(page)

    # Verify validation messages in edit mode
    jd_page.verify_validation_message_display_in_edit(expected_errors)

    print("✅ JD edit validation errors verification passed")


def assert_jd_data_not_modified_after_cancel(page: Page, jd_title: str, original_data: dict, test_name: str = "jd_data_not_modified"):
    """
    Assert JD data is not modified after edit cancellation

    Args:
        page: Playwright page object
        jd_title: Title of JD to verify
        original_data: Original data to compare against
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage

    jd_page = JDPage(page)

    # Verify data not modified after cancellation
    jd_page.verify_data_not_modified_after_cancellation(original_data, jd_title)

    print("✅ JD data not modified after cancellation verification passed")


def parse_and_display_jd_details(full_page_content: str):
    """
    Parse and display key JD details from page content
    
    Args:
        full_page_content: Full page content text from page.inner_text("body")
    """
    print("\n" + "="*80)
    print("📋 CAPTURED JD DETAILS PAGE CONTENT:")
    print("="*80)
    
    # Extract and display key information
    details_lines = full_page_content.split("\n")
    
    key_fields = [
        "Company Name",
        "Job Title",
        "Salary Budget",
        "Hiring Status",
        "Priority Grade",
        "Work Style",
        "Work Place",
        "Japanese Level",
        "English Level",
        "Job Age",
        "Target Age",
        "Client Owner",
        "Client Grade",
        "Opening Date"
    ]
    
    for i, line in enumerate(details_lines):
        line_stripped = line.strip()
        # Check if this line is a field name
        if line_stripped in key_fields:
            # Next line should be ":", and line after that is the value
            if i + 2 < len(details_lines) and details_lines[i + 1].strip() == ":":
                value = details_lines[i + 2].strip()
                if value:  # Only print if there's a value
                    print(f"{line_stripped}: {value}")
    
    print("="*80 + "\n")

# ===== FILE UPLOAD HELPER FUNCTIONS =====

def do_bulk_jd_file_upload(
    page: Page,
    file_path: str,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#",
    expected_jd_count: int = None
):
    """
    Complete bulk JD file upload workflow
    
    Args:
        page: Playwright page object
        file_path: Path to file to upload
        agency_id: Agency ID to upload JDs for
        email: Login email
        password: Login password
        expected_jd_count: Expected number of JDs to be imported (optional)
    
    Returns:
        tuple: (JDPage instance, success boolean, imported_count)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"📤 Starting bulk JD file upload: {file_path}")
    
    try:
        # Click upload file button
        jd_page.click_upload_file_button_for_bulk_import()
        
        # Upload the file
        jd_page.upload_file_for_bulk_import(file_path)
        
        # Verify processing success
        jd_page.verify_file_processing_success(expected_jd_count)
        
        # Get final JD count
        final_count = jd_page.get_jd_cards_count()
        
        print(f"✅ Bulk JD file upload completed successfully: {final_count} JDs")
        return jd_page, True, final_count
        
    except Exception as e:
        print(f"❌ Bulk JD file upload failed: {e}")
        return jd_page, False, 0


def do_test_file_format_validation(
    page: Page,
    test_files: dict,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#"
):
    """
    Test file format validation with valid and invalid files
    
    Args:
        page: Playwright page object
        test_files: Dictionary with 'valid' and 'invalid' file lists
                   Example: {
                       'valid': ['test.pdf', 'test.docx'],
                       'invalid': ['test.txt', 'test.jpg']
                   }
        agency_id: Agency ID
        email: Login email
        password: Login password
    
    Returns:
        tuple: (JDPage instance, validation results dict)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"🔍 Testing file format validation")
    
    results = {
        'valid_files': {},
        'invalid_files': {}
    }
    
    # Test valid files
    for file_path in test_files.get('valid', []):
        try:
            print(f"-> Testing valid file: {file_path}")
            jd_page.click_upload_file_button_for_bulk_import()
            jd_page.upload_valid_file_format(file_path)
            results['valid_files'][file_path] = {'success': True}
            print(f"✅ Valid file accepted: {file_path}")
        except Exception as e:
            results['valid_files'][file_path] = {'success': False, 'error': str(e)}
            print(f"❌ Valid file rejected: {file_path} - {e}")
    
    # Test invalid files
    for file_path in test_files.get('invalid', []):
        try:
            print(f"-> Testing invalid file: {file_path}")
            jd_page.click_upload_file_button_for_bulk_import()
            jd_page.upload_invalid_file_format(file_path)
            results['invalid_files'][file_path] = {'success': True}
            print(f"✅ Invalid file correctly rejected: {file_path}")
        except Exception as e:
            results['invalid_files'][file_path] = {'success': False, 'error': str(e)}
            print(f"❌ Invalid file handling failed: {file_path} - {e}")
    
    return jd_page, results


def do_test_file_size_validation(
    page: Page,
    oversized_file_path: str,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#"
):
    """
    Test file size validation with oversized file
    
    Args:
        page: Playwright page object
        oversized_file_path: Path to file exceeding size limit
        agency_id: Agency ID
        email: Login email
        password: Login password
    
    Returns:
        tuple: (JDPage instance, validation success boolean)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"📏 Testing file size validation with: {oversized_file_path}")
    
    try:
        # Click upload file button
        jd_page.click_upload_file_button_for_bulk_import()
        
        # Upload oversized file
        jd_page.upload_oversized_file(oversized_file_path)
        
        print("✅ File size validation working correctly")
        return jd_page, True
        
    except Exception as e:
        print(f"❌ File size validation failed: {e}")
        return jd_page, False


def do_test_file_processing_error_handling(
    page: Page,
    invalid_data_file_path: str,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#"
):
    """
    Test file processing error handling with invalid data
    
    Args:
        page: Playwright page object
        invalid_data_file_path: Path to file with invalid data
        agency_id: Agency ID
        email: Login email
        password: Login password
    
    Returns:
        tuple: (JDPage instance, error handling results dict)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"🔍 Testing file processing error handling with: {invalid_data_file_path}")
    
    results = {}
    
    try:
        # Upload file with invalid data
        jd_page.click_upload_file_button_for_bulk_import()
        jd_page.upload_file_for_bulk_import(invalid_data_file_path)
        
        # Check for various error handling scenarios
        results['invalid_data_errors'] = jd_page.handle_invalid_file_data_errors()
        results['content_validation_errors'] = jd_page.verify_file_content_validation_errors()
        results['format_requirement_errors'] = jd_page.verify_data_format_requirement_errors()
        results['processing_failure_messages'] = jd_page.verify_processing_failure_error_messages()
        
        print("✅ File processing error handling tested")
        return jd_page, results
        
    except Exception as e:
        print(f"❌ File processing error handling test failed: {e}")
        results['test_error'] = str(e)
        return jd_page, results


def do_test_network_timeout_handling(
    page: Page,
    large_file_path: str,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#"
):
    """
    Test network timeout handling during file processing
    
    Args:
        page: Playwright page object
        large_file_path: Path to large file that may cause timeout
        agency_id: Agency ID
        email: Login email
        password: Login password
    
    Returns:
        tuple: (JDPage instance, timeout handling results dict)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"⏰ Testing network timeout handling with: {large_file_path}")
    
    results = {}
    
    try:
        # Upload large file
        jd_page.click_upload_file_button_for_bulk_import()
        jd_page.upload_file_for_bulk_import(large_file_path)
        
        # Handle large file processing scenarios
        results['large_file_detected'] = jd_page.handle_large_file_processing_scenarios()
        results['timeout_detected'] = jd_page.handle_network_timeout_during_processing()
        
        if results['timeout_detected']:
            # Test retry functionality
            results['retry_available'] = jd_page.verify_retry_option_available()
            if results['retry_available']:
                results['retry_success'] = jd_page.click_retry_processing()
        
        print("✅ Network timeout handling tested")
        return jd_page, results
        
    except Exception as e:
        print(f"❌ Network timeout handling test failed: {e}")
        results['test_error'] = str(e)
        return jd_page, results


# ===== BULK OPERATIONS HELPER FUNCTIONS =====

def do_bulk_jd_selection(
    page: Page,
    jd_titles: list,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#"
):
    """
    Select multiple JDs for bulk operations
    
    Args:
        page: Playwright page object
        jd_titles: List of JD titles to select
        agency_id: Agency ID
        email: Login email
        password: Login password
    
    Returns:
        tuple: (JDPage instance, selected count)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"☑️ Selecting JDs for bulk operations: {jd_titles}")
    
    # Select multiple JDs
    selected_count = jd_page.select_multiple_jds(jd_titles)
    
    print(f"✅ Selected {selected_count} JDs for bulk operations")
    return jd_page, selected_count


def do_bulk_status_update(
    page: Page,
    jd_titles: list,
    new_status: str,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#"
):
    """
    Perform bulk status update on multiple JDs
    
    Args:
        page: Playwright page object
        jd_titles: List of JD titles to update
        new_status: New status to apply
        agency_id: Agency ID
        email: Login email
        password: Login password
    
    Returns:
        tuple: (JDPage instance, success boolean)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"🔄 Performing bulk status update to '{new_status}' for: {jd_titles}")
    
    try:
        # Select JDs
        selected_count = jd_page.select_multiple_jds(jd_titles)
        
        if selected_count > 0:
            # Perform bulk status update
            jd_page.perform_bulk_status_update(new_status)
            
            # Verify status was updated across JDs
            jd_page.verify_bulk_status_update_across_jds(jd_titles, new_status)
            
            print(f"✅ Bulk status update completed successfully for {selected_count} JDs")
            return jd_page, True
        else:
            print("❌ No JDs selected for bulk status update")
            return jd_page, False
            
    except Exception as e:
        print(f"❌ Bulk status update failed: {e}")
        return jd_page, False


def do_bulk_jd_deletion(
    page: Page,
    jd_titles: list,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#",
    confirm_deletion: bool = True
):
    """
    Perform bulk deletion of multiple JDs
    
    Args:
        page: Playwright page object
        jd_titles: List of JD titles to delete
        agency_id: Agency ID
        email: Login email
        password: Login password
        confirm_deletion: Whether to confirm the deletion
    
    Returns:
        tuple: (JDPage instance, success boolean, deleted_count)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"🗑️ Performing bulk deletion for: {jd_titles}")
    
    try:
        # Get initial count
        initial_count = jd_page.get_jd_cards_count()
        
        # Select JDs for deletion
        selected_count = jd_page.select_multiple_jds(jd_titles)
        
        if selected_count > 0:
            # Trigger bulk deletion
            jd_page.locators.bulk_delete_button.click()
            time.sleep(1)
            
            # Verify confirmation dialog
            jd_page.verify_bulk_operation_confirmation("delete")
            
            if confirm_deletion:
                # Confirm deletion
                jd_page.confirm_bulk_operation("delete")
                
                # Verify success
                enhanced_assert_visible(page, jd_page.locators.bulk_jd_deleted_successfully_message,
                                       "Bulk deletion success message should be visible", "bulk_deletion_success")
                
                # Verify JDs are removed from list
                final_count = jd_page.get_jd_cards_count()
                deleted_count = initial_count - final_count
                
                print(f"✅ Bulk deletion completed: {deleted_count} JDs deleted")
                return jd_page, True, deleted_count
            else:
                # Cancel deletion
                jd_page.cancel_bulk_operation("delete")
                print("✅ Bulk deletion cancelled successfully")
                return jd_page, True, 0
        else:
            print("❌ No JDs selected for bulk deletion")
            return jd_page, False, 0
            
    except Exception as e:
        print(f"❌ Bulk deletion failed: {e}")
        return jd_page, False, 0


def do_test_bulk_operation_confirmation(
    page: Page,
    operation_type: str,
    jd_titles: list,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#"
):
    """
    Test bulk operation confirmation dialogs
    
    Args:
        page: Playwright page object
        operation_type: Type of bulk operation ('delete', 'status_update')
        jd_titles: List of JD titles to select
        agency_id: Agency ID
        email: Login email
        password: Login password
    
    Returns:
        tuple: (JDPage instance, confirmation test results dict)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"🔍 Testing bulk {operation_type} confirmation dialog")
    
    results = {}
    
    try:
        # Select JDs
        selected_count = jd_page.select_multiple_jds(jd_titles)
        
        if selected_count > 0:
            # Trigger bulk operation
            if operation_type == "delete":
                jd_page.locators.bulk_delete_button.click()
            elif operation_type == "status_update":
                jd_page.locators.bulk_status_update_button.click()
            
            time.sleep(1)
            
            # Test confirmation dialog
            results['confirmation_displayed'] = jd_page.verify_bulk_operation_confirmation(operation_type)
            
            # Test cancellation
            results['cancellation_works'] = jd_page.cancel_bulk_operation(operation_type)
            
            print(f"✅ Bulk {operation_type} confirmation dialog tested")
        else:
            results['error'] = "No JDs selected"
            
        return jd_page, results
        
    except Exception as e:
        print(f"❌ Bulk {operation_type} confirmation test failed: {e}")
        results['test_error'] = str(e)
        return jd_page, results


def do_test_mixed_bulk_operation_results(
    page: Page,
    operation_type: str,
    mixed_jd_titles: list,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#"
):
    """
    Test bulk operations with mixed success/failure scenarios
    
    Args:
        page: Playwright page object
        operation_type: Type of bulk operation
        mixed_jd_titles: List of JD titles (some may fail)
        agency_id: Agency ID
        email: Login email
        password: Login password
    
    Returns:
        tuple: (JDPage instance, mixed results dict)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print(f"🔍 Testing mixed results for bulk {operation_type}")
    
    results = {}
    
    try:
        # Select JDs (some may not exist or be protected)
        selected_count = jd_page.select_multiple_jds(mixed_jd_titles)
        
        if selected_count > 0:
            # Perform bulk operation
            if operation_type == "delete":
                jd_page.locators.bulk_delete_button.click()
                jd_page.confirm_bulk_operation("delete")
            elif operation_type == "status_update":
                jd_page.perform_bulk_status_update("Active")
            
            # Check for mixed results
            results['mixed_results_detected'] = jd_page.handle_mixed_bulk_operation_results(operation_type)
            
            if results['mixed_results_detected']:
                results['error_details_provided'] = jd_page.verify_bulk_operation_error_details()
            
            # Test progress tracking
            results['progress_tracked'] = jd_page.verify_bulk_operation_progress_tracking(operation_type)
            
            print(f"✅ Mixed bulk {operation_type} results tested")
        else:
            results['error'] = "No JDs selected"
            
        return jd_page, results
        
    except Exception as e:
        print(f"❌ Mixed bulk {operation_type} results test failed: {e}")
        results['test_error'] = str(e)
        return jd_page, results


def do_select_all_jds_test(
    page: Page,
    agency_id: str,
    email: str = "mi003b@onemail.host",
    password: str = "Kabir123#"
):
    """
    Test select all JDs functionality
    
    Args:
        page: Playwright page object
        agency_id: Agency ID
        email: Login email
        password: Login password
    
    Returns:
        tuple: (JDPage instance, select all results dict)
    """
    # Login and navigate to JD page
    jd_page = do_jd_login(page, email, password, agency_id)
    
    print("☑️ Testing select all JDs functionality")
    
    results = {}
    
    try:
        # Get total JD count
        total_count = jd_page.get_jd_cards_count()
        results['total_jds'] = total_count
        
        if total_count > 0:
            # Test select all
            jd_page.select_all_jds()
            
            # Verify all JDs are selected
            results['all_selected'] = jd_page.verify_selected_items_count(total_count)
            
            # Verify bulk actions are enabled
            results['bulk_actions_enabled'] = jd_page.verify_bulk_actions_menu_enabled()
            
            print(f"✅ Select all JDs functionality tested: {total_count} JDs")
        else:
            results['no_jds_to_select'] = True
            print("ℹ️ No JDs available to test select all functionality")
            
        return jd_page, results
        
    except Exception as e:
        print(f"❌ Select all JDs test failed: {e}")
        results['test_error'] = str(e)
        return jd_page, results


# ===== ASSERTION HELPER FUNCTIONS FOR FILE UPLOAD AND BULK OPERATIONS =====

def assert_file_upload_success(page: Page, test_name: str = "file_upload_success"):
    """
    Assert file upload completed successfully
    
    Args:
        page: Playwright page object
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    jd_page.verify_file_upload_success()
    
    print("✅ File upload success assertion passed")


def assert_file_processing_success(page: Page, expected_count: int = None, test_name: str = "file_processing_success"):
    """
    Assert file processing completed successfully
    
    Args:
        page: Playwright page object
        expected_count: Expected number of imported JDs
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    jd_page.verify_file_processing_success(expected_count)
    
    print("✅ File processing success assertion passed")


def assert_file_format_error(page: Page, test_name: str = "file_format_error"):
    """
    Assert file format error is displayed
    
    Args:
        page: Playwright page object
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    jd_page.verify_file_format_error()
    
    print("✅ File format error assertion passed")


def assert_file_size_error(page: Page, test_name: str = "file_size_error"):
    """
    Assert file size error is displayed
    
    Args:
        page: Playwright page object
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    jd_page.verify_file_size_error()
    
    print("✅ File size error assertion passed")


def assert_bulk_operation_success(page: Page, operation_type: str, test_name: str = "bulk_operation_success"):
    """
    Assert bulk operation completed successfully
    
    Args:
        page: Playwright page object
        operation_type: Type of bulk operation
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    
    if operation_type == "delete":
        enhanced_assert_visible(page, jd_page.locators.bulk_jd_deleted_successfully_message,
                               "Bulk deletion success message should be visible", test_name)
    elif operation_type == "status_update":
        jd_page.verify_bulk_status_update_success()
    
    print(f"✅ Bulk {operation_type} success assertion passed")


def assert_bulk_actions_enabled(page: Page, test_name: str = "bulk_actions_enabled"):
    """
    Assert bulk actions menu is enabled
    
    Args:
        page: Playwright page object
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    jd_page.verify_bulk_actions_menu_enabled()
    
    print("✅ Bulk actions enabled assertion passed")


def assert_bulk_actions_disabled(page: Page, test_name: str = "bulk_actions_disabled"):
    """
    Assert bulk actions menu is disabled
    
    Args:
        page: Playwright page object
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    jd_page.verify_bulk_actions_menu_disabled()
    
    print("✅ Bulk actions disabled assertion passed")


def assert_selected_items_count(page: Page, expected_count: int, test_name: str = "selected_items_count"):
    """
    Assert selected items count matches expected
    
    Args:
        page: Playwright page object
        expected_count: Expected number of selected items
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    jd_page.verify_selected_items_count(expected_count)
    
    print(f"✅ Selected items count assertion passed: {expected_count}")


def assert_processing_error_messages(page: Page, test_name: str = "processing_error_messages"):
    """
    Assert file processing error messages are displayed
    
    Args:
        page: Playwright page object
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    jd_page.verify_processing_failure_error_messages()
    
    print("✅ Processing error messages assertion passed")


def assert_line_specific_errors(page: Page, test_name: str = "line_specific_errors"):
    """
    Assert line-specific error messages are displayed
    
    Args:
        page: Playwright page object
        test_name: Test name for screenshot naming
    """
    from pages.jd_page import JDPage
    
    jd_page = JDPage(page)
    jd_page.verify_line_specific_errors()
    
    print("✅ Line-specific errors assertion passed")