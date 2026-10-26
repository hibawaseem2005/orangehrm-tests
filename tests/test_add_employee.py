import re
import random
from playwright.sync_api import Page, expect

ADD_URL = "/web/index.php/pim/addEmployee"
LIST_URL = "/web/index.php/pim/viewEmployeeList"


def unique_first_name():
    return f"Hiba{random.randint(1000, 9999)}"


def add_employee(page: Page, first_name: str, last_name: str):
    """Helper: fills the Add Employee form and clicks Save."""
    page.goto(ADD_URL)
    page.fill("input[name='firstName']", first_name)
    page.fill("input[name='lastName']", last_name)
    page.click("button[type='submit']")


def test_add_employee_valid(logged_in_page: Page, browser_name):
    page = logged_in_page
    first = unique_first_name()
    add_employee(page, first, "Tester")
    page.screenshot(path=f"screenshots/{browser_name}_TC_ADDEMP_001_valid_employee2.png")
    expect(page.get_by_text("Successfully Saved")).to_be_visible()
    
    expect(page).to_have_url(re.compile(r".*/pim/viewPersonalDetails/empNumber/\d+"))

    # wait until the page has actually loaded the employee's data
    expect(page.get_by_role("heading", name="Personal Details")).to_be_visible()
    expect(page.locator("input[name='firstName']")).to_have_value(first)

    page.screenshot(path=f"screenshots/{browser_name}_TC_ADDEMP_001_valid_employee.png")

def test_add_employee_empty_names(logged_in_page: Page, browser_name):
    page = logged_in_page
    page.goto(ADD_URL)
    page.click("button[type='submit']")
    expect(page.get_by_text("Required", exact=True)).to_have_count(2)
    
    expect(page).to_have_url(re.compile(r".*/pim/addEmployee"))
    page.screenshot(path=f"screenshots/{browser_name}_TC_ADDEMP_002_empty_names.png")


def test_new_employee_in_list(logged_in_page: Page, browser_name):
    page = logged_in_page
    first = unique_first_name()
    add_employee(page, first, "Tester")
    page.screenshot(path=f"screenshots/{browser_name}_TC_ADDEMP_003_in_list1.png")
    expect(page.get_by_text("Successfully Saved")).to_be_visible()

    page.goto(LIST_URL)
    page.get_by_placeholder("Type for hints...").first.fill(first)
    page.get_by_role("button", name="Search").click()

    expect(page.get_by_role("row").filter(has_text=first)).to_be_visible()
    page.screenshot(path=f"screenshots/{browser_name}_TC_ADDEMP_003_in_list.png")