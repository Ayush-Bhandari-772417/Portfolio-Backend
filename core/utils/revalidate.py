# apps/core/utils/revalidate.py

import requests
from django.conf import settings

def trigger_revalidation(paths=None, tags=None):
    if not settings.FRONTEND_REVALIDATE_URL:
        return
    payload = {
        "secret": settings.REVALIDATE_SECRET
    }
    if paths:
        payload["paths"] = paths
    if tags:
        payload["tags"] = tags
    try:
        requests.post(
            settings.FRONTEND_REVALIDATE_URL,
            json=payload,
            timeout=5
        )
    except requests.RequestException:
        pass
