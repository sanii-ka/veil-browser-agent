
def inspect_page(page):
    """Collect visible interactive elements from the current page."""

    elements = page.locator(
        "input, textarea, select, button, a, [role='button'], [role='combobox']"
    )

    results = []

    count = min(elements.count(), 100)

    for i in range(count):
        element = elements.nth(i)

        try:
            if not element.is_visible():
                continue

            results.append({
                "tag": element.evaluate("(el) => el.tagName"),
                "type": element.get_attribute("type"),
                "role": element.get_attribute("role"),
                "label": element.get_attribute("aria-label"),
                "placeholder": element.get_attribute("placeholder"),
                "text": element.inner_text()[:200],
                "name": element.get_attribute("name"),
            })

        except Exception:
            # Skip elements that disappear or cannot be inspected.
            continue

    return results