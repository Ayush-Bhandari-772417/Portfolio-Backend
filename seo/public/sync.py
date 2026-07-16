from django.core.management import call_command
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
@permission_classes([AllowAny])
def sync_provider(request, type: str):
    """Trigger provider sync management commands.

    Expected type: one of: gsc | serp | backlinks
    """
    type = (type or '').lower().strip()

    mapping = {
        'gsc': 'sync_gsc',
        'serp': 'sync_serp',
        'backlinks': 'sync_backlinks',
    }

    cmd = mapping.get(type)
    if not cmd:
        return Response(
            {'error': 'Unknown sync type', 'type': type},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # Most commands accept --days/--site-url/--dry-run etc.
        # We call without extra args; they handle env defaults.
        call_command(cmd)
    except Exception as e:
        return Response(
            {'error': 'Sync failed', 'type': type, 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response({'ok': True, 'type': type, 'command': cmd})

