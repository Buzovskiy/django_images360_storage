from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions

from .models import Image360
from .serializers import Image360Serializer
from .permissions import CheckAPIKEYAuth


class Image360ViewSet(viewsets.ReadOnlyModelViewSet):
    """
    http://127.0.0.1:8000/api/image360/
    """
    queryset = Image360.objects.all()
    serializer_class = Image360Serializer
    permission_classes = [CheckAPIKEYAuth]

