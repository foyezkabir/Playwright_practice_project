# Add Client Modal - Complete Field Documentation

**Generated via MCP Chrome DevTools Browser Walkthrough**  
**Date:** Based on live inspection of https://bprp-qa.shadhinlab.xyz/agency/173/client-list/  
**Purpose:** Fix test locators and validation assertions for client CRUD tests

---

## Modal Structure

**Modal Heading:** "Add New Client" (level 2 heading)  
**Close Button:** "Close modal" button  
**Action Buttons:** "Cancel" and "Create"

---

## Text Input Fields

All text input fields use **labels** (not placeholders) and have a **maxLength of 50 characters**.

### 1. English First Name ⚠️ REQUIRED
- **Label:** `English First Name` (with red asterisk `*`)
- **Field Name:** `english_first_name`
- **Field ID:** `english_first_name`
- **Locator:** `page.get_by_label("English First Name")`
- **Max Length:** 50 characters
- **Validation Messages:**
  - Empty: `"First name is required"`
  - Min Length (< 3): `"First name must be at least 3 characters"`
  - Special Characters: `"First name can't accept special characters"`

### 2. English Last Name ⚠️ REQUIRED
- **Label:** `English Last Name` (with red asterisk `*`)
- **Field Name:** `english_last_name`
- **Field ID:** `english_last_name`
- **Locator:** `page.get_by_label("English Last Name")`
- **Max Length:** 50 characters
- **Validation Messages:**
  - Empty: `"Last name is required"`
  - Min Length (< 3): Expected similar to first name
  - Special Characters: Expected similar to first name

### 3. Japanese First Name
- **Label:** `Japanese First Name` (with red asterisk `*`)
- **Field Name:** `japanese_first_name`
- **Field ID:** `japanese_first_name`
- **Locator:** `page.get_by_label("Japanese First Name")`
- **Max Length:** 50 characters
- **Validation:** Similar validation expected as English first name

### 4. Japanese Last Name
- **Label:** `Japanese Last Name` (with red asterisk `*`)
- **Field Name:** `japanese_last_name`
- **Field ID:** `japanese_last_name`
- **Locator:** `page.get_by_label("Japanese Last Name")`
- **Max Length:** 50 characters
- **Validation:** Similar validation expected as English last name

### 5. Job Title
- **Label:** `Job title` (with red asterisk `*`)
- **Field Name:** `job_title`
- **Field ID:** `job_title`
- **Locator:** `page.get_by_label("Job title")`
- **Max Length:** 50 characters
- **Validation:** Likely has required validation

### 6. Phone Number
- **Label:** `Number` (with red asterisk `*`)
- **Field Name:** `phone_contacts[0].value`
- **Field ID:** `phone_contacts[0].value`
- **Locator:** `page.get_by_label("Number", exact=True)` (exact=True to avoid matching "Phone Numbers" heading)
- **Max Length:** 50 characters
- **Additional:** Phone label dropdown with label "Label"

---

## Dropdown Fields

All dropdown fields have labels with red asterisks indicating required status.

### 7. Gender ⚠️ REQUIRED
- **Label:** `Gender` (with red asterisk `*`)
- **Locator:** `page.get_by_label("Gender")`
- **Options:** Not captured (needs further testing)

### 8. Department ⚠️ REQUIRED
- **Label:** `Department` (with red asterisk `*`)
- **Locator:** `page.get_by_label("Department")`
- **Options:** Not captured (needs further testing)

### 9. Company ⚠️ REQUIRED
- **Label:** `Company` (with red asterisk `*`)
- **Locator:** `page.get_by_label("Company")`
- **Validation Messages:**
  - Empty: `"Company is required."`
- **Options:** Searchable dropdown (contains "Search..." placeholder)

### 10. English Level ⚠️ REQUIRED
- **Label:** `English Level` (with red asterisk `*`)
- **Locator:** `page.get_by_label("English Level")`
- **Options:** Not captured (needs further testing)

### 11. Japanese Level ⚠️ REQUIRED
- **Label:** `Japanese Level` (with red asterisk `*`)
- **Locator:** `page.get_by_label("Japanese Level")`
- **Options:** Not captured (needs further testing)

---

## Email Address Fields

### 12. Email ⚠️ REQUIRED (At Least One)
- **Label:** `Email` (with red asterisk `*`)
- **Field Name:** `email_contacts[0].email` (based on previous error message)
- **Locator:** `page.get_by_label("Email")`
- **Validation Messages:**
  - Empty: `"At least one email address is required"`
  - Invalid Format: `"Invalid email address"`
  - Label Required: `"Email name/label is required when address is provided"`
  - Public Domain: Expected to reject gmail.com, yahoo.com, etc. (needs testing)
- **Additional:** Email label dropdown with label "Label"
- **Button:** "+ Add Email Address" to add more email fields

---

## File Upload Field

