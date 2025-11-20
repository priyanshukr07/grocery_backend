from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, Category, Product, CartItem, WishlistItem, Order, OrderItem


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )


# Product Admin with Image Preview
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'image_preview')
    list_filter = ('category',)
    search_fields = ('name',)

    readonly_fields = ('image_preview',)

    # admin.py
    def image_preview(self, obj):
        first = obj.images.first()
        if first and first.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover; border-radius:5px;" />', first.image.url)
        return "(No Image)"

    image_preview.short_description = "Image"


# Register Models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(WishlistItem)
admin.site.register(Order)
admin.site.register(OrderItem)

