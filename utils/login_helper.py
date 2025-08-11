
from playwright.sync_api import Page, expect
from utils.config import BASE_URL
from pages.login_page import LoginPage


def do_login(page: Page, email: str, password: str):
    login_page = LoginPage(page)
    login_page.navigate_to_landing_page(BASE_URL + "/login")
    # login_page.click_get_started()
    if email:
        login_page.fill_email(email)
    if password:
        login_page.fill_password(password)
    login_page.click_sign_in()
    return login_page