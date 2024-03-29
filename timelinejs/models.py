from django.db import models
from django.urls import reverse
# Create your models here.


class Text(models.Model):
    headline = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)


class Media(models.Model):
    url = models.URLField(unique=False)
    caption = models.CharField(max_length=100, blank=True, null=True)
    credit = models.CharField(max_length=100, blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    alt = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    link_target = models.CharField(max_length=100, blank=True, null=True)


class Slide(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    text = models.ForeignKey(Text, on_delete=models.SET_NULL, blank=True, null=True)
    media = models.ForeignKey(Media, on_delete=models.CASCADE, blank=True, null=True)
    group = models.CharField(max_length=50, blank=True, null=True)
    display_date = models.CharField(max_length=50, blank=True, null=True)
    background_color = models.CharField(max_length=50, blank=True, null=True)
    autolink = models.BooleanField(default=True, blank=True, null=True)
    unique_id = models.CharField(max_length=100, blank=True, null=True)


class Era(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    text = models.ForeignKey(Text, on_delete=models.SET_NULL, blank=True, null=True)


class Events(models.Model):
    title = models.ForeignKey(Slide, on_delete=models.CASCADE, related_name="event_title")
    scale = models.CharField(max_length=100, default="human")
    events = models.ManyToManyField(Slide)
    era = models.ManyToManyField(Era)
    def get_absolute_url(self):
        return reverse('timelinejs-details', args=[str(self.id)])

    def get_events(self):
        return self.events.all().order_by('start_date')

    def get_era(self):
        return self.era.all().order_by('start_date')

    def __str__(self):
        return self.title.text.headline