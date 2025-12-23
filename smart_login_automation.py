"""
Smart Login Automation
----------------------
AI-assisted UI automation using Playwright with self-healing selectors.

Features:
- Intelligent selector weighting
- Fallback mechanisms for unstable DOMs
- ML-ready (Linear Regression demo)
- React-compatible login testing

Author: Arash Amoozandeh
"""

import json
import os
from playwright.sync_api import sync_playwright
from sklearn.linear_model import LinearRegression


WEIGHT_FILE = "selectors_weight.json"


# -----------------------------
# Storage
# -----------------------------
def load_weights():
    if os.path.exists(WEIGHT_FILE):
        with open(WEIGHT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_weights(weights):
    with open(WEIGHT_FILE, "w", encoding="utf-8") as f:
        json.dump(weights, f, ensure_ascii=False, indent=4)


# -----------------------------
# Selector Intelligence
# -----------------------------
def select_best_selector(weights, field_type):
    return sorted(
        weights.get(field_type, {}).items(),
        key=lambda x: x[1],
        reverse=True
    )


def update_weight(weights, field_type, selector):
    weights.setdefault(field_type, {})
    weights[field_type][selector] = weights[field_type].get(selector, 0) + 1


def find_element(page, weights, field_type):
    for selector, score in select_best_selector(weights, field_type):
        try:
            el = page.wait_for_selector(selector, timeout=2000)
            if el.is_visible():
                print(f"✅ {field_type} found: {selector} ({score})")
                update_weight(weights, field_type, selector)
                return el
        except Exception:
            pass

    print(f"⚠️ fallback for {field_type}")

    fallback = {
        "username": ["input#username", "input:nth-of-type(1)"],
        "password": ["input#password", "input:nth-of-type(2)"],
        "login_button": ["button", "input[type=submit]"]
    }

    for selector in fallback.get(field_type, []):
        el = page.query_selector(selector)
        if el:
            update_weight(weights, field_type, selector)
            return el

    raise Exception(f"{field_type} not found")


# -----------------------------
# ML (Demo / Extendable)
# -----------------------------
def predictive_analysis(test_data):
    X = [row[:-1] for row in test_data]
    y = [row[-1] for row in test_data]

    model = LinearRegression()
    model.fit(X, y)
    return model.predict(X).tolist()


# -----------------------------
# Main Test
# -----------------------------
def run_smart_login_test():
    weights = load_weights()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("login_test.html")

        predictions = predictive_analysis([
            [1, 2, 10],
            [3, 4, 20],
            [5, 6, 30]
        ])
        print("Predictions:", predictions)

        find_element(page, weights, "username").fill("my_test_user")
        find_element(page, weights, "password").fill("my_secure_password")
        find_element(page, weights, "login_button").click()

        page.wait_for_timeout(3000)

        if "خطایی در ارتباط با سرور" in page.content():
            print("✅ UI interaction successful")

        save_weights(weights)
        browser.close()


if __name__ == "__main__":
    run_smart_login_test()
