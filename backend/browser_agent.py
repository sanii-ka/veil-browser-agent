
from playwright.sync_api import sync_playwright
from page_inspector import inspect_page


def verify_result(page, expected_url=None, expected_text=None):
    """Verify whether the browser reached the expected result."""

    current_url = page.url
    page_title = page.title()

    url_ok = (
        expected_url is None
        or expected_url in current_url
    )

    text_ok = (
        expected_text is None
        or expected_text.lower()
        in page.locator("body").inner_text().lower()
    )

    return {
        "verified": url_ok and text_ok,
        "current_url": current_url,
        "page_title": page_title,
        "url_check": url_ok,
        "text_check": text_ok
    }


def find_element(page, target):
    """Find an element using inspected properties."""

    elements = inspect_page(page)
    target = target.strip().lower()

    for element in elements:
        values = [
            element.get("label"),
            element.get("placeholder"),
            element.get("name"),
            element.get("text"),
        ]

        for value in values:
            if value and value.strip().lower() == target:
                return element

    for element in elements:
        values = [
            element.get("label"),
            element.get("placeholder"),
            element.get("name"),
            element.get("text"),
        ]

        for value in values:
            if value and target in value.lower():
                return element

    return None


def build_locator(page, element):
    """Build a Playwright locator from inspected properties."""

    tag = element["tag"].lower()

    name = element.get("name")
    label = element.get("label")
    placeholder = element.get("placeholder")
    text = element.get("text")

    if label:
        locator = page.get_by_label(label, exact=True)

    elif placeholder:
        locator = page.get_by_placeholder(
            placeholder, exact=True
        )

    elif name:
        locator = page.locator(
            f'{tag}[name="{name}"]'
        )

    elif text and tag in ("button", "a"):
        locator = page.get_by_text(text, exact=True)

    else:
        raise ValueError(
            "No reliable locator found for this element"
        )

    return locator


def execute_plan(plan):
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        results = []

        try:
            # Execute planned browser actions
            for action in plan.get("actions", []):

                action_type = action.get("action")
                target = action.get("target", "")

                print("\nExecuting:", action)

                try:
                    if action_type == "navigate":

                        page.goto(target)
                        page.wait_for_load_state(
                            "domcontentloaded"
                        )

                        results.append({
                            "action": action,
                            "status": "success",
                            "message": "Page opened"
                        })

                    elif action_type == "type":

                        element = find_element(page, target)

                        if not element:
                            raise ValueError(
                                f"Could not find input: {target}"
                            )

                        locator = build_locator(page, element)
                        locator.fill(action["value"])

                        print("Text entered.")

                        # Current prototype behavior:
                        # submit the field by pressing Enter.
                        locator.press("Enter")

                        print("Enter key pressed.")

                        page.wait_for_timeout(3000)

                        results.append({
                            "action": action,
                            "status": "success",
                            "message": "Text entered and Enter pressed",
                            "current_url": page.url
                        })

                    elif action_type == "click":

                        element = find_element(page, target)

                        if not element:
                            raise ValueError(
                                "Could not find clickable element: "
                                f"{target}"
                            )

                        locator = build_locator(page, element)
                        locator.click()

                        page.wait_for_timeout(3000)

                        results.append({
                            "action": action,
                            "status": "success",
                            "message": "Element clicked",
                            "current_url": page.url
                        })

                    else:
                        raise ValueError(
                            f"Unsupported action: {action_type}"
                        )

                except Exception as error:
                    print("Action failed:", error)

                    results.append({
                        "action": action,
                        "status": "failed",
                        "error": str(error)
                    })

            # -------------------------
            # FINAL VERIFICATION
            # -------------------------
            print("\nVerifying final result...")

            expected_url = plan.get("expected_url")
            expected_text = plan.get("expected_text")

            try:
                verification = verify_result(
                    page,
                    expected_url=expected_url,
                    expected_text=expected_text
                )

                results.append({
                    "verification": verification
                })

                print("\nVerification result:")
                print(verification)

                if verification["verified"]:
                    print("\nVerification passed!")
                else:
                    print("\nVerification failed!")

            except Exception as error:
                verification = {
                    "verified": False,
                    "error": str(error)
                }

                results.append({
                    "verification": verification
                })

                print("\nVerification error:", error)

            print("\nExecution results:")

            for result in results:
                print(result)

            input("\nPress Enter to close browser...")

            return results

        finally:
            browser.close()