# Copilot Instructions for Black Pigeon Automation Project

## Project Overview
- This is an end-to-end test automation suite for the Black Pigeon web app, built with Playwright and Pytest.
- Major components: `pages/` (page objects), `locators/` (selectors), `tests/` (test cases), `utils/` (helpers), `random_values_generator/` (random data), `screenshots/` (test artifacts).
- Tests cover login, signup, agency CRUD, email verification, password reset, and more.

## Key Patterns & Conventions
- **Page Object Model:** All browser actions are abstracted in classes under `pages/` (e.g., `AgencyPage`). Use these for navigation, form filling, and assertions.
- **Locators:** Centralized in `locators/` (e.g., `loc_agency.py`). Always use locator objects from these files for selectors.
- **Test Naming:** All test files and functions use the `test_` prefix. Example: `test_agency_04_verify_create_new_agency_functionality`.
- **Random Data:** Use `random_values_generator/` for generating unique emails, agency names, etc. Import these utilities in tests to avoid collisions.
- **Screenshots:** On failure, screenshots are saved in `screenshots/` (organized by feature).
- **Configuration:** All pytest and Playwright options are set in `pytest.ini`. Do not hardcode browser or slowmo settings in tests.

## Developer Workflows
- **Environment Setup:**
  - Create a venv: `python -m venv venv` and activate it.
  - Install dependencies: `pip install -r requirements.txt`
  - Install Playwright browsers: `python -m playwright install`
- **Running Tests:**
  - Run all tests: `pytest`
  - Run a specific test: `pytest -k <test_name>`
  - View HTML report: open `report.html` after test run.
- **Debugging:**
  - Use `--slowmo` and `--browser` options in `pytest.ini` for step-by-step debugging.
  - Screenshots and HTML reports are generated automatically for failures.

## Integration Points
- **Playwright:** Used for browser automation. All browser actions go through Playwright's sync API.
- **Pytest:** Test runner and reporting. Custom markers and options in `pytest.ini`.
- **External Data:** Test data (e.g., login credentials) may be read from `inputs/` (e.g., Excel files).

## Examples
- To add a new test for agency creation, use the page object from `pages/agency_page.py` and locators from `locators/loc_agency.py`. Generate a random name using `random_values_generator/random_agency_name.py`.
- To assert UI state, use Playwright's `expect` with locators from the page object.

## Special Notes
- Always use the page object and locator pattern—do not use raw selectors in tests.
- Do not modify browser settings in test files; use `pytest.ini`.
- All test artifacts (screenshots, reports) are saved in the project root or `screenshots/`.

---
For more details, see `README.md` and `pytest.ini`. If conventions change, update this file to keep Copilot agents productive.
