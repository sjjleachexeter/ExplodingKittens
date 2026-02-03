from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="Scanner"),
    path("scan", views.scan_barcode, name="scan_barcode"),
]