from rest_framework import serializers
from ..models.promotion import Promotions, PromotionProducts, PromotionTypes
from ..models.product import Products, Types


class ProductsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'avatar', 'from_saleprice', 'to_saleprice']

        # extra_kwargs = {
        #     'name': {
        #         'required': False
        #     },
        #     'avatar': {
        #         'required': False
        #     },
        #     'from_saleprice': {
        #         'required': False
        #     },
        #     'to_saleprice': {
        #         'required': False
        #     },
        #
        # }


class PromotionProductSerializer(serializers.ModelSerializer):
    product = ProductsListSerializer(read_only=True)
    class Meta:
        model = PromotionProducts
        fields = ['id' ,'promotion', 'product']


class PromotionSerializer(serializers.ModelSerializer):
    time_create = serializers.DateTimeField(format='%H:%M:%S %d/%m/%Y', read_only=True)
    time_from = serializers.DateTimeField(format='%H:%M:%S %d/%m/%Y', input_formats=['%H:%M:%S %d/%m/%Y'])
    time_to = serializers.DateTimeField(format='%H:%M:%S %d/%m/%Y', input_formats=['%H:%M:%S %d/%m/%Y'])
    promotions = PromotionProductSerializer(many=True, read_only=True)
    class Meta:
        model = Promotions
        fields = ['id' ,'name','type', 'time_from', 'time_to', 'value', 'max_value', 'comment', 'time_create', 'on_delete', 'promotions']
        read_only_fields = ['id' ,'time_create', 'on_delete']

#_____________CREATE______________
class CreatePromotionProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionProducts
        fields = ['id' ,'product']



class DeletePromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotions
        fields = ['on_delete']


class GetTypeProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Types
        fields = ['id', 'type']


class AddProductsPromotionSerializer(serializers.ModelSerializer):
    # product = ProductsListSerializer(read_only=True)
    class Meta:
        model = PromotionProducts
        fields = ['id', 'promotion', 'product']


class AddProductsPromotionSerializer1(serializers.ModelSerializer):
    product = ProductsListSerializer(read_only=True)
    class Meta:
        model = PromotionProducts
        fields = ['id', 'promotion', 'product']