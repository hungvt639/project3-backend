from rest_framework import serializers
from ..models.deliveryaddress import DeliveryAddress
import re
r = re.compile(r'^\d{0}?(0|9)\d{9}$')


class DeliveryAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryAddress
        fields = ['id', 'user', 'fullname', 'phone', 'address', 'default']

    def validate(self, attrs):
        # print(attrs)
        if not r.search(attrs.get("phone")):
            raise serializers.ValidationError({"message": ["Số điện thoại không hợp lệ"]})
        return attrs

    def create(self, validated_data):
        add = DeliveryAddress.objects.create(
            user=validated_data.get('user'),
            fullname=validated_data.get('fullname'),
            phone=validated_data.get('phone'),
            address=validated_data.get('address'),
            default=validated_data.get('default')
        )
        address = DeliveryAddress.objects.filter(user=validated_data.get('user'), default=True)
        if address:
            if validated_data.get('default'):
                for addr in address:
                    addr.default = False
                    addr.save()
        else:
            add.default = True
        add.save()
        return add


class UpdateDeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['fullname', 'phone', 'address', 'default']

    def update(self, instance, validated_data):
        if validated_data.get("default"):
            dellivery_address = DeliveryAddress.objects.filter(user=instance.user, on_delete=False)
            for del_add in dellivery_address:
                del_add.default = False
                del_add.save()
        instance.default = validated_data.get('default')
        instance.fullname = validated_data.get('fullname')
        instance.phone = validated_data.get('phone')
        instance.address = validated_data.get('address')
        instance.save()
        return instance

    def validate(self, attrs):
        # print(attrs)
        if not r.search(attrs.get("phone")):
            raise serializers.ValidationError({"message": ["Số điện thoại không hợp lệ"]})
        return attrs


class DeleteDeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ['on_delete']

    def update(self, instance, validated_data):
        instance.on_delete = True
        instance.save()
        if instance.default == True:
            dellivery_address = DeliveryAddress.objects.filter(user=instance.user, on_delete=False).last()
            dellivery_address.default = True
            dellivery_address.save()
        return instance