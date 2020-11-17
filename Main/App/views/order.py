from ..models.notify import Notify
from ..models.order import Order, OrderProduct
from ..serializer.order import OrderSerializer, UpdateOrderManageSerializer, UpdateOrderUserSerializer, CreateOrderSerializer
from rest_framework.response import Response
from rest_framework import status, parsers, generics
from django.core.paginator import Paginator
from ..utils.check_permission import check_permission
from Users.models import MyUsers


class OrderView(generics.ListCreateAPIView):

    def get(self, request, *args, **kwargs):
        perm = "App.view_order"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            user = MyUsers.objects.get(id=request.user.id)
            order = Order.objects.filter(user=user)
            serializer = OrderSerializer(order, many=True)
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 20))
            pagination = Paginator(serializer.data, limit)
            result = pagination.get_page(page)
            response = {
                "total": order.count(),
                "data": result.object_list,
                "page": result.number,
                "has_next": result.has_next(),
                "has_prev": result.has_previous()
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(data, status=status_code)

    def post(self, request, *args, **kwargs):
        perm = "App.add_order"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                request.data['user'] = request.user.id
                serializer = CreateOrderSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data.copy()
                    data.pop('user')
                    response = {
                        "data": data
                    }
                    return Response(response, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e: raise e
            except:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)


class DetailOrderView(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        perm = "App.view_order"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get('id')
                user = MyUsers.objects.get(id=request.user.id)
                order = Order.objects.filter(user=user)
                order = order.get(id=id)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e: raise e
            except:
                return Response({"message": "Không có đơn hàng này"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data, status=status_code)

    def put(self, request, *args, **kwargs):
        perm = "App.change_order"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get('id')
                user = MyUsers.objects.get(id=request.user.id)
                order = Order.objects.filter(user=user)
                order = order.get(id=id)
                if order.status >= 5:
                    return Response({'message': 'Không thể thay đổi trạng thái đơn hàng đã hủy'}, status=status.HTTP_400_BAD_REQUEST)
                if user.groups.filter(name='admin').exists():
                    serializer = UpdateOrderManageSerializer(order, data=request.data)
                else:
                    if order.status > 1:
                        return Response({'message': 'Không thể hủy trạng thái đơn hàng khi đã chốt đơn'}, status=status.HTTP_400_BAD_REQUEST)
                    serializer = UpdateOrderUserSerializer(order, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data.copy()
                    return Response(data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Order.DoesNotExist:
                return Response({"message": "Không có đơn hàng này"}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status_code)