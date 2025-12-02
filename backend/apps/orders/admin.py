from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("book", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "status", "total_price", "created_at")
    list_filter = ("status", "payment_type", "created_at")
    inlines = [OrderItemInline]
    search_fields = ("full_name", "phone")
    readonly_fields = ("total_price",)
