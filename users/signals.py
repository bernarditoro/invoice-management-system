from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User, ClientProfile


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created and instance.is_client:
            # If user is marked as client, create a client profile
            ClientProfile.objects.create(user=instance)
