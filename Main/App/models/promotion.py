from django.db import models
from .product import Products, Types

type = [
    (0, "%"),
    (1, "vnd"),
]
class Promotions(models.Model):
    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=type, default=1)
    time_from = models.DateTimeField()
    time_to = models.DateTimeField()
    value = models.IntegerField()
    max_value = models.IntegerField(blank=True, default=0)
    comment = models.CharField(max_length=200, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    on_delete = models.BooleanField(default=False)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {}: {} - {}".format(self.name, self.type, self.value, self.time_from, self.time_to)

class PromotionTypes(models.Model):
    promotion = models.ForeignKey(Promotions, related_name="promotiontype", on_delete=models.CASCADE)
    type = models.ForeignKey(Types, related_name="types", on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return "{} - {}".format(self.promotion, self.type)


class PromotionProducts(models.Model):
    promotion = models.ForeignKey(Promotions, related_name="promotions", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name="products", on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return "{} - {}".format(self.promotion, self.product)