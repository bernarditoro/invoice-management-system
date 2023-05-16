from django import forms
from django.forms import BaseModelFormSet

from djangoformsetjs.utils import formset_media_js

from .models import Invoice, InvoiceItem


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ("issued_to", "due_date", "notes")


class InvoiceItemForm(forms.ModelForm):    
    class Meta:
        model = InvoiceItem
        fields = ("project", "amount", "description")
        widgets = {
            "project": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "₦5000"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Item Description", "rows": "2"}),
        }

    class Media(object):
        js = formset_media_js + (
            # Other form media here
        )


class InvoiceItemFormset(BaseModelFormSet):
    ...
    