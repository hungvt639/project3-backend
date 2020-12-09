from ..models.product import Types, Products, Details, Amounts, Image, Describe
from ..serializer.product import TypesSerializer, ProductsLítSerializer, DetailsSerialiser, AmountsSerializer, \
    ImageSerializer, DescribeSerializer, DetailProductSerializer, UpdateAmountDetailProductSerializer, CreateProductsSerializer, DescriptionSerializer
from rest_framework.response import Response
from rest_framework import status, permissions, parsers, generics
from django.core.paginator import Paginator
from ..utils.check_permission import check_permission


class Type(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TypesSerializer

    def get(self, request, *args, **kwargs):
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

    def post(self, request, *args, **kwargs):
        perm = "App.add_types"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                serializer = TypesSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
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
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)


class Product(generics.ListCreateAPIView):
    # serializer_class = ProductsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        type = Types.objects.filter(on_delete=False)
        product = Products.objects.filter(type__in=type, on_delete=False)
        type = int(request.GET.get('type', 0))
        type = Types.objects.filter(id=type)
        if type:
            product = product.filter(type=type.first())
        serializer = ProductsLítSerializer(product, many=True)
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
                serializer = CreateProductsSerializer(data=request.data)
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
        serializer = DetailProductSerializer(detail, many=True)
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
        perm = "App.add_amounts"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                detail = Details.objects.get(id=request.data['detail'])
                d_serializer = UpdateAmountDetailProductSerializer(detail, data={'amount': request.data['amount']+detail.amount})
                serializer = AmountsSerializer(data=request.data)
                if d_serializer.is_valid():
                    if serializer.is_valid():
                        d_serializer.save()
                        serializer.save()
                        data = serializer.data.copy()
                        response = {
                            "data": data
                        }
                        return Response(response, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(d_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Details.DoesNotExist:
                return Response({"message": "Không có sản phẩm này"}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data, status_code)


class Images(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ImageSerializer
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser,)

    def get(self, request, *args, **kwargs):
        image = Image.objects.all()
        serializer = ImageSerializer(image, many=True)
        response = {
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        perm = "App.add_image"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                serializer = ImageSerializer(data=request.data)
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


class Describes(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = DescribeSerializer

    def get(self, request, *args, **kwargs):
        describe = Describe.objects.all()
        serializer = DescribeSerializer(describe, many=True)
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        pagination = Paginator(serializer.data, limit)
        result = pagination.get_page(page)
        response = {
            "total": describe.count(),
            "data": result.object_list,
            "page": result.number,
            "has_next": result.has_next(),
            "has_prev": result.has_previous()
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        perm = "App.add_describe"
        validate, data, status_code = check_permission(request, perm)
        if validate:
            try:
                serializer = DescribeSerializer(data=request.data)
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
