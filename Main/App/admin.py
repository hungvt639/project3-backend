from django.contrib import admin
from .models.product import Types, Products, Details, Amounts, Image, Describe
from .models.cart import Carts


admin.site.register(Types)
admin.site.register(Products)
admin.site.register(Details)
admin.site.register(Amounts)
admin.site.register(Image)
admin.site.register(Describe)

admin.site.register(Carts)