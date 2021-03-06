# Generated by Django 2.1.3 on 2018-12-11 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_auto_20181210_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaints_Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complainer_user', models.IntegerField(null=True)),
                ('doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Document')),
            ],
        ),
    ]
