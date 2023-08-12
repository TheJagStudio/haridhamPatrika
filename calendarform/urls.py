from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.signin, name="signin"),
    path("order/", views.order, name="order"),
    path("payment/", views.payment, name="payment"),
]
