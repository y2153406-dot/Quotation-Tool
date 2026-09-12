from django.shortcuts import redirect, render

from .forms import QuoteRequestForm


def quote_request(request):
    if request.method == "POST":
        form = QuoteRequestForm(request.POST)

        if form.is_valid():

            quote_request = form.save(commit=False)

            # Get the selected customer
            customer = form.cleaned_data["customer"]

            # Automatically assign customer's business
            quote_request.business = customer.business

            # Save the quote request
            quote_request.save()

            return redirect(
                "quote_request_success"
            )

    else:
        form = QuoteRequestForm()

    return render(
        request,
        "quotations/quote_request.html",
        {"form": form}
    )


def quote_request_success(request):
    return render(
        request,
        "quotations/quote_request_success.html"
    )