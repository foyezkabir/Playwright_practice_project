"""
JD Test Helpers Class
Organized wrapper for all JD helper functions and utilities
"""

from playwright.sync_api import Page
from utils.jd_helper import (
    do_jd_login,
    do_create_jd,
    do_search_and_verify_jd,
    do_apply_jd_filters,
    do_delete_jd,
    assert_jd_edit_validation_errors,
    assert_search_results_count,
    assert_filtered_results_count,
    assert_no_search_results,
    do_comprehensive_search_test,
    do_test_filter_clearing_functionality,
    do_test_all_clear_button,
    do_test_multi_filter_combinations,
    do_test_no_results_scenarios,
    do_bulk_jd_file_upload,
    do_bulk_jd_selection,
    do_bulk_jd_deletion,
    do_bulk_status_update
)


class JDHelpers:
    """
    Organized wrapper class for all JD helper functions
    """
    
    @staticmethod
    def login(page: Page, email: str, password: str, agency_id: str):
        """Login and navigate to JD page"""
        return do_jd_login(page, email, password, agency_id)
    
    @staticmethod
    def create_jd(page: Page, jd_data: dict, agency_id: str, email: str = "mi003b@onemail.host", password: str = "Kabir123#"):
        """Create JD with provided data"""
        return do_create_jd(page, jd_data, agency_id, email, password)
    
    @staticmethod
    def search_and_verify(page: Page, search_term: str, expected_results: list = None):
        """Search for JDs and verify results"""
        return do_search_and_verify_jd(page, search_term, expected_results)
    
    @staticmethod
    def apply_filters(page: Page, filters: dict):
        """Apply filters to JD list"""
        return do_apply_jd_filters(page, filters)
    
    @staticmethod
    def delete_jd(page: Page, jd_title: str, agency_id: str, email: str = "mi003b@onemail.host", password: str = "Kabir123#", from_detail_view: bool = False, confirm_deletion: bool = True):
        """Delete JD with confirmation"""
        return do_delete_jd(page, jd_title, agency_id, email, password, from_detail_view, confirm_deletion)
    
    # Search helpers
    @staticmethod
    def comprehensive_search_test(page: Page, search_test_cases: list):
        """Run comprehensive search tests"""
        return do_comprehensive_search_test(page, search_test_cases)
    
    @staticmethod
    def test_no_results_scenarios(page: Page, no_results_terms: list = ["nonexistentterm123", "zzzzzzz", "!@#$%"]):
        """Test search scenarios with no results"""
        return do_test_no_results_scenarios(page, no_results_terms)
    
    # Filter helpers
    @staticmethod
    def test_filter_clearing(page: Page):
        """Test filter clearing functionality"""
        return do_test_filter_clearing_functionality(page)
    
    @staticmethod
    def test_all_clear_button(page: Page, test_filters: dict = None):
        """Test all clear button functionality"""
        return do_test_all_clear_button(page, test_filters)
    
    @staticmethod
    def test_multi_filter_combinations(page: Page, combinations: list):
        """Test multiple filter combinations"""
        return do_test_multi_filter_combinations(page, combinations)
    
    # File upload helpers
    @staticmethod
    def bulk_file_upload(page: Page, file_path: str, agency_id: str, email: str = "mi003b@onemail.host", password: str = "Kabir123#"):
        """Upload bulk JD file"""
        return do_bulk_jd_file_upload(page, file_path, agency_id, email, password)
    
    # Bulk operation helpers
    @staticmethod
    def bulk_selection(page: Page, jd_titles: list, agency_id: str, email: str = "mi003b@onemail.host", password: str = "Kabir123#"):
        """Select multiple JDs for bulk operations"""
        return do_bulk_jd_selection(page, jd_titles, agency_id, email, password)
    
    @staticmethod
    def bulk_deletion(page: Page, jd_titles: list, agency_id: str, email: str = "mi003b@onemail.host", password: str = "Kabir123#"):
        """Delete multiple JDs in bulk"""
        return do_bulk_jd_deletion(page, jd_titles, agency_id, email, password)
    
    @staticmethod
    def bulk_status_update(page: Page, jd_titles: list, new_status: str, agency_id: str, email: str = "mi003b@onemail.host", password: str = "Kabir123#"):
        """Update status of multiple JDs"""
        return do_bulk_status_update(page, jd_titles, new_status, agency_id, email, password)
    
    # Assertion helpers
    @staticmethod
    def assert_validation_errors(page: Page, expected_errors: list, test_name: str = "jd_edit_validation_errors"):
        """Assert JD validation errors are displayed"""
        return assert_jd_edit_validation_errors(page, expected_errors, test_name)
    
    @staticmethod
    def assert_search_count(page: Page, search_term: str, expected_count: int, test_name: str = "search_results_count"):
        """Assert search results count"""
        return assert_search_results_count(page, search_term, expected_count, test_name)
    
    @staticmethod
    def assert_filtered_count(page: Page, filters: dict, expected_count: int, test_name: str = "filtered_results_count"):
        """Assert filtered results count"""
        return assert_filtered_results_count(page, filters, expected_count, test_name)
    
    @staticmethod
    def assert_no_results(page: Page, search_term: str, test_name: str = "no_search_results"):
        """Assert no search results"""
        return assert_no_search_results(page, search_term, test_name)