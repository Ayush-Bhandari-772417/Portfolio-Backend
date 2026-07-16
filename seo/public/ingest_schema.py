from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from seo.models import SchemaMarkup


@api_view(['POST'])
@permission_classes([AllowAny])
def ingest_schema_node(request):
    """Upsert one JSON-LD node into SchemaMarkup.

    Expected body:
    {
      "page_path": "/",
      "schema_type": "Person",   # or node['@type']
      "json": { ... },           # JSON-LD node object
      "validate": true|false
    }
    """
    page_path = request.data.get('page_path')
    schema_type = request.data.get('schema_type')
    node_json = request.data.get('json')
    validate = bool(request.data.get('validate', False))

    if not page_path or not schema_type or node_json is None:
        return Response(
            {'error': 'page_path, schema_type, and json are required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    schema, _ = SchemaMarkup.objects.update_or_create(
        page_path=page_path,
        schema_type=schema_type,
        defaults={
            'json_content': node_json,
            'generated_at': timezone.now(),
            'is_valid': False,
            'validation_errors': [],
        },
    )

    if validate:
        errors = []
        json_content = schema.json_content
        if '@context' not in str(json_content):
            errors.append('Missing @context')
        if '@type' not in str(json_content):
            errors.append('Missing @type')
        schema.is_valid = len(errors) == 0
        schema.validation_errors = errors
        schema.save()

    return Response({'ok': True, 'page_path': schema.page_path, 'schema_type': schema.schema_type})

