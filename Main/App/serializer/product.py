from rest_framework import serializers
from ..models.product import Types, Products, Details, Amounts, Image, Describe


class TypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Types
        fields = ['id', 'type']


class AmountsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Amounts
        fields = ['detail', 'price', 'amount', 'time_create']


class DetailsSerialiser(serializers.ModelSerializer):
    amounts = AmountsSerializer(many=True, read_only=True)

    class Meta:
        model = Details
        fields = ['product', 'size', 'color', 'price', 'saleprice', 'amount', 'amounts']


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['product', 'img']


class DescribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Describe
        fields = ['product', 'header', 'context']


class ProductsSerializer(serializers.ModelSerializer):
    details = DetailsSerialiser(many=True, read_only=True)
    image = ImageSerializer(many=True, read_only=True)
    describe = DescribeSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = ['id', 'name', 'avatar', 'sold', 'type', 'from_saleprice', 'to_saleprice', 'comments', 'details', 'image', 'describe']


class TypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Types
        fields = ['id', 'type']