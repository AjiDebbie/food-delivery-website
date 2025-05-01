from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from .views import *

app_name="customer"

urlpatterns=[
    path("", CustomerHome,name="customer/index.html"),
    path("home/", CustomerHome,name="home"),
    path("about/",CustomerAbout, name="about"),
    path("menu/",CustomerMenu, name="menu"),
    path("menu/detail/<int:id>/",MenuDetail, name="detail"),
    
    path("cart/",login_required(CustomerCart), name="cart"),

    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/clear/', cart_clear, name='cart_clear'),
    path('cart/checkout/', CheckOut),
    path('order/<int:order_id>/', Order, name='order_detail'),
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)