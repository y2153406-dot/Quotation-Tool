from django.urls import path

from . import views


urlpatterns = [
    path(
        "request-quote/",
        views.quote_request,
        name="quote_request",
    ),

    path(
        "request-quote/success/",
        views.quote_request_success,
        name="quote_request_success",
    ),
]