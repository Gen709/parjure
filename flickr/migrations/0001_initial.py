# Generated by Django 4.1.1 on 2022-11-01 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flickr',
            fields=[
                ('pk', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_taken', models.CharField(max_length=30)),
                ('date_taken_obj', models.DateTimeField()),
                ('credit', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=500)),
                ('desc', models.TextField()),
                ('link_to_original_photo', models.URLField()),
                ('link_to_photo_thumbnail', models.URLField()),
            ],
        ),
    ]
