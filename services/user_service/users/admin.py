from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile
from .forms import UserCreationForm, UserChangeForm


class ProfileInlines(admin.StackedInline):
    model = Profile

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = [ProfileInlines]

    fieldsets = (
        ("Information User", {"fields":("phone",)}),
        ("Permissions", {"fields":("is_active", "is_staff", "is_superuser")}),
    )

    add_fieldsets = (
        ("Creation User", {"fields":("phone", "password1", "password2")}),
    )

    list_display = ["phone"]
    search_fields = ["phone"]
    ordering = ["-id"]

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)

