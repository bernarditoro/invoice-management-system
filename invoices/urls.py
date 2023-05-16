from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = "invoices"

urlpatterns = [
    path("", views.InvoiceListView.as_view(), name="invoice_list"),
    path("create-new/", views.InvoiceCreateView.as_view(), name="create_invoice"),
    path("<invoice_number>/", TemplateView.as_view(template_name="invoices/invoice_detail.html")),
]
