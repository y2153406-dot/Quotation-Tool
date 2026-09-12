from datetime import timedelta
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import QuoteRequestForm
from .models import QuoteRequestItem, Quotation
from .pdf.quotation_pdf import generate_quotation_pdf


def quote_request(request):
    if request.method == "POST":
        form = QuoteRequestForm(request.POST)

        if form.is_valid():
            # -----------------------------------------
            # 1. Create Quote Request
            # -----------------------------------------
            quote_request = form.save(commit=False)

            customer = form.cleaned_data["customer"]

            # Automatically assign business
            quote_request.business = customer.business

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

            return redirect("quote_request_success")

    else:
        form = QuoteRequestForm()

    return render(
        request,
        "quotations/quote_request.html",
        {
            "form": form,
        },
    )


def quote_request_success(request):
    return render(
        request,
        "quotations/quote_request_success.html"
    )


def quotation_pdf(request, quotation_id):
    """
    Generate and return the quotation PDF.
    """

    quotation = get_object_or_404(
        Quotation.objects.select_related(
            "business",
            "customer",
            "quote_request",
        ),
        id=quotation_id,
    )

    pdf = generate_quotation_pdf(quotation)

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'inline; filename="{quotation.quotation_number}.pdf"'
    )

    return response


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

    total_quotations = quotations.count()
    draft_quotations = quotations.filter(
        status="draft"
    ).count()
    sent_quotations = quotations.filter(
        status="sent"
    ).count()
    accepted_quotations = quotations.filter(
        status="accepted"
    ).count()

    return render(
        request,
        "quotations/quotation_dashboard.html",
        {
            "quotations": quotations,
            "total_quotations": total_quotations,
            "draft_quotations": draft_quotations,
            "sent_quotations": sent_quotations,
            "accepted_quotations": accepted_quotations,
        },
    )
def send_quotation_email(request, quotation_id):
    """
    Generate quotation PDF and send it to the customer by email.
    """

    quotation = get_object_or_404(
        Quotation.objects.select_related(
            "business",
            "customer",
            "quote_request",
        ),
        id=quotation_id,
    )

    # Generate PDF
    pdf = generate_quotation_pdf(quotation)

    subject = (
        f"Quotation {quotation.quotation_number} "
        f"from {quotation.business.name}"
    )

    message = f"""
Dear {quotation.customer.name},

Please find attached your quotation
{quotation.quotation_number}.

Quotation Amount: ₹{quotation.grand_total:,.2f}

Valid Until: {
    quotation.valid_until.strftime("%d %b %Y")
    if quotation.valid_until
    else "N/A"
}

Thank you for your business.

Regards,
{quotation.business.name}
{quotation.business.email}
{quotation.business.phone}
"""

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=None,
        to=[quotation.customer.email],
    )

    email.attach(
        f"{quotation.quotation_number}.pdf",
        pdf,
        "application/pdf",
    )

    email.send(fail_silently=False)

    quotation.status = "sent"
    quotation.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    return redirect("quotation_dashboard")