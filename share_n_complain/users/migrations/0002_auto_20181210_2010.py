# Generated by Django 2.1.3 on 2018-12-10 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='prof_pic_num',
            field=models.IntegerField(default=6),
        ),
    ]
