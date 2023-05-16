from django.urls import path

from . import views


app_name = "projects"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="project_list"),
    path("add-new/", views.ProjectCreateView.as_view(), name="add_project"),
]
