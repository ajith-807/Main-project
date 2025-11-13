from django.contrib import admin
from django.urls import path,include
from shop import views
from django.conf.urls.static import static
from django.conf import settings
app_name="shop"
urlpatterns = [
    path('',views.Categoryview.as_view(),name="category"),
    path('product/<int:i>',views.Productview.as_view(),name="product"),
    path('productdetail/<int:i>',views.Productdetails.as_view(),name="productdetail"),
    path('register',views.Register.as_view(),name="register"),
    path('login',views.Login.as_view(),name="login"),
    path('logout',views.Logout.as_view(),name="logout"),
    path('addcategory',views.AddCategory.as_view(),name="addcategory"),
    path('addproduct',views.AddProduct.as_view(),name="addproduct"),
    path('addstock/<int:i>',views.Addstock.as_view(),name="addstock")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)