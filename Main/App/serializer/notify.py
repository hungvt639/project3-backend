from rest_framework import serializers
from ..models.notify import Notify


class NotifySerializer(serializers.ModelSerializer):
    time_create = serializers.DateTimeField(format='%H:%M:%S %d-%m-%Y')

    class Meta:
        model = Notify
        fields = ['id', 'head', 'content', 'status', 'time_create']


class CreateNotifySerializer(serializers.ModelSerializer):

    class Meta:
        model = Notify
        fields = ['id', 'user', 'head', 'content']


class UpdateNotifySerializer(serializers.ModelSerializer):

    class Meta:
        model = Notify
        fields = ['status']