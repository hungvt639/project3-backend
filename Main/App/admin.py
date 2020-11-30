from django.contrib import admin
from .models.product import Types, Products, Details, Amounts, Image, Describe, Description
from .models.cart import Carts
from .models.notify import Notify
from .models.order import Order, OrderProduct
from .models.deliveryaddress import DeliveryAddress

admin.site.register(Types)
admin.site.register(Products)
admin.site.register(Details)
admin.site.register(Amounts)
admin.site.register(Image)
admin.site.register(Describe)
admin.site.register(Description)

admin.site.register(Carts)

admin.site.register(Notify)

admin.site.register(Order)
admin.site.register(OrderProduct)

admin.site.register(DeliveryAddress)