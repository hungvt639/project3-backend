from ..models.product import Types, Products, Details, Amounts, Image, Describe
from ..serializer.product import TypesSerializer, ProductsSerializer, DetailsSerialiser, AmountsSerializer, \
    ImageSerializer, DescribeSerializer, AvatarProductSerializer, UpdateFromPriceProductSerializer, \
    UpdateToPriceProductSerializer, DetailProductSerializer
from rest_framework.response import Response
from rest_framework import status, permissions, parsers, generics
from ..utils.check_permission import check_permission
from ..utils.function import get_min_price
import os


class DetailProducts(generics.ListCreateAPIView):
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            id = kwargs.get('id')
            product = Products.objects.get(id=id)
            serializer = ProductsSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
                return Response({"message": "Không có sản phẩm này"}, status=status.HTTP_404_NOT_FOUND)
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
                Products.objects.get(id=id).delete()
                return Response(status=status.HTTP_200_OK)
            except Products.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
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
                raise e
            except Details.DoesNotExist:
                return Response({"message": "Không có sản phẩm này"}, status=status.HTTP_404_NOT_FOUND)
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
                return Response({"message": "Không có loại sản phẩm này"}, status=status.HTTP_404_NOT_FOUND)
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
                Types.objects.get(id=id).delete()
                return Response(status=status.HTTP_200_OK)
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