from rest_framework.permissions import BasePermission
from .models import Website


class CheckAPIKEYAuth(BasePermission):
    def has_permission(self, request, view):
        # API_KEY should be in request headers to authenticate requests
        api_key_secret = request.META.get('HTTP_APIKEY', None)
        if api_key_secret is None or not api_key_secret:
            return False

        return Website.objects.filter(api_key=api_key_secret).all().count()
