from playwright.sync_api import Page, expect

def test_search_existing_employee(page: Page):
    # 1. Login
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    
    # 2. Search Positive (Use a real name like "Peter")
    page.get_by_role("link", name="PIM").click()
    page.get_by_placeholder("Type for hints...").first.fill("Peter")
    page.get_by_role("button", name="Search").click()
    
    # 3. Verify Result (Wait for the table to load and show Peter)
    expect(page.get_by_text("Peter").first).to_be_visible(timeout=10000)


def test_search_nonsense_employee(page: Page):
    # 1. Login
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    
    # 2. Search Negative
    page.get_by_role("link", name="PIM").click()
    page.get_by_placeholder("Type for hints...").first.fill("XYZRandomName123")
    page.get_by_role("button", name="Search").click()
    
    # 3. Verify "No Records Found"
    expect(page.get_by_text("No Records Found").first).to_be_visible(timeout=10000)