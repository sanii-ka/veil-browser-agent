
from playwright.sync_api import sync_playwright
from page_inspector import inspect_page


def find_search_input(page):
    elements = inspect_page(page)

    for element in elements:
        if (
            element["tag"] == "INPUT"
            and (
                element["type"] == "search"
                or element["name"] == "search"
            )
        ):
            return element

    return None


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.wikipedia.org")
    page.wait_for_load_state("domcontentloaded")

    search_input = find_search_input(page)

    if search_input:
        print("Search input found:", search_input)

        search_box = page.locator(
            f'input[name="{search_input["name"]}"]'
        )

        search_box.fill("Artificial intelligence")

        page.get_by_role("button", name="Search").click()

        page.wait_for_timeout(3000)

        print("Current URL:", page.url)
        print("Page title:", page.title())

        if "Artificial_intelligence" in page.url:
            print("SUCCESS: Search opened the article.")
        else:
            print("Search may have opened results or failed.")

    else:
        print("Search input not found.")

    input("Press Enter to close...")
    browser.close()