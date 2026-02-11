from django.urls import path

from . import views

urlpatterns = [
    path("<int:product_id>", views.display_passport, name="passport_display"),
    path("node/<int:node_id>", views.display_node_info, name="node_info_display"),
    path("", views.return_to_scanner, name="passport_return_to_scanner"),

]