from rest_framework import serializers
from ..models.deliveryaddress import DeliveryAddress
import re
r = re.compile(r'^\d{0}?(0|9)\d{9}$')


class DeliveryAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryAddress
        fields = ['user', 'phone', 'address', 'default']

    def validate(self, attrs):
        if r.search(attrs.get("phone")):
            serializers.ValidationError({"message": "Số điện thoại không hợp lệ"})
        return attrs


class UpdateDeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['default']


class DeleteDeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['on_delete']