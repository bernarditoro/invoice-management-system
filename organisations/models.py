from django.db import models


# Create your models here.
class Organisation(models.Model):
    name = models.CharField(max_length=250)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, default=" ")

    def __str__(self) -> str:
        return self.name
