"""
Signup Helper Module
Contains utility functions for signup tests
"""

import pytest
from playwright.sync_api import Page
from pages.signup_page import SignupPage
from utils.config import BASE_URL
from random_values_generator.random_email import RandomEmail

# Initialize random email generator
random_email = RandomEmail()

def do_signup(page: Page, full_name: str = None, email: str = None, password: str = None, confirm_password: str = None):
    """
    Helper function to fill signup form with specified data and click signup button
    Similar to do_login helper for login tests
    
    Args:
        page: Playwright page object
        full_name: Full name to fill (optional)
        email: Email to fill (optional) 
        password: Password to fill (optional)
        confirm_password: Confirm password to fill (optional)
    
    Returns:
        SignupPage instance
    """
    signup_page = SignupPage(page)
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")
    
    if full_name:
        signup_page.fill_full_name(full_name)
    if email:
        signup_page.fill_email(email)
    if password:
        signup_page.fill_password(password)
    if confirm_password:
        signup_page.fill_confirm_password(confirm_password)
    
    signup_page.click_sign_up_button()
    return signup_page

def fill_valid_signup_form(signup_page, email=None):
    """
    Helper function to fill signup form with valid data (without clicking signup button)
    """
    if email is None:
        email = random_email.generate_email()
    
    signup_page.fill_full_name("John Doe")
    signup_page.fill_email(email)
    signup_page.fill_password("Kabir123#")
    signup_page.fill_confirm_password("Kabir123#")
    return email

def navigate_to_signup_page(signup_page):
    """
    Helper function to navigate to signup page
    """
    signup_page.navigate_to_landing_page(BASE_URL + "/sign-up")

def navigate_to_landing_and_signup(signup_page):
    """
    Helper function to navigate from landing page to signup
    """
    signup_page.navigate_to_landing_page(BASE_URL)
    signup_page.click_get_started()
    signup_page.click_sign_in_link()
