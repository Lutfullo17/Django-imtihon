from django.contrib import admin
from .models import Product, Category, Comment,  Like

admin.site.register(Comment)
admin.site.register(Like)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "category", "created_by", "created_at")

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        ab = super().get_queryset(request)
        if request.user.is_superuser:
            return ab
        if getattr(request.user, "role", None) == "seller":
            return ab.filter(created_by= request.user)
        return ab

    def has_change_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True

        if getattr(request.user, "role", None) == "seller":
                return obj.created_by == request.user
        return request.user.is_staff

    def has_delete_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return None
        if getattr(request.user, "role", None) == "seller":
                return obj.created_by == request.user
        return request.user.is_staff


