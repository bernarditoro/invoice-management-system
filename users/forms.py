from django import forms

from .models import User

from organisations.models import Organisation


class ClientUserForm(forms.ModelForm):
    organisation = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")
