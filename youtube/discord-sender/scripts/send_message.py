#!/usr/bin/env python3
"""
Discord Message Sender Script
Sends messages to a Discord channel using the Discord API
"""

import os
import sys
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional

MAX_MESSAGE_LENGTH = 2000
DEFAULT_RETRY_AFTER = 2.0
MAX_RETRIES = 3

def load_env_file(env_path: Path) -> Dict[str, str]:
    """Load key=value pairs from a .env file."""
    env_vars: Dict[str, str] = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars

def find_env_vars() -> Dict[str, str]:
    """
    Search for environment variables in multiple locations:
    1. Current directory
    2. Skill root directory (two levels up)
    3. Repository root (cwd when running the script)
    4. User home directory
    """
    script_dir = Path(__file__).parent
    candidate_paths = [
        script_dir.parent / '.env',
        script_dir.parent.parent / '.env',
        Path.cwd() / '.env',
        Path.home() / '.env',
    ]

    aggregated: Dict[str, str] = {}
    for path in candidate_paths:
        aggregated.update(load_env_file(path))
    return aggregated

def chunk_message(message: str, max_length: int = MAX_MESSAGE_LENGTH) -> List[str]:
    """Split a message into Discord-safe chunks."""
    if len(message) <= max_length:
        return [message]

    chunks: List[str] = []
    current_chunk: List[str] = []
    current_length = 0

    for paragraph in message.split('\n'):
        paragraph_with_newline = paragraph + '\n'
        paragraph_length = len(paragraph_with_newline)

        if paragraph_length > max_length:
            # Fallback: split paragraph itself into hard chunks
            start = 0
            while start < len(paragraph):
                end = start + max_length
                chunks.append(paragraph[start:end])
                start = end
            continue

        if current_length + paragraph_length > max_length:
            chunks.append(''.join(current_chunk).rstrip())
            current_chunk = [paragraph_with_newline]
            current_length = paragraph_length
        else:
            current_chunk.append(paragraph_with_newline)
            current_length += paragraph_length

    if current_chunk:
        chunks.append(''.join(current_chunk).rstrip())

    return chunks

def post_with_retry(url: str, headers: Dict[str, str], content: str) -> Dict[str, any]:
    """Send a single message chunk with retry logic for rate limits."""
    payload = {"content": content}
    attempt = 0

    while attempt < MAX_RETRIES:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code in (200, 201):
            return {
                "success": True,
                "response": response.json()
            }

        if response.status_code == 429:
            retry_after = response.headers.get('Retry-After')
            delay = float(retry_after) if retry_after else DEFAULT_RETRY_AFTER
            print(f"⚠️  Rate limited. Retrying in {delay} seconds...", file=sys.stderr)
            time.sleep(delay)
            attempt += 1
            continue

        return {
            "success": False,
            "error": f"Failed to send message: {response.status_code}",
            "details": response.text
        }

    return {
        "success": False,
        "error": "Exceeded maximum retry attempts due to rate limiting."
    }

def send_discord_message(message: str, channel_id: Optional[str] = None, token: Optional[str] = None):
    """
    Send a (possibly long) message to Discord by chunking it and respecting rate limits.
    """
    env_vars = find_env_vars()

    if not token:
        token = env_vars.get('DISCORD_BOT_TOKEN') or os.getenv('DISCORD_BOT_TOKEN')
    if not channel_id:
        channel_id = env_vars.get('DISCORD_CHANNEL_ID') or os.getenv('DISCORD_CHANNEL_ID')

    if not token:
        raise ValueError("Discord bot token not found. Please set DISCORD_BOT_TOKEN in .env or environment.")
    if not channel_id:
        raise ValueError("Discord channel ID not found. Please set DISCORD_CHANNEL_ID in .env or environment.")

    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }

    chunks = chunk_message(message)
    responses = []

    for index, chunk in enumerate(chunks, start=1):
        print(f"⏩ Sending chunk {index}/{len(chunks)} ({len(chunk)} chars)", file=sys.stderr)
        result = post_with_retry(url, headers, chunk)
        if not result.get("success"):
            result["failed_chunk_index"] = index
            return result
        responses.append(result["response"])

    return {
        "success": True,
        "message": f"Sent {len(chunks)} chunk(s) successfully.",
        "responses": responses
    }

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python send_message.py <message> [channel_id] [token]")
        print("\nExample:")
        print('  python send_message.py "Hello from Claude!"')
        print('  python send_message.py "Hello" 1234567890 "your_bot_token"')
        sys.exit(1)

    message = sys.argv[1]
    channel_id = sys.argv[2] if len(sys.argv) > 2 else None
    token = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        print("=" * 70)
        print("🚀 Discord Message Sender")
        print("=" * 70)
        preview = (message[:100] + '...') if len(message) > 100 else message
        print(f"Message preview: {preview}")
        print("-" * 70)

        result = send_discord_message(message, channel_id, token)

        if result["success"]:
            print("✅ SUCCESS!")
            print(result["message"])
            last_response = result["responses"][-1]
            print(f"Last Message ID: {last_response.get('id', 'N/A')}")
            print(f"Channel ID: {last_response.get('channel_id', 'N/A')}")
            print(f"Timestamp: {last_response.get('timestamp', 'N/A')}")
            print("=" * 70)
        else:
            print("❌ FAILED!")
            print(f"Error: {result.get('error')}")
            if 'details' in result:
                print(f"Details: {result['details']}")
            if 'failed_chunk_index' in result:
                print(f"Failed chunk: {result['failed_chunk_index']}")
            print("=" * 70)
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
