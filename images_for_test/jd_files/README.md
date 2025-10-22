# JD Test Files Documentation

This directory contains various test files for JD (Job Description) upload functionality testing.

## File Categories

### Valid Files

#### `valid_jd_document.txt`
- **Purpose**: Standard valid JD document for successful upload testing
- **Size**: ~1.5KB
- **Format**: Plain text
- **Content**: Complete job description with all standard sections
- **Expected Result**: Should upload successfully

#### `small_jd_file.txt`
- **Purpose**: Test minimum file size requirements
- **Size**: ~150 bytes
- **Format**: Plain text
- **Content**: Minimal JD information
- **Expected Result**: Should upload successfully (if no minimum size limit) or show appropriate error

#### `bulk_jd_data.csv`
- **Purpose**: Bulk JD upload testing with valid CSV data
- **Size**: ~1KB
- **Format**: CSV
- **Content**: 10 valid JD records with all required fields
- **Expected Result**: Should process all records successfully

#### `test_document.json`
- **Purpose**: Test JSON format support (if supported)
- **Size**: ~800 bytes
- **Format**: JSON
- **Content**: Structured JD data in JSON format
- **Expected Result**: Should upload successfully if JSON is supported format

#### `special_characters.txt`
- **Purpose**: Test handling of special characters and Unicode
- **Size**: ~1.2KB
- **Format**: Plain text with Unicode characters
- **Content**: JD with various special characters, symbols, and Unicode
- **Expected Result**: Should handle special characters correctly

### Invalid Files

#### `invalid_format.xyz`
- **Purpose**: Test file format validation
- **Size**: ~200 bytes
- **Format**: Invalid extension (.xyz)
- **Content**: Valid JD content but wrong file extension
- **Expected Result**: Should reject with "Invalid file format" error

#### `empty_file.txt`
- **Purpose**: Test empty file handling
- **Size**: 0 bytes
- **Format**: Plain text (empty)
- **Content**: No content
- **Expected Result**: Should reject with "Empty file" or "No content" error

#### `corrupted_data.txt`
- **Purpose**: Test corrupted/malformed data handling
- **Size**: ~600 bytes
- **Format**: Plain text with corrupted characters
- **Content**: JD with invalid characters and corrupted data
- **Expected Result**: Should show parsing errors or data validation errors

#### `large_jd_file.txt`
- **Purpose**: Test file size limits
- **Size**: ~15KB (large content)
- **Format**: Plain text
- **Content**: Extremely detailed JD document
- **Expected Result**: Should upload successfully if under size limit, or show "File too large" error

#### `invalid_csv_data.csv`
- **Purpose**: Test CSV data validation
- **Size**: ~800 bytes
- **Format**: CSV with invalid data
- **Content**: CSV with missing required fields, invalid data types, and format errors
- **Expected Result**: Should show specific validation errors for each invalid row

## Test Scenarios

### File Format Testing
1. Upload `valid_jd_document.txt` - should succeed
2. Upload `invalid_format.xyz` - should fail with format error
3. Upload `test_document.json` - depends on supported formats

### File Size Testing
1. Upload `small_jd_file.txt` - test minimum size handling
2. Upload `large_jd_file.txt` - test maximum size limits
3. Upload `empty_file.txt` - test empty file handling

### Data Validation Testing
1. Upload `bulk_jd_data.csv` - should process all valid records
2. Upload `invalid_csv_data.csv` - should show validation errors
3. Upload `corrupted_data.txt` - should handle corrupted data gracefully

### Character Encoding Testing
1. Upload `special_characters.txt` - test Unicode and special character support

### Error Handling Testing
1. Upload non-existent file - test file not found error
2. Upload file during network interruption - test network error handling
3. Upload multiple files simultaneously - test concurrent upload handling

## Expected File Format Support

Based on typical JD systems, the following formats are commonly supported:
- `.txt` - Plain text files
- `.csv` - Comma-separated values for bulk upload
- `.pdf` - PDF documents (not included in test files)
- `.doc/.docx` - Microsoft Word documents (not included in test files)

## File Size Limits

Typical file size limits for JD uploads:
- Minimum: Usually no minimum or very small (1KB)
- Maximum: Usually 5-10MB for documents, 1-2MB for bulk data files

## Usage in Tests

These files should be used in automated tests as follows:

```python
# Example usage in test cases
def test_valid_file_upload():
    file_path = "images_for_test/jd_files/valid_jd_document.txt"
    # Upload file and verify success

def test_invalid_format_rejection():
    file_path = "images_for_test/jd_files/invalid_format.xyz"
    # Upload file and verify format error

def test_bulk_upload():
    file_path = "images_for_test/jd_files/bulk_jd_data.csv"
    # Upload CSV and verify all records processed
```

## Maintenance

- Update file contents periodically to reflect current JD standards
- Add new test files as new scenarios are identified
- Remove or update files that become obsolete
- Ensure file sizes remain appropriate for testing purposes

## Notes

- All files are designed to be small enough for quick test execution
- File contents are realistic but fictional
- Files are safe to use in automated testing environments
- No sensitive or real company information is included