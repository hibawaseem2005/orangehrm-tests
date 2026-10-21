import pytest

BASE = "https://opensource-demo.orangehrmlive.com"

@pytest.fixture
def logged_in_page(page):
    page.goto(f"{BASE}/web/index.php/auth/login")
    page.fill("input[name='username']", "Admin")
    page.fill("input[name='password']", "admin123")
    page.click("button[type='submit']")
    page.wait_for_url("**/dashboard/index")
    return page