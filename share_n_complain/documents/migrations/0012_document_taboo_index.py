# Generated by Django 2.1.3 on 2018-12-05 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0011_document_locked_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='taboo_index',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]