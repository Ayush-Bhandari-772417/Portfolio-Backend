# backend/config/security.py
import os

def get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0]
    return request.META.get("REMOTE_ADDR")


def is_allowed_admin_ip(request):
    print("ADMIN LOGIN IP:", get_client_ip(request))

    allowed = os.getenv("ADMIN_ALLOWED_IPS", "")

    allowed_ips = [ip.strip() for ip in allowed.split(",")]

    client_ip = get_client_ip(request)

    return client_ip in allowed_ips
