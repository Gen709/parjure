# Generated by Django 4.1.1 on 2024-01-31 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0014_alter_flikrphoto_serie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flikrphoto',
            name='text',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]