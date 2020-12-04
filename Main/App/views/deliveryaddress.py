from ..models.deliveryaddress import DeliveryAddress
from ..serializer.deliveryaddress import DeliveryAddressSerializer, UpdateDeliveryAddressSerializer, DeleteDeliveryAddressSerializer
from rest_framework.response import Response
from rest_framework import status, parsers, generics
from django.core.paginator import Paginator
from ..utils.check_permission import check_permission
from Users.models import MyUsers


class DeliveryAddressView(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        perm = "App.view_deliveryaddress"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            user = MyUsers.objects.get(id=request.user.id)
            order_by = request.GET.get("order-by", 0)
            deliveryaddress = DeliveryAddress.objects.filter(user=user, on_delete=False)
            if order_by:
                deliveryaddress = deliveryaddress.order_by('-default')
            serializer = DeliveryAddressSerializer(deliveryaddress, many=True)
            response = {
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(data, status=status_code)

    def post(self, request, *args, **kwargs):
        perm = "App.add_deliveryaddress"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            # import pdb; pdb.set_trace()
            try:
                request.data['user'] = request.user.id
                serializer = DeliveryAddressSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    user = MyUsers.objects.get(id=request.user.id)
                    deliveryaddress = DeliveryAddress.objects.filter(user=user, on_delete=False)
                    serializer = DeliveryAddressSerializer(deliveryaddress, many=True)
                    response = {
                        "data": serializer.data
                    }
                    return Response(response, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e: raise e
            except:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)


class DetailDeliveryAddressView(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        perm = "App.view_deliveryaddress"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get('id')
                user = MyUsers.objects.get(id=request.user.id)
                deliveryaddress = DeliveryAddress.objects.filter(user=user, on_delete=False)
                deliveryaddress = deliveryaddress.get(id=id)
                serializer = DeliveryAddressSerializer(deliveryaddress)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data, status=status_code)

    def put(self, request, *args, **kwargs):
        perm = "App.change_deliveryaddress"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get('id')
                user = MyUsers.objects.get(id=request.user.id)
                deliveryaddress = DeliveryAddress.objects.filter(user=user, on_delete=False)
                deliveryaddress = deliveryaddress.get(id=id)
                serializer = UpdateDeliveryAddressSerializer(deliveryaddress, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    deliveryaddress = DeliveryAddress.objects.filter(user=user, on_delete=False)
                    serializer = DeliveryAddressSerializer(deliveryaddress, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except DeliveryAddress.DoesNotExist:
                return Response({"message": ["Không có địa chỉ này"]}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status_code)

    def delete(self, request, *args, **kwargs):
        perm = "App.delete_deliveryaddress"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get("id")
                user = MyUsers.objects.get(id=request.user.id)
                deliveryaddress = DeliveryAddress.objects.filter(user=user, on_delete=False)
                deliveryaddress = deliveryaddress.get(id=id)
                serializer = DeleteDeliveryAddressSerializer(deliveryaddress, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    deliveryaddress = DeliveryAddress.objects.filter(user=user, on_delete=False)
                    serializers = DeliveryAddressSerializer(deliveryaddress, many=True)
                    return Response(serializers.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except DeliveryAddress.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)