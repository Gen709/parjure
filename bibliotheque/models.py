from django.db import models


# https://stackoverflow.com/questions/805393/what-is-the-best-way-to-access-stored-procedures-in-djangos-orm
# Create your models here.

class TypeDocument(models.Model):
    desc = models.CharField(max_length=100)


class Library(models.Model):
    parent = models.IntegerField(null=True, default=True)
    lft = models.IntegerField()
    rgt = models.IntegerField()
    item = models.TextField()
    desc = models.ForeignKey(TypeDocument, on_delete=models.SET_NULL, null=True)
    is_true = models.BooleanField(null=True)
