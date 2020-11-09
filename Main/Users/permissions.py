from rest_framework import permissions
from .models import MyUsers
from django.contrib.auth.models import Permission


def user_permission(id):

    user = MyUsers.objects.get(pk=id)
    permission_list = [
        Permission.objects.get(codename='view_myusers'),
        Permission.objects.get(codename='change_myusers'),

        Permission.objects.get(codename='view_snippet'),
        Permission.objects.get(codename='change_snippet'),
        Permission.objects.get(codename='add_snippet'),
        Permission.objects.get(codename='delete_snippet')
    ]
    user.user_permissions.set(permission_list)