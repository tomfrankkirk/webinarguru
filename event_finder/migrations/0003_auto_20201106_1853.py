# Generated by Django 3.1.2 on 2020-11-06 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_finder', '0002_auto_20201004_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='tweet_id',
            field=models.BigIntegerField(),
        ),
    ]
