# Generated by Django 2.2.14 on 2020-07-04 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.IntegerField(max_length=8)),
                ('secret', models.CharField(max_length=255)),
            ],
        ),
    ]
