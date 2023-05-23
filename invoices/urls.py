from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = "invoices"

urlpatterns = [
    path("", views.InvoiceListView.as_view(), name="invoice_list"),
    path("create-new/", views.InvoiceCreateView.as_view(), name="create_invoice"),
    path("update/<invoice_number>/", views.InvoiceUpdateView.as_view(), name="update_invoice"),
    path("<invoice_number>/", views.InvoiceDetailView.as_view(), name="invoice_detail"),
]
