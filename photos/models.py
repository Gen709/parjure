from django.db import models

# Create your models here.


class PhotosLibrary(models.Model):
    # pass
    date = models.DateTimeField()
    file = models.ImageField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
