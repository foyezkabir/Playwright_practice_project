"""
JD File Test Helper
Utilities for managing test files in JD upload testing scenarios
"""

import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class JDFileTestHelper:
    """
    Helper class for managing JD test files and upload scenarios
    """
    
    def __init__(self):
        """Initialize with test files directory"""
        self.test_files_dir = Path("images_for_test/jd_files")
        self.ensure_test_files_directory()
        
        # Define file categories for testing
        self.valid_files = {
            "valid_jd_document.txt": "Valid JD document with proper format",
            "small_jd_file.txt": "Small valid JD file for size testing",
            "bulk_jd_data.csv": "CSV file with multiple JD entries"
        }
        
        self.invalid_files = {
            "invalid_format.xyz": "File with unsupported format",
            "corrupted_data.txt": "File with corrupted/invalid data",
            "invalid_csv_data.csv": "CSV with invalid data structure"
        }
        
        self.size_test_files = {
            "empty_file.txt": "Empty file for size validation",
            "large_jd_file.txt": "Large file for size limit testing"
        }
        
        self.special_files = {
            "special_characters.txt": "File with special characters in content",
            "test_document.json": "JSON format file for format testing"
        }
    
    def ensure_test_files_directory(self):
        """Ensure test files directory exists"""
        self.test_files_dir.mkdir(parents=True, exist_ok=True)
    
    def get_test_file_path(self, filename: str) -> str:
        """
        Get full path to a test file
        
        Args:
            filename: Name of the test file
            
        Returns:
            str: Full path to the test file
        """
        return str(self.test_files_dir / filename)
    
    def get_valid_file_path(self, file_type: str = "default") -> str:
        """
        Get path to a valid test file
        
        Args:
            file_type: Type of valid file needed ("default", "small", "bulk")
            
        Returns:
            str: Full path to valid test file
        """
        file_map = {
            "default": "valid_jd_document.txt",
            "small": "small_jd_file.txt", 
            "bulk": "bulk_jd_data.csv"
        }
        filename = file_map.get(file_type, "valid_jd_document.txt")
        return self.get_test_file_path(filename)
    
    def get_invalid_file_path(self, error_type: str = "format") -> str:
        """
        Get path to an invalid test file
        
        Args:
            error_type: Type of invalid file ("format", "corrupted", "data")
            
        Returns:
            str: Full path to invalid test file
        """
        file_map = {
            "format": "invalid_format.xyz",
            "corrupted": "corrupted_data.txt",
            "data": "invalid_csv_data.csv"
        }
        filename = file_map.get(error_type, "invalid_format.xyz")
        return self.get_test_file_path(filename)
    
    def get_size_test_file_path(self, size_type: str = "empty") -> str:
        """
        Get path to size-specific test file
        
        Args:
            size_type: Type of size test ("empty", "large")
            
        Returns:
            str: Full path to size test file
        """
        file_map = {
            "empty": "empty_file.txt",
            "large": "large_jd_file.txt"
        }
        filename = file_map.get(size_type, "empty_file.txt")
        return self.get_test_file_path(filename)
    
    def get_special_file_path(self, special_type: str = "characters") -> str:
        """
        Get path to special test file
        
        Args:
            special_type: Type of special file ("characters", "json")
            
        Returns:
            str: Full path to special test file
        """
        file_map = {
            "characters": "special_characters.txt",
            "json": "test_document.json"
        }
        filename = file_map.get(special_type, "special_characters.txt")
        return self.get_test_file_path(filename)
    
    def file_exists(self, filename: str) -> bool:
        """
        Check if test file exists
        
        Args:
            filename: Name of the test file
            
        Returns:
            bool: True if file exists, False otherwise
        """
        file_path = self.test_files_dir / filename
        return file_path.exists()
    
    def get_file_size(self, filename: str) -> int:
        """
        Get size of test file in bytes
        
        Args:
            filename: Name of the test file
            
        Returns:
            int: File size in bytes, 0 if file doesn't exist
        """
        file_path = self.test_files_dir / filename
        if file_path.exists():
            return file_path.stat().st_size
        return 0
    
    def get_file_extension(self, filename: str) -> str:
        """
        Get file extension
        
        Args:
            filename: Name of the test file
            
        Returns:
            str: File extension (e.g., '.txt', '.csv')
        """
        return Path(filename).suffix
    
    def is_valid_format(self, filename: str) -> bool:
        """
        Check if file has valid format for JD upload
        
        Args:
            filename: Name of the test file
            
        Returns:
            bool: True if format is valid, False otherwise
        """
        valid_extensions = ['.txt', '.csv', '.pdf', '.doc', '.docx']
        return self.get_file_extension(filename).lower() in valid_extensions
    
    def get_all_test_files(self) -> Dict[str, List[str]]:
        """
        Get all available test files organized by category
        
        Returns:
            Dict[str, List[str]]: Dictionary with file categories and file lists
        """
        return {
            "valid_files": list(self.valid_files.keys()),
            "invalid_files": list(self.invalid_files.keys()),
            "size_test_files": list(self.size_test_files.keys()),
            "special_files": list(self.special_files.keys())
        }
    
    def get_file_info(self, filename: str) -> Dict[str, any]:
        """
        Get comprehensive information about a test file
        
        Args:
            filename: Name of the test file
            
        Returns:
            Dict[str, any]: File information including path, size, format, etc.
        """
        file_path = self.get_test_file_path(filename)
        
        # Determine file category
        category = "unknown"
        description = "Unknown file"
        
        if filename in self.valid_files:
            category = "valid"
            description = self.valid_files[filename]
        elif filename in self.invalid_files:
            category = "invalid"
            description = self.invalid_files[filename]
        elif filename in self.size_test_files:
            category = "size_test"
            description = self.size_test_files[filename]
        elif filename in self.special_files:
            category = "special"
            description = self.special_files[filename]
        
        return {
            "filename": filename,
            "path": file_path,
            "exists": self.file_exists(filename),
            "size": self.get_file_size(filename),
            "extension": self.get_file_extension(filename),
            "is_valid_format": self.is_valid_format(filename),
            "category": category,
            "description": description
        }
    
    def validate_upload_scenario(self, filename: str) -> Tuple[bool, str]:
        """
        Validate if file is suitable for upload testing scenario
        
        Args:
            filename: Name of the test file
            
        Returns:
            Tuple[bool, str]: (is_valid, validation_message)
        """
        if not self.file_exists(filename):
            return False, f"File '{filename}' does not exist"
        
        file_size = self.get_file_size(filename)
        if file_size == 0:
            return False, f"File '{filename}' is empty"
        
        if not self.is_valid_format(filename):
            return False, f"File '{filename}' has invalid format"
        
        # Check if file is too large (assuming 10MB limit)
        max_size = 10 * 1024 * 1024  # 10MB in bytes
        if file_size > max_size:
            return False, f"File '{filename}' exceeds size limit ({file_size} bytes)"
        
        return True, f"File '{filename}' is valid for upload testing"
    
    def get_upload_test_scenarios(self) -> Dict[str, Dict[str, str]]:
        """
        Get predefined upload test scenarios with expected outcomes
        
        Returns:
            Dict[str, Dict[str, str]]: Test scenarios with file paths and expected results
        """
        return {
            "valid_upload": {
                "file": self.get_valid_file_path("default"),
                "expected_result": "success",
                "description": "Valid file upload should succeed"
            },
            "invalid_format": {
                "file": self.get_invalid_file_path("format"),
                "expected_result": "format_error",
                "description": "Invalid format should show format error"
            },
            "empty_file": {
                "file": self.get_size_test_file_path("empty"),
                "expected_result": "size_error",
                "description": "Empty file should show size error"
            },
            "large_file": {
                "file": self.get_size_test_file_path("large"),
                "expected_result": "size_error",
                "description": "Large file should show size limit error"
            },
            "corrupted_data": {
                "file": self.get_invalid_file_path("corrupted"),
                "expected_result": "data_error",
                "description": "Corrupted data should show validation error"
            },
            "bulk_upload": {
                "file": self.get_valid_file_path("bulk"),
                "expected_result": "success",
                "description": "Bulk CSV upload should succeed"
            }
        }
   