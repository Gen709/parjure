from django.db import models
from django.urls import reverse

class PrimaryArchivePhotos(models.Model):
    date = models.DateField()
    path = models.CharField(max_length=255)
    
# Create your models here.
class FlikrPhoto(models.Model):
    label = models.CharField(max_length=255)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    source = models.URLField(unique=True)  # Unique constraint for source
    url = models.URLField()
    media = models.CharField(max_length=255)
    caption = models.CharField(max_length=100, blank=True, null=True)
    group = models.CharField(max_length=100, blank=True, null=True)
    headline = models.CharField(max_length=100, blank=True, null=True)
    text = models.CharField(max_length=500, blank=True, null=True)
    date_taken = models.DateTimeField(blank=True, null=True, default=None)
    serie = models.BigIntegerField(null=True, default=None)
    is_new = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('flikr-detail', args=[str(self.id)])
    def __str__(self):
        return self.label
    
    class Meta:
        ordering = ['date_taken']


class PhotosLibrary(models.Model):
    # pass
    date = models.DateTimeField()
    file = models.ImageField(upload_to='images/', blank=True, null=True)
    caption = models.CharField(max_length=100, blank=True, null=True)
    group = models.CharField(max_length=100, blank=True, null=True)
    headline = models.CharField(max_length=100, blank=True, null=True)
    text = models.CharField(max_length=100, blank=True, null=True)


class TimelineEra(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    text_headline = models.CharField(max_length=100)
    text_text = models.TextField(null=True, blank=True)


class Album(models.Model):
    name = models.CharField(max_length=250, unique=True)
    desc = models.TextField(blank=True, null=True)
    photos = models.ManyToManyField(FlikrPhoto, blank=True)

    def __str__(self):
        return self.name