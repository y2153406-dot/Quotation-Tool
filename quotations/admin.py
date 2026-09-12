from django.contrib import admin

from .models import (
    Business,
    Customer,
    Service,
    QuoteRequest,
    QuoteRequestItem,
)


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "gst_number",
        "created_at",
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company_name",
        "email",
        "phone",
        "business",
        "created_at",
    )
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "business",
        "price",
        "is_active",
        "created_at",
    )

    list_filter = (
        "business",
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "business",
        "quantity",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "business",
        "created_at",
    )

    search_fields = (
        "customer__name",
        "customer__email",
        "requirements",
    )

@admin.register(QuoteRequestItem)
class QuoteRequestItemAdmin(admin.ModelAdmin):
    list_display = (
        "quote_request",
        "service",
        "quantity",
        "unit_price",
        "total_price_display",
        "created_at",
    )

    list_filter = (
        "service",
        "created_at",
    )

    search_fields = (
        "service__name",
        "quote_request__customer__name",
    )

    def total_price_display(self, obj):
        return obj.total_price

    total_price_display.short_description = "Total"