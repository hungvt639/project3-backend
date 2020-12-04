from rest_framework import serializers
from ..models.order import Order, OrderProduct
from ..utils.function import get_price_order_product
from .deliveryaddress import DeliveryAddressSerializer
from ..models.deliveryaddress import DeliveryAddress
from ..models.cart import Carts
from .product import DetailProductSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    product_detail = DetailProductSerializer()

    class Meta:
        model = OrderProduct
        fields = ['id', 'product_detail', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    time_create = serializers.DateTimeField(format='%H:%M:%S %d-%m-%Y', read_only=True)
    time_update = serializers.DateTimeField(format='%H:%M:%S %d-%m-%Y', read_only=True)
    product = OrderProductSerializer(many=True, read_only=True)
    delivery_address = DeliveryAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'price', 'status', 'time_create', 'message', 'time_update', 'product', 'delivery_address']
        read_only_fields = ['price', 'status', 'time_create', 'time_update']


class CreateOrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = ['id', 'product_detail', 'amount']

    def validate(self, attrs):
        if attrs.get('amount') <= 0:
            raise serializers.ValidationError({"message": ["Số lượng sản phẩm phải lớn hơn 0"]})
        return attrs


class CreateOrderSerializer(serializers.ModelSerializer):
    product = CreateOrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'message', 'delivery_address']

    def create(self, validated_data):
        products = validated_data.get('product')
        price = sum([get_price_order_product(i) for i in products])
        order = Order.objects.create(
            user=validated_data.get('user'),
            price=price+30000,
            status=1,
            message=validated_data.get('message'),
            delivery_address=validated_data.get('delivery_address')
        )
        for product in products:
            order_product = OrderProduct.objects.create(
                order=order,
                product_detail=product.get('product_detail'),
                amount=product.get('amount')
            )
            product_detail = product.get('product_detail')
            user = validated_data.get('user')
            Carts.objects.filter(user=user, product_detail=product_detail).delete()
            product_detail.amount = product_detail.amount - product.get('amount')
            product_detail.save()
            order_product.save()
        order.save()
        return order

    def validate(self, attrs):
        deli_add = DeliveryAddress.objects.filter(user=attrs.get('user'), on_delete=False)
        if attrs.get('delivery_address') not in deli_add:
            raise serializers.ValidationError({"message": ["Không có địa chỉ này trong danh sách địa chỉ của bạn"]})
        if not len(attrs.get('product')):
            raise serializers.ValidationError({'message': ['Không có sản phẩm nào trong đơn hàng']})
        products = attrs.get('product')
        for product in products:
            if product.get("amount") > product.get('product_detail').amount:
                raise serializers.ValidationError({'message': ["Số lượng sản phẩm ({}) lớn hơn số hàng có sẵn trong kho".format(str(product.get("product_detail")))]})
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
    time_create = serializers.DateTimeField(format='%H:%M:%S %d-%m-%Y', read_only=True)
    time_update = serializers.DateTimeField(format='%H:%M:%S %d-%m-%Y', read_only=True)
    product = OrderProductSerializer(many=True, read_only=True)
    delivery_address = DeliveryAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'price', 'status', 'time_create', 'message', 'time_update', 'product', 'delivery_address']
        read_only_fields = ['id', 'user', 'price', 'time_create', 'message', 'time_update', 'product', 'delivery_address']

    def validate(self, attrs):
        if attrs.get('status') < 5:
            raise serializers.ValidationError({'message': ['Bạn không thể chuyển đơn hàng về trạng thái này']})
        return attrs

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status')
        products = OrderProduct.objects.filter(order=instance)
        for product in products:
            p = product.product_detail
            p.amount = p.amount + product.amount
            p.save()
        instance.save()
        return instance