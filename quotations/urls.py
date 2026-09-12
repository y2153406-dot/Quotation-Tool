from django.urls import path

from . import views


urlpatterns = [
    path(
        "quote/",
        views.quote_request,
        name="quote_request",
    ),

    path(
        "quote/success/",
        views.quote_request_success,
        name="quote_request_success",
    ),

    path(
        "quotations/",
        views.quotation_dashboard,
        name="quotation_dashboard",
    ),

    path(
        "quotations/<int:quotation_id>/pdf/",
        views.quotation_pdf,
        name="quotation_pdf",
    ),
]