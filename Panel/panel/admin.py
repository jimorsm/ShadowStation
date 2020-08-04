from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import PanelUserChangeForm, PanelUserCreationForm
from .models import PanelUser


# Register your models here.

class PanelUserAdmin(UserAdmin):
    form = PanelUserChangeForm
    add_form = PanelUserCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')


admin.site.register(PanelUser, PanelUserAdmin)
