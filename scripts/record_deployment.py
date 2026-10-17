"""Verify the actual Pages URL and record it only after successful deployment."""
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from datetime import datetime, timezone
import argparse, json

parser = argparse.ArgumentParser()
parser.add_argument("--url", required=True, help="Actual privacy.html URL returned from GitHub Pages")
parser.add_argument("--repository", required=True, help="Actual owner/repository from authenticated GitHub")
args = parser.parse_args()
parsed = urlparse(args.url)
if parsed.scheme != "https" or not parsed.hostname or not parsed.path.endswith("/privacy.html"):
    raise SystemExit("Expected a public HTTPS privacy.html URL")
with urlopen(Request(args.url, headers={"User-Agent": "TakodaLegalVerification/1.0"}), timeout=30) as response:
    final = urlparse(response.url)
    if response.status != 200 or final.scheme != "https":
        raise SystemExit("A public HTTPS 200 response is required")
    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        raise SystemExit("The policy must be served as HTML")
    body = response.read().decode("utf-8")
    if "com.takodadigital.theartofdining" not in body or "Privacy Policy" not in body:
        raise SystemExit("The live page is not the intended policy")
owner, name = args.repository.split("/", 1)
status = {"published": True, "github_username": owner,
          "repository_url": f"https://github.com/{owner}/{name}",
          "privacy_url": args.url, "verified_at": datetime.now(timezone.utc).isoformat()}
root = Path(__file__).resolve().parents[1]
(root / "deployment-status.json").write_text(json.dumps(status, indent=2)+"\n", encoding="utf-8")
print("Verified public Privacy Policy URL:", args.url)
print("No browser login or authentication headers were used. Global geographic reach is not proven by this check.")
