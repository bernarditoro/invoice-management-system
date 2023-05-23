from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from .models import Payment


# Create your views here.
def verify_payment(request, ref, *args, **kwargs):
    payment = get_object_or_404(Payment, ref=ref)

    if payment.verify_payment():
        messages.success(request, "Payment completed successfully!")

    else:
        messages.error(request, "Payment could not be verified!")

    return redirect("invoices:invoice_list")
