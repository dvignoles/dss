# Generated by Django 2.1.3 on 2018-11-21 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='interests',
            field=models.CharField(default='none', max_length=100),
            preserve_default=False,
        ),
    ]
