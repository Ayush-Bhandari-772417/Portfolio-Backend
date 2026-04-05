# apps/core/utils/revalidate.py

import requests
from django.conf import settings

def trigger_revalidation(paths=None, tags=None):
    """
    Hybrid revalidation:
    - paths: exact pages
    - tags: scalable invalidation
    """

    url = getattr(settings, "FRONTEND_REVALIDATE_URL", None)

    if not url:
        print("[REVALIDATE] FRONTEND_REVALIDATE_URL missing")
        return

    payload = {
        "paths": paths or [],
        "tags": tags or [],
    }

    try:
        res = requests.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {settings.REVALIDATE_SECRET}"
            },
            timeout=5
        )

        print("[REVALIDATE] Triggered")
        print("Paths:", payload["paths"])
        print("Tags:", payload["tags"])
        print("Status:", res.status_code)

    except Exception as e:
        print("[REVALIDATE ERROR]", str(e))