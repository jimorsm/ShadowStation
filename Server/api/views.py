from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions

from .lib import SSControl
from .models import Account
from .serializers import AccountSerializer
from .serializers import UserSerializer


# Create your views here.

class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        port = self.request.data.get('port')
        secret = self.request.data.get('secret')
        c = SSControl()
        c.add(int(port), secret)


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def perform_update(self, serializer):
        old_port = self.get_object().port
        port = self.request.data.get('port')
        secret = self.request.data.get('secret')
        c = SSControl()
        c.update(int(old_port), int(port), secret)
        super().perform_update(serializer)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
