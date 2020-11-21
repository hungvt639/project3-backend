from .models import MyUsers
from rest_framework import serializers
from django.contrib.auth.models import Group
import re
r = re.compile(r'^\d{0}?(0|9)\d{9}$')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    birthday = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'], allow_null=True)

    class Meta:
        model = MyUsers
        fields = ['id', 'groups', 'email', 'first_name', 'last_name', 'phone', 'sex', 'address', 'birthday', 'avatar']


class EditAvatar(serializers.ModelSerializer):
    class Meta:
        model = MyUsers
        fields = ['avatar',]


class EditUserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    birthday = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'], allow_null=True)

    class Meta:
        model = MyUsers
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'sex', 'address', 'birthday', 'avatar', 'groups']

    def validate(self, attrs):
        if not r.search(attrs.get("phone")):
            raise serializers.ValidationError({"message": ["Số điện thoại không hợp lệ"]})
        return attrs


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUsers
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'avatar']
        write_only_fields = ('password', )
        read_only_fields = ('id', )

    def create(self, validated_data):
        user = MyUsers.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePassworSerializer(serializers.ModelSerializer):
    model = MyUsers
    fields = ['password']
