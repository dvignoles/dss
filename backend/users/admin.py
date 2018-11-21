from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

def promote_user(admin, request, queryset):
	queryset.update(is_OU=True)
promote_user.short_description = "Promote GU to OU"

def demote_user(admin, request, queryset):
	queryset.update(is_OU=False)
demote_user.short_description = "Demote OU to GU"

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'interests', 'is_OU']
    actions = [promote_user, demote_user]

admin.site.register(CustomUser, CustomUserAdmin)