
from browser_agent import execute_plan


def main():
    plan = {
        "task": "Search Wikipedia for Artificial Intelligence",

        "actions": [
            {
                "action": "navigate",
                "target": "https://www.wikipedia.org"
            },
            {
                "action": "type",
                "target": "search",
                "value": "Artificial intelligence"
            }
        ],

        # These are used by the final verification step.
        "expected_url": "/wiki/Artificial_intelligence",
        "expected_text": "Artificial intelligence"
    }

    print("Starting Veil Browser Agent...")
    print("Task:", plan["task"])

    results = execute_plan(plan)

    print("\nFinal execution summary:")

    for result in results:
        print(result)


if __name__ == "__main__":
    main()