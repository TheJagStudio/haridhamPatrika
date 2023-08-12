from django.urls import path

from . import views

urlpatterns = [
    path("allList/", views.allList, name="allList"),
]
