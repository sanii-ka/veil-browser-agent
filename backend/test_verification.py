
from playwright.sync_api import sync_playwright
from browser_agent import verify_result


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Opening Wikipedia article...")
        page.goto(
            "https://en.wikipedia.org/wiki/Artificial_intelligence"
        )

        page.wait_for_load_state("domcontentloaded")

        result = verify_result(
            page,
            expected_url="/wiki/Artificial_intelligence",
            expected_text="Artificial intelligence"
        )

        print("\nVerification result:")
        print(result)

        if result["verified"]:
            print("\nVerification passed!")
        else:
            print("\nVerification failed!")

        input("\nPress Enter to close browser...")
        browser.close()


if __name__ == "__main__":
    main()