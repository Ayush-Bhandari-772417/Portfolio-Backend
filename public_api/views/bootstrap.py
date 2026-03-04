# apps/public_api/views/bootstrap.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db import connection

from public_api.services.bootstrap_service import BootstrapService
from public_api.serializers.bootstrap import BootstrapSerializer

@method_decorator(cache_page(60 * 30), name="dispatch")
class BootstrapView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = BootstrapService.get_data()
        serializer = BootstrapSerializer(data)
        return Response(serializer.data)