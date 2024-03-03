from re import I
import stat
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, FileResponse
from django.shortcuts import render, redirect
from django_pos.wsgi import *
from django_pos import settings
from django.template.loader import get_template
from customers.models import Customer
from products.models import Product
from weasyprint import HTML, CSS
from .models import Sale, SaleDetail
import json
from company.models import Company
import qrcode
from io import BytesIO
import base64
from PIL import Image
from inventory.models import Inventory

# TODO separate `is_ajax` function to a separate file to avoid repetition


def is_ajax(request: HttpRequest) -> bool:
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


@login_required(login_url="/accounts/login/")
def sales_list_view(request: HttpRequest) -> HttpResponse:
    context = {"active_icon": "sales", "sales": Sale.objects.all()}
    return render(request, "sales/sales.html", context=context)


@login_required(login_url="/accounts/login/")
def sales_add_view(request: HttpRequest) -> HttpResponse:
    context = {
        "active_icon": "sales",
        "customers": [c.to_select2() for c in Customer.objects.all()],
    }

    if request.method == "POST":
        if is_ajax(request=request):
            # Save the POST arguments
            data = json.load(request)
            # {'customer': '3', 'sub_total': '80000', 'tax_percentage': '0', 'tax_amount': '0', 'grand_total': '80000', 'amount_payed': '80000', 'amount_change': 0, 'products': [{'id': 2, 'name': 'Hp Elitebook G5', 'price': 80000, 'count': 1, 'total': 80000, 'total_product': 1}
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
                        inv.quantity -= prod["count"]
                        inv.save()
            detail = SaleDetail(sale=sale)
            detail.save()
            detail.products.set(products)
            messages.success(request, "Sale added successfully!", extra_tags="success")
            return redirect("sales:sales_add")

    return render(request, "sales/sales_add.html", context=context)


@login_required(login_url="/accounts/login/")
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
        details = SaleDetail.objects.filter(sale=sale)

        context = {
            "active_icon": "sales",
            "sale": sale,
            "details": details,
        }
        return render(request, "sales/sales_details.html", context=context)
    except Exception as e:
        messages.success(
            request, "There was an error getting the sale!", extra_tags="danger"
        )
        print(e)
        return redirect("sales:sales_list")


@login_required(login_url="/accounts/login/")
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
    details = SaleDetail.objects.filter(sale=sale)
    prods = details.first().products.all()
    product_data = []
    for prod in prods:
        print(details.first().get_specific_product_count(prod.id))
        product_data.append(
            {
                "id": prod.id,
                "name": prod.name,
                "price": prod.price,
                "count": details.first().get_specific_product_count(prod.id),
                "total": details.first().get_specific_product_count(prod.id)
                * prod.price,
            }
        )
    # product counts

    print(product_data)

    template = get_template("sales/sales_receipt_pdf.html")
    context = {
        "sale": sale,
        "company": company,
        "logo": logo_base64,
        "product_data": product_data,
        # 0701575348
    }

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
    pdf = HTML(string=html_template).write_pdf(stylesheets=[CSS(css_url)])

    return HttpResponse(pdf, content_type="application/pdf")


def kra_logo(request: HttpRequest) -> HttpResponse:
    logo = "static/img/kra_logo.png"

    return FileResponse(open(logo, "rb"), content_type="image/png")
