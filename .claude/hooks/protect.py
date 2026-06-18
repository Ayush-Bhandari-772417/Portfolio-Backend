import json, sys, re

BLOCKED_EXACT = {
    ".env",
    "db.sqlite3",
}

BLOCKED_PATTERNS = [
    r".*__pycache__.*",
    r".*\.py[cod]$",
    r".*\$py\.class$",
    r"^venv/.*",
    r"^env/.*",
    r"staticfiles/.*",
    r"media/.*",
    r".*\.log$",
]

data = json.load(sys.stdin)
path = data.get("tool_input", {}).get("path", "")

# Normalize to forward slashes
path = path.replace("\\", "/")

if any(path.endswith(f) or path == f for f in BLOCKED_EXACT):
    print(json.dumps({"allow": False, "reason": f"[Django] Blocked sensitive file: {path}"}))
    sys.exit(0)

for pattern in BLOCKED_PATTERNS:
    if re.search(pattern, path):
        print(json.dumps({"allow": False, "reason": f"[Django] Blocked by pattern {pattern}: {path}"}))
        sys.exit(0)

print(json.dumps({"allow": True}))