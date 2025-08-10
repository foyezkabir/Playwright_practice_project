# Black Pigeon Automation Project

This project automates end-to-end testing for the Black Pigeon web application using Playwright and Pytest.

## Features
- Automated browser tests for login, signup, agency management, email verification, password reset, and more
- Screenshots on test failures
- HTML test reports
- Random data generation for test isolation

## Project Structure
```
├── complete_automation.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── report.html
├── inputs/
├── locators/
├── pages/
├── random_values_generator/
├── screenshots/
├── tests/
├── utils/
```

## Setup Instructions

### 1. Clone the Repository
```powershell
git clone <your-repo-url>
cd "Projects - Shadhin/black pigeon"
```

### 2. Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

### 3. Install Requirements
```powershell
pip install -r requirements.txt
```

### 4. Install Playwright Browsers
```powershell
python -m playwright install
```

### 5. Run Tests
```powershell
pytest
```
Or for a specific test:
```powershell
pytest -k test_agency_04_verify_create_new_agency_functionality
```

### 6. View HTML Report
After running tests, open `report.html` in your browser.

## Notes
- All test configuration is in `pytest.ini`.
- Screenshots are saved in the `screenshots/` folder on failures.
- You can adjust browser type and slowmo in `pytest.ini`.

## Troubleshooting
- If Playwright browsers are not installed, run `python -m playwright install` again.
- If you see import errors, ensure your virtual environment is activated.

## Useful Links
- [Playwright Python Docs](https://playwright.dev/python/docs/intro)
- [Pytest Docs](https://docs.pytest.org/en/stable/)

---
For any issues, please contact the project maintainer.
