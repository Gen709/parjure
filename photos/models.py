from django.db import models

# Create your models here.


class PhotosLibrary(models.Model):
    # pass
    date = models.DateTimeField()
    file = models.ImageField(upload_to='images/', blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
