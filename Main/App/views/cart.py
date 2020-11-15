from ..models.cart import Carts
from ..models.product import Details
from ..serializer.cart import CartSerializer, CreateCartSerializer, UpdateCartSerializer
from rest_framework.response import Response
from rest_framework import status, permissions, parsers, generics
from django.core.paginator import Paginator
from ..utils.check_permission import check_permission
from Users.models import MyUsers


class CartView(generics.ListCreateAPIView):

    def get(self, request, *args, **kwargs):
        perm = 'App.view_carts'
        validate, data, status_code = check_permission(request, perm)
        if validate:
            user = MyUsers.objects.get(id=request.user.id)
            cart = Carts.objects.filter(user=user)
            serializer = CartSerializer(cart, many=True)
            res = {
                "data": serializer.data
            }
            return Response(res, status=status_code)
        else:
            return Response(data, status=status_code)

    def post(self, request, *args, **kwargs):
        perm = 'App.add_carts'
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                request.data['user'] = request.user.id
                user = MyUsers.objects.get(id=request.data['user'])
                detail = Details.objects.get(id=request.data['product_detail'])
                carts = Carts.objects.filter(user=user, product_detail=detail).first()
                if carts:
                    if not "update" in request.data:
                        request.data['amount'] = request.data['amount'] + carts.amount
                    serializer = UpdateCartSerializer(carts, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        data = serializer.data.copy()
                        res = {
                            "message": "Cập nhật số lượng thành công",
                            "data": data
                        }
                        return Response(res, status=status.HTTP_200_OK)
                else:
                    serializer = CreateCartSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        data = serializer.data.copy()
                        res = {
                            "message": "Thêm vào giỏ hàng thành công",
                            "data": data
                        }
                        return Response(res, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Details.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status_code)


class DetailCartView(generics.ListCreateAPIView):

    def put(self, request, *args, **kwargs):
        perm = "App.change_carts"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get('id')
                user = MyUsers.objects.get(id=request.user.id)
                carts = Carts.objects.filter(user=user)
                cart = carts.get(id=id)
                serializer = UpdateCartSerializer(cart, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data.copy()
                    res = {
                        "message": "Cập nhật số lượng thành công",
                        "data": data
                    }
                    return Response(res, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Carts.DoesNotExist:
                return Response({"message": "Không sản phẩn này trong giỏ hàng"}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status_code)

    def delete(self, request, *args, **kwargs):
        perm = "App.delete_carts"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get("id")
                user = MyUsers.objects.get(id=request.user.id)
                carts = Carts.objects.filter(user=user)
                carts.get(id=id).delete()
                return Response(status=status.HTTP_200_OK)
            except Carts.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)