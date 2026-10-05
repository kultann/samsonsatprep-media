"""Rebuild shorts/index.json from shorts/*/post.json. Run after adding or editing shorts."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "shorts"
entries = []
for f in sorted(root.glob("*/post.json")):
    p = json.loads(f.read_text())
    p["folder"] = f.parent.name
    p.setdefault("id", f.parent.name)
    entries.append(p)
entries.sort(key=lambda p: p["publish_at"])
(root / "index.json").write_text(json.dumps(entries, indent=1, ensure_ascii=False) + "\n")
print(f"index.json: {len(entries)} shorts")
