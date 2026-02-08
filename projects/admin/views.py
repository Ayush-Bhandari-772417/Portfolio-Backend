# apps/projects/admin/views.py
from rest_framework import viewsets
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from config.authentication import CookieJWTAuthentication
from config.permissions import IsSecureAdmin
from django.shortcuts import get_object_or_404
from core.utils.revalidate import trigger_revalidation

from ..models import Project, ProjectGallery
from ..serializers import ProjectSerializer


class AdminProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsSecureAdmin]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    authentication_classes = [CookieJWTAuthentication]
    lookup_field = "slug"  # default slug for detail URLs

    def get_object(self):
        lookup = self.kwargs.get(self.lookup_field)

        # allow numeric ID or slug
        if lookup.isdigit():
            return get_object_or_404(Project, pk=int(lookup))
        return get_object_or_404(Project, slug=lookup)
    
    def get_queryset(self):
        return Project.objects.all()

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        project = serializer.save(user=self.request.user)
        self._handle_gallery_files(project)

    def perform_update(self, serializer):
        project = serializer.save()
        self._handle_gallery_files(project)
        self._handle_gallery_deletions(project)

    def _handle_gallery_files(self, project):
        """Save all new gallery images"""
        gallery_files = self.request.FILES.getlist("gallery")
        for file in gallery_files:
            ProjectGallery.objects.create(project=project, image=file)

    def _handle_gallery_deletions(self, project):
        """Delete gallery images marked for removal"""
        delete_ids = self.request.data.getlist("delete_gallery")
        ProjectGallery.objects.filter(
            id__in=delete_ids,
            project=project
        ).delete()