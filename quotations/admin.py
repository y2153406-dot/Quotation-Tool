from django.contrib import admin

from .models import (
    Business,
    Customer,
    Service,
    QuoteRequest,
    QuoteRequestItem,
    Quotation,
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

    search_fields = (
        "name",
        "email",
        "phone",
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

    list_filter = (
        "business",
        "created_at",
    )

    search_fields = (
        "name",
        "company_name",
        "email",
        "phone",
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
        "created_at",
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
        "status",
        "subtotal_display",
        "discount_display",
        "tax_display",
        "grand_total_display",
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

    readonly_fields = (
        "subtotal_display",
        "discount_display",
        "taxable_amount_display",
        "tax_display",
        "grand_total_display",
    )

    fieldsets = (
        (
            "Request Information",
            {
                "fields": (
                    "business",
                    "customer",
                    "requirements",
                    "status",
                )
            },
        ),
        (
            "Pricing",
            {
                "fields": (
                    "discount_percentage",
                    "tax_percentage",
                    "subtotal_display",
                    "discount_display",
                    "taxable_amount_display",
                    "tax_display",
                    "grand_total_display",
                )
            },
        ),
    )

    def subtotal_display(self, obj):
        return f"₹{obj.subtotal:,.2f}"

    subtotal_display.short_description = "Subtotal"

    def discount_display(self, obj):
        return f"₹{obj.discount_amount:,.2f}"

    discount_display.short_description = "Discount"

    def taxable_amount_display(self, obj):
        return f"₹{obj.taxable_amount:,.2f}"

    taxable_amount_display.short_description = "Taxable Amount"

    def tax_display(self, obj):
        return f"₹{obj.tax_amount:,.2f}"

    tax_display.short_description = "GST"

    def grand_total_display(self, obj):
        return f"₹{obj.grand_total:,.2f}"

    grand_total_display.short_description = "Grand Total"


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
        return f"₹{obj.total_price:,.2f}"

    total_price_display.short_description = "Total"

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = (
        "quotation_number",
        "customer",
        "business",
        "grand_total",
        "status",
        "valid_until",
        "created_at",
    )

    list_filter = (
        "status",
        "business",
        "created_at",
    )

    search_fields = (
        "quotation_number",
        "customer__name",
        "customer__email",
    )

    readonly_fields = (
        "quotation_number",
        "subtotal",
        "discount_amount",
        "tax_amount",
        "grand_total",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Quotation Information",
            {
                "fields": (
                    "quotation_number",
                    "quote_request",
                    "business",
                    "customer",
                    "status",
                    "valid_until",
                )
            },
        ),
        (
            "Pricing",
            {
                "fields": (
                    "subtotal",
                    "discount_percentage",
                    "discount_amount",
                    "tax_percentage",
                    "tax_amount",
                    "grand_total",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )