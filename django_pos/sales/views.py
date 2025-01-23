from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django_pos.wsgi import *
from django_pos import settings
from django.template.loader import get_template
from customers.models import Customer
from pos.models import Notifications

from products.models import Product
from weasyprint import HTML, CSS
from .models import Sale, SaleDetail, SaleItem
import json
from company.models import Company
import qrcode
from io import BytesIO
import base64
from PIL import Image
from inventory.models import Inventory


def is_ajax(request: HttpRequest) -> bool:
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


@login_required(login_url="/users/login/")
def sales_list_view(request: HttpRequest) -> HttpResponse:
    sale_details = SaleDetail.objects.all()
    context = {"sales": sale_details}
    return render(request, "sales/sales.html", context=context)


@login_required(login_url="/users/login/")
def sales_add_view(request: HttpRequest) -> HttpResponse:
    context = {
        "customers": [c.to_select2() for c in Customer.objects.all()],
    }

    if request.method == "POST":
        if is_ajax(request=request):

            data = json.load(request)

            customer_id = int(data["customer"])
            customer = Customer.objects.get(id=customer_id)
            sub_total = float(data["sub_total"])
            tax_percentage = float(data["tax_percentage"])
            tax_amount = float(data["tax_amount"])
            grand_total = float(data["grand_total"])
            amount_payed = float(data["amount_payed"])
            amount_change = float(data["amount_change"])

            prods = data["products"]
            # Create the sale
            sale = Sale(
                customer=customer,
                sub_total=sub_total,
                tax_percentage=tax_percentage,
                tax_amount=tax_amount,
                grand_total=grand_total,
                amount_payed=amount_payed,
                amount_change=amount_change,
            )
            sale.save()
            # Create the sale details
            products = []
            for prod in prods:
                product = Product.objects.get(id=prod["id"])
                products.append(product)
                # Update the inventory
                if product.track_inventory:
                    inv = Inventory.objects.filter(product=product)
                    if inv.exists():
                        inv = inv.first()
                        # # for each product check of inventory quantity > 0
                        if inv.quantity > 0:
                            inv.quantity -= prod["count"]
                            inv.save()
                        else:
                            # not enough stocks, add notification
                            Notifications.objects.create(
                                title="Inventory Update Failed",
                                message=f"Inventory update failed for {inv.product.name}. Items left: {inv.quantity}.",
                                user=request.user,
                            )

                            return JsonResponse(
                                {
                                    "status": "error",
                                    "message": f"Not enough inventory quantity for {inv.product.name}. Please adjust the inventory before proceeding.",
                                }
                            )
            # Create the sale items
            sale_items = []
            for prod in prods:
                product = Product.objects.get(id=prod["id"])
                sale_item = SaleItem(
                    product=product,
                    quantity=prod["count"],
                )
                sale_item.save()
                sale_items.append(sale_item)
            # sale details
            sale_detail = SaleDetail(sale=sale)
            sale_detail.save()
            sale_detail.items.set(sale_items)

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Sale created successfully!",
                    "sale_id": sale.id,
                }
            )
    elif request.method == "GET":
        return render(request, "sales/sales_add.html", context=context)
    else:
        # method isn't allowed
        return JsonResponse({"message": "Method not allowed"}, status=405)


@login_required(login_url="/users/login/")
def sales_details_view(request: HttpRequest, sale_id: str) -> HttpResponse:
    """
    Args:
        request: HttpRequest
        sale_id: ID of the sale to view
    """
    try:
        # Get the sale
        sale = Sale.objects.get(id=sale_id)

        # Get the sale details
        details = SaleDetail.objects.filter(sale=sale).first()

        context = {
            "sale": sale,
            "details": details,
        }
        return render(request, "sales/sales_details.html", context=context)
    except Exception as e:
        messages.success(
            request, "There was an error getting the sale!", extra_tags="danger"
        )
        return redirect("sales:sales_list")


@login_required(login_url="/users/login/")
def receipt_pdf_view(request: HttpRequest, sale_id: str) -> HttpResponse:
    """
    Args:
        request: HttpRequest
        sale_id: ID of the sale to view the receipt
    """
    logo_path = "static/img/kra_logo.png"

    logo_img = Image.open(open(logo_path, "rb"))
    logo_img = logo_img.resize((50, 50))
    logo_stream = BytesIO()
    logo_img.save(logo_stream, format="PNG")
    logo_value = logo_stream.getvalue()
    logo_base64 = base64.b64encode(logo_value).decode("utf-8")

    # Get the sale
    sale = Sale.objects.get(id=sale_id)

    # Get the company details
    company = Company.objects.first()

    if company:
        company = company.to_dict()
    else:
        company = None

    # Get the sale details
    details = SaleDetail.objects.filter(sale=sale).first()
    items = []

    for item in details.items.all():
        product = item.product
        items.append(
            {
                "name": product.name,
                "quantity": item.quantity,
                "price": product.price,
                "total": item.total(),
            }
        )

    template = get_template("sales/sales_receipt_pdf.html")
    context = {
        "sale": sale,
        "company": company,
        "logo": logo_base64,
        "items": items,
    }
    # check if the sale has been printed
    if not sale.receipt_is_printed:
        context["printed"] = False
        sale.receipt_is_printed = True
        sale.save()
    else:
        context["printed"] = True

    qrcode_details = sale.to_json()

    qr = qrcode.make(qrcode_details, box_size=2.5)
    qr_image = qr.get_image()
    stream = BytesIO()
    qr_image.save(stream, format="PNG")
    qr_image_data = stream.getvalue()

    qr_image_base64 = base64.b64encode(qr_image_data).decode("utf-8")

    context["qr_code"] = qr_image_base64

    html_template = template.render(context)

    # CSS Boostrap
    css_url = os.path.join(
        settings.BASE_DIR, "static/css/receipt_pdf/bootstrap.min.css"
    )

    # Create the pdf
    pdf = HTML(
        string=html_template,
    ).write_pdf(
        stylesheets=[CSS(css_url)],
    )

    return HttpResponse(pdf, content_type="application/pdf")


def kra_logo(request: HttpRequest) -> FileResponse:
    logo = "static/img/kra_logo.png"
    return FileResponse(open(logo, "rb"), content_type="image/png")


def watermark(request: HttpRequest) -> FileResponse:
    mark = "static/img/mark.png"
    return FileResponse(open(mark, "rb"), content_type="image/png")
