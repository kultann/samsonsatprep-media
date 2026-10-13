# samsonsatprep-media

Video hosting for @samsonsatprep shorts. GitHub Pages serves the MP4s so Instagram can fetch Reels by URL; the auto-poster (samsonsatprep-autopost) reads `shorts/index.json` and posts each short at its `publish_at`.

- `shorts/<post_id>/video.mp4`, `cover.jpg`, `post.json` — one folder per short (made by the renderer)
- `shorts/index.json` — every short's post.json in one list. Rebuild it after adding shorts: `python3 tools/build_index.py`
- `.github/workflows/maintain.yml` — daily: deletes a short's video 48 h after it's live on every platform (reads the auto-poster's public `state/posted.json`), so the Pages site stays under 1 GB
- `tiktok_weekly.json` — shorts already put in a weekly TikTok folder (TikTok is posted by hand since 2026-10-13). Written by `samsonsatprep-autopost/tools/tiktok_week.py`; push it after each weekly run. The daily prune keeps a short's video until it's listed here (or the bot posted it to TikTok earlier).

Push about one week of shorts at a time. Old videos stay in git history; when the repo passes ~3 GB, delete it on GitHub and re-create it with the same name (the Pages URL stays the same, nothing else depends on its history).
