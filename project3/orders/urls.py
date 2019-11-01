from django.urls import path
from . import views

urlpatterns = [
    path("menu", views.index, name="menu"),
    path("pick/<int:id>", views.pick_product, name="pick_product"),
    path("cart", views.cart, name="cart"),
    path("orders", views.orders, name="orders"),
    path("order/<int:id>", views.order, name="order"),
]
