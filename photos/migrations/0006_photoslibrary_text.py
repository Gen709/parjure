# Generated by Django 4.1.1 on 2022-09-26 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0005_photoslibrary_headline'),
    ]

    operations = [
        migrations.AddField(
            model_name='photoslibrary',
            name='text',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
