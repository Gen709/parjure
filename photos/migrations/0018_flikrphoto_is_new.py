# Generated by Django 4.1.1 on 2024-03-25 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0017_primaryarchivephotos'),
    ]

    operations = [
        migrations.AddField(
            model_name='flikrphoto',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
    ]
