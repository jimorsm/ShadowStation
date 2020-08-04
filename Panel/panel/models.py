from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class Server(models.Model):
    host = models.CharField(max_length=255, null=False)
    ip = models.GenericIPAddressField(null=True)
    auth_user = models.CharField(max_length=255, null=False)
    auth_secret = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.host


class Account(models.Model):
    port = models.IntegerField(validators=(MinValueValidator(1024), MaxValueValidator(65535)), null=False)
    secret = models.CharField(max_length=255, null=False)
    server = models.ForeignKey('Server', on_delete=models.CASCADE, related_name='accounts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts', null=True,
                             default=None, blank=False)

    def __str__(self):
        return '{}@{}'.format(self.port, self.server)

class PanelUser(AbstractUser):
    email = models.EmailField(null=False, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

