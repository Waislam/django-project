# Generated by Django 2.1.2 on 2018-11-16 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20181113_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]