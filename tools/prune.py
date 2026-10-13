"""Delete videos of shorts that have been live on every platform for PRUNE_HOURS (default 48).

Reads the auto-poster's public posting log; keeps post.json (small) as the record.
TikTok is posted by hand since 2026-10-13: for TikTok a short counts as done once it's in tiktok_weekly.json
(written by samsonsatprep-autopost/tools/tiktok_week.py when it builds that week's TikTok folder), or when
the bot posted it to TikTok earlier. Until then the video is kept. PRUNE_DRY_RUN=1 lists without deleting.
"""
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import urlopen

STATE_URL = os.environ.get("STATE_URL", "https://raw.githubusercontent.com/kultann/samsonsatprep-autopost/main/state/posted.json")
HOURS = float(os.environ.get("PRUNE_HOURS", "48"))
DRY = os.environ.get("PRUNE_DRY_RUN", "0") == "1"
root = Path(__file__).resolve().parent.parent / "shorts"
WEEKLY = root.parent / "tiktok_weekly.json"
state = json.load(urlopen(STATE_URL, timeout=60))
try:
    weekly = json.loads(WEEKLY.read_text()) if WEEKLY.exists() else {}
except ValueError:
    weekly = {}
now = datetime.now(timezone.utc)
removed = 0
for f in sorted(root.glob("*/post.json")):
    p = json.loads(f.read_text())
    pid = p.get("id", f.parent.name)
    done = dict(state.get(pid, {}))
    if "tiktok" not in done and isinstance(weekly.get(pid), dict) and weekly[pid].get("at"):
        done["tiktok"] = {"at": weekly[pid]["at"]}  # in a weekly TikTok folder (posted by hand)
    if not p.get("platforms") or not all(pl in done for pl in p["platforms"]):
        continue
    last = max(datetime.fromisoformat(v["at"]) for v in done.values())
    if now - last < timedelta(hours=HOURS):
        continue
    for name in (p.get("video"), p.get("cover")):
        if name and (f.parent / name).exists():
            if DRY:
                print(f"would prune {f.parent.name}/{name}")
            else:
                (f.parent / name).unlink()
            removed += 1
print(f"{'would prune' if DRY else 'pruned'} {removed} file(s)")
