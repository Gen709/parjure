# Generated by Django 4.1.1 on 2022-10-12 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bibliotheque', '0006_library_is_true'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='library',
            new_name='DocumentItem',
        ),
    ]