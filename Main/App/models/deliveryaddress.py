from django.db import models
from Users.models import MyUsers


class DeliveryAddress(models.Model):
    user = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=200)
    default = models.BooleanField(default=False)