from django.urls import path

from . import views


urlpatterns = [

    # Home
    path(
        "",
        views.home,
        name="home",
    ),

    # Quote Request
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

    # Quotation Dashboard
    path(
        "quotations/",
        views.quotation_dashboard,
        name="quotation_dashboard",
    ),

    # Quotation PDF
    path(
        "quotations/<int:quotation_id>/pdf/",
        views.quotation_pdf,
        name="quotation_pdf",
    ),

    # Send Quotation Email
    path(
        "quotations/<int:quotation_id>/send-email/",
        views.send_quotation_email,
        name="send_quotation_email",
    ),

    # Public Quotation
    path(
        "quotation/view/<uuid:public_token>/",
        views.public_quotation_view,
        name="public_quotation_view",
    ),

    # Accept Quotation
    path(
        "quotation/view/<uuid:public_token>/accept/",
        views.accept_quotation,
        name="accept_quotation",
    ),

    # Reject Quotation
    path(
        "quotation/view/<uuid:public_token>/reject/",
        views.reject_quotation,
        name="reject_quotation",
    ),
]