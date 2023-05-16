from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ("slug", "date_created", "last_updated")
        