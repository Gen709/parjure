# Generated by Django 4.1.1 on 2022-11-24 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timelinejs', '0006_rename_pk_era_id_rename_pk_events_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='url',
            field=models.URLField(),
        ),
    ]
