from django.contrib import admin

from .models import TypeDocument, DocumentItem, DocumentText

model_list = [TypeDocument, DocumentItem, DocumentText]

# Register your models here.

for model in model_list:
    admin.site.register(model)