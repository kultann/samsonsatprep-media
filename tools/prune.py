"""Delete videos of shorts that have been live on every platform for PRUNE_HOURS (default 48).

Reads the auto-poster's public posting log; keeps post.json (small) as the record.
"""
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import urlopen

STATE_URL = os.environ.get("STATE_URL", "https://raw.githubusercontent.com/kultann/samsonsatprep-autopost/main/state/posted.json")
HOURS = float(os.environ.get("PRUNE_HOURS", "48"))
root = Path(__file__).resolve().parent.parent / "shorts"
state = json.load(urlopen(STATE_URL, timeout=60))
now = datetime.now(timezone.utc)
removed = 0
for f in sorted(root.glob("*/post.json")):
    p = json.loads(f.read_text())
    done = state.get(p.get("id", f.parent.name), {})
    if not p.get("platforms") or not all(pl in done for pl in p["platforms"]):
        continue
    last = max(datetime.fromisoformat(v["at"]) for v in done.values())
    if now - last < timedelta(hours=HOURS):
        continue
    for name in (p.get("video"), p.get("cover")):
        if name and (f.parent / name).exists():
            (f.parent / name).unlink()
            removed += 1
print(f"pruned {removed} file(s)")
