# Generated by Django 4.1.1 on 2024-01-25 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0013_alter_flikrphoto_serie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flikrphoto',
            name='serie',
            field=models.BigIntegerField(default=None, null=True),
        ),
    ]