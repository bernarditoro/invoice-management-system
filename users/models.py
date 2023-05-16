from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from organisations.models import Organisation


# Create your models here.
class CustomUserManager(UserManager):
    def create_client(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("Client must have an email address!")
        
        if not username:
            raise ValueError("Client must have a username!")
        
        client = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_client=True
        )

        client.set_password(password)
        client.save(using=self._db)

        return client


class User(AbstractUser):
    is_client = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name()

    @property
    def number_of_projects(self):
        """
        This returns the number of projects assigned to me by this user
        """

        return len(self.hires.all())


class ClientProfile(models.Model):
    user = models.OneToOneField(User, related_name="client_profile", on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, blank=True, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s client profile"
    