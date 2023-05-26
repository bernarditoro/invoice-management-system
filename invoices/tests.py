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

        self.project_3 = Project.objects.create(
            name="Test Project Three",
            description="This is a third test project",
        )

        self.client_user = get_user_model().objects.create(
            email="client@email.com",
            username="testclient",
            first_name="Test",
            last_name="Client",
            is_client=True
        )

        self.invoice = Invoice.objects.create(
            due_date=date.today(),
            notes="This is a test invoice note.",
            issued_to=self.client_user
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

    def test_invoice_file(self):
        self.assertIsNotNone(self.invoice.invoice_file)
        self.assertEqual(self.invoice.invoice_file.url.split("/")[-1], f"Invoice-{self.invoice.invoice_number}.pdf")
    

class InvoiceURLTestCase(BaseInvoiceTestCase):
    def setUp(self):
        super().setUp()

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
        self.assertEqual(len(self.project_1.invoice_items.all()), 2)

    def test_invoice_detail_url(self):
        response = self.client.get(self.invoice.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["payment"])
        self.assertTemplateUsed("invoices/invoice_detail.html")

    def test_invoice_update_url(self):
        data = {
            "issued_to": self.client_user.pk,
            "due_date": self.invoice.due_date,
            "notes": "This is an update note",

            "form-TOTAL_FORMS": "3",
            "form-INITIAL_FORMS": "2",

            "form-0-project": self.project_1.pk,
            "form-0-amount": "10000",
            "form-0-description": "This is one item description",
            "form-0-id": self.invoice_item_1.id,

            "form-1-project": self.project_2.pk,
            "form-1-amount": "20000",
            "form-1-description": "This is two item description",
            "form-1-id": self.invoice_item_2.id,

            "form-2-project": self.project_3.pk,
            "form-2-amount": "50000",
            "form-2-description": "This is another item description"
        }

        response = self.client.post(self.invoice.get_update_url(), data=data)

        self.assertEqual(response.status_code, 302)
        # self.assertEqual(len(self.invoice.items.all()), 3)
        # self.assertEqual(self.invoice.notes, "This is an update note")
