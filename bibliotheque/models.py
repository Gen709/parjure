from django.db import models

# Create your models here.

class library(models.Model):
    parent = models.IntegerField(null=True, default=True)
    lft = models.IntegerField()
    rgt = models.IntegerField()
    item = models.CharField(max_length=250, blank=True, null=True, default=None)