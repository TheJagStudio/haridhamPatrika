from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('useradd/', views.userAdd, name='userAdd'),
    path('useredit/', views.userEdit, name='userEdit'),
    path('userlist/', views.userList, name='userList'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('profile/<slug:dataid>/',views.profile,name='profile'),
]