from ..models.Snippets import Snippet
from ..serializer.snippets import SnippetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


class SnippetList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, format=None):
        permission = "App.view_snippet"
        user = request.user
        if user.has_perm(permission):
        # import pdb; pdb.set_trace()
            snippets = Snippet.objects.all()
            serializer = SnippetSerializer(snippets, many=True)
            return Response(serializer.data)
        else:
            return Response({"Error": "You can view Snippets"})

    def post(self, request, format=None):
        # import pdb; pdb.set_trace()
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)