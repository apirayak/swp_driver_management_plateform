from django.contrib import admin
from .models import (
    Role,
    User,
    DriverProfile,
    OperatorProfile,
    AdminProfile,
    Warehouse,
    Bank,
)


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ("bank_code", "bank_name_th", "bank_name_eng")
    search_fields = ("bank_code", "bank_name_th", "bank_name_eng")


class DriverProfileInline(admin.StackedInline):
    model = DriverProfile
    can_delete = False
    verbose_name_plural = "Driver Information"


class OperatorProfileInline(admin.StackedInline):
    model = OperatorProfile
    can_delete = False
    verbose_name_plural = "Operator Information"


class AdminProfileInline(admin.StackedInline):
    model = AdminProfile
    can_delete = False
    verbose_name_plural = "Admin Information"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "role")
    list_filter = ("role",)
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)

    def get_inline_instances(self, request, obj=None):
        inlines = []
        if obj is not None:
            if obj.role and obj.role.role_name == "driver":
                inlines.append(
                    DriverProfileInline(self.model, self.admin_site)
                )
            elif obj.role and obj.role.role_name == "operator":
                inlines.append(
                    OperatorProfileInline(self.model, self.admin_site)
                )
            elif obj.role and obj.role.role_name == "admin":
                inlines.append(AdminProfileInline(self.model, self.admin_site))
        return inlines


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("role_name", "role_description")


admin.site.register(Warehouse)
