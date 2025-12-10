---
name: url-shortener
description: Shorten all URLs in text using the Bitly API. Use this skill when users request to shorten URLs, convert long URLs to short links, or make text more concise by replacing URLs with bit.ly links. Works with any text containing HTTP/HTTPS URLs.
---

# URL Shortener

## Overview

This skill automatically finds and shortens all URLs in a given text using the Bitly API. Convert lengthy URLs into compact bit.ly links to make text more readable and shareable.

## When to Use This Skill

Use this skill when:
- User explicitly requests to shorten URLs in text
- User wants to make URLs more compact or readable
- User asks to convert URLs to bit.ly links
- User provides text with long URLs that need shortening
- User wants to prepare text for platforms with character limits (Twitter, SMS, etc.)

## Quick Start

To shorten URLs in text:

1. Ensure `BITLY_TOKEN` is set in the environment or `.env` file
2. Execute the bundled script with the text containing URLs:

```bash
python scripts/shorten_urls.py "Check out this article: https://www.example.com/very/long/path/to/article"
```

The script will output the modified text with shortened URLs.

## How It Works

The skill uses `scripts/shorten_urls.py` to:

1. **Extract URLs**: Scan the input text for all HTTP/HTTPS URLs using regex
2. **Shorten via Bitly**: Call the Bitly API to create shortened bit.ly links
3. **Replace URLs**: Substitute original URLs with their shortened versions
4. **Return result**: Output the modified text with all URLs shortened

### Script Usage

**Basic usage:**
```bash
python scripts/shorten_urls.py "Your text with URLs here"
```

**Verbose mode** (shows progress and URL mapping):
```bash
python scripts/shorten_urls.py --verbose "Your text with URLs here"
python scripts/shorten_urls.py -v "Your text with URLs here"
```

### Example

**Input:**
```
Visit our website at https://www.example.com/blog/2024/article and
documentation at https://docs.example.com/getting-started/installation/guide
```

**Output:**
```
Visit our website at https://bit.ly/3xYz123 and
documentation at https://bit.ly/4aBc789
```

## Setup Requirements

### 1. Install Dependencies

The script requires Python packages:

```bash
pip install requests python-dotenv
```

### 2. Configure Bitly API Token

Create a `.env` file in the working directory with your Bitly token:

```bash
BITLY_TOKEN=your_bitly_api_token_here
```

**To obtain a Bitly token:**
1. Sign up at https://bitly.com/a/sign_up
2. Navigate to Settings → Developer Settings → API
3. Generate an access token
4. Copy the token to your `.env` file

### 3. Verify Setup

Test the configuration:

```bash
python scripts/shorten_urls.py "Test: https://example.com"
```

If configured correctly, this will output text with a shortened bit.ly URL.

## Workflow Guidelines

### For User Requests

When a user asks to shorten URLs:

1. **Verify prerequisites**: Check that dependencies and `BITLY_TOKEN` are configured
2. **Extract text**: Get the text from user input or file
3. **Execute script**: Run `scripts/shorten_urls.py` with the text
4. **Return result**: Provide the modified text to the user
5. **Handle errors**: If API fails, inform the user and suggest troubleshooting steps

### Handling Multiple URLs

The script automatically handles multiple URLs in the same text, shortening each unique URL once and replacing all occurrences.

### Preserving Context

The script only replaces URLs, leaving all other text unchanged. Formatting, spacing, and non-URL content remain intact.

## Troubleshooting

### "BITLY_TOKEN not found"

**Cause**: The `BITLY_TOKEN` environment variable is not set.

**Solution**:
1. Create a `.env` file in the working directory
2. Add `BITLY_TOKEN=your_token_here`
3. Ensure `python-dotenv` is installed: `pip install python-dotenv`

### "Invalid BITLY_TOKEN or insufficient permissions"

**Cause**: The provided token is invalid or expired.

**Solution**:
1. Verify the token is correct (no extra spaces or quotes)
2. Generate a new token at https://bitly.com/a/settings/api
3. Update the `.env` file with the new token

### "requests library not found"

**Cause**: The `requests` package is not installed.

**Solution**:
```bash
pip install requests
```

### "Failed to shorten URL"

**Cause**: Network issues or Bitly API errors.

**Solution**:
1. Check internet connectivity
2. Verify the URL is valid and accessible
3. Try again after a short delay (rate limiting)
4. Use `--verbose` flag to see detailed error messages

### No URLs Found

If the script reports "No URLs found", ensure:
- URLs start with `http://` or `https://`
- URLs are not wrapped in special characters that break the regex
- The text contains valid URL patterns

## Advanced Usage

### Integrating with Files

To shorten URLs in a file:

```bash
# Read file, shorten URLs, and save to new file
python scripts/shorten_urls.py "$(cat input.txt)" > output.txt
```

### Custom Workflows

The script can be integrated into larger workflows by importing it as a module:

```python
from scripts.shorten_urls import shorten_urls_in_text, load_bitly_token

token = load_bitly_token()
modified_text, url_mapping = shorten_urls_in_text("Your text here", token)
```

## Notes

- The script requires a Bitly account and API token (free tier available)
- All URLs (including already-shortened ones) will be converted to bit.ly links
- Shortened URLs are permanent and can be managed in the Bitly dashboard
- API rate limits apply based on Bitly account tier
