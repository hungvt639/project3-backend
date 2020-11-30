from django.db import models
from Users.models import MyUsers


class DeliveryAddress(models.Model):
    user = models.ForeignKey(MyUsers, related_name="delivery_address", on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    fullname = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    default = models.BooleanField(default=False)
    on_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + ": " + self.phone + " - " + self.address