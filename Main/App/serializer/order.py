from rest_framework import serializers
from ..models.order import Order, OrderProduct
from ..utils.function import get_price_order_product


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = ['id', 'detail_product', 'amount']

    def validate(self, attrs):
        if attrs.get('amount') <= 0:
            raise serializers.ValidationError({"message": "Số lượng sản phẩm phải lớn hơn 0"})
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    time_create = serializers.DateTimeField(format='%H:%M:%S %d-%m-%Y', read_only=True)
    time_update = serializers.DateTimeField(format='%H:%M:%S %d-%m-%Y', read_only=True)
    product = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'price', 'status', 'time_create', 'time_update', 'product']
        read_only_fields = ['price', 'status', 'time_create', 'time_update']

    def create(self, validated_data):
        products = validated_data.get('product')
        price = sum([get_price_order_product(i) for i in products])
        order = Order.objects.create(
            user=validated_data.get('user'),
            price=price,
            status=1
        )
        for product in products:
            order_product = OrderProduct.objects.create(
                order=order,
                detail_product=product.get('detail_product'),
                amount=product.get('amount')
            )
            order_product.save()
        order.save()
        return order


class UpdateOrderManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate(self, attrs):
        print(1)
        import pdb; pdb.set_trace()
        return attrs


class UpdateOrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate(self, attrs):
        print(2)
        import pdb; pdb.set_trace()
        return attrs