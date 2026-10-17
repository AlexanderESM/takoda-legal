"""Set the effective date immediately before the actual publication commit."""
from datetime import datetime, timezone
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
today = datetime.now(timezone.utc).date()
path = root / "privacy.html"
text = path.read_text(encoding="utf-8")
pattern = r'<time datetime="[^\"]+" data-publication-date="">[^<]+</time>'
replacement = f'<time datetime="{today.isoformat()}" data-publication-date="">{today.day} {today.strftime("%B %Y")}</time>'
text, count = re.subn(pattern, replacement, text)
if count != 1:
    raise SystemExit("Expected exactly one effective-date element")
path.write_text(text, encoding="utf-8")
print("Effective date set for publication:", today.isoformat())
