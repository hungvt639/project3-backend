from django.db import models
from Users.models import MyUsers
from .product import Details
from .promotion import Promotions

class Carts(models.Model):
    user = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    product_detail = models.ForeignKey(Details, on_delete=models.CASCADE)
    amount = models.IntegerField()
    promotion = models.ForeignKey(Promotions, related_name="cart", on_delete=models.CASCADE, blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Cart - " + str(self.user) + " - " + str(self.product_detail)