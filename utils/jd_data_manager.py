"""
JD Data Management Utilities
Provides data cleanup, isolation, and management strategies for JD testing
"""

import os
import json
import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from random_values_generator.random_jd_data import JDTestData


class JDDataManager:
    """
    Manages JD test data lifecycle including creation, tracking, and cleanup
    """
    
    def __init__(self, test_session_id: str = None):
        """
        Initialize JD data manager
        
        Args:
            test_session_id: Unique identifier for test session
        """
        self.test_session_id = test_session_id or f"session_{int(time.time())}"
        self.data_dir = "test_data/jd_sessions"
        self.session_file = os.path.join(self.data_dir, f"{self.test_session_id}.json")
        self.created_jds = []
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def track_created_jd(self, jd_data: JDTestData, jd_id: str = None):
        """
        Track a JD that was created during testing
        
        Args:
            jd_data: The JD data that was used to create the JD
            jd_id: The ID of the created JD (if available)
        """
        jd_record = {
            'jd_id': jd_id,
            'position_title': jd_data.position_title,
            'company': jd_data.company,
            'created_at': datetime.now().isoformat(),
            'test_session': self.test_session_id
        }
        
        self.created_jds.append(jd_record)
        self.save_session_data()
    
    def save_session_data(self):
        """Save current session data to file"""
        session_data = {
            'session_id': self.test_session_id,
            'created_at': datetime.now().isoformat(),
            'created_jds': self.created_jds
        }
        
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
    
    def load_session_data(self) -> Dict:
        """Load session data from file"""
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                return json.load(f)
        return {}
    
    def get_created_jds(self) -> List[Dict]:
        """Get list of JDs created in this session"""
        return self.created_jds.copy()
    
    def cleanup_session_data(self):
        """Clean up session data file"""
        if os.path.exists(self.session_file):
            os.remove(self.session_file)
    
    def get_all_test_sessions(self) -> List[str]:
        """Get all test session files"""
        if not os.path.exists(self.data_dir):
            return []
        
        return [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
    
    def cleanup_old_sessions(self, days_old: int = 7):
        """
        Clean up test session files older than specified days
        
        Args:
            days_old: Number of days after which to clean up sessions
        """
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        for session_file in self.get_all_test_sessions():
            file_path = os.path.join(self.data_dir, session_file)
            file_time = datetime.fromtimestamp(os.path.getctime(file_path))
            
            if file_time < cutoff_date:
                os.remove(file_path)
                print(f"Cleaned up old test session: {session_file}")


class JDTestDataIsolation:
    """
    Provides data isolation strategies for parallel test execution
    """
    
    @staticmethod
    def get_isolated_test_data(test_name: str, worker_id: str = None) -> JDTestData:
        """
        Generate isolated test data for a specific test
        
        Args:
            test_name: Name of the test function
            worker_id: Worker ID for parallel execution (pytest-xdist)
            
        Returns:
            JDTestData: Isolated test data
        """
        from random_values_generator.random_jd_data import generate_complete_jd_data
        
        # Create unique identifier for this test instance
        timestamp = str(int(time.time() * 1000))  # Millisecond precision
        worker_suffix = f"_{worker_id}" if worker_id else ""
        test_suffix = f"_{test_name.replace('test_', '')}"
        
        # Generate base data
        jd_data = generate_complete_jd_data()
        
        # Make it unique for this test instance
        jd_data.position_title = f"{jd_data.position_title}{test_suffix}{worker_suffix}_{timestamp}"
        jd_data.company = f"{jd_data.company}{worker_suffix}_{timestamp}"
        
        return jd_data
    
    @staticmethod
    def get_isolated_search_data(test_name: str, worker_id: str = None) -> Dict:
        """
        Generate isolated search test data
        
        Args:
            test_name: Name of the test function
            worker_id: Worker ID for parallel execution
            
        Returns:
            dict: Isolated search test data
        """
        from random_values_generator.random_jd_data import generate_search_test_data
        
        timestamp = str(int(time.time() * 1000))
        worker_suffix = f"_{worker_id}" if worker_id else ""
        
        search_data = generate_search_test_data()
        
        # Make search terms unique
        for key, jd_data in search_data.items():
            jd_data.position_title = f"{jd_data.position_title}{worker_suffix}_{timestamp}"
            jd_data.company = f"{jd_data.company}{worker_suffix}_{timestamp}"
        
        return search_data
    
    @staticmethod
    def get_isolated_filter_data(test_name: str, worker_id: str = None) -> Dict:
        """
        Generate isolated filter test data
        
        Args:
            test_name: Name of the test function
            worker_id: Worker ID for parallel execution
            
        Returns:
            dict: Isolated filter test data
        """
        from random_values_generator.random_jd_data import generate_filter_test_data
        
        timestamp = str(int(time.time() * 1000))
        worker_suffix = f"_{worker_id}" if worker_id else ""
        
        filter_data = generate_filter_test_data()
        
        # Make filter data unique
        for key, jd_data in filter_data.items():
            jd_data.position_title = f"{jd_data.position_title}{worker_suffix}_{timestamp}"
            jd_data.company = f"{jd_data.company}{worker_suffix}_{timestamp}"
        
        return filter_data


class JDTestDataValidator:
    """
    Validates JD test data before use in tests
    """
    
    @staticmethod
    def validate_required_fields(jd_data: JDTestData) -> Dict[str, bool]:
        """
        Validate that required fields are present and valid
        
        Args:
            jd_data: JD data to validate
            
        Returns:
            dict: Validation results
        """
        return {
            'position_title_valid': bool(jd_data.position_title and jd_data.position_title.strip()),
            'company_valid': bool(jd_data.company and jd_data.company.strip()),
            'work_style_valid': bool(jd_data.work_style and jd_data.work_style.strip()),
            'workplace_valid': bool(jd_data.workplace and jd_data.workplace.strip())
        }
    
    @staticmethod
    def validate_salary_range(jd_data: JDTestData) -> bool:
        """
        Validate salary range if both min and max are provided
        
        Args:
            jd_data: JD data to validate
            
        Returns:
            bool: True if salary range is valid or not provided
        """
        if jd_data.min_salary is not None and jd_data.max_salary is not None:
            return jd_data.max_salary > jd_data.min_salary
        return True
    
    @staticmethod
    def validate_age_range(jd_data: JDTestData) -> bool:
        """
        Validate age range if both min and max are provided
        
        Args:
            jd_data: JD data to validate
            
        Returns:
            bool: True if age range is valid or not provided
        """
        if jd_data.job_age_min is not None and jd_data.job_age_max is not None:
            return jd_data.job_age_max > jd_data.job_age_min
        return True
    
    @staticmethod
    def validate_complete_jd_data(jd_data: JDTestData) -> Dict[str, bool]:
        """
        Perform complete validation of JD data
        
        Args:
            jd_data: JD data to validate
            
        Returns:
            dict: Complete validation results
        """
        required_fields = JDTestDataValidator.validate_required_fields(jd_data)
        
        validation_results = {
            **required_fields,
            'salary_range_valid': JDTestDataValidator.validate_salary_range(jd_data),
            'age_range_valid': JDTestDataValidator.validate_age_range(jd_data),
            'overall_valid': True
        }
        
        # Check overall validity
        validation_results['overall_valid'] = all(validation_results.values())
        
        return validation_results


class JDTestDataSetup:
    """
    Provides setup and teardown utilities for JD test data
    """
    
    def __init__(self, data_manager: JDDataManager):
        """
        Initialize with data manager
        
        Args:
            data_manager: JD data manager instance
        """
        self.data_manager = data_manager
    
    def setup_test_jds(self, jd_data_list: List[JDTestData]) -> List[str]:
        """
        Setup JDs for testing (would create them via API if available)
        
        Args:
            jd_data_list: List of JD data to create
            
        Returns:
            list: List of created JD IDs
        """
        created_ids = []
        
        for jd_data in jd_data_list:
            # In a real implementation, this would call the API to create JDs
            # For now, we'll simulate by generating IDs and tracking
            jd_id = f"jd_{int(time.time() * 1000)}"
            created_ids.append(jd_id)
            
            # Track the created JD
            self.data_manager.track_created_jd(jd_data, jd_id)
        
        return created_ids
    
    def teardown_test_jds(self, jd_ids: List[str]):
        """
        Teardown JDs after testing (would delete them via API if available)
        
        Args:
            jd_ids: List of JD IDs to delete
        """
        for jd_id in jd_ids:
            # In a real implementation, this would call the API to delete JDs
            print(f"Would delete JD: {jd_id}")
    
    def setup_search_scenario(self, search_data: Dict) -> Dict[str, str]:
        """
        Setup JDs for search testing scenario
        
        Args:
            search_data: Search test data
            
        Returns:
            dict: Mapping of data keys to created JD IDs
        """
        created_mapping = {}
        
        for key, jd_data in search_data.items():
            jd_id = self.setup_test_jds([jd_data])[0]
            created_mapping[key] = jd_id
        
        return created_mapping
    
    def setup_filter_scenario(self, filter_data: Dict) -> Dict[str, str]:
        """
        Setup JDs for filter testing scenario
        
        Args:
            filter_data: Filter test data
            
        Returns:
            dict: Mapping of data keys to created JD IDs
        """
        created_mapping = {}
        
        for key, jd_data in filter_data.items():
            jd_id = self.setup_test_jds([jd_data])[0]
            created_mapping[key] = jd_id
        
        return created_mapping


# Utility functions for easy access
def get_jd_data_manager(test_session_id: str = None) -> JDDataManager:
    """
    Get a JD data manager instance
    
    Args:
        test_session_id: Optional session ID
        
    Returns:
        JDDataManager: Data manager instance
    """
    return JDDataManager(test_session_id)


def get_isolated_jd_data(test_name: str, worker_id: str = None) -> JDTestData:
    """
    Get isolated JD test data for a specific test
    
    Args:
        test_name: Name of the test function
        worker_id: Worker ID for parallel execution
        
    Returns:
        JDTestData: Isolated test data
    """
    return JDTestDataIsolation.get_isolated_test_data(test_name, worker_id)


def validate_jd_test_data(jd_data: JDTestData) -> Dict[str, bool]:
    """
    Validate JD test data
    
    Args:
        jd_data: JD data to validate
        
    Returns:
        dict: Validation results
    """
    return JDTestDataValidator.validate_complete_jd_data(jd_data)


def cleanup_old_test_sessions(days_old: int = 7):
    """
    Clean up old test session files
    
    Args:
        days_old: Number of days after which to clean up sessions
    """
    manager = JDDataManager()
    manager.cleanup_old_sessions(days_old)