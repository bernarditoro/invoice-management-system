from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.edit import ProcessFormView
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.contrib import messages

from home.views import BaseListView
from .models import InvoiceItem, Invoice
from .forms import (
    InvoiceItemForm,
    InvoiceForm,
    InvoiceItemFormset,
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
                                            extra=1,
                                            formset=InvoiceItemFormset,
                                            can_delete=True)
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
        print("Invalid Form")

        messages.error(self.request, "An error occurred!")

        return self.render_to_response(self.get_context_data())
    
    def get_context_data(self, **kwargs):
        kwargs["invoice_form"], kwargs["item_formset"] = self.get_forms()
        kwargs["page"] = "invoices"

        return super().get_context_data(**kwargs)
    
    def get_success_url(self):
        return ""


class InvoiceListView(BaseListView):
    model = Invoice
    template_name = "invoices/invoice_list.html"
    context_object_name = "invoices"
    extra_context = {"page": "invoices"}
        