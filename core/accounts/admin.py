from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profiles

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_superuser')
    list_filter = ('email', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)
    
    fieldsets = (
        ('Authentication', {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Group Permissions", {"fields": ("groups", "user_permissions")}),
        ("Important date", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profiles)