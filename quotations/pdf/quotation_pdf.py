from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_quotation_pdf(quotation):
    """
    Generate a PDF for a quotation and return PDF bytes.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()

    # -----------------------------------------
    # Custom Styles
    # -----------------------------------------

    title_style = ParagraphStyle(
        "QuotationTitle",
        parent=styles["Title"],
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=12,
        leading=15,
        spaceAfter=6,
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
    )

    right_style = ParagraphStyle(
        "Right",
        parent=normal_style,
        alignment=TA_RIGHT,
    )

    # -----------------------------------------
    # Story
    # -----------------------------------------

    story = []

    # -----------------------------------------
    # Business Header
    # -----------------------------------------

    story.append(
        Paragraph(
            quotation.business.name,
            ParagraphStyle(
                "BusinessName",
                parent=styles["Heading1"],
                fontSize=18,
                leading=22,
                alignment=TA_CENTER,
            ),
        )
    )

    if quotation.business.address:
        story.append(
            Paragraph(
                quotation.business.address,
                ParagraphStyle(
                    "BusinessAddress",
                    parent=normal_style,
                    alignment=TA_CENTER,
                ),
            )
        )

    business_contact = (
        f"Email: {quotation.business.email}"
        f" &nbsp;&nbsp; "
        f"Phone: {quotation.business.phone}"
    )

    story.append(
        Paragraph(
            business_contact,
            ParagraphStyle(
                "BusinessContact",
                parent=normal_style,
                alignment=TA_CENTER,
            ),
        )
    )

    if quotation.business.gst_number:
        story.append(
            Paragraph(
                f"GSTIN: {quotation.business.gst_number}",
                ParagraphStyle(
                    "GSTIN",
                    parent=normal_style,
                    alignment=TA_CENTER,
                ),
            )
        )

    story.append(Spacer(1, 8 * mm))

    # -----------------------------------------
    # Quotation Title
    # -----------------------------------------

    story.append(
        Paragraph(
            "QUOTATION",
            title_style,
        )
    )

    story.append(Spacer(1, 4 * mm))

    # -----------------------------------------
    # Quotation Information
    # -----------------------------------------

    quotation_info = [
        [
            Paragraph("<b>Quotation Number</b>", normal_style),
            Paragraph(
                quotation.quotation_number,
                normal_style,
            ),
            Paragraph("<b>Date</b>", normal_style),
            Paragraph(
                quotation.created_at.strftime("%d %b %Y"),
                normal_style,
            ),
        ],
        [
            Paragraph("<b>Status</b>", normal_style),
            Paragraph(
                quotation.get_status_display(),
                normal_style,
            ),
            Paragraph("<b>Valid Until</b>", normal_style),
            Paragraph(
                quotation.valid_until.strftime("%d %b %Y")
                if quotation.valid_until
                else "-",
                normal_style,
            ),
        ],
    ]

    info_table = Table(
        quotation_info,
        colWidths=[
            35 * mm,
            55 * mm,
            30 * mm,
            45 * mm,
        ],
    )

    info_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.whitesmoke,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.25,
                    colors.lightgrey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    story.append(info_table)

    story.append(Spacer(1, 8 * mm))

    # -----------------------------------------
    # Customer Details
    # -----------------------------------------

    story.append(
        Paragraph(
            "Bill To",
            heading_style,
        )
    )

    customer_lines = [
        f"<b>{quotation.customer.name}</b>",
    ]

    if quotation.customer.company_name:
        customer_lines.append(
            quotation.customer.company_name
        )

    if quotation.customer.email:
        customer_lines.append(
            quotation.customer.email
        )

    if quotation.customer.phone:
        customer_lines.append(
            quotation.customer.phone
        )

    if quotation.customer.address:
        customer_lines.append(
            quotation.customer.address
        )

    customer_text = "<br/>".join(customer_lines)

    customer_table = Table(
        [
            [
                Paragraph(
                    customer_text,
                    normal_style,
                )
            ]
        ],
        colWidths=[165 * mm],
    )

    customer_table.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.lightgrey,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.whitesmoke,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    story.append(customer_table)

    story.append(Spacer(1, 8 * mm))

    # -----------------------------------------
    # Services Table
    # -----------------------------------------

    story.append(
        Paragraph(
            "Services",
            heading_style,
        )
    )

    service_data = [
        [
            Paragraph("<b>#</b>", normal_style),
            Paragraph("<b>Service</b>", normal_style),
            Paragraph("<b>Qty</b>", normal_style),
            Paragraph("<b>Unit Price</b>", right_style),
            Paragraph("<b>Total</b>", right_style),
        ]
    ]

    items = quotation.quote_request.items.select_related(
        "service"
    ).all()

    for index, item in enumerate(items, start=1):
        service_data.append(
            [
                Paragraph(str(index), normal_style),
                Paragraph(
                    item.service.name,
                    normal_style,
                ),
                Paragraph(
                    str(item.quantity),
                    normal_style,
                ),
                Paragraph(
                    f"₹{item.unit_price:,.2f}",
                    right_style,
                ),
                Paragraph(
                    f"₹{item.total_price:,.2f}",
                    right_style,
                ),
            ]
        )

    service_table = Table(
        service_data,
        colWidths=[
            12 * mm,
            70 * mm,
            18 * mm,
            32 * mm,
            33 * mm,
        ],
        repeatRows=1,
    )

    service_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.black,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.lightgrey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    story.append(service_table)

    story.append(Spacer(1, 8 * mm))

    # -----------------------------------------
    # Pricing Summary
    # -----------------------------------------

    summary_data = [
        [
            Paragraph("Subtotal", normal_style),
            Paragraph(
                f"₹{quotation.subtotal:,.2f}",
                right_style,
            ),
        ],
        [
            Paragraph(
                f"Discount ({quotation.discount_percentage}%)",
                normal_style,
            ),
            Paragraph(
                f"- ₹{quotation.discount_amount:,.2f}",
                right_style,
            ),
        ],
        [
            Paragraph(
                f"GST ({quotation.tax_percentage}%)",
                normal_style,
            ),
            Paragraph(
                f"₹{quotation.tax_amount:,.2f}",
                right_style,
            ),
        ],
        [
            Paragraph(
                "<b>Grand Total</b>",
                normal_style,
            ),
            Paragraph(
                f"<b>₹{quotation.grand_total:,.2f}</b>",
                right_style,
            ),
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            120 * mm,
            45 * mm,
        ],
        hAlign="RIGHT",
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "LINEABOVE",
                    (0, 0),
                    (-1, 0),
                    0.5,
                    colors.grey,
                ),
                (
                    "LINEABOVE",
                    (0, -1),
                    (-1, -1),
                    1,
                    colors.black,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    story.append(summary_table)

    story.append(Spacer(1, 12 * mm))

    # -----------------------------------------
    # Requirements
    # -----------------------------------------

    if quotation.quote_request.requirements:
        story.append(
            Paragraph(
                "Project Requirements",
                heading_style,
            )
        )

        story.append(
            Paragraph(
                quotation.quote_request.requirements,
                normal_style,
            )
        )

        story.append(Spacer(1, 8 * mm))

    # -----------------------------------------
    # Footer Message
    # -----------------------------------------

    story.append(
        Paragraph(
            "Thank you for your business!",
            ParagraphStyle(
                "ThankYou",
                parent=normal_style,
                alignment=TA_CENTER,
                fontSize=11,
                spaceBefore=10,
            ),
        )
    )

    # -----------------------------------------
    # Build PDF
    # -----------------------------------------

    document.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf