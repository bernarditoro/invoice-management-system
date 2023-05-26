from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView
from django.urls import reverse

from .models import Payment

from home.views import BaseListView


# Create your views here.
def verify_payment(request, ref, *args, **kwargs):
    payment = get_object_or_404(Payment, ref=ref)

    if payment.verify_payment():
        messages.success(request, "Payment completed successfully!")

    else:
        messages.error(request, "Payment could not be verified!")

    return redirect("invoices:invoice_list")


class PaymentListView(BaseListView):
    model = Payment
    context_object_name = "payments"
    extra_context = {"page": "payments"}


class PaymentDeleteView(DeleteView):
    http_method_names = ("post", )
    slug_field = "ref"
    slug_url_kwarg = "ref"
    model = Payment

    def get_success_url(self):
        return reverse("payments:payment_list")

