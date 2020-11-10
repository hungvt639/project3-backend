from ..models.product import Types, Products, Details, Amounts, Image
from ..serializer.product import TypesSerializer, ProductsSerializer, DetailsSerialiser, AmountsSerializer, ImageSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.core.paginator import Paginator
from ..utils.check_permission import check_permission


class Type(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TypesSerializer

    def get(self, request, *args, **kwargs):
        type = Types.objects.all()
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

    def post(self, request, *args, **kwargs):
        perm = "App.add_types"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                serializer = TypesSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data.copy()
                    response = {
                        "data":data
                    }
                    return Response(response, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)


class Product(generics.ListCreateAPIView):
    # serializer_class = ProductsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, *args, **kwargs):
        product = Products.objects.all()
        serializer = ProductsSerializer(product, many=True)
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        pagination = Paginator(serializer.data, limit)
        result = pagination.get_page(page)
        response = {
            "total": product.count(),
            "data": result.object_list,
            "page": result.number,
            "has_next": result.has_next(),
            "has_prev": result.has_previous()
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        perm = "App.add_products"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                serializer = ProductsSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data.copy()
                    response = {
                        "data": data
                    }
                    return Response(response, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)


class Detail(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = DetailsSerialiser

    def get(self, request, *args, **kwargs):
        detail = Details.objects.all()
        serializer = DetailsSerialiser(detail, many=True)
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        pagination = Paginator(serializer.data, limit)
        result = pagination.get_page(page)
        response = {
            "total": detail.count(),
            "data": result.object_list,
            "page": result.number,
            "has_next": result.has_next(),
            "has_prev": result.has_previous()
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        perm = "App.add_details"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                serializer = DetailsSerialiser(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data.copy()
                    response = {
                        "data": data
                    }
                    return Response(response, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)


class Amount(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = AmountsSerializer

    def get(self, request, *args, **kwargs):
        amount = Amounts.objects.all()
        serializer = AmountsSerializer(amount, many=True)
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        pagination = Paginator(serializer.data, limit)
        result = pagination.get_page(page)
        response = {
            "total": amount.count(),
            "data": result.object_list,
            "page": result.number,
            "has_next": result.has_next(),
            "has_prev": result.has_previous()
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        perm = "App.add_details"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                serializer = AmountsSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data.copy()
                    response = {
                        "data": data
                    }
                    return Response(response, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)