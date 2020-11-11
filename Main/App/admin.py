from django.contrib import admin
# from .models.Snippets import Snippet
# from .models.image import File
from .models.product import Types, Products, Details, Amounts, Image, Describe
# admin.site.register(Snippet)
# admin.site.register(File)

admin.site.register(Types)
admin.site.register(Products)
admin.site.register(Details)
admin.site.register(Amounts)
admin.site.register(Image)
admin.site.register(Describe)