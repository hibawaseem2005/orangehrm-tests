import pytest

@pytest.fixture
def logged_in_page(page):
    page.goto("/web/index.php/auth/login")
    page.fill("input[name='username']", "Admin")
    page.fill("input[name='password']", "admin123")
    page.click("button[type='submit']")
    page.wait_for_url("**/dashboard/index")
    return page