
from playwright.sync_api import Page

def test_api_update_employee(page: Page):
    # Login to get session
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    page.wait_for_url("**/dashboard/**")

    # Create dummy employee first to update
    create_res = page.request.post(
        "https://opensource-demo.orangehrmlive.com/web/index.php/api/v2/pim/employees",
        data={"firstName": "UpdateTest", "lastName": "User"}
    )
    emp_id = create_res.json()['data']['empNumber']

    # Update Request (PUT)
    response = page.request.put(
        f"https://opensource-demo.orangehrmlive.com/web/index.php/api/v2/pim/employees/{emp_id}/personal-details",
        data={"firstName": "UpdatedName", "lastName": "UpdatedLast", "gender": "1", "maritalStatus": "Single"}
    )
    assert response.status == 200

def test_api_delete_employee(page: Page):
    # Login to get session
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    page.wait_for_url("**/dashboard/**")

    # Create dummy employee first to delete
    create_res = page.request.post(
        "https://opensource-demo.orangehrmlive.com/web/index.php/api/v2/pim/employees",
        data={"firstName": "DeleteTest", "lastName": "User"}
    )
    emp_id = create_res.json()['data']['empNumber']

    # Delete Request (DELETE)
    response = page.request.delete(
        "https://opensource-demo.orangehrmlive.com/web/index.php/api/v2/pim/employees",
        data={"ids": [emp_id]}
    )
    assert response.status == 200

