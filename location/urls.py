from django.urls import path

from . import views

urlpatterns = [
    path('cityAdd/', views.cityAdd, name='cityAdd'),
]