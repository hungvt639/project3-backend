from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.core.paginator import Paginator
from ..utils.check_permission import check_permission
from ..models.promotion import Promotions, PromotionProducts
from ..serializer.promotion import PromotionSerializer, DeletePromotionSerializer, GetTypeProductSerializer, \
    ProductsListSerializer, AddProductsPromotionSerializer, PromotionProductSerializer
from ..models.product import Types, Products
from django.db.models import Q
from django.utils import timezone


class PromotionView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        promotion = Promotions.objects.all()

        value = int(request.GET.get('value', 0))
        if value:
            if value == 1:
                now = timezone.now()
                promotion = promotion.filter(on_delete=False, time_from__lt=now, time_to__gt=now)
            if value == 2:
                now = timezone.now()
                promotion = promotion.filter(Q(on_delete=True) | Q(time_from__gt=now) | Q(time_to__lt=now))

        type = int(request.GET.get('type', 0))
        if type:
            promotion = promotion.filter(type=(type - 1))

        inputs = request.GET.get('input', "")
        if inputs:
            promotion = promotion.filter(
                Q(name__contains=inputs) | Q(name__contains=inputs.lower()) | Q(name__contains=inputs.upper()))
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        serializer = PromotionSerializer(promotion.order_by('-time_create'), many=True)
        pagination = Paginator(serializer.data, limit)
        result = pagination.get_page(page)
        response = {
            "total": promotion.count(),
            "data": result.object_list,
            "page": result.number,
            "has_next": result.has_next(),
            "has_prev": result.has_previous()
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        perm = "App.add_promotions"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                print(request.data)
                serializer = PromotionSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data.copy(), status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                raise e
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status_code)


class DetailPromotionView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            id = kwargs.get('id')
            promotion_product = Products.objects.filter(~Q(products__promotion__id=id))
            type = Types.objects.filter(on_delete=False)
            serializer = GetTypeProductSerializer(type, many=True)
            list_types = serializer.data
            for t in list_types:
                products = promotion_product.filter(on_delete=False, type__id=t["id"])
                serializer = ProductsListSerializer(products, many=True)
                t['products'] = serializer.data
            return Response(list_types, status=status.HTTP_200_OK)
        except Exception as e:
            raise e
        except:
            return Response({"message": "Không có đơn hàng này"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        perm = "App.change_promotions"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get('id')
                promotion = Promotions.objects.get(id=id)
                serializer = PromotionSerializer(promotion, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data.copy(), status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Promotions.DoesNotExist:
                return Response({"message": "Không có khuyến mãi này"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                raise e
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status_code)

    def post(self, request, *args, **kwargs):
        perm = "App.delete_promotions"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get('id')
                promotion = Promotions.objects.get(id=id)
                print(request.data)
                serializer = DeletePromotionSerializer(promotion, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Promotions.DoesNotExist:
                return Response({"message": ["Không có khuyến mãi này"]}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status_code)


class AddProductPromotionView(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        perm = "App.add_promotionproducts"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                serializer = AddProductsPromotionSerializer(data=request.data, many=True)
                if serializer.is_valid():
                    serializer.save()
                    list = PromotionProductSerializer(serializer.instance, many=True)
                    return Response(list.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                raise e
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status_code)


class PromotionProductDetailView(generics.ListCreateAPIView):
    def delete(self, request, *args, **kwargs):
        perm = "App.delete_promotionproducts"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get('id')
                PromotionProducts.objects.get(id=id).delete()
                return Response(status=status.HTTP_200_OK)
            except PromotionProducts.DoesNotExist:
                return Response({"message": ["Không có sản phẩm này trong danh sách khuyến mãi"]},
                                status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status_code)
