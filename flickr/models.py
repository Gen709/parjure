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

    @property
    def date_dict(self):
        return {'year': self.date_taken_obj.year,
                'month': self.date_taken_obj.month,
                'day': self.date_taken_obj.day,
                'hour': self.date_taken_obj.hour,
                'minute': self.date_taken_obj.minute,
                'second': self.date_taken_obj.second
                }
