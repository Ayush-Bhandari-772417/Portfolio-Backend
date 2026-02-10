# # # backend/config/authentication.py
# # from rest_framework_simplejwt.authentication import JWTAuthentication

# # class CookieJWTAuthentication(JWTAuthentication):
# #     """
# #     Reads JWT from HttpOnly cookie instead of Authorization header
# #     """

# #     def authenticate(self, request):
# #         print("==== Backend Cookies ====")
# #         print(request.COOKIES)
# #         print("========================")
# #         raw_token = request.COOKIES.get("access")
# #         if not raw_token:
# #             return None

# #         validated_token = self.get_validated_token(raw_token)
# #         return self.get_user(validated_token), validated_token


# # config/authentication.py
# from rest_framework_simplejwt.authentication import JWTAuthentication

# class CookieJWTAuthentication(JWTAuthentication):
#     def authenticate(self, request):
#         raw_token = request.COOKIES.get("access")

#         if not raw_token:
#             return None

#         validated_token = self.get_validated_token(raw_token)
#         return self.get_user(validated_token), validated_token








# config/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get("access")

        if not raw_token:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except Exception:
            raise AuthenticationFailed("Invalid or expired access token")

        user = self.get_user(validated_token)
        return user, validated_token
