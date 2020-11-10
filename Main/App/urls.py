from django.urls import path
from .views import snippets, image, product

urlpatterns = [
    path('snippets/', snippets.SnippetList.as_view()),
    path('image/', image.FileUpload.as_view()),
    path('product/type/', product.Type.as_view()),
    path('product/product/', product.Product.as_view()),
    path('product/detail/', product.Detail.as_view()),
    path('product/amount/', product.Amount.as_view()),
]
