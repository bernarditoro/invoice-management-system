from django.contrib import admin

from .models import Invoice, InvoiceItem


# Register your models here.
class InvoiceItemInline(admin.StackedInline):
    model = InvoiceItem


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline, ]


admin.site.register(Invoice, InvoiceAdmin)
