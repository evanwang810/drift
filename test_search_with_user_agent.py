#!/usr/bin/env python3
"""Test search with different user agents."""

import requests
from bs4 import BeautifulSoup

def test_search_with_user_agents():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    ]

    query = "agentic workflows"

    for ua in user_agents:
        print(f"\nTesting with User-Agent: {ua[:60]}...")
        headers = {"User-Agent": ua}
        try:
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            response = requests.get(url, headers=headers, timeout=10)

            print(f"  Status: {response.status_code}")

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = list(soup.select('.result__a'))
                print(f"  Number of '.result__a' elements: {len(results)}")

                # Check for CAPTCHA
                if "captcha" in response.text.lower():
                    print("  ⚠️ CAPTCHA detected!")

                # Check for block message
                if "bots use" in response.text.lower():
                    print("  ⚠️ Block message detected!")
            elif response.status_code == 202:
                print("  ⚠️ Status 202 (rate limited)")
            else:
                print(f"  ⚠️ Unexpected status: {response.status_code}")

        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    test_search_with_user_agents()
