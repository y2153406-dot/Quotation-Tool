from datetime import timedelta

from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import QuoteRequestForm
from .models import QuoteRequestItem, Quotation


def quote_request(request):
    if request.method == "POST":
        form = QuoteRequestForm(request.POST)

        if form.is_valid():
            # -----------------------------------------
            # 1. Create Quote Request
            # -----------------------------------------
            quote_request = form.save(commit=False)

            # Get selected customer
            customer = form.cleaned_data["customer"]

            # Automatically assign business
            quote_request.business = customer.business

            # Save quote request
            quote_request.save()

            # -----------------------------------------
            # 2. Get Selected Services
            # -----------------------------------------
            selected_services = form.cleaned_data["services"]

            # -----------------------------------------
            # 3. Create Quote Request Items
            # -----------------------------------------
            for service in selected_services:
                quantity = int(
                    request.POST.get(
                        f"quantity_{service.id}",
                        1
                    )
                )

                # Prevent invalid quantity
                if quantity < 1:
                    quantity = 1

                QuoteRequestItem.objects.create(
                    quote_request=quote_request,
                    service=service,
                    quantity=quantity,
                    unit_price=service.price,
                )

            # -----------------------------------------
            # 4. Calculate Quotation Amounts
            # -----------------------------------------
            subtotal = quote_request.subtotal
            discount_amount = quote_request.discount_amount
            tax_amount = quote_request.tax_amount
            grand_total = quote_request.grand_total

            # -----------------------------------------
            # 5. Generate Quotation Number
            # -----------------------------------------
            quotation_number = (
                f"QT-{timezone.now().year}-{quote_request.id:04d}"
            )

            # -----------------------------------------
            # 6. Create Quotation
            # -----------------------------------------
            Quotation.objects.create(
                quote_request=quote_request,
                quotation_number=quotation_number,
                customer=quote_request.customer,
                business=quote_request.business,
                subtotal=subtotal,
                discount_percentage=quote_request.discount_percentage,
                discount_amount=discount_amount,
                tax_percentage=quote_request.tax_percentage,
                tax_amount=tax_amount,
                grand_total=grand_total,
                status="draft",
                valid_until=(
                    timezone.now().date()
                    + timedelta(days=15)
                ),
            )

            # -----------------------------------------
            # 7. Redirect to Success Page
            # -----------------------------------------
            return redirect("quote_request_success")

    else:
        form = QuoteRequestForm()

    # -----------------------------------------
    # Render Quote Request Form
    # -----------------------------------------
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
def quotation_dashboard(request):
    quotations = (
        Quotation.objects
        .select_related(
            "customer",
            "business",
            "quote_request",
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "quotations/quotation_dashboard.html",
        {
            "quotations": quotations,
        },
    )