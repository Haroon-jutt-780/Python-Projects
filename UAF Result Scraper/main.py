import re, os
from playwright.sync_api import Error, Playwright, TimeoutError, sync_playwright


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
        user_input = input("Enter your AG Number (****-ag-****): ").strip().lower()
        if re.fullmatch(r'\d{4}-ag-\d{1,5}', user_input):
            return user_input
        print("Invalid Input! Format must be YYYY-ag-XXXX.")



def run(playwright: Playwright) -> None:

    LMS_URL = "https://lms.uaf.edu.pk/login/index.php"

    #Gets AG from User
    ag_num = get_ag()

    #Opens chromium
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        #Open portal and search for query
        page.goto(LMS_URL, timeout=10000)
        page.get_by_role("textbox", name="Registration No").fill(ag_num)
        page.get_by_role("button", name="Result").click()
        page.wait_for_selector("table.table.tab-content", timeout=10000)

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

        #Prints Result in formatted block
        print("=" * 50)
        print(f"{info_rows[0][0]} {info_rows[0][1]}")
        print(f"{info_rows[1][0]}: {info_rows[1][1]}")
        print("=" * 50)

        for index, row in enumerate(result_rows):
            print(f"{row[0]:<10}{row[3]:^10}{row[10]:^10}{row[11]:^10}")
            if index == 0:
                print("-" * 50)

        print("=" * 50)

    except TimeoutError:
        #Catches Timeout Error if server is down
        print("\n[!] Error: LMS server timed out. The server might be down or unreachable.")

    except Error as e:
        # Catches any other Playwright issues (e.g., No Wi-Fi, bad URL, browser crash)
        print(f"Playwright error: {e}")
        
    finally:
        context.close()
        browser.close()

if __name__ == "__main__":
    display_welcome_banner() 
    with sync_playwright() as playwright:
        run(playwright)
