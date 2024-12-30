from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Captain, Client

@admin.register(Captain)
class CaptainAdmin(UserAdmin):
    model = Captain
    list_display = (
        "email",
        "phone_number",
        "is_active",
        "is_staff",
        "is_verified",
    )
    list_filter = (
        "is_active",
        "is_staff",
    )
    search_fields = (
        "email",
        "phone_number",
    )
    ordering = (
        "email",
        "is_verified",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "is_verified",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "phone_number",
                ),
            },
        ),
    )

@admin.register(Client)
class ClientAdmin(UserAdmin):
    model = Client
    list_display = (
        "email",
        "phone_number",
        "is_active",
        "is_staff",
        "is_verified",
    )
    list_filter = (
        "is_active",
        "is_staff",
    )
    search_fields = (
        "email",
        "phone_number",
    )
    ordering = (
        "email",
        "is_verified",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "is_verified",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "phone_number",
                ),
            },
        ),
    )