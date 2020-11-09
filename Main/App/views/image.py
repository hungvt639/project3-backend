from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..serializer.image import FileSerializer
from rest_framework.parsers import MultiPartParser


class FileUpload(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