### 13. Logo
- **Label:** `Logo`
- **Upload Text:** "Upload Logo"
- **Accepted Formats:** jpg, png, jpeg, gif (based on agency tests)
- **Max Size:** 5 MB (based on agency tests)
- **Validation Messages:**
  - Invalid Format: `"Only accept jpg, png, jpeg, gif file"`
  - Size Exceeded: `"File can't be larger than 5 MB"`

---

## Dynamic Field Sections

### Phone Numbers
- **Section Label:** "Phone Numbers"
- **Fields:** Label dropdown + Number textbox
- **Add Button:** "+ Add Phone Number"

### Email Addresses
- **Section Label:** "Email Addresses"
- **Fields:** Label dropdown + Email textbox
- **Add Button:** "+ Add Email Address"

---

## Validation Error Locators (Exact Text)

### Required Field Errors
```python
first_name_required_error = page.get_by_text("First name is required")
last_name_required_error = page.get_by_text("Last name is required")
company_required_error = page.get_by_text("Company is required.")
email_required_error = page.get_by_text("At least one email address is required")
```

### Field Constraint Errors
```python
first_name_min_length_error = page.get_by_text("First name must be at least 3 characters")
first_name_special_char_error = page.get_by_text("First name can't accept special characters")
invalid_email_error = page.get_by_text("Invalid email address")
email_label_required_error = page.get_by_text("Email name/label is required when address is provided")
```

### File Upload Errors (Expected, not tested)
```python
file_format_error = page.get_by_text("Only accept jpg, png, jpeg, gif file")
file_size_error = page.get_by_text("File can't be larger than 5 MB")
```

---

## Key Findings

1. **No Placeholders:** All input fields have `placeholder=None` - they use labels via `<label>` elements
2. **Label-Based Locators:** Must use `page.get_by_label()` not `page.get_by_placeholder()`
3. **Exact Text Matching:** Validation messages require exact text including punctuation
4. **Max Length:** All text inputs limited to 50 characters
5. **Required Fields:** Indicated by red asterisk `*` in label
6. **Dynamic Arrays:** Phone and email use array notation: `phone_contacts[0].value`, `email_contacts[0].email`
7. **Searchable Dropdown:** Company field has searchable dropdown (contains "Search..." text)
8. **Email Label Validation:** Email requires both address AND label to be filled

---

## Test Case Mapping

### TC_03: Create Client Without Any Information
- Check all required field errors appear:
  - `first_name_required_error`
  - `last_name_required_error`
  - `company_required_error`
  - `email_required_error`

### TC_04: Create Client Without Required Fields
- Same as TC_03 (test already passing)

### TC_05: Create Client With Invalid Email
- Fill first name, last name, company
- Fill email with invalid format (no @ symbol)
- Check: `invalid_email_error`

### TC_06: Create Client With Public Domain Email
- Fill first name, last name, company
- Fill email with @gmail.com
- Check for public domain rejection (message text needs discovery)

### TC_07: Min Length Validation
- Fill first name with 2 characters
- Check: `first_name_min_length_error`

### TC_08: Special Character Validation
- Fill first name starting with special character
- Check: `first_name_special_char_error`

---

## Updated Locator Recommendations

### Replace in `locators/loc_client.py`:
```python
# Text Input Fields - Use get_by_label
self.english_first_name_input = page.get_by_label("English First Name")
self.english_last_name_input = page.get_by_label("English Last Name")
self.japanese_first_name_input = page.get_by_label("Japanese First Name")
self.japanese_last_name_input = page.get_by_label("Japanese Last Name")
self.job_title_input = page.get_by_label("Job title")
self.phone_number_input = page.get_by_label("Number", exact=True)
self.email_input = page.get_by_label("Email")

# Dropdown Fields - Use get_by_label
self.gender_dropdown = page.get_by_label("Gender")
self.department_dropdown = page.get_by_label("Department")
self.company_dropdown = page.get_by_label("Company")
self.english_level_dropdown = page.get_by_label("English Level")
self.japanese_level_dropdown = page.get_by_label("Japanese Level")

# Validation Errors - Use get_by_text with exact text
self.first_name_required_error = page.get_by_text("First name is required")
self.last_name_required_error = page.get_by_text("Last name is required")
self.first_name_min_length_error = page.get_by_text("First name must be at least 3 characters")
self.first_name_special_char_error = page.get_by_text("First name can't accept special characters")
self.company_required_error = page.get_by_text("Company is required.")
self.email_required_error = page.get_by_text("At least one email address is required")
self.invalid_email_error = page.get_by_text("Invalid email address")
self.email_label_required_error = page.get_by_text("Email name/label is required when address is provided")
```

---

## Next Steps

1. ✅ Update `locators/loc_client.py` with all label-based locators
2. ✅ Update validation error locators with exact text
3. ⏳ Fix TC_03 company dropdown issue (use `get_by_label("Company")`)
4. ⏳ Fix TC_05 email clear issue (use `get_by_label("Email")`)
5. ⏳ Test dropdown options (Gender, Department, English/Japanese Level)
6. ⏳ Test public domain email rejection
7. ⏳ Test file upload validations
8. ⏳ Update all remaining test cases (TC_06-TC_26) with correct locators
