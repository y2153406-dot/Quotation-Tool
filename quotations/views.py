from django.shortcuts import redirect, render

from .forms import QuoteRequestForm
from .models import QuoteRequestItem


def quote_request(request):

    if request.method == "POST":

        form = QuoteRequestForm(request.POST)

        if form.is_valid():

            quote_request = form.save(commit=False)

            # Get selected customer
            customer = form.cleaned_data["customer"]

            # Automatically assign business
            quote_request.business = customer.business

            # Save quote request
            quote_request.save()


            # Get selected services
            selected_services = form.cleaned_data["services"]


            # Create quote items
            for service in selected_services:

                quantity = int(
                    request.POST.get(
                        f"quantity_{service.id}",
                        1
                    )
                )

                if quantity < 1:
                    quantity = 1


                QuoteRequestItem.objects.create(
                    quote_request=quote_request,
                    service=service,
                    quantity=quantity,
                    unit_price=service.price,
                )


            return redirect(
                "quote_request_success"
            )

    else:

        form = QuoteRequestForm()


    return render(
        request,
        "quotations/quote_request.html",
        {
            "form": form,
        }
    )


def quote_request_success(request):

    return render(
        request,
        "quotations/quote_request_success.html"
    )