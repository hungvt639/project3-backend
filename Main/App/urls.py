from django.urls import path
from .views import snippets, image, product, product_detail


urlpatterns = [

    path('product/type/', product.Type.as_view()),
    path('product/type/<int:id>/', product_detail.DetailTypes.as_view()),
    path('product/product/', product.Product.as_view()),
    path('product/product/<uuid:id>/', product_detail.DetailProducts.as_view()),
    path('product/detail/', product.Detail.as_view()),
    path('product/detail/<int:id>/', product_detail.DetailProductsDetails.as_view()),
    path('product/amount/', product.Amount.as_view()),
    path('product/image/', product.Images.as_view()),
    path('product/image/<int:id>/', product_detail.DetailImages.as_view()),
    path('product/describe/', product.Describes.as_view()),
    path('product/describe/<int:id>/', product_detail.DetailDescribes.as_view()),

]
