from django.db import models
from Users.models import MyUsers
from .product import Details


class Carts(models.Model):
    user = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    product_detail = models.ForeignKey(Details, on_delete=models.CASCADE)
    amount = models.IntegerField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Cart - " + str(self.user) + " - " + str(self.product_detail)