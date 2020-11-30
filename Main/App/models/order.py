from django.db import models
from Users.models import MyUsers
from .product import Details
from .deliveryaddress import DeliveryAddress
import uuid

ORDER_STATUS = [
    (1, "Chờ xác nhận"),
    (2, "Chờ lấy hàng"),
    (3, "Đang giao"),
    (4, "Đã giao"),
    (5, "Đã hủy"),
    (6, "Đã xóa")
]


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(MyUsers, related_name="user", on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(DeliveryAddress, related_name="delivery_address", on_delete=models.CASCADE)
    price = models.IntegerField()
    status = models.IntegerField(choices=ORDER_STATUS, default=1)
    message = models.CharField(max_length=250, null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Order by" + str(self.user) + ": " + str(self.id)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name="product", on_delete=models.CASCADE)
    detail_product = models.ForeignKey(Details, on_delete=models.CASCADE)
    amount = models.IntegerField()