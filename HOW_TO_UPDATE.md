# Workout Tracker - AI Agent Instructions

This document is intended for AI agents working on this repository to understand the architecture and the standard operating procedure for updating the workout plan.

## Project Structure
- `index.html`: The main web application containing the UI, tabs, and embedded YouTube videos.
- `workout_plan.md`: A markdown version of the current workout plan, meant to match the website.
- `youtube_videos.json`: A JSON dictionary mapping exercise names to their corresponding YouTube video IDs.
- `serve.py`: A simple Python HTTP server to view the site locally with CORS enabled.

## How to Update the Workout Plan

When a user requests a change to the workout plan, **DO NOT** attempt to manually edit `index.html` using regex or partial file replacements (e.g., `multi_replace_file_content`). The HTML structure for the tabs and exercise rows is complex, deeply nested, and prone to breaking during manual diffs.

Instead, use the following **programmatic approach**:

1. **Create a temporary Python script** (e.g., `update_site.py`) in the workspace.
2. **Embed the user's prompt**: Hardcode the user's requested text plan into the script as a multi-line string.
3. **Generate `workout_plan.md`**: Programmatically format and rewrite the Markdown file based on the parsed string.
4. **Regenerate `index.html`**:
   - Read the existing `index.html` and extract the header (everything before the `<!-- Day 1 -->` or `<section class="tab-content">` blocks).
   - Iterate over the parsed plan to generate the new HTML for each `<section id="dayX">`.
   - Match exercise names with video IDs from `youtube_videos.json`.
   - Update the tab names in the header `<nav class="tabs-nav">` using a regex substitution to match the newly generated days.
   - Extract and append the bottom `<script>` block from the original `index.html`.
5. **Execute the script** using terminal tools to overwrite both `index.html` and `workout_plan.md`.
6. **Clean up**: Delete the temporary Python script.

## Video Matching Logic

When generating the HTML, you will need to map exercises to videos robustly to handle user variations (e.g., "Dumbbell bent over row (standing, hinge at hips)").

Here is a recommended matching logic snippet:

```python
import json

with open('youtube_videos.json', 'r') as f:
    videos = json.load(f)

video_id = ""
for v_name, v_id in videos.items():
    # Basic inclusion match
    if v_name.lower() in exercise_name.lower():
        # Prevent generic short words (like "Squat") from falsely matching specific variations (like "Bulgarian split squat")
        if len(v_name) > 10: 
            video_id = v_id
            break

# First fallback: standard inclusion
if not video_id:
    for v_name, v_id in videos.items():
         if v_name.lower() in exercise_name.lower():
             video_id = v_id
             break

# Second fallback: manual overrides for known missing keys
if not video_id:
    if "shoulder press" in exercise_name.lower() and "dumbbell" in exercise_name.lower():
        video_id = "guW_ENwLOMI"
    elif "single arm row" in exercise_name.lower():
        video_id = "dFzUjzfih7k"
    elif "glute bridge" in exercise_name.lower() and "dumbbell" in exercise_name.lower():
        video_id = "V-Pk0ZfoszU"
```

## UI Details to Preserve
- Optional exercises should be flagged in the HTML with the following inline span tag appended to the `<h3>` title:
  `<span style="color: #ff9800; font-size: 0.8em; margin-left: 8px; border: 1px solid #ff9800; padding: 2px 6px; border-radius: 4px; vertical-align: middle;">Optional</span>`
- Each exercise needs an inferred type (e.g., `Dumbbell`, `Resistance Band`, `Bodyweight`) extracted from the text and displayed beneath the exercise title.
- Keep the tab logic (Javascript) and CSS styling strictly intact.
