from django.db import models
from django.conf import settings

from projects.models import Project


# Create your models here.
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=200, blank=True)
    issued_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                  related_name="invoices", limit_choices_to={"is_client": True})
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    notes = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    invoice_file = models.FileField(upload_to="invoices/",
                                    blank=True,
                                    null=True,
                                    help_text="This field is populated by the system and holds the pdf version of the invoice.")

    def __str__(self):
        return self.invoice_number

    def get_total_amount(self):
        return sum(item.amount for item in self.items.all())


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="invoices", on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    description = models.TextField()

    class Meta:
        verbose_name = "Invoice Item"
        verbose_name_plural = "Invoice Items"

    def __str__(self):
        return f"{self.invoice} Item"
