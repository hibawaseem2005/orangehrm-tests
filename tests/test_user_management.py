from playwright.sync_api import Page, expect

def test_user_management_search(page: Page):
    # Login (Timeout barhaya hai taaki slow internet par load ho jaye)
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login", timeout=60000)
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    
    # User Management Positive Search
    page.get_by_role("link", name="Admin").click()
    page.get_by_placeholder("Type for hints...").first.fill("Admin")
    page.get_by_role("button", name="Search").click()
    expect(page.get_by_text("Admin").first).to_be_visible(timeout=15000)

def test_user_management_empty_fields(page: Page):
    # Login
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login", timeout=60000)
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    
    # User Management Negative (Empty Fields)
    page.get_by_role("link", name="Admin").click()
    page.get_by_role("button", name="Add").click()
    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("Required").first).to_be_visible(timeout=15000)

def test_user_management_password_mismatch(page: Page):
    # Login
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login", timeout=60000)
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    
    # User Management Negative (Mismatched Passwords)
    page.get_by_role("link", name="Admin").click()
    page.get_by_role("button", name="Add").click()
    
    # Password fields fill karein (Wait for page to load)
    page.wait_for_selector("input[type='password']", timeout=15000)
    page.locator("input[type='password']").nth(0).fill("Pass1234!")
    page.locator("input[type='password']").nth(1).fill("Different123!")
    
    page.get_by_role("button", name="Save").click()
    expect(page.get_by_text("Passwords do not match")).to_be_visible(timeout=15000)

def test_user_management_add_user(page: Page):
    # Login
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login", timeout=60000)
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    
    # User Management Positive (Check Add User page opens)
    page.get_by_role("link", name="Admin").click()
    page.get_by_role("button", name="Add").click()
    
    # Check heading with more time
    expect(page.get_by_role("heading", name="Add User")).to_be_visible(timeout=15000)