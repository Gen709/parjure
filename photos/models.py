from django.db import models

# Create your models here.


class PhotosLibrary(models.Model):
    # pass
    date = models.DateTimeField()
    file = models.ImageField(upload_to='images/', blank=True, null=True)
    caption = models.CharField(max_length=100, blank=True, null=True)
    group = models.CharField(max_length=100, blank=True, null=True)
    headline=models.CharField(max_length=100, blank=True, null=True)
    text=models.CharField(max_length=100, blank=True, null=True)
