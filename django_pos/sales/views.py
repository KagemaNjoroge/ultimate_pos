from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django_pos.wsgi import *
from customers.models import Customer
from pos.models import Notifications
from datetime import datetime, timedelta
from products.models import Product
from .models import Sale, SaleItem
import json
from company.models import Company
from inventory.models import Inventory
from .invoice import create_invoice_pdf
from .serializers import SaleSerializer
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.http import require_http_methods


class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


def is_ajax(request: HttpRequest) -> bool:
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


@login_required()
def sales_list_view(request: HttpRequest) -> HttpResponse:
    sales = Sale.objects.all().order_by("-date_added")
    context = {"sales": sales}
    return render(request, "sales/sales.html", context=context)


@login_required()
@require_http_methods(["GET", "POST"])
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

            for prod in prods:
                product = Product.objects.get(id=prod["id"])
                sale_item = SaleItem(
                    product=product,
                    quantity=prod["count"],
                    sale=sale,
                )
                sale_item.save()

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Sale created successfully!",
                    "sale_id": sale.id,
                }
            )
    elif request.method == "GET":
        return render(request, "sales/sales_add.html", context=context)


@login_required()
def sales_details_view(request: HttpRequest, sale_id: str) -> HttpResponse:
    sale = get_object_or_404(Sale, id=sale_id)
    # Get the sale details
    items = SaleItem.objects.filter(sale=sale)
    context = {
        "sale": sale,
        "items": items,
        "items_count": items.count() if items else 0,
    }
    return render(request, "sales/sales_details.html", context=context)


@login_required()
@require_http_methods(["GET"])
def receipt_pdf_view(request: HttpRequest, sale_id: int) -> HttpResponse:
    sale = get_object_or_404(Sale, id=sale_id)
    customer = sale.customer
    # Get the company details
    company = Company.objects.first()

    if company:
        company_info = company.to_dict()
        # TODO: Handle case where company info is incomplete or missing
    else:
        company_info = {
            "name": "TomorrowAI",
            "address": "123 Business Street, Nairobi, Kenya",
            "phone": "+1 (123) 456-7890",
            "email": "info@ultimatepos.com",
            "tax_id": "TAX-123456789",
            "website": "www.ultimatepos.com",
            "registration_number": "REG-987654321",
        }

    # Get the sale details
    details = SaleItem.objects.filter(sale=sale)
    items = []

    for item in details:
        product = item.product
        items.append(
            {
                "product_name": product.name,
                "quantity": item.quantity,
                "unit_price": product.price,
                "total": item.total(),
                "description": product.description or "",
                "sku": product.get_sku or "N/A",
            }
        )

    # Determine payment status
    if sale.amount_payed >= sale.grand_total:
        payment_status = "Paid"
    elif sale.amount_payed > 0:
        payment_status = "Partial"
    else:
        payment_status = "Unpaid"

    invoice_data = {
        "company_info": {
            "name": company_info.get("name", "TomorrowAI"),
            "address": company_info.get(
                "address", "123 Business Street, Nairobi, Kenya"
            ),
            "phone": company_info.get("phone", "+1 (123) 456-7890"),
            "email": company_info.get("email", "info@ultimatepos.com"),
            "tax_id": company_info.get("tax_id", "TAX-123456789"),
            "website": company_info.get("website", "www.ultimatepos.com"),
            "registration_number": company_info.get(
                "registration_number", "REG-987654321"
            ),
        },
        "customer_info": {
            "name": customer.get_full_name(),
            "address": customer.address or "",
            "phone": customer.phone or "",
            "email": customer.email or "",
            "customer_id": f"CUST-{customer.id}",
            "tax_number": customer.tax_number or "",
        },
        "invoice_info": {
            "invoice_number": f"INV-{datetime.now().strftime('%Y')}-{sale_id.zfill(4)}",
            "date": f"{sale.date_added.strftime('%Y-%m-%d')}",
            "due_date": f"{(sale.date_added + timedelta(days=30)).strftime('%Y-%m-%d')}",
            "reference": f"SALE-{sale_id}",
            "payment_method": "Cash/Card",
        },
        "items": items,
        "totals": {
            "subtotal": float(sale.sub_total),
            "tax": float(sale.tax_amount),
            "discount": float(sale.discount) if sale.discount else 0,
            "total": float(sale.grand_total),
            "paid_amount": float(sale.amount_payed),
            "balance_due": float(sale.grand_total - sale.amount_payed),
        },
        "payment_status": payment_status,
        # "notes": "Thank you for your purchase. We appreciate your business.",
        # "payment_instructions": "For questions regarding this invoice, please contact our customer service.",
        # "qr_data": f"https://pay.ultimatepos.com/inv-{sale_id}",
    }

    # Generate the PDF invoice using the create_invoice_pdf function
    pdf_content = create_invoice_pdf(invoice_data)

    # Return the PDF as an HTTP response
    return HttpResponse(pdf_content, content_type="application/pdf")
