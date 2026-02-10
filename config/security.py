# # backend/config/security.py
# import os

# def get_client_ip(request):
#     xff = request.META.get("HTTP_X_FORWARDED_FOR")
#     if xff:
#         return xff.split(",")[0]
#     return request.META.get("REMOTE_ADDR")

# def is_allowed_admin_ip(request):
#     allowed = os.getenv("ADMIN_ALLOWED_IPS", "").strip()

#     # ✅ Allow if not configured (prevents production crash)
#     if not allowed:
#         return True

#     allowed_ips = [ip.strip() for ip in allowed.split(",")]
#     client_ip = get_client_ip(request)

#     return client_ip in allowed_ips
# backend/config/security.py
import os
from django.conf import settings

def get_client_ip(request):
    """
    Trust X-Forwarded-For ONLY in production (behind Railway proxy).
    """
    if not settings.DEBUG:
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


def is_allowed_admin_ip(request):
    allowed = os.getenv("ADMIN_ALLOWED_IPS", "").strip()

    if not allowed:
        return True  # explicit allow if not configured

    allowed_ips = [ip.strip() for ip in allowed.split(",")]
    client_ip = get_client_ip(request)

    return client_ip in allowed_ips
