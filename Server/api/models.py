from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.


class Account(models.Model):
    port = models.IntegerField(null=False, unique=True, validators=[MaxValueValidator(65535), MinValueValidator(1024)])
    secret = models.CharField(max_length=255, null=False)
    owner = models.ForeignKey('auth.User', related_name='accounts', on_delete=models.CASCADE)


class Traffic(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    traffic_log = models.IntegerField()
    traffic_used = models.IntegerField()
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='traffics')

    class Meta:
        ordering=['create_time']
