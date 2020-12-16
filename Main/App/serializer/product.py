from rest_framework import serializers
from ..models.product import Types, Products, Details, Amounts, Image, Describe, Description
from ..utils.function import get_min_price

class TypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Types
        fields = ['id', 'type']




class DetailsSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Details
        fields = ['id', 'product', 'size', 'color', 'price', 'saleprice', 'amount']
        read_only_fields=['amount']

    def validate(self, attrs):
        if attrs.get('saleprice') < 0:
            raise serializers.ValidationError({'message': ['Giá bán phải lớn hơn hoặc bằng 0']})
        return attrs

    def create(self, validated_data):
        detail = Details.objects.create(
            product=validated_data.get('product'),
            size=validated_data.get('size'),
            color=validated_data.get('color'),
            price=validated_data.get('price'),
            saleprice=validated_data.get('saleprice')
        )
        detail.save()
        product = validated_data.get('product')
        details = Details.objects.filter(product=product, on_delete=False)
        p_min = min(details, key=get_min_price)
        p_max = max(details, key=get_min_price)
        saleprice = validated_data.get('saleprice')
        if product.from_saleprice > p_min.saleprice:
            product.from_saleprice = saleprice
        if product.to_saleprice < p_max.saleprice:
            product.to_saleprice = p_max.saleprice
        product.save()
        return detail





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
        #     raise serializers.ValidationError({'message': 'số lượng đã bán phải lớn hơn hoặc bằng 0'})
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


class EditDetailsSerialiser(serializers.ModelSerializer):
    product = ProductSerializerDetails(read_only=True)
    class Meta:
        model = Details
        fields = ['id', 'product', 'size', 'color', 'price', 'saleprice', 'amount']
        read_only_fields = ['product', 'amount']

    def validate(self, attrs):
        if attrs.get('saleprice') < 0:
            raise serializers.ValidationError({'message': ['Giá bán phải lớn hơn hoặc bằng 0']})
        return attrs

    def update(self, instance, validated_data):
        instance.size = validated_data.get('size')
        instance.color = validated_data.get('color')
        instance.price = validated_data.get('price')
        instance.saleprice = validated_data.get('saleprice')
        instance.save()
        product = instance.product
        details = Details.objects.filter(product=product, on_delete=False)
        p_min = min(details, key=get_min_price)
        p_max = max(details, key=get_min_price)
        saleprice = validated_data.get('saleprice')
        if product.from_saleprice > p_min.saleprice:
            product.from_saleprice = saleprice
        if product.to_saleprice < p_max.saleprice:
            product.to_saleprice = p_max.saleprice
        product.save()
        return instance

class AmountsSerializer(serializers.ModelSerializer):
    time_create = serializers.DateTimeField(format='%H:%M:%S %d-%m-%Y', read_only=True)
    detail=DetailProductSerializer(read_only=True)
    class Meta:
        model = Amounts
        fields = ['id', 'detail', 'price', 'amount', 'note' , 'is_plus', 'time_create']

class CreateAmountsSerializer(serializers.ModelSerializer):
    time_create = serializers.DateTimeField(format='%H:%M:%S %d-%m-%Y', read_only=True)
    class Meta:
        model = Amounts
        fields = ['id', 'detail', 'price', 'amount', 'note' , 'is_plus', 'time_create']

    def validate(self, attrs):
        if attrs.get('amount') <= 0:
            raise serializers.ValidationError({'message': ['Số lượng phải lớn hơn 0.']})
        if attrs.get('price') <= 0:
            raise serializers.ValidationError({'message': ['Giá bán tiền phải lớn hơn 0.']})
        if not attrs.get('is_plus'):
            if attrs.get('amount') > attrs.get('detail').amount:
                raise serializers.ValidationError({'message': ['Số lượng trừ đi phải nhỏ hơn hoặc bằng số lượng trong kho.']})
        return attrs

    def create(self, validated_data):
        detail = validated_data.get('detail')
        amounts = Amounts.objects.create(
            detail=detail,
            price=validated_data.get('price'),
            amount=validated_data.get('amount'),
            note=validated_data.get('note'),
            is_plus=validated_data.get('is_plus')
        )
        if amounts.is_plus:
            detail.amount += amounts.amount
        else:
            detail.amount -= amounts.amount
        if detail.amount >= 0:
            detail.save()
        amounts.save()
        return amounts
