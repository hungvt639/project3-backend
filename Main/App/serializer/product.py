from rest_framework import serializers
from ..models.product import Types, Products, Details, Amounts, Image, Describe, Description


class TypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Types
        fields = ['id', 'type']


class AmountsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Amounts
        fields = ['id', 'detail', 'price', 'amount', 'time_create']


class DetailsSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Details
        fields = ['id', 'product', 'size', 'color', 'price', 'saleprice', 'amount']

    def validate(self, attrs):
        if attrs.get('saleprice') < 0:
            raise serializers.ValidationError({'message': 'Giá bán phải lớn hơn hoặc bằng 0'})
        if attrs.get('amount') <= 0:
            raise serializers.ValidationError({'message': 'Số lượng phải lớn hơn 0'})
        return attrs


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'product', 'img']

    def validate(self, attrs):
        img = attrs.get('img')
        if img.content_type not in ['image/jpeg', 'image/png',  'image/tiff', 'image/gif']:
            raise serializers.ValidationError({"message": "Định dạng ảnh không hợp lệ"})
        return attrs


class DescribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Describe
        fields = ['id', 'product', 'context']


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ['id', 'product', 'text', 'img']

    def validate(self, attrs):
        img = attrs.get('img')
        if img.content_type not in ['image/jpeg', 'image/png', 'image/tiff', 'image/gif']:
            raise serializers.ValidationError({"message": "Định dạng ảnh không hợp lệ"})
        return attrs


class ProductsLítSerializer(serializers.ModelSerializer):
    type = TypesSerializer()
    # details = DetailsSerialiser(many=True, read_only=True)
    # image = ImageSerializer(many=True, read_only=True)
    # describe = DescribeSerializer(many=True, read_only=True)
    # description = DescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = ['id', 'name', 'avatar', 'sold', 'type', 'from_saleprice', 'to_saleprice', 'comments']
        # fields = ['id', 'name', 'avatar', 'sold', 'type', 'from_saleprice', 'to_saleprice', 'comments', 'details', 'image', 'describe', 'description']


class ProductsSerializer(serializers.ModelSerializer):
    type = TypesSerializer()
    details = DetailsSerialiser(many=True, read_only=True)
    image = ImageSerializer(many=True, read_only=True)
    describe = DescribeSerializer(many=True, read_only=True)
    description = DescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = ['id', 'name', 'avatar', 'sold', 'type', 'from_saleprice', 'to_saleprice', 'comments', 'details', 'image', 'describe', 'description']


class CreateProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = ['id', 'name', 'sold', 'type', 'from_saleprice', 'to_saleprice', 'comments' ]

    def validate(self, attrs):
        # if attrs.get('sold') < 0:
        #     raise serializers.ValidationError({'mesage': 'số lượng đã bán phải lớn hơn hoặc bằng 0'})
        if attrs.get('from_saleprice') < 0:
            raise serializers.ValidationError({'message': ['Giá bán thấp nhất phải lớn hơn hoặc bằng 0']})
        if attrs.get('to_saleprice') < 0:
            raise serializers.ValidationError({'message': ['Giá bán cao nhất phải lớn hơn hoặc bằng 0']})
        if attrs.get('to_saleprice') < attrs.get('from_saleprice'):
            raise serializers.ValidationError({'message': ['Giá bán thấp nhất phải lớn hơn hoặc bằng giá bán cao nhất']})
        return attrs


class AvatarProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'avatar']

    def validate(self, attrs):
        img = attrs.get('avatar')
        # import pdb; pdb.set_trace()
        if img.content_type not in ['image/jpeg', 'image/png', 'image/tiff', 'image/gif']:
            raise serializers.ValidationError({"message": ["Định dạng ảnh không hợp lệ"]})
        return attrs


class UpdateFromPriceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['from_saleprice']


class UpdateToPriceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['to_saleprice']


class ProductSerializerDetails(serializers.ModelSerializer):
    type = TypesSerializer()

    class Meta:
        model = Products
        fields = ['id', 'name', 'avatar', 'sold', 'type', 'from_saleprice', 'to_saleprice', 'comments' ]


class DetailProductSerializer(serializers.ModelSerializer):
    product = ProductSerializerDetails()

    class Meta:
        model = Details
        fields = ['id', 'product', 'size', 'color', 'price', 'saleprice', 'amount']


class UpdateAmountDetailProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ['amount']

    def validate(self, attrs):
        if attrs.get('amount') < 0:
            raise serializers.ValidationError({"message": "Tổng số lượng phải lớn hơn hoặc bằng 0"})
        return attrs