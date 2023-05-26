from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.mail import EmailMessage
from django.core.files.uploadedfile import SimpleUploadedFile

from projects.models import Project

from .tasks import generate_pdf


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
    class Meta:
        ordering = ("-invoice_number", )

    def __str__(self):
        return self.invoice_number
    
    def get_absolute_url(self):
        return reverse("invoices:invoice_detail", kwargs={"invoice_number": self.invoice_number})

    def get_update_url(self):
        return reverse("invoices:update_invoice", kwargs={"invoice_number": self.invoice_number})
    
    def get_total_amount(self):
        return sum(item.amount for item in self.items.all())
    
    def get_balance_payment(self):
        """
        For payments in instalments, calculate all completed payments and determine the balance
        """
        payments = self.payments.filter(status="completed")

        paid_amount = sum(payment.get_payment_amount() for payment in payments)

        return self.get_total_amount() - paid_amount
        
    def generate_invoice_file(self):
        if self.invoice_file:
            self.invoice_file.delete()

        context = {
            "invoice": self,
            "invoice_items": self.items.all(),
        }

        pdf_file = generate_pdf("invoices/invoice_detail.html", context)

        self.invoice_file = SimpleUploadedFile("Invoice-" + self.invoice_number + ".pdf", pdf_file,
                                               content_type="application/pdf")
        self.save()

        return self.invoice_file


    def get_invoice_file(self):
        return self.invoice_file or self.generate_invoice_file()

    def send_by_mail(self,
                     subject: str = "",
                     message: str = "",
                     to_email: str = ""):
        invoice_pdf_path = self.generate_invoice_file().path
        subject = subject or f"Invoice Available [Invoice {self.invoice_number}]"
        message = message or f"""Dear {self.issued_to.first_name}, \n

                                 Thank you for your business, always a pleasure to work with you! \n
                                 A new invoice in the amount of ₦{self.get_balance_payment()} has been generated. \n
                                 Payment of this invoice by {self.due_date} would be appreciated. \n
                            """
        to_email = to_email or self.issued_to.email

        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                to=[to_email],
                from_email=settings.EMAIL_HOST_USER
            )

            # from django.core.mail.message import attach
            # import requests
            # response = requests.get("http://yoururl/somefile.pdf")
            # email.attach("Filename", response.content, mimetype="application/pdf")

            email.attach_file(invoice_pdf_path)  # TODO: Modify this path to above in production.
            email.content_subtype = "html"
            email.send()

        except FileNotFoundError:
            return False, "File does not exist!"

        except TimeoutError:
            return False, "Connection did not go through!"

        except Exception as e:
            raise e

        else:
            return True, "Mail sent successfully!"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="invoice_items", on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    description = models.TextField()

    class Meta:
        verbose_name = "Invoice Item"
        verbose_name_plural = "Invoice Items"

    def __str__(self):
        return f"{self.invoice} Item"
