from ..models.notify import Notify
from ..models.product import Details
from ..serializer.notify import NotifySerializer, CreateNotifySerializer, UpdateNotifySerializer
from rest_framework.response import Response
from rest_framework import status, parsers, generics
from django.core.paginator import Paginator
from ..utils.check_permission import check_permission
from Users.models import MyUsers


class NotifyView(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        perm = "App.view_notify"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            user = MyUsers.objects.get(id=request.user.id)
            notify = Notify.objects.filter(user=user)
            serializer = NotifySerializer(notify, many=True)
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 20))
            pagination = Paginator(serializer.data, limit)
            result = pagination.get_page(page)
            response = {
                "total": notify.count(),
                "data": result.object_list,
                "page": result.number,
                "has_next": result.has_next(),
                "has_prev": result.has_previous()
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(data, status=status_code)

    def post(self, request, *args, **kwargs):
        perm = "App.add_notify"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                request.data['user'] = request.user.id
                serializer = CreateNotifySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data.copy()
                    data.pop('user')
                    response = {
                        "data": data
                    }
                    return Response(response, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)


class DetailNotifyView(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        perm = "App.view_notify"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get('id')
                user = MyUsers.objects.get(id=request.user.id)
                notify = Notify.objects.filter(user=user)
                notify = notify.get(id=id)
                serializer = NotifySerializer(notify)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data, status=status_code)

    def put(self, request, *args, **kwargs):
        perm = "App.change_notify"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get('id')
                user = MyUsers.objects.get(id=request.user.id)
                notify = Notify.objects.filter(user=user)
                notify = notify.get(id=id)
                serializer = UpdateNotifySerializer(notify, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data.copy()
                    return Response(data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Notify.DoesNotExist:
                return Response({"message": "Không có thông báo này"}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status_code)

    def delete(self, request, *args, **kwargs):
        perm = "App.delete_notify"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get("id")
                user = MyUsers.objects.get(id=request.user.id)
                notify = Notify.objects.filter(user=user)
                notify = notify.get(id=id)
                notify.delete()
                return Response(status=status.HTTP_200_OK)
            except Notify.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)