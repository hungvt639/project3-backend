from rest_framework import serializers
from ..models.product import Types, Products, Details, Amounts, Image, Describe


class AmountsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Amounts
        fields = ['id', 'detail', 'price', 'amount', 'time_create']


class DetailsSerialiser(serializers.ModelSerializer):
    # amounts = AmountsSerializer(many=True, read_only=True)

    class Meta:
        model = Details
        fields = ['id', 'product', 'size', 'color', 'price', 'saleprice', 'amount']


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'product', 'img']


class DescribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Describe
        fields = ['id', 'product', 'header', 'context']


class ProductsSerializer(serializers.ModelSerializer):
    details = DetailsSerialiser(many=True, read_only=True)
    image = ImageSerializer(many=True, read_only=True)
    describe = DescribeSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = ['id', 'name', 'avatar', 'sold', 'type', 'from_saleprice', 'to_saleprice', 'comments', 'details', 'image', 'describe']


class AvatarProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'avatar']


class TypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Types
        fields = ['id', 'type']


class UpdateFromPriceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['from_saleprice']


class UpdateToPriceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['to_saleprice']