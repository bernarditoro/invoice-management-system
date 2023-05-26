from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.edit import ProcessFormView
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import DetailView
from django.http import Http404
from django.conf import settings

from home.views import BaseListView

from .models import InvoiceItem, Invoice
from .forms import (
    InvoiceItemForm,
    InvoiceForm,
    InvoiceItemFormset,
    InvoiceMailForm
)


class InvoiceCreateView(TemplateResponseMixin, ContextMixin, ProcessFormView):
    """
    This view is a little complicated. The logic is to combine initialisation and
    processing of both forms in one function.
    
    """
    template_name = "invoices/create_invoice.html"

    def get_form_classes(self):
        item_formset = modelformset_factory(InvoiceItem,
                                            form=InvoiceItemForm,
                                            formset=InvoiceItemFormset)
        invoice_form = InvoiceForm

        return invoice_form, item_formset
    
    def get_forms(self, *args, **kwargs):
        invoice_form, item_formset = self.get_form_classes()
        request = self.request

        if self.request.method in ("POST", "PUT"):
            return invoice_form(data=request.POST), item_formset(data=request.POST)

        else:
            return invoice_form(), item_formset(queryset=InvoiceItem.objects.none())
        
    def post(self, request, **kwargs):
        forms = self.get_forms()

        if all(form.is_valid() for form in forms):
            return self.form_valid(forms)
        else:
            return self.form_invalid(forms)
        
    def form_valid(self, forms):
        # Spread the forms => (invoice_form, item_formset)
        invoice_form, item_formset = forms

        self.invoice = invoice_form.save()
        invoice_items = item_formset.save(commit=False)

        for item in invoice_items:
            item.invoice = self.invoice
            item.save()

        messages.success(self.request, "Invoice saved successfully!")

        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, forms):
        print ("One form is invalid!")
        messages.error(self.request, "An error occurred!")

        return self.render_to_response(self.get_context_data())
    
    def get_context_data(self, **kwargs):
        kwargs["invoice_form"], kwargs["item_formset"] = self.get_forms()
        kwargs["page"] = "invoices"
        kwargs["subsection"] = "Create"

        return super().get_context_data(**kwargs)
    
    def get_success_url(self):
        return self.invoice.get_absolute_url()


class InvoiceListView(BaseListView):
    model = Invoice
    template_name = "invoices/invoice_list.html"
    context_object_name = "invoices"
    extra_context = {"page": "invoices"}


class InvoiceDetailView(DetailView):
    model = Invoice
    context_object_name = "invoice"
    slug_field = "invoice_number"
    slug_url_kwarg = "invoice_number"
    template_name = "invoices/invoice_detail.html"

    def get_items(self):
        return self.get_object().items.all()
    
    def get_all_payments(self):
        """Return all payments for this invoice (for admins view)"""
        return self.get_object().payments.all()    
    
    def get_payment(self):
        """ Return latest pending payment (for client's viewing) and none if client has paid"""
        payments = self.get_all_payments()

        return None if self.get_object().is_paid else payments.filter(status="pending")[0]

    def get_context_data(self, **kwargs):
        kwargs["invoice_items"] = self.get_items()
        kwargs["paystack_public_key"] = settings.PAYSTACK_PUBLIC_KEY
        kwargs["payment"] = self.get_payment()

        return super().get_context_data(**kwargs)
    
    def post(self, request, **kwargs):
        form = InvoiceMailForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            response= self.get_object().send_by_mail(
                message=cd["message"],
                to_email=cd["recipient_mail"]
            )

            messages.success(request, response[1]) if response[0] else messages.error(request, response[1])
                            
        else:
            messages.error(request, "Form is not valid!")

        return super().get(request, **kwargs)
    

class InvoiceUpdateView(InvoiceCreateView):
    def get_invoice(self):
        try:
            return Invoice.objects.get(invoice_number=self.kwargs["invoice_number"])
        
        except Invoice.DoesNotExist:
            raise Http404("Invoice does not exist!")
        
    def get_forms(self, *args, **kwargs):
        invoice_form, item_formset = self.get_form_classes()
        request = self.request
        invoice = self.get_invoice()

        if self.request.method in ("POST", "PUT"):
            return invoice_form(data=request.POST, instance=invoice), item_formset(data=request.POST)

        else:
            return invoice_form(instance=invoice), item_formset(queryset=InvoiceItem.objects.filter(invoice=invoice))

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)    
        context["subsection"] = "Update"
        context["invoice"] = self.get_invoice()
        
        return context
