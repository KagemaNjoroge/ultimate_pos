from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, cm
import os
from datetime import datetime
import io
import qrcode
import tempfile


def create_invoice_pdf(invoice_data, output_path=None):
    """
    Generate a PDF invoice based on the provided data

    Args:
        invoice_data (dict): Dictionary containing invoice details with the following keys:
            - company_info: Dict with company name, address, phone, email, logo_path, website, registration_number
            - customer_info: Dict with customer name, address, phone, email, customer_id, tax_number
            - invoice_info: Dict with invoice number, date, due_date, reference, terms, payment_method
            - items: List of dicts with product name, quantity, unit_price, total, description, sku
            - totals: Dict with subtotal, tax, discount, total, paid_amount, balance_due
            - payment_status: String ('Paid', 'Unpaid', 'Partial', 'Overdue', 'Cancelled')
            - notes: String with additional notes
            - payment_terms: String with payment terms
            - payment_instructions: String with payment instructions
            - qr_data: String with data to encode in QR code (e.g., payment link or invoice verification)
            - additional_info: Dict with any additional fields to display
        output_path (str, optional): Path to save the PDF file. If None, returns PDF as bytes.

    Returns:
        str or bytes: Path to saved PDF file, or PDF content as bytes if output_path is None
    """
    # Create a buffer if no output path is specified
    if output_path is None:
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
    else:
        c = canvas.Canvas(output_path, pagesize=A4)

    width, height = A4  # Standard ISO A4 size

    # Set up styles
    styles = getSampleStyleSheet()

    # Start at the top of the page
    y_position = height - 1 * cm

    # Draw payment status watermark if provided
    payment_status = invoice_data.get("payment_status", "").upper()
    if payment_status:
        # Save canvas state
        c.saveState()

        # Set transparency and rotation for the watermark
        c.setFillColorRGB(0.95, 0.95, 0.95, alpha=0.7)  # Light gray with transparency
        c.translate(width / 2, height / 2)
        c.rotate(45)

        # Choose color based on status
        if payment_status == "PAID":
            c.setFillColorRGB(0, 0.6, 0, alpha=0.3)  # Green with transparency
        elif payment_status == "UNPAID":
            c.setFillColorRGB(0.8, 0, 0, alpha=0.3)  # Red with transparency
        elif payment_status == "PARTIAL":
            c.setFillColorRGB(0.9, 0.6, 0, alpha=0.3)  # Orange with transparency
        elif payment_status == "OVERDUE":
            c.setFillColorRGB(0.8, 0, 0, alpha=0.4)  # Darker red with transparency
        elif payment_status == "CANCELLED":
            c.setFillColorRGB(0.1, 0.1, 0.1, alpha=0.4)  # Dark gray with transparency

        # Draw the watermark
        c.setFont("Helvetica-Bold", 80)
        text_width = c.stringWidth(payment_status, "Helvetica-Bold", 80)
        c.drawString(-text_width / 2, 0, payment_status)

        # Restore canvas state
        c.restoreState()

    # Company Logo (if available)
    if "logo_path" in invoice_data.get("company_info", {}):
        logo_path = invoice_data["company_info"]["logo_path"]
        if os.path.exists(logo_path):
            c.drawImage(
                logo_path,
                1 * cm,
                y_position - 2.5 * cm,
                width=2 * inch,
                height=1 * inch,
                preserveAspectRatio=True,
            )  # Company Info (right-aligned)
    company = invoice_data.get("company_info", {})

    # Use direct text drawing for company info with right alignment
    company_name = company.get("name", "Company Name")
    company_address = company.get("address", "Company Address")
    company_phone = f"Phone: {company.get('phone', 'N/A')}"
    company_email = f"Email: {company.get('email', 'N/A')}"
    company_tax = f"Tax ID: {company.get('tax_id', 'N/A')}"

    # Calculate text width for right alignment
    c.setFont("Helvetica-Bold", 10)
    name_width = c.stringWidth(company_name, "Helvetica-Bold", 10)
    c.drawString(width - name_width - 2 * cm, y_position, company_name)

    c.setFont("Helvetica", 9)
    address_width = c.stringWidth(company_address, "Helvetica", 9)
    c.drawString(width - address_width - 2 * cm, y_position - 15, company_address)

    phone_width = c.stringWidth(company_phone, "Helvetica", 9)
    c.drawString(width - phone_width - 2 * cm, y_position - 30, company_phone)

    email_width = c.stringWidth(company_email, "Helvetica", 9)
    c.drawString(width - email_width - 2 * cm, y_position - 45, company_email)

    tax_width = c.stringWidth(company_tax, "Helvetica", 9)
    c.drawString(width - tax_width - 2 * cm, y_position - 60, company_tax)

    # Move down after company header
    y_position -= 3 * cm

    # Invoice Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(
        1 * cm, y_position, "INVOICE"
    )  # Invoice Info - Enhanced with more details
    invoice_info = invoice_data.get("invoice_info", {})
    c.setFont("Helvetica-Bold", 10)
    c.drawString(
        1 * cm,
        y_position - 0.7 * cm,
        f"Invoice #: {invoice_info.get('invoice_number', 'N/A')}",
    )
    c.drawString(
        1 * cm,
        y_position - 1.2 * cm,
        f"Date: {invoice_info.get('date', datetime.now().strftime('%Y-%m-%d'))}",
    )
    c.drawString(
        1 * cm,
        y_position - 1.7 * cm,
        f"Due Date: {invoice_info.get('due_date', 'N/A')}",
    )

    # Additional invoice information
    if invoice_info.get("reference"):
        c.drawString(
            1 * cm,
            y_position - 2.2 * cm,
            f"Reference: {invoice_info.get('reference')}",
        )

    if invoice_info.get("payment_method"):
        c.drawString(
            1 * cm,
            y_position - 2.7 * cm,
            f"Payment Method: {invoice_info.get('payment_method')}",
        )

    # Payment status prominently displayed (in addition to watermark)
    payment_status = invoice_data.get("payment_status", "")
    if payment_status:
        # Set color based on status
        if payment_status.upper() == "PAID":
            c.setFillColorRGB(0, 0.6, 0)  # Green
        elif payment_status.upper() == "UNPAID":
            c.setFillColorRGB(0.8, 0, 0)  # Red
        elif payment_status.upper() == "PARTIAL":
            c.setFillColorRGB(0.9, 0.6, 0)  # Orange
        elif payment_status.upper() == "OVERDUE":
            c.setFillColorRGB(0.8, 0, 0)  # Red
        elif payment_status.upper() == "CANCELLED":
            c.setFillColorRGB(0.3, 0.3, 0.3)  # Dark gray

        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(
            width - 2 * cm, y_position, f"Status: {payment_status.upper()}"
        )
        c.setFillColorRGB(0, 0, 0)  # Reset to black

    # QR code for digital payment or verification
    qr_data = invoice_data.get("qr_data")
    if qr_data:
        # Generate QR code
        qr_code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_code.add_data(qr_data)
        qr_code.make(fit=True)

        qr_img = qr_code.make_image(fill_color="black", back_color="white")

        # Save QR to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            qr_path = tmp_file.name
            qr_img.save(qr_path)

        # Draw QR code on PDF
        c.drawImage(
            qr_path,
            width - 3.5 * cm,
            y_position - 3.5 * cm,
            width=2.5 * cm,
            height=2.5 * cm,
        )

        # Clean up temporary file
        try:
            os.unlink(qr_path)
        except:
            pass

    # Customer Info - Enhanced
    y_position -= 3 * cm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1 * cm, y_position, "Bill To:")

    customer = invoice_data.get("customer_info", {})

    # Use plain text instead of HTML for customer info
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1 * cm, y_position - 15, customer.get("name", "Customer Name"))

    c.setFont("Helvetica", 9)
    c.drawString(1 * cm, y_position - 30, customer.get("address", "Customer Address"))
    c.drawString(1 * cm, y_position - 45, f"Phone: {customer.get('phone', 'N/A')}")
    c.drawString(1 * cm, y_position - 60, f"Email: {customer.get('email', 'N/A')}")

    # Additional customer information
    line_offset = 75
    if customer.get("customer_id"):
        c.drawString(
            1 * cm,
            y_position - line_offset,
            f"Customer ID: {customer.get('customer_id')}",
        )
        line_offset += 15

    if customer.get("tax_number"):
        c.drawString(
            1 * cm,
            y_position - line_offset,
            f"Tax Number: {customer.get('tax_number')}",
        )
        line_offset += 15

    # Ship To section if different from billing
    if invoice_data.get("shipping_info"):
        shipping = invoice_data.get("shipping_info", {})
        ship_y = y_position
        c.setFont("Helvetica-Bold", 10)
        c.drawString(width / 2, ship_y, "Ship To:")

        c.setFont("Helvetica-Bold", 9)
        c.drawString(
            width / 2,
            ship_y - 15,
            shipping.get("name", customer.get("name", "Customer Name")),
        )

        c.setFont("Helvetica", 9)
        c.drawString(
            width / 2, ship_y - 30, shipping.get("address", "Shipping Address")
        )
        if shipping.get("phone"):
            c.drawString(width / 2, ship_y - 45, f"Phone: {shipping.get('phone')}")
        if shipping.get("email"):
            c.drawString(
                width / 2, ship_y - 60, f"Email: {shipping.get('email')}"
            )  # Calculate maximum height of either billing or shipping info
    max_info_height = line_offset + 15  # Default height of billing info

    if invoice_data.get("shipping_info"):
        max_info_height = max(max_info_height, 75)  # Minimum height for shipping info

    # Move down for items table with proper spacing
    y_position -= max_info_height * 0.5 + 1.5 * cm  # Additional spacing

    # Item table header
    items_data = [["Item", "Quantity", "Unit Price", "Total"]]

    # Add items
    for item in invoice_data.get("items", []):
        items_data.append(
            [
                item.get("product_name", "Product"),
                str(item.get("quantity", 0)),
                f"${item.get('unit_price', 0):.2f}",
                f"${item.get('total', 0):.2f}",
            ]
        )

    # Create table
    table = Table(items_data, colWidths=[9 * cm, 3 * cm, 3 * cm, 3 * cm])

    # Style the table
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                ("ALIGN", (0, 1), (0, -1), "LEFT"),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
            ]
        )
    )

    # Draw the table on the PDF
    table.wrapOn(c, width - 2 * cm, 500)
    table.drawOn(c, 1 * cm, y_position - len(items_data) * 20)

    # Move down after items table
    y_position -= (
        len(items_data) + 1
    ) * 20 + 1 * cm  # Totals - Enhanced with payment status
    totals = invoice_data.get("totals", {})
    totals_data = [
        ["Subtotal:", f"${totals.get('subtotal', 0):.2f}"],
        ["Tax:", f"${totals.get('tax', 0):.2f}"],
        ["Discount:", f"${totals.get('discount', 0):.2f}"],
        ["Total:", f"${totals.get('total', 0):.2f}"],
    ]

    # Add payment information if available
    if "paid_amount" in totals:
        totals_data.append(["Amount Paid:", f"${totals.get('paid_amount', 0):.2f}"])
        totals_data.append(
            [
                "Balance Due:",
                f"${totals.get('balance_due', totals.get('total', 0) - totals.get('paid_amount', 0)):.2f}",
            ]
        )

    # Create table for totals
    totals_table = Table(totals_data, colWidths=[4 * cm, 3 * cm])

    # Style the totals table
    totals_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (0, -1), "RIGHT"),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("FONTNAME", (0, -1), (1, -1), "Helvetica-Bold"),
                ("LINEABOVE", (0, -1), (1, -1), 1, colors.black),
                ("BOTTOMPADDING", (0, 0), (1, -2), 6),
            ]
        )
    )

    # Position totals at the right side
    totals_table.wrapOn(c, width - 2 * cm, 100)
    totals_table.drawOn(c, width - 8 * cm, y_position - len(totals_data) * 20)

    # Move down for notes
    y_position -= (
        len(totals_data) + 1
    ) * 20 + 1 * cm  # Add notes section with multiple information blocks
    y_notes = y_position
    notes_offset = 0
    instructions_offset = 0

    # Notes - Left side
    left_column_width = width / 2 - 1.5 * cm  # Ensure there's a gap between columns

    if "notes" in invoice_data:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1 * cm, y_notes, "Notes:")
        c.setFont("Helvetica", 9)

        # Split notes into multiple lines if needed
        notes = invoice_data["notes"]
        text_object = c.beginText(1 * cm, y_notes - 20)
        text_object.setFont("Helvetica", 9)

        # Handle multi-line notes with proper wrapping
        from textwrap import wrap

        wrapped_text = []
        for paragraph in notes.split("\n"):
            wrapped_text.extend(
                wrap(paragraph, width=65)
            )  # Narrower width for left column

        for i, line in enumerate(wrapped_text):
            text_object.textLine(line)
            notes_offset = max(notes_offset, (i + 1) * 15)

        c.drawText(text_object)

    # Payment Instructions - Right side with clear separation
    if "payment_instructions" in invoice_data:
        # Position at the right side of the page with margin
        right_col_x = width / 2 + 0.5 * cm

        c.setFont("Helvetica-Bold", 10)
        c.drawString(right_col_x, y_notes, "Payment Instructions:")
        c.setFont("Helvetica", 9)

        # Split payment instructions into multiple lines
        instructions = invoice_data["payment_instructions"]
        text_object = c.beginText(right_col_x, y_notes - 20)
        text_object.setFont("Helvetica", 9)

        # Handle multi-line payment instructions with proper wrapping
        from textwrap import wrap

        wrapped_instructions = []
        for paragraph in instructions.split("\n"):
            wrapped_instructions.extend(
                wrap(paragraph, width=50)
            )  # Narrower width for right column

        for i, line in enumerate(wrapped_instructions):
            text_object.textLine(line)
            instructions_offset = max(instructions_offset, (i + 1) * 15)

        c.drawText(
            text_object
        )  # Additional info section - positioned below both notes and payment instructions
    if "additional_info" in invoice_data:
        additional_info = invoice_data["additional_info"]
        if additional_info:
            # Calculate the maximum offset between notes and payment instructions
            max_offset = max(notes_offset, instructions_offset) + 40
            y_pos_additional = y_notes - max_offset

            c.setFont("Helvetica-Bold", 10)
            c.drawString(1 * cm, y_pos_additional, "Additional Information:")
            c.setFont("Helvetica", 9)

            # Display additional information in two columns if there are many items
            items = list(additional_info.items())
            if len(items) > 4:
                # First column
                line_y = y_pos_additional - 20
                for i in range(0, len(items) // 2 + len(items) % 2):
                    key, value = items[i]
                    c.drawString(1 * cm, line_y, f"{key}: {value}")
                    line_y -= 15

                # Second column
                line_y = y_pos_additional - 20
                for i in range(len(items) // 2 + len(items) % 2, len(items)):
                    key, value = items[i]
                    c.drawString(width / 2 + 0.5 * cm, line_y, f"{key}: {value}")
                    line_y -= 15
            else:
                # Single column for few items
                line_y = y_pos_additional - 20
                for key, value in additional_info.items():
                    c.drawString(1 * cm, line_y, f"{key}: {value}")
                    line_y -= 15

    # Add footer with payment terms and thank you note
    c.setFont("Helvetica", 9)
    footer_y = 2 * cm
    # c.drawString(
    #     1 * cm,
    #     footer_y,
    #     f"Payment Terms: {invoice_data.get('payment_terms', 'Due on receipt')}",
    # )
    c.drawString(1 * cm, footer_y - 15, "Thank you for your business!")

    # Add company website if available
    if "website" in invoice_data.get("company_info", {}):
        c.drawString(
            1 * cm, footer_y - 30, f"{invoice_data['company_info']['website']}"
        )

    # Add page number at the bottom
    c.setFont("Helvetica", 8)

    c.drawRightString(width - 1 * cm, 1 * cm, "Page 1 of 1")

    # Set PDF metadata properties
    invoice_number = invoice_data.get("invoice_info", {}).get("invoice_number", "")
    customer_name = invoice_data.get("customer_info", {}).get("name", "")

    # Set the document title that will show in the browser tab
    title = f"Receipt #{invoice_number} - {customer_name}"
    c.setTitle(title)

    # You can also set other metadata properties
    c.setSubject(f"Invoice {invoice_number}")
    c.setAuthor(invoice_data.get("company_info", {}).get("name", "UltimatePOS"))

    # Save the PDF
    c.save()

    if output_path is None:
        buffer.seek(0)
        return buffer.getvalue()
    else:
        return output_path
