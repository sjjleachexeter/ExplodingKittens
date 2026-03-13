from django.urls import path

from . import views
urlpatterns = [
    path("<int:product_id>", views.display_passport, name="passport_display"),
    path("node/<str:node_id>", views.display_node_info, name="node_info_display"),
    path("", views.return_to_scanner, name="passport_return_to_scanner"),

    path("create_node", views.create_node, name="create_node"),
    path("create_ingredient", views.create_ingredient, name="create_ingredient"),
    path("edit_node/<str:node_id>", views.create_node, name="edit_node"),
    path("create_passport", views.create_passport, name="create_passport"),
    path("edit_passport/<int:product_id>", views.edit_passport, name="edit_passport"),
    path("edit_claims/<int:product_id>", views.edit_claims, name="edit_claims"),
    path("edit_evidence/<int:product_id>", views.edit_evidence, name="edit_evidence"),

]

