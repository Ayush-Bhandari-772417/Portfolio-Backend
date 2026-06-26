# apps/subscription/public/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from django.conf import settings
import requests
from config.public.base import PublicBaseCreateViewSet
from ..models import Subscription
from ..serializers import SubscriptionSerializer

class SubscriptionRateThrottle(AnonRateThrottle):
    rate = "3/min"

class PublicSubscriptionViewSet(PublicBaseCreateViewSet):
    serializer_class = SubscriptionSerializer
    throttle_classes = [SubscriptionRateThrottle]
    queryset = Subscription.objects.none()

    def create(self, request, *args, **kwargs):
        token = request.data.get("token")
        if not token:
            return Response(
                {"error": "Missing reCAPTCHA token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ---- reCAPTCHA verification ----
        recaptcha_secret = getattr(settings, "RECAPTCHA_SECRET_KEY", None)
        if not recaptcha_secret:
            # Misconfiguration — fail loudly in logs, safely to client
            import logging
            logging.getLogger(__name__).error(
                "RECAPTCHA_SECRET_KEY is not configured in settings"
            )
            return Response(
                {"error": "Server configuration error. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            recaptcha_res = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={"secret": recaptcha_secret, "response": token},
                timeout=5,      # ← never hang more than 5 seconds
            ).json()
        except requests.exceptions.Timeout:
            return Response(
                {"error": "Security verification timed out. Please try again."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except requests.exceptions.RequestException:
            return Response(
                {"error": "Security verification unavailable. Please try again."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        if (
            not recaptcha_res.get("success")
            or recaptcha_res.get("score", 0) < 0.5
            or recaptcha_res.get("action") != "subscribe"
        ):
            return Response(
                {"error": "reCAPTCHA failed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ---- Save subscription ----
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT"),
        )

        return Response(
            {"message": "Subscribed successfully!"},
            status=status.HTTP_201_CREATED
        )