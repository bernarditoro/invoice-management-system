from django.db import models
from django.utils.text import slugify
from django.conf import settings

from taggit.managers import TaggableManager


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, default="")
    project_url = models.URLField(null=True, blank=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="hires", on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        ordering = ("-date_created", "-last_updated")

    def __str__(self):
        return self.name
    
    def save(self, **kwargs):
        self.slug = slugify(self.name)

        super().save(**kwargs)
