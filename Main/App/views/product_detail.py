from ..models.product import Types, Products, Details, Amounts, Image, Describe
from ..serializer.product import TypesSerializer, ProductsSerializer, DetailsSerialiser, AmountsSerializer, \
    ImageSerializer, DescribeSerializer, AvatarProductSerializer, UpdateFromPriceProductSerializer, \
    UpdateToPriceProductSerializer, DetailProductSerializer
from rest_framework.response import Response
from rest_framework import status, permissions, parsers, generics
from ..utils.check_permission import check_permission
from ..utils.function import get_min_price
from django.core.paginator import Paginator
from .product import Type


class DetailProducts(generics.ListCreateAPIView):
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            id = kwargs.get('id')
            product = Products.objects.get(id=id)
            serializer = ProductsSerializer(product)
            same_product = Products.objects.filter(type=product.type).exclude(id=id)[0:4]
            # import pdb; pdb.set_trace()
            serializer_same = ProductsSerializer(same_product, many=True)
            res = {
                "product": serializer.data,
                "same_product": serializer_same.data
            }
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        perm = "App.change_products"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get('id')
                product = Products.objects.get(id=id)
                if "avatar" in request.data:
                    serializer = AvatarProductSerializer(product, data=request.data)
                else:
                    serializer = ProductsSerializer(product, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data.copy()
                    return Response(data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Products.DoesNotExist:
                return Response({"message": ["Không có sản phẩm này"]}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status_code)

    def delete(self, request, *args, **kwargs):
        perm = "App.delete_products"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get("id")
                product = Products.objects.get(id=id)
                product.on_delete = True
                product.save()
                return Response(status=status.HTTP_200_OK)
            except Products.DoesNotExist:
                return Response({"message": ["Không có sản phẩm này."]}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response({"message": ["Đã có lỗi sảy ra, bạn vui lòng thử lại sau."]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)


class DetailProductsDetails(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            id = kwargs.get('id')
            detail = Details.objects.get(id=id)
            serializer = DetailProductSerializer(detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        perm = "App.change_details"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get('id')
                detail = Details.objects.get(id=id)
                serializer = DetailsSerialiser(detail, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    product = Products.objects.get(id=serializer.data['product'])
                    details = Details.objects.filter(product=product)
                    p_min = min(details, key=get_min_price)
                    p_max = max(details, key=get_min_price)

                    p_serializer = UpdateFromPriceProductSerializer(product, data={'from_saleprice': p_min.saleprice})
                    if p_serializer.is_valid():
                        p_serializer.save()

                    p_serializer = UpdateToPriceProductSerializer(product, data={'to_saleprice': p_max.saleprice})
                    if p_serializer.is_valid():
                        p_serializer.save()
                    data = serializer.data.copy()
                    return Response(data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Details.DoesNotExist:
                return Response({"message": ["Không có sản phẩm này"]}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status_code)

    def delete(self, request, *args, **kwargs):
        perm = "App.delete_details"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get("id")
                Details.objects.get(id=id).delete()
                return Response(status=status.HTTP_200_OK)
            except Details.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)


class DetailTypes(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            id = kwargs.get('id')
            type = Types.objects.get(id=id)
            serializer = TypesSerializer(type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        perm = "App.change_types"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get('id')
                type = Types.objects.get(id=id)
                serializer = TypesSerializer(type, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data.copy()
                    return Response(data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Types.DoesNotExist:
                return Response({"message": ["Không có loại sản phẩm này"]}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status_code)

    def delete(self, request, *args, **kwargs):
        perm = "App.delete_types"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get("id")
                type = Types.objects.get(id=id)
                type.on_delete = True
                type.save()
                type = Types.objects.filter(on_delete=False)
                serializer = TypesSerializer(type, many=True)
                page = int(request.GET.get('page', 1))
                limit = int(request.GET.get('limit', 20))
                pagination = Paginator(serializer.data, limit)
                result = pagination.get_page(page)
                response = {
                    "total": type.count(),
                    "data": result.object_list,
                    "page": result.number,
                    "has_next": result.has_next(),
                    "has_prev": result.has_previous()
                }
                return Response(response, status=status.HTTP_200_OK)
            except Types.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)


class DetailDescribes(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def put(self, request, *args, **kwargs):
        perm = "App.change_describe"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get('id')
                describe = Describe.objects.get(id=id)
                serializer = DescribeSerializer(describe, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data.copy()
                    return Response(data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Describe.DoesNotExist:
                return Response({"message": "Không có mô tả này"}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status=status_code)

    def delete(self, request, *args, **kwargs):
        perm = "App.delete_describe"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get("id")
                Describe.objects.get(id=id).delete()
                return Response(status=status.HTTP_200_OK)
            except Describe.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)


class DetailImages(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def delete(self, request, *args, **kwargs):
        perm = "App.delete_image"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                id = kwargs.get("id")
                Image.objects.get(id=id).delete()
                return Response(status=status.HTTP_200_OK)
            except Describe.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)