from django.urls import path

from . import views

urlpatterns = [
    path("", views.details, name="details"),
    path("districtFinder/", views.districtFinder, name="districtFinder"),
    path("talukaFinder/", views.talukaFinder, name="talukaFinder"),
    path("cityFinder/", views.cityFinder, name="cityFinder"),
    path("entryFinder/", views.entryFinder, name="entryFinder"),
    path("listFinder/", views.listFinder, name="listFinder"),
    path("labelExporter/", views.labelExporter, name="labelExporter"),
    path("payOneYear/", views.payOneYear, name="payOneYear"),
    path("profileEdit/", views.profileEdit, name="profileEdit"),
    path("dataUpdater/", views.dataUpdater, name="dataUpdater"),
]
