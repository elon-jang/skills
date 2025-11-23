#!/usr/bin/env python3
"""
URL Shortener Script using Bitly API

Finds all URLs in a given text and shortens them using Bitly API.
Requires BITLY_TOKEN in environment variables or .env file.

Usage:
    python shorten_urls.py "Your text with https://example.com/long/url here"
"""

import os
import re
import sys
import json
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Warning: 'python-dotenv' not found. Install with: pip install python-dotenv", file=sys.stderr)
    load_dotenv = lambda: None


# URL regex pattern - matches http:// and https:// URLs
URL_PATTERN = r'https?://[^\s<>"\']+'

# Bitly API endpoint
BITLY_API_URL = "https://api-ssl.bitly.com/v4/shorten"


def load_bitly_token():
    """Load Bitly API token from environment or .env file."""
    # Try loading from .env file
    load_dotenv()

    token = os.getenv('BITLY_TOKEN')
    if not token:
        print("Error: BITLY_TOKEN not found in environment variables or .env file", file=sys.stderr)
        print("\nTo fix this:", file=sys.stderr)
        print("1. Create a .env file in your working directory", file=sys.stderr)
        print("2. Add: BITLY_TOKEN=your_token_here", file=sys.stderr)
        print("3. Get your token from: https://bitly.com/a/sign_up", file=sys.stderr)
        sys.exit(1)

    return token


def shorten_url(url, token):
    """
    Shorten a single URL using Bitly API.

    Args:
        url: The long URL to shorten
        token: Bitly API token

    Returns:
        Shortened URL string or None if failed
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = {
        'long_url': url
    }

    try:
        response = requests.post(BITLY_API_URL, headers=headers, json=data, timeout=10)

        if response.status_code in [200, 201]:
            result = response.json()
            return result.get('link')
        elif response.status_code == 400:
            error_data = response.json()
            print(f"Warning: Failed to shorten '{url}': {error_data.get('message', 'Bad request')}", file=sys.stderr)
            return None
        elif response.status_code == 403:
            print(f"Error: Invalid BITLY_TOKEN or insufficient permissions", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Warning: Failed to shorten '{url}': HTTP {response.status_code}", file=sys.stderr)
            return None

    except requests.exceptions.RequestException as e:
        print(f"Warning: Network error while shortening '{url}': {e}", file=sys.stderr)
        return None


def shorten_urls_in_text(text, token, verbose=False):
    """
    Find and shorten all URLs in the given text.

    Args:
        text: Input text containing URLs
        token: Bitly API token
        verbose: Print detailed information

    Returns:
        Tuple of (modified_text, url_mapping)
    """
    # Find all URLs in the text
    urls = re.findall(URL_PATTERN, text)

    if not urls:
        if verbose:
            print("No URLs found in the text.", file=sys.stderr)
        return text, {}

    if verbose:
        print(f"Found {len(urls)} URL(s) to shorten...", file=sys.stderr)

    # Create mapping of original -> shortened URLs
    url_mapping = {}
    modified_text = text

    for url in urls:
        # Skip if already shortened
        if url in url_mapping:
            continue

        if verbose:
            print(f"Shortening: {url}", file=sys.stderr)

        shortened = shorten_url(url, token)

        if shortened:
            url_mapping[url] = shortened
            # Replace all occurrences of this URL
            modified_text = modified_text.replace(url, shortened)
            if verbose:
                print(f"  → {shortened}", file=sys.stderr)
        else:
            if verbose:
                print(f"  → Keeping original URL", file=sys.stderr)

    return modified_text, url_mapping


def main():
    """Main function to handle command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python shorten_urls.py <text>", file=sys.stderr)
        print("   or: python shorten_urls.py --verbose <text>", file=sys.stderr)
        print("\nExample: python shorten_urls.py 'Check out https://example.com/page'", file=sys.stderr)
        sys.exit(1)

    # Check for verbose flag
    verbose = False
    text_index = 1

    if sys.argv[1] == '--verbose' or sys.argv[1] == '-v':
        verbose = True
        text_index = 2
        if len(sys.argv) < 3:
            print("Error: No text provided", file=sys.stderr)
            sys.exit(1)

    # Get input text
    text = ' '.join(sys.argv[text_index:])

    # Load Bitly token
    token = load_bitly_token()

    # Process text
    modified_text, url_mapping = shorten_urls_in_text(text, token, verbose=verbose)

    # Output results
    print(modified_text)

    # Print mapping as JSON to stderr if verbose
    if verbose and url_mapping:
        print("\nURL Mapping:", file=sys.stderr)
        print(json.dumps(url_mapping, indent=2), file=sys.stderr)


if __name__ == '__main__':
    main()
