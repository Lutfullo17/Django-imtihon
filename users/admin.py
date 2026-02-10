from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailCode, Cart, Order, OrderItem


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ("id", "username", "email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email", "phone")
    ordering = ("-id",)

    fieldsets = UserAdmin.fieldsets + (
        ("Qo‘shimcha", {"fields": ("role", "phone", "image")}),
    )


admin.site.register(EmailCode)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
