from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions

from .models import Image360
from .serializers import Image360Serializer


class Image360ViewSet(viewsets.ReadOnlyModelViewSet):
    """
    http://127.0.0.1:8000/api/image360/
    """
    queryset = Image360.objects.all()
    serializer_class = Image360Serializer
    # permission_classes = [permissions.]

# class Image360View(APIView):
#     """
#     http://127.0.0.1:8000/api/image360/
#     """
#     def get(self, request):
#         images360 = Image360.objects.all()
#         # the many param informs the serializer that it will be serializing more than a single object.
#         # serializer = Image360Serializer(images360, many=True)
#         serializer = Image360Serializer(images360, context={'request': request})
#         return Response({"image360": serializer.data})
