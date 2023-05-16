from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path("", views.ClientListView.as_view(), name="client_list"),
    path("add-client/", views.ClientCreateView.as_view(), name="add_client"),
]
