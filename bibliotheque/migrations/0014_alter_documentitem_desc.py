# Generated by Django 4.1.1 on 2022-12-09 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bibliotheque', '0013_documentitem_text_alter_documentitem_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentitem',
            name='desc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bibliotheque.typedocument'),
        ),
    ]
