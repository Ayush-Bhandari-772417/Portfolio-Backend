# apps/contacts/public/views.py
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
import requests
from django.conf import settings
from ..models import ContactMessage
from ..serializers import ContactMessageSerializer


class ContactMessageRateThrottle(AnonRateThrottle):
    rate = "3/min"  # only 3 messages per minute per IP


class PublicContactMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Public contact form (POST only, secure, throttled, reCAPTCHA protected)"""
    serializer_class = ContactMessageSerializer
    throttle_classes = [ContactMessageRateThrottle]
    queryset = ContactMessage.objects.none()  # 🚫 never expose messages publicly

    def create(self, request, *args, **kwargs):
        # ---- reCAPTCHA Validation ----
        token = request.data.get("token")
        if not token:
            return Response({"error": "Missing reCAPTCHA token"}, status=status.HTTP_400_BAD_REQUEST)

        recaptcha_res = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": settings.RECAPTCHA_SECRET_KEY, "response": token}
        ).json()

        if (
            not recaptcha_res.get("success")
            or recaptcha_res.get("score", 0) < 0.5
            or recaptcha_res.get("action") != "contact"
        ):
            return Response({"error": "reCAPTCHA failed"}, status=status.HTTP_400_BAD_REQUEST)

        # ---- Save message ----
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save IP + User-Agent
        serializer.save(
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT")
        )

        return Response({"message": "Message sent successfully!"}, status=status.HTTP_201_CREATED)
