# Generated by Django 4.1.1 on 2022-09-22 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibliotheque', '0003_alter_library_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='item',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
