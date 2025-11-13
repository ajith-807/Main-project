from django.contrib import admin
from django.urls import path,include
from cart import views
from django.conf.urls.static import static
from django.conf import settings
app_name="cart"
urlpatterns = [
    path('addtocart/<int:i>',views.AddtoCart.as_view(),name="addtocart"),
    path('cartview',views.CartView.as_view(),name="cartview"),
    path('cartminus/<int:i>',views.MinusCart.as_view(),name="cartminus"),
    path('cartdelete/<int:i>',views.CartDelete.as_view(),name="cartdelete"),
    path('checkout',views.CheckoutView.as_view(),name="checkout"),
    path('payment_success/<i>',views.Paymentsuccess.as_view(),name="success"),
    path('yourorders',views.YourOrders.as_view(),name="orders")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)