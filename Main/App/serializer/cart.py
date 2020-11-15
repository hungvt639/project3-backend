from rest_framework import serializers
from ..models.cart import Carts
from .product import DetailProductSerializer


class CartSerializer(serializers.ModelSerializer):
    product_detail = DetailProductSerializer(read_only=True)

    class Meta:
        model = Carts
        fields = ['id', 'product_detail', 'amount', 'time_create', 'time_update']


class CreateCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carts
        fields = ['product_detail', 'amount', 'user']

    def validate(self, attrs):
        if attrs.get('amount') <= 0:
            raise serializers.ValidationError({'message': 'Số lượng hàng trong giỏ phải lớn hơn 0'})
        return attrs


class UpdateCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carts
        fields = ['amount']

    def validate(self, attrs):
        if attrs.get('amount') <= 0:
            raise serializers.ValidationError({'message': 'Số lượng hàng trong giỏ phải lớn hơn 0'})
        return attrs
