from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'port', 'secret')


class UserSerializer(serializers.ModelSerializer):
    accounts = serializers.PrimaryKeyRelatedField(many=True, queryset=Account.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username')
