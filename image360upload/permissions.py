from rest_framework.permissions import BasePermission


class CheckAPIKEYAuth(BasePermission):
    def has_permission(self, request, view):
        # API_KEY should be in request headers to authenticate requests
        api_key_secret = request.META.get('HTTP_APIKEY')
        print(api_key_secret == '222')
        return api_key_secret == '222'