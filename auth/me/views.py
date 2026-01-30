# # apps/auth/me/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response

# class MeView(APIView):
#     def get(self, request):
#         user = request.user
#         return Response({
#             "id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "is_staff": user.is_staff,
#             "is_superuser": user.is_superuser,
#         })






# apps/auth/me/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MeView(APIView):
    """
    Returns current authenticated user
    """
    def get(self, request):
        user = request.user
        if not user or not user.is_authenticated:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        })
