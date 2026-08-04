import re, os
from playwright.sync_api import Playwright, sync_playwright, expect


def display_welcome_banner() -> None:
    clear_screen()
    print("=" * 75)
    print("        📰 UAF RESULT SCRAPER 📰        ")
    print("=" * 75)
    print(" Purpose: Automatically extracts full results with Course ID, Total Marks")
    print("          and Grades in a foramtted block directly from the UAF LMS portal.")
    print("=" * 75 + "\n")


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def get_ag() -> str:
    while True:
        user_input = input("Enter AG Number (****-ag-****): ").strip().lower()
        if re.fullmatch(r'\d{4}-ag-\d{1,5}', user_input):
            return user_input
        print("Invalid Input! Format must be YYYY-ag-XXXX.")



def run(playwright: Playwright) -> None:
    ag_num = get_ag()
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    #Open portal and search for query
    page.goto("https://lms.uaf.edu.pk/login/index.php")
    page.get_by_role("textbox", name="Registration No").fill(ag_num)
    page.get_by_role("button", name="Result").click()
    page.wait_for_selector("table.table.tab-content")

    #Stores both table's data separately
    student_info_table = page.locator("table").nth(0)
    course_result_table = page.locator("table").nth(1)

    info_rows = [
        row.locator("td, th").all_inner_texts()
        for row in student_info_table.locator("tr").all()
    ]

    result_rows = [
        row.locator("td, th").all_inner_texts()
        for row in course_result_table.locator("tr").all()
    ]

    print("=" * 50)
    print(f"{info_rows[0][0]} {info_rows[0][1]}")
    print(f"{info_rows[1][0]}: {info_rows[1][1]}")
    print("=" * 50)


    for index, row in enumerate(result_rows):
        print(f"{row[0]:<10}{row[3]:^10}{row[10]:^10}{row[11]:^10}")
        if index == 0:
            print("-" * 50)

    print("=" * 50)

    # ---------------------
    context.close()
    browser.close()

if __name__ == "__main__":
    clear_screen()
    display_welcome_banner() 
    with sync_playwright() as playwright:
        run(playwright)
