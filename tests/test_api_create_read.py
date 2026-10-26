import random
from playwright.sync_api import Page

EMPLOYEES_API = "/web/index.php/api/v2/pim/employees"


def new_employee_body():
    return {
        "firstName": f"ApiUser{random.randint(1000, 9999)}",
        "middleName": "",
        "lastName": "Tester",
        "empPicture": None,
        "employeeId": str(random.randint(100000, 999999)),
    }


def test_api_create_employee(logged_in_page: Page):
    api = logged_in_page.request
    body = new_employee_body()

    response = api.post(EMPLOYEES_API, data=body)

    print("\n--- TC_API_001: CREATE EMPLOYEE (POST) ---")
    print("Endpoint     :", EMPLOYEES_API)
    print("Request body :", body)
    print("Status code  :", response.status)
    print("Response     :", response.json())

    assert response.status == 200
    data = response.json()["data"]
    assert data["empNumber"] > 0
    assert data["firstName"] == body["firstName"]
    assert data["lastName"] == body["lastName"]


def test_api_read_employees(logged_in_page: Page):
    api = logged_in_page.request

    body = new_employee_body()
    created = api.post(EMPLOYEES_API, data=body)
    assert created.status == 200

    response = api.get(EMPLOYEES_API, params={"nameOrId": body["firstName"], "limit": 50, "offset": 0})

    print("\n--- TC_API_002: READ EMPLOYEES (GET) ---")
    print("Endpoint     :", EMPLOYEES_API)
    print("Searched for :", body["firstName"])
    print("Status code  :", response.status)
    print("Total found  :", len(response.json()["data"]))
    print("Response     :", response.json()["data"])

    assert response.status == 200
    result = response.json()
    assert isinstance(result["data"], list)
    names = [emp["firstName"] for emp in result["data"]]
    assert body["firstName"] in names