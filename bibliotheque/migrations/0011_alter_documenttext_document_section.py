# Generated by Django 4.1.1 on 2022-12-09 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bibliotheque', '0010_rename_pk_documentitem_id_rename_pk_typedocument_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documenttext',
            name='document_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bibliotheque.documentitem', unique=True),
        ),
    ]
