# Generated by Django 3.0.3 on 2020-10-04 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_finder', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Webinar',
            new_name='Event',
        ),
    ]
