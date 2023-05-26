from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from .models import Payment


# Create your tests here.
class PaymentTestCase(TestCase):
    def setUp(self):
        self.payment = Payment.objects.create(
            amount_paid=20000,
            method="cash",
            status="completed",
            date_paid=timezone.now(),
        )

        self.client = Client()

    def test_model_setup(self):
        self.assertIsInstance(self.payment, Payment)
        self.assertIsNotNone(self.payment.ref)

    def test_model_methods(self):
        self.assertEqual(self.payment.get_payment_amount(), 20000)


class PaymentURLTestCase(PaymentTestCase):
    def test_payment_list_url(self):
        response = self.client.get(reverse("payments:payment_list"))

        self.assertEqual(response.status_code, 200)

    def test_payment_delete_url(self):
        ref = self.payment.ref

        response = self.client.post(reverse("payments:delete_payment", kwargs={"ref":ref}), data={})

        self.assertEqual(response.status_code, 302)
        # self.assertRaises(Payment.DoesNotExist, Payment.objects.get(ref=ref))
