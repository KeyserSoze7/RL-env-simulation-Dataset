import requests
import json
import time
import random
from pathlib import Path



OUTPUT_FILE = Path("data/task_instruction_data.jsonl")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

GITHUB_API = "https://api.github.com/search/issues"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "rl-env-seeddata-research"
}

QUERY = "is:issue is:public language:python"

MAX_PAGES = 10        # 10 * 100 = 1000 issues
SLEEP_SECONDS = 2     # be polite


# Helpers

def infer_project_type(text):
    text = text.lower()
    if any(k in text for k in ["bug", "error", "fix", "crash"]):
        return "bugfix"
    if any(k in text for k in ["docs", "documentation", "readme"]):
        return "documentation"
    return "feature"

def infer_component(text):
    components = ["backend", "frontend", "api", "database", "infra"]
    for c in components:
        if c in text.lower():
            return c
    return random.choice(components)

def infer_complexity(title, body):
    length = len((title + (body or "")).split())
    return min(10, max(3, length // 8))


# Scraper

def scrape():
    count = 0

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for page in range(1, MAX_PAGES + 1):
            print(f"Fetching page {page}/{MAX_PAGES}")

            response = requests.get(
                GITHUB_API,
                headers=HEADERS,
                params={
                    "q": QUERY,
                    "sort": "created",
                    "order": "desc",
                    "per_page": 100,
                    "page": page,
                },
            )

            response.raise_for_status()
            items = response.json().get("items", [])

            for issue in items:
                title = issue.get("title", "").strip()
                body = (issue.get("body") or "").strip()

                if len(title) < 8 or len(body) < 20:
                    continue

                record = {
                    "instruction": "Generate a realistic enterprise task title and description.",
                    "input": {
                        "project_type": infer_project_type(title + body),
                        "team": "engineering",
                        "component": infer_component(title + body),
                        "complexity": infer_complexity(title, body),
                    },
                    "output": {
                        "title": title,
                        "description": body[:800],  # truncate long issues
                    },
                }

                f.write(json.dumps(record) + "\n")
                count += 1

            time.sleep(SLEEP_SECONDS)

    print(f"\n✅ Done. Collected {count} samples.")
    print(f"📄 Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape()
