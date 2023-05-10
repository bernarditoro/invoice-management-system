from django.db import models
from django.contrib.auth.models import AbstractUser

from organisations.models import Organisation


# Create your models here.
class User(AbstractUser):
    is_client = models.BooleanField(default=False)


class ClientProfile(models.Model):
    user = models.OneToOneField(User, related_name="client_profile", on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, blank=True, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s client profile"
    