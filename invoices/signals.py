from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Invoice

from payments.models import Payment


@receiver(post_save, sender=Invoice)
def invoice_post_save(sender, instance, created, **kwargs):
    if created:
        date = instance.date_created.strftime('%Y%m%d')

        instance.invoice_number = f"{date}-00{instance.id}"
        instance.save()

        # Create payment object
        Payment.objects.create(invoice=instance)

        # Send the invoice to client
        instance.send_by_mail()

    else:
        # In case of an update, check if there is a pending balance and create a payment if there is
        while instance.get_balance_payment() > 0 and instance.is_paid:
            instance.is_paid = False
            instance.save()

            Payment.objects.create(invoice=instance,
                                   amount_paid=instance.get_balance_payment())
            