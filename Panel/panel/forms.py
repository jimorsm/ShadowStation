from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Account


class PanelUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ("username", "email")


class PanelUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'


# TODO:
class PanelUserModifyForm(forms.Form):
    username = forms.CharField()

    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput,
    )


class AccountToUserForm(forms.Form):
    add_accounts = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        objects = Account.objects.filter(user=None)
        CHOICES = [(str(obj.id), str(obj)) for obj in objects]
        self.fields['add_accounts'].choices = CHOICES
        self.fields['add_accounts'].label = False
