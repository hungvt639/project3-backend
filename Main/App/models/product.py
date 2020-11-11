from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from Users.models import MyUsers
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
import uuid


class Types(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    avatar = models.FileField(upload_to='image/product',blank=True, null=True, default="avatar.jpg")
    sold = models.IntegerField(default=0)
    type = models.ForeignKey(Types, related_name='products', on_delete=models.CASCADE)
    from_saleprice = models.IntegerField()
    to_saleprice = models.IntegerField()
    comments = models.TextField(max_length=1000, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Details(models.Model):
    product = models.ForeignKey(Products, related_name="details", on_delete=models.CASCADE)
    size = models.CharField(max_length=3)
    color = models.CharField(max_length=20)
    price = models.IntegerField()
    saleprice = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return str(self.product) + ": " + self.color + ": " + self.size


class Amounts(models.Model):
    detail = models.ForeignKey(Details, related_name="amounts", on_delete=models.CASCADE)
    price = models.IntegerField()
    amount = models.IntegerField()
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.detail) + ": " + str(self.amount)


class Image(models.Model):
    product = models.ForeignKey(Products, related_name="image", on_delete=models.CASCADE)
    img = models.FileField(upload_to='image/product')

    def __str__(self):
        return "Images prduct: " + str(self.product)


class Describe(models.Model):
    product = models.ForeignKey(Products, related_name="describe", on_delete=models.CASCADE)
    header = models.CharField(max_length=100)
    context = models.CharField(max_length=200)

    def __str__(self):
        return str(self.product) + ": " + self.header