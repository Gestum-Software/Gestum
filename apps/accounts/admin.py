from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm
    fieldsets = UserAdmin.fieldsets


admin.site.register(CustomUser, CustomUserAdmin)
