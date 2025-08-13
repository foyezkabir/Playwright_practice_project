# Test Case: Login and Agency Management Workflow

## Objective
Verify the end-to-end behavior of user login, agency modal handling, and full CRUD (Create, Read, Update, Delete) operations for agencies.

## Prerequisites
- URL: `https://bprp-qa.shadhinlab.xyz/`
- Credentials:
  - Email: `50st3o@mepost.pw`
  - Password: `Kabir123#`

---

## Test Steps

### 1. Setup and Login
- Open the browser and go to `https://bprp-qa.shadhinlab.xyz/`.
- Locate the email input field and enter `50st3o@mepost.pw`.
- Locate the password input field and enter `Kabir123#`.
- Click the submit button to log in.

---

### 2. Check for Agency Modal
- After login, check if the **"Create Agency" modal** is visible.
  - If it is visible, that means no agency exists yet.
    - In the modal, find the agency name input field and enter `New Agency`.
    - Click the submit button to create the agency.
    - Confirm that the system redirects to the agency details page.
    - On that page, check for the text:  
      `"Dashboard - This is a protected route for authenticated users only."`
    - Use the go_back to return to the All Agencies page.
    - Wait for the page to fully load.
  - If the modal is not visible, that means an agency already exists. Proceed to the next step.

---

### 3. Edit the Agency
- On the All Agencies page, find the agency card that contains the text `New Agency`.
- Inside that card, find the three-dot menu button (it might be labeled "menu" or have a class like "dots" or "kebab").
- Click that button to open the menu.
- Wait for the dropdown menu to appear.
- Click the "Edit" option in the menu.
- In the edit form, change the agency name to `edited agency`.
- Save the changes.
- Wait for the page to reload.
- Confirm that the agency card now displays the updated name: `edited agency`.

---

### 4. Delete the Agency
- On the All Agencies page, find the agency card that contains the text `edited agency`.
- Click the three-dot menu button in that card.
- Wait for the dropdown menu to appear.
- Click the "Delete" option in the menu.
- If a confirmation dialog appears, confirm the deletion.
- Verify that the agency card is no longer visible on the page.
- Confirm that the **"Create Agency" modal** appears again, indicating no agencies remain.

---

## Expected Outcomes

### ✅ Login
- User is authenticated successfully.

### ✅ Modal Handling
- Modal appears if no agency exists.
- Modal does not appear if an agency exists.

### ✅ Agency Creation
- Agency is created successfully.
- System redirects to agency details page with correct message.

### ✅ Agency Editing
- Agency name is updated and reflected on the All Agencies page.

### ✅ Agency Deletion
- Agency is removed.
- Create Agency modal reappears.

---

## Notes
- This test case covers the full agency lifecycle.
- Ensure that the browser is fully loaded and stable before proceeding to each step.
- Test environment must be clean or reset if agency data persists across sessions.

---

## Author
Automated Test Case  
Generated for QA and development use.