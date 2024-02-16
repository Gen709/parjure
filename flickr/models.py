from django.db import models
# Create your models here.

class Flickr(models.Model):
    date_taken = models.CharField(max_length=30)
    date_taken_obj = models.DateTimeField()
    credit = models.CharField(max_length=200)
    title = models.CharField(max_length=500)
    desc = models.TextField()
    link_to_original_photo = models.URLField()
    link_to_photo_thumbnail = models.URLField()

    class Meta:
        ordering = ['date_taken_obj',]


    def __str__(self):
        return self.date_taken +" - " + self.title
    
    @property
    def date_dict(self):
        return {'year': self.date_taken_obj.year,
                'month': self.date_taken_obj.month,
                'day': self.date_taken_obj.day,
                'hour': self.date_taken_obj.hour,
                'minute': self.date_taken_obj.minute,
                'second': self.date_taken_obj.second
                }


class Album(models.Model):
    name = models.CharField(max_length=250, unique=True)
    desc = models.TextField(blank=True, null=True)
    photos = models.ManyToManyField(Flickr, blank=True)

    def __str__(self):
        return self.name



# class TimeLineJSFlickr(models.Model):
