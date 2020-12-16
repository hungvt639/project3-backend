from django.urls import path
from .views import product, product_detail, cart, notify, order, deliveryaddress


urlpatterns = [
    path('product/type/', product.Type.as_view(), name="type"),
    path('product/type/<int:id>/', product_detail.DetailTypes.as_view()),
    path('product/product/', product.Product.as_view()),
    path('product/product/<uuid:id>/', product_detail.DetailProducts.as_view()),
    path('product/detail/', product.Detail.as_view()),
    path('product/detail/<int:id>/', product_detail.DetailProductsDetails.as_view()),
    path('product/amount/', product.Amount.as_view()),
    path('product/image/<uuid:id>/', product.Images.as_view()),
    path('product/image/<int:id>/', product_detail.DetailImages.as_view()),
    path('product/describe/', product.Describes.as_view()),
    path('product/describe/<int:id>/', product_detail.DetailDescribes.as_view()),

    path('cart/', cart.CartView.as_view()),
    path('cart/<int:id>/', cart.DetailCartView.as_view()),

    path('notify/', notify.NotifyView.as_view()),
    path('notify/<int:id>/', notify.DetailNotifyView.as_view()),

    path('order/', order.OrderView.as_view()),
    path('order/<uuid:id>/', order.DetailOrderView.as_view()),

    path('delivery-address/', deliveryaddress.DeliveryAddressView.as_view()),
    path('delivery-address/<int:id>/', deliveryaddress.DetailDeliveryAddressView.as_view()),
]
