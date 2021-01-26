from rest_framework import serializers
from ..models.cart import Carts
from .product import DetailProductSerializer
from ..models.promotion import Promotions


class PromotionSerializer(serializers.ModelSerializer):
    time_create = serializers.DateTimeField(format='%H:%M:%S %d/%m/%Y', read_only=True)
    time_from = serializers.DateTimeField(format='%H:%M:%S %d/%m/%Y', input_formats=['%H:%M:%S %d/%m/%Y'])
    time_to = serializers.DateTimeField(format='%H:%M:%S %d/%m/%Y', input_formats=['%H:%M:%S %d/%m/%Y'])
    class Meta:
        model = Promotions
        fields = ['id' ,'name','type', 'time_from', 'time_to', 'value', 'max_value', 'comment', 'time_create', 'on_delete',]
        read_only_fields = ['id' ,'time_create', 'on_delete']


class CartSerializer(serializers.ModelSerializer):
    product_detail = DetailProductSerializer(read_only=True)
    promotion=PromotionSerializer(read_only=True)
    class Meta:
        model = Carts
        fields = ['id', 'product_detail', 'amount', 'promotion', 'time_create', 'time_update']


class CreateCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carts
        fields = ['id', 'product_detail', 'amount', 'user', 'promotion']

    def validate(self, attrs):
        if attrs.get('amount') <= 0:
            raise serializers.ValidationError({'message': 'Số lượng hàng trong giỏ phải lớn hơn 0'})
        return attrs


class UpdateCartSerializer(serializers.ModelSerializer):
    product_detail = DetailProductSerializer(read_only=True,)
    promotion = PromotionSerializer(read_only=True)
    class Meta:
        model = Carts
        fields = ['id', 'product_detail', 'amount', 'promotion', 'time_create', 'time_update']
        read_only_fields = ['id', 'product_detail', 'promotion', 'time_create', 'time_update']

    def validate(self, attrs):
        if attrs.get('amount') <= 0:
            raise serializers.ValidationError({'message': 'Số lượng hàng trong giỏ phải lớn hơn 0'})
        return attrs
