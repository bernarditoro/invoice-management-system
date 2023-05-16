from django.views.generic import CreateView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import ClientUserForm
from .models import ClientProfile

from organisations.models import Organisation

from home.views import BaseListView


# Create your views here.
class ClientCreateView(CreateView):
    form_class = ClientUserForm
    template_name = "users/add_client.html"
    extra_context = {"page": "clients"}

    def form_valid(self, form):
        cd = form.cleaned_data

        client = form.save(commit=False)
        client.is_client = True
        client.save()

        try:
            organisation = Organisation.objects.get(name__iexact=cd["organisation"])
        except Organisation.DoesNotExist:
            organisation = Organisation.objects.create(name=cd["organisation"])

        ClientProfile.objects.create(organisation=organisation, user=client)

        messages.success(self.request, "Client added successfully!")

        return redirect(self.get_success_url())
    

    def get_success_url(self) -> str:
        return reverse("users:client_list")
    
    def form_invalid(self, form):
        messages.error(self.request, "Client could not be added at this time!")

        return super().form_invalid(form)
    

class ClientListView(BaseListView):
    template_name = "users/client_list.html"
    context_object_name = "clients"
    extra_context = {"page": "clients"}
    
    def get_queryset(self):
        return get_user_model().objects.filter(is_client=True)
    