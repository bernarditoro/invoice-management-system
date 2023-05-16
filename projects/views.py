from home.views import BaseListView

from .models import Project
from .forms import ProjectForm

from django.views.generic import CreateView
from django.contrib import messages


# Create your views here.
class ProjectListView(BaseListView):
    model = Project
    context_object_name = "projects"
    template_name = "projects/project_list.html"
    extra_context = {"page": "projects"}


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    extra_context = {"page": "projects"}
    template_name = "projects/add_project.html"

    def form_invalid(self, form):
        messages.error(self.request, "An error occurred!")

        return super().form_invalid(form)
    
    def form_valid(self, form):
        messages.success(self.request, "Project added successfully!")

        return super().form_valid(form)
    
    def get_success_url(self) -> str:
       return "" # TODO: Replace with get_absolute_url()
        