from django.urls import path
from main.views import show_main, show_experience, show_technologies, show_projects, create_project, update_project, delete_project

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("technologies/", show_technologies, name="show_technologies"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<int:project_id>/edit/", update_project, name="update_project"),
    path("projects/<int:project_id>/delete/", delete_project, name="delete_project"),
]