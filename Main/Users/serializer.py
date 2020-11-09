from .models import MyUsers
from rest_framework import serializers
from App.models.Snippets import Snippet


class UserSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'], allow_null=True)
    class Meta:
        model = MyUsers
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'sex', 'address', 'birthday', 'avatar']


class EditAvatar(serializers.ModelSerializer):
    class Meta:
        model = MyUsers
        fields = ['avatar',]


class EditUserSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'], allow_null=True)
    class Meta:
        model = MyUsers
        fields = ['email', 'first_name', 'last_name', 'phone', 'sex', 'address', 'birthday', 'avatar']


class CreateUserSerializer(serializers.ModelSerializer):
    # birthday = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'], allow_null=True)

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

    # def validate(self, attrs):
    #     import pdb; pdb.set_trace()