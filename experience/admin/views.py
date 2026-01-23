# apps/experience/admin/views.py
from rest_framework import viewsets, permissions, filters, parsers
from django.db import models
from ..models import Experience
from ..serializers import ExperienceSerializer

class AdminExperienceViewSet(viewsets.ModelViewSet):
    """Admin API (CRUD, JWT protected) with search + ordering"""

    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAdminUser]

    # Consistent with Qualification admin
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    # Searchable fields
    search_fields = [
        "title",
        "organization",
        "location",
        "responsibilities",
    ]

    # Sortable fields
    ordering_fields = [
        "start_date",
        "end_date",
        "title",
        "organization",
        "location",
    ]

    # Query ordering (ongoing experiences first)
    def get_queryset(self):
        return Experience.objects.all().order_by(
            models.Case(
                models.When(end_date__isnull=True, then=models.Value(0)),  # ongoing jobs
                default=models.Value(1),
                output_field=models.IntegerField(),
            ),
            "-start_date",
        )



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
# Import models from other apps
from projects.models import Project
from creations.models import Creation
from skills.models import Skill
from services.models import Service
from contacts.models import ContactMessage
from hires.models import HiringMessage
from subscription.models import Subscription
from qualifications.models import Qualification
from socialmedia.models import SocialMedia

@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    """
    Return summary counts for the admin dashboard.
    Protected by JWT and accessible only to admin users.
    """
    data = {
        "contacts": ContactMessage.objects.count(),
        "creations": Creation.objects.count(),
        "experiences": Experience.objects.count(),
        "hires": HiringMessage.objects.count(),
        "projects": Project.objects.count(),
        "qualifications": Qualification.objects.count(),
        "services": Service.objects.count(),
        "skills": Skill.objects.count(),
        "socialmedia": SocialMedia.objects.count(),
        "subscriptions": Subscription.objects.count(),
    }
    return Response(data)
