# Generated by Django 2.2.14 on 2020-07-05 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_traffic_last_log'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='traffic',
            options={'ordering': ['create_time']},
        ),
    ]
