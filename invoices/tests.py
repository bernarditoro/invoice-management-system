from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from .models import Invoice, InvoiceItem

from datetime import date

from projects.models import Project


# Create your tests here.
class BaseInvoiceTestCase(TestCase):
    def setUp(self):
        self.project_1 = Project.objects.create(
            name="Test Project One",
            description="This is a test project",
        )

        self.project_2 = Project.objects.create(
            name="Test Project Two",
            description="This is a second test project",
        )

        self.invoice = Invoice.objects.create(
            due_date=date.today(),
            notes="This is a test invoice note."
        )

        self.invoice_item_1 = self.invoice.items.create(
            project=self.project_1,
            amount=10000,
            description="This is a test invoice item description for item 1"
        )

        self.invoice_item_2 = self.invoice.items.create(
            project=self.project_2,
            amount=5000,
            description="This is a test invoice item description for item 2"
        )

        self.client = Client()


class InvoiceModelTestCase(BaseInvoiceTestCase):
    def test_model_setup(self):
        self.assertIsInstance(self.invoice_item_1, InvoiceItem)
        self.assertIsInstance(self.invoice_item_2, InvoiceItem)
        self.assertEqual(len(self.invoice.items.all()), 2)
        self.assertIsNotNone(self.invoice.invoice_number)


class InvoiceURLTestCase(BaseInvoiceTestCase):
    def setUp(self):
        super().setUp()

        self.client_user = get_user_model().objects.create(
            email="client@email.com",
            username="testclient",
            first_name="Test",
            last_name="Client",
            is_client=True
        )

        self.client = Client()

    def test_invoice_list_url(self):
        response = self.client.get("/invoices/")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["invoices"], Invoice.objects.all())
        self.assertTemplateUsed("invoices/invoice_list.html")

    def test_invoice_create_url(self):
        data = {
            "issued_to": self.client_user.pk,
            "due_date": date.today(),
            "notes": "This is another test invoice note!",

            "form-TOTAL_FORMS": "1",
            "form-INITIAL_FORMS": "0",
            "form-0-project": self.project_1.pk,
            "form-0-amount": "7000",
            "form-0-description": "Test Invoice Item Description",
        }

        response = self.client.post("/invoices/create-new/", data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.project_1.invoices.all()), 2)
