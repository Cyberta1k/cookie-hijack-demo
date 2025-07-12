#!/usr/bin/env python3
"""
Extract the 'li_at' session cookie from Chrome for LinkedIn using browser-cookie3.

Author: Abhiraj Singh
License: MIT
"""

import browser_cookie3
import sys

def extract_li_at_cookie():
    """
    Extracts the 'li_at' cookie from Chrome for the domain 'linkedin.com'.
    Returns:
        str: The value of the 'li_at' cookie, or None if not found.
    """
    try:
        cookies = browser_cookie3.chrome(domain_name='linkedin.com')
        for cookie in cookies:
            if cookie.name == 'li_at':
                return cookie.value
        return None
    except Exception as error:
        print(f"[!] Error extracting cookies: {error}", file=sys.stderr)
        return None

def main():
    print("[*] Extracting 'li_at' cookie from Chrome...")
    li_at = extract_li_at_cookie()

    if li_at:
        print("\n✅ 'li_at' cookie value:\n")
        print(li_at)
    else:
        print("\n⚠️ 'li_at' cookie not found. Make sure you're logged into LinkedIn in Chrome.")

if __name__ == "__main__":
    main()
