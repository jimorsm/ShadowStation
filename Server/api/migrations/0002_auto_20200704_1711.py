# Generated by Django 2.2.14 on 2020-07-04 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='port',
            field=models.IntegerField(),
        ),
    ]
