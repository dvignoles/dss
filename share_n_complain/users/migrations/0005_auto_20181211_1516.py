# Generated by Django 2.1.3 on 2018-12-11 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20181210_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='prof_pic_num',
            field=models.IntegerField(default=11),
        ),
    ]