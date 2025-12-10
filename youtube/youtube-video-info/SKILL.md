---
name: youtube-video-info
description: Fetch detailed information about YouTube videos using Google's YouTube Data API v3. This skill should be used when users request information about YouTube videos such as title, channel, views, likes, description, or other metadata. Accepts YouTube URLs or video IDs as input.
---

# YouTube Video Info

## Overview

This skill enables fetching comprehensive information about YouTube videos using the YouTube Data API v3. It retrieves video metadata including title, description, channel information, statistics (views, likes, comments), duration, tags, and thumbnails.

## When to Use This Skill

Use this skill when:
- User provides a YouTube video URL or ID and requests information about it
- User asks for video statistics (views, likes, comment count)
- User needs video metadata (title, description, channel name, publish date)
- User wants to analyze or summarize YouTube video details

## Quick Start

To fetch YouTube video information, use the `get_video_info.py` script located in the `scripts/` directory.

### Basic Usage

```bash
python scripts/get_video_info.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Or with just the video ID:

```bash
python scripts/get_video_info.py "VIDEO_ID"
```

### Output Format Options

**Human-readable format (default):**
```bash
python scripts/get_video_info.py "VIDEO_ID"
```

**JSON format (for programmatic use):**
```bash
python scripts/get_video_info.py "VIDEO_ID" --json
```

## API Key Configuration

The script requires a Google API key with YouTube Data API v3 enabled. The API key can be provided through multiple methods (in order of precedence):

1. **Command-line argument:**
   ```bash
   python scripts/get_video_info.py "VIDEO_ID" --api-key "YOUR_API_KEY"
   ```

2. **.env file (recommended):**
   Create or use an existing `.env` file with:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

   The script automatically searches for `.env` in:
   - Current working directory
   - User home directory
   - Parent directories of the script

   To specify a custom .env file location:
   ```bash
   python scripts/get_video_info.py "VIDEO_ID" --env-file /path/to/.env
   ```

3. **Environment variable:**
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   python scripts/get_video_info.py "VIDEO_ID"
   ```

## Supported URL Formats

The script accepts multiple YouTube URL formats:

- Full URL: `https://www.youtube.com/watch?v=VIDEO_ID`
- Short URL: `https://youtu.be/VIDEO_ID`
- Direct video ID: `VIDEO_ID` (11 characters)

## Output Information

The script retrieves the following information:

### Video Metadata
- **Title**: Video title
- **Description**: Full video description
- **Published Date**: When the video was published
- **Duration**: Video length in ISO 8601 format

### Channel Information
- **Channel Name**: Name of the channel that uploaded the video
- **Channel ID**: Unique identifier for the channel

### Statistics
- **View Count**: Total number of views
- **Like Count**: Total number of likes
- **Comment Count**: Total number of comments

### Additional Details
- **Tags**: Video tags (if available)
- **Category ID**: YouTube category identifier
- **Privacy Status**: Public, private, or unlisted
- **Thumbnails**: URLs for various thumbnail sizes

## Example Workflow

When a user asks about a YouTube video:

1. **Extract the video URL or ID** from the user's request
2. **Check for API key availability** in .env file or environment
3. **Execute the script:**
   ```bash
   python scripts/get_video_info.py "USER_PROVIDED_URL_OR_ID"
   ```
4. **Parse the output** and present relevant information to the user
5. **If JSON format is needed** for further processing, add the `--json` flag

## Error Handling

The script handles common errors:
- **Invalid video ID/URL**: Returns an error message if the video ID cannot be extracted
- **Video not found**: Returns an error if the video doesn't exist or is unavailable
- **API key issues**: Clear error messages if the API key is missing or invalid
- **Network errors**: Handles connection and request failures gracefully

## Dependencies

The script requires the `requests` library. Install it using:

```bash
pip install requests
```

## Example Interactions

**User Request:** "Tell me about this YouTube video: https://www.youtube.com/watch?v=dQw4w9WgXcQ"

**Workflow:**
1. Extract video ID: `dQw4w9WgXcQ`
2. Run: `python scripts/get_video_info.py "dQw4w9WgXcQ"`
3. Parse output and present to user with title, channel, views, likes, and description summary

**User Request:** "How many views does video ID abc123xyz45 have?"

**Workflow:**
1. Run: `python scripts/get_video_info.py "abc123xyz45" --json`
2. Parse JSON output
3. Extract and report the view count from `statistics.view_count`

## Notes

- The YouTube Data API has quota limits. Each request consumes quota units.
- Ensure the API key has YouTube Data API v3 enabled in the Google Cloud Console.
- Some video information may be unavailable depending on privacy settings or video status.
- The script automatically truncates long descriptions in human-readable output (first 300 characters).
