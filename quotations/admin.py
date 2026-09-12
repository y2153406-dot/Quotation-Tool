from django.contrib import admin

from .models import Business, Customer


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