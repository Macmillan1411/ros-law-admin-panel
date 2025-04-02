from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "get_full_name",
        "email",
        "role",
        "approved",
        "is_active",
    )
    list_filter = ("role", "approved", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "patronymic")

    fieldsets = UserAdmin.fieldsets + (
        ("Role Information", {"fields": ("role",)}),
        ("Personal Information", {"fields": ("patronymic", "position")}),
        ("Approval Status", {"fields": ("approved", "approval_date")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role Information", {"fields": ("role",)}),
        (
            "Personal Information",
            {"fields": ("first_name", "last_name", "patronymic", "position", "email")},
        ),
        ("Approval Status", {"fields": ("approved",)}),
    )

    readonly_fields = ("approval_date",)

    actions = ["approve_users"]

    def approve_users(self, request, queryset):
        from django.utils import timezone

        updated = queryset.update(
            approved=True, is_active=True, approval_date=timezone.now()
        )
        self.message_user(
            request, f"{updated} пользователей было успешно подтверждено."
        )

    approve_users.short_description = "Подтвердить выбранных пользователей"

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = "ФИО"


admin.site.register(User, CustomUserAdmin)
