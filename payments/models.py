from django.db import models

from invoices.models import Invoice

import secrets


# Create your models here.
class Payment(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("refunded", "Refunded"),
    )

    METHOD_CHOICES = (
        ("transfer", "Bank Transfer"),
        ("card", "Card"),
        ("cash", "Cash"),
    )

    ref = models.CharField(max_length=50, unique=True, blank=True)
    transaction_id = models.PositiveBigIntegerField(blank=True, null=True)
    invoice = models.ForeignKey(Invoice, related_name="payments", on_delete=models.SET_NULL, null=True)
    amount_paid = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True, null=True)
    date_paid = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.ref}"
    
    def save(self, *args, **kwargs):
        while not self.ref:
            self.ref = secrets.token_urlsafe(10)

        super().save(*args, **kwargs)

    def get_payment_amount(self):
        return self.amount_paid if self.amount_paid else self.invoice.get_total_amount()
