from playwright.sync_api import Page, expect

def test_mock_empty_list(page: Page):
    # Login
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    
    # Intercept API and return Empty list
    page.route("**/api/v2/pim/employees?*", lambda route: route.fulfill(
        status=200, content_type="application/json", body='{"data": [], "meta": {"total": 0}}'
    ))
    
    page.get_by_role("link", name="PIM").click()
    expect(page.get_by_text("No Records Found").first).to_be_visible(timeout=10000)

def test_mock_500_error(page: Page):
    # Login
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    
    # Intercept API and return 500 Error
    page.route("**/api/v2/pim/employees?*", lambda route: route.fulfill(
        status=500, content_type="application/json", body='{"error": "Internal Server Error"}'
    ))
    
    page.get_by_role("link", name="PIM").click()
    expect(page.locator("body")).to_be_visible()

# ==========================================
# BUG TEST (This test MUST fail on purpose)
# ==========================================
def test_intentional_bug_search(page: Page):
    # Login
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    
    # BUG INJECTION: Intercept the API and return empty data
    page.route("**/api/v2/pim/employees?*", lambda route: route.fulfill(
        status=200, content_type="application/json", body='{"data": [], "meta": {"total": 0}}'
    ))
    
    page.get_by_role("link", name="PIM").click()
    
    # Wait for data to load
    page.wait_for_timeout(2000) 
    
    # Check "No Records Found" (This will pass)
    expect(page.get_by_text("No Records Found").first).to_be_visible(timeout=5000)
    
    # BUG CHECK: We look for a table row. Since API is empty, this WILL FAIL intentionally.
    expect(page.locator(".oxd-table-row").nth(1)).to_be_visible(timeout=3000)