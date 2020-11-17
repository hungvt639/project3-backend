from rest_framework import serializers
from ..models.order import Order, OrderProduct
from ..utils.function import get_price_order_product
from .deliveryaddress import DeliveryAddressSerializer
from ..models.deliveryaddress import DeliveryAddress

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
    delivery_address = DeliveryAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'price', 'status', 'time_create', 'time_update', 'product', 'delivery_address']
        read_only_fields = ['price', 'status', 'time_create', 'time_update']


class CreateOrderSerializer(serializers.ModelSerializer):
    product = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'delivery_address']

    def create(self, validated_data):
        products = validated_data.get('product')
        price = sum([get_price_order_product(i) for i in products])
        order = Order.objects.create(
            user=validated_data.get('user'),
            price=price,
            status=1,
            delivery_address=validated_data.get('delivery_address')
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

    def validate(self, attrs):
        deli_add = DeliveryAddress.objects.filter(user=attrs.get('user'), on_delete=False)
        if attrs.get('delivery_address') not in deli_add:
            raise serializers.ValidationError({"message": "Không có địa chỉ này trong danh sách địa chỉ của bạn"})
        if not len(attrs.get('product')):
            raise serializers.ValidationError({'message': 'Không có sản phẩm nào trong đơn hàng'})
        return attrs


class UpdateOrderManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    # def validate(self, attrs):
    #     print(attrs)
    #     import pdb; pdb.set_trace()
    #     return attrs


class UpdateOrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate(self, attrs):
        if attrs.get('status') < 5:
            raise serializers.ValidationError({'message': 'Bạn không thể chuyển đơn hàng về trạng thái này'})
        return attrs