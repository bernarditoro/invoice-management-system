from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, ClientProfile


# Register your models here.
class ClientProfileInline(admin.TabularInline):
    model = ClientProfile


class CustomUserAdmin(UserAdmin):
    inlines = [ClientProfileInline]
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("is_client",)}),
    )


admin.site.register(User, CustomUserAdmin)
