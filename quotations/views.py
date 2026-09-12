from datetime import timedelta

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import QuoteRequestForm
from .models import QuoteRequestItem, Quotation
from .pdf.quotation_pdf import generate_quotation_pdf


# ============================================================
# HOME
# ============================================================

def home(request):
    return render(
        request,
        "quotations/home.html"
    )


# ============================================================
# QUOTE REQUEST
# ============================================================

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


# ============================================================
# QUOTE REQUEST SUCCESS
# ============================================================

def quote_request_success(request):

    return render(
        request,
        "quotations/quote_request_success.html"
    )


# ============================================================
# QUOTATION PDF
# ============================================================

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


# ============================================================
# QUOTATION DASHBOARD
# ============================================================

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

    viewed_quotations = quotations.filter(
        status="viewed"
    ).count()

    accepted_quotations = quotations.filter(
        status="accepted"
    ).count()

    rejected_quotations = quotations.filter(
        status="rejected"
    ).count()

    return render(
        request,
        "quotations/quotation_dashboard.html",
        {
            "quotations": quotations,
            "total_quotations": total_quotations,
            "draft_quotations": draft_quotations,
            "sent_quotations": sent_quotations,
            "viewed_quotations": viewed_quotations,
            "accepted_quotations": accepted_quotations,
            "rejected_quotations": rejected_quotations,
        },
    )

# ============================================================
# SEND QUOTATION EMAIL
# ============================================================

def send_quotation_email(request, quotation_id):
    """
    Generate quotation PDF and send it to the customer by email.
    """

    # -----------------------------------------
    # 1. Get Quotation
    # -----------------------------------------

    quotation = get_object_or_404(
        Quotation.objects.select_related(
            "business",
            "customer",
            "quote_request",
        ),
        id=quotation_id,
    )

    # -----------------------------------------
    # 2. Get Customer Email
    # -----------------------------------------

    customer_email = (
        quotation.customer.email or ""
    ).strip()

    # Debug information
    print("=" * 60)
    print("QUOTATION EMAIL")
    print("Quotation:", quotation.quotation_number)
    print("Customer:", quotation.customer.name)
    print("Customer Email:", repr(customer_email))
    print("=" * 60)

    # -----------------------------------------
    # 3. Check Customer Email
    # -----------------------------------------

    if not customer_email:
        return HttpResponse(
            "Customer email address is missing.",
            status=400,
        )

    # -----------------------------------------
    # 4. Generate Quotation PDF
    # -----------------------------------------

    pdf = generate_quotation_pdf(quotation)

    # -----------------------------------------
    # 5. Create Public Quotation URL
    # -----------------------------------------

    public_url = request.build_absolute_uri(
        f"/quotation/view/{quotation.public_token}/"
    )

    # -----------------------------------------
    # 6. Email Subject
    # -----------------------------------------

    subject = (
        f"Quotation {quotation.quotation_number} "
        f"from {quotation.business.name}"
    )

    # -----------------------------------------
    # 7. Valid Until
    # -----------------------------------------

    valid_until = (
        quotation.valid_until.strftime("%d %b %Y")
        if quotation.valid_until
        else "N/A"
    )

    # -----------------------------------------
    # 8. Email Body
    # -----------------------------------------

    message = f"""
Dear {quotation.customer.name},

Please find attached your quotation
{quotation.quotation_number}.

Quotation Amount: ₹{quotation.grand_total:,.2f}

Valid Until: {valid_until}

You can also view your quotation online:

{public_url}

Thank you for your business.

Regards,
{quotation.business.name}
{quotation.business.email}
{quotation.business.phone}
"""

    # -----------------------------------------
    # 9. Create Email
    # -----------------------------------------

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email="y2153406@gmail.com",
        to=[customer_email],
    )

    # -----------------------------------------
    # 10. Attach PDF
    # -----------------------------------------

    email.attach(
        f"{quotation.quotation_number}.pdf",
        pdf,
        "application/pdf",
    )

    # -----------------------------------------
    # 11. Send Email
    # -----------------------------------------

    print("Sending quotation email...")
    print("Sending to:", customer_email)

    sent_count = email.send(
        fail_silently=False
    )

    print("Email send result:", sent_count)

    # -----------------------------------------
    # 12. Update Status
    # -----------------------------------------

    if sent_count == 1:

        quotation.status = "sent"

        quotation.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        print("Quotation status updated to SENT.")

    # -----------------------------------------
    # 13. Redirect Dashboard
    # -----------------------------------------

    return redirect(
        "quotation_dashboard"
    )


# ============================================================
# PUBLIC QUOTATION VIEW
# ============================================================

def public_quotation_view(request, public_token):

    quotation = get_object_or_404(
        Quotation.objects.select_related(
            "business",
            "customer",
            "quote_request",
        ).prefetch_related(
            "quote_request__items__service"
        ),
        public_token=public_token,
    )

    return render(
        request,
        "quotations/public_quotation.html",
        {
            "quotation": quotation,
            "items": quotation.quote_request.items.all(),
        },
    )


# ============================================================
# ACCEPT QUOTATION
# ============================================================

def accept_quotation(request, public_token):

    if request.method != "POST":
        return redirect(
            "public_quotation_view",
            public_token=public_token,
        )

    quotation = get_object_or_404(
        Quotation,
        public_token=public_token,
    )

    # -----------------------------------------
    # Check quotation expiry
    # -----------------------------------------

    if (
        quotation.valid_until
        and quotation.valid_until < timezone.now().date()
        and quotation.status in ["draft", "sent", "viewed"]
    ):
        quotation.status = "expired"

        quotation.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return redirect(
            "public_quotation_view",
            public_token=public_token,
        )

    # -----------------------------------------
    # Accept quotation
    # -----------------------------------------

    if quotation.status in ["sent", "viewed"]:

        quotation.status = "accepted"

        quotation.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

    return redirect(
        "public_quotation_view",
        public_token=public_token,
    )

# ============================================================
# REJECT QUOTATION
# ============================================================

def reject_quotation(request, public_token):

    if request.method != "POST":
        return redirect(
            "public_quotation_view",
            public_token=public_token,
        )

    quotation = get_object_or_404(
        Quotation,
        public_token=public_token,
    )

    # -----------------------------------------
    # Check quotation expiry
    # -----------------------------------------

    if (
        quotation.valid_until
        and quotation.valid_until < timezone.now().date()
        and quotation.status in ["draft", "sent", "viewed"]
    ):
        quotation.status = "expired"

        quotation.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return redirect(
            "public_quotation_view",
            public_token=public_token,
        )

    # -----------------------------------------
    # Reject quotation
    # -----------------------------------------

    if quotation.status in ["sent", "viewed"]:

        quotation.status = "rejected"

        quotation.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

    return redirect(
        "public_quotation_view",
        public_token=public_token,
    )