
from playwright.sync_api import sync_playwright
from page_inspector import inspect_page

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.wikipedia.org")
    page.wait_for_load_state("domcontentloaded")

    elements = inspect_page(page)

    for element in elements:
        print(element)

    input("Press Enter to close...")
    browser.close()