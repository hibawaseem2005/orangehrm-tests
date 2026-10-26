import re
from playwright.sync_api import Page, expect

LOGIN_URL = "/web/index.php/auth/login"

def test_valid_login(logged_in_page: Page):
    expect(logged_in_page).to_have_url(re.compile(r".*/dashboard/index"))
    expect(logged_in_page.get_by_role("heading", name="Dashboard")).to_be_visible()
    logged_in_page.wait_for_timeout(5000)   # remove before submitting

def test_invalid_password(page: Page):
    page.goto(LOGIN_URL)
    page.fill("input[name='username']", "Admin")
    page.fill("input[name='password']", "wrongpass")
    page.click("button[type='submit']")
    expect(page.get_by_text("Invalid credentials")).to_be_visible()
    expect(page).to_have_url(re.compile(r".*/auth/login"))
    page.wait_for_timeout(5000)   # remove before submitting

def test_empty_login(page: Page):
    page.goto(LOGIN_URL)
    page.click("button[type='submit']")
    expect(page.get_by_text("Required")).to_have_count(2)
    page.wait_for_timeout(5000)   # remove before submitting