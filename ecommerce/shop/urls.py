from django.contrib import admin
from django.urls import path,include
from shop import views
from django.conf.urls.static import static
from django.conf import settings
app_name="shop"
urlpatterns = [
    path('',views.Categoryview.as_view(),name="category"),
    path('product/<int:i>',views.Product.as_view(),name="product"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)