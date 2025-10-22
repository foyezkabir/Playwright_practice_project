"""
JD Test Data Class
Organized wrapper for all JD test data generation functions
"""

from random_values_generator.random_jd_data import (
    generate_complete_jd_data,
    generate_invalid_jd_data_cases,
    generate_position_title,
    generate_workplace_location,
    generate_minimal_jd_data,
    generate_multiple_jd_data,
    generate_bulk_jd_data,
    generate_search_test_data,
    generate_filter_test_data,
    generate_edge_case_jd_data,
    JDTestData
)


class JDTestData:
    """
    Organized wrapper class for all JD test data generation functions
    """
    
    @staticmethod
    def complete():
        """Generate complete JD data with all fields"""
        return generate_complete_jd_data()
    
    @staticmethod
    def minimal():
        """Generate minimal JD data with only required fields"""
        return generate_minimal_jd_data()
    
    @staticmethod
    def invalid_cases():
        """Generate invalid JD data cases for validation testing"""
        return generate_invalid_jd_data_cases()
    
    @staticmethod
    def multiple(count: int = 5):
        """Generate multiple JD data sets"""
        return generate_multiple_jd_data(count)
    
    @staticmethod
    def bulk(count: int = 20):
        """Generate bulk JD data for performance testing"""
        return generate_bulk_jd_data(count)
    
    @staticmethod
    def for_search():
        """Generate JD data specifically for search testing"""
        return generate_search_test_data()
    
    @staticmethod
    def for_filters():
        """Generate JD data specifically for filter testing"""
        return generate_filter_test_data()
    
    @staticmethod
    def edge_cases():
        """Generate edge case JD data for validation testing"""
        return generate_edge_case_jd_data()
    
    @staticmethod
    def position_title():
        """Generate random position title"""
        return generate_position_title()
    
    @staticmethod
    def workplace_location():
        """Generate random workplace location"""
        return generate_workplace_location()


# Import the original JDTestData class for type hints
from random_values_generator.random_jd_data import JDTestData as JDDataClass