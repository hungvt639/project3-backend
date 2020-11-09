from rest_framework import serializers
from ..models.Snippets import Snippet
from Users.serializer import UserSerializer


class SnippetSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    owner = UserSerializer

    class Meta:
        model = Snippet
        fields = ['created', 'title', 'code', 'linenos', 'language', 'style', 'owner']