# Generated by Django 2.2.14 on 2020-07-05 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20200705_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='traffic',
            name='last_log',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
