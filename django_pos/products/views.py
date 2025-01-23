import openpyxl
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from company.models import Company
from rest_framework.decorators import api_view, renderer_classes
from inventory.models import Inventory
from .models import Category, Product
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser


@login_required(login_url="/users/login/")
def categories_list_view(request: HttpRequest) -> HttpResponse:
    context = {
        "categories": Category.objects.all(),
    }
    return render(request, "products/categories.html", context=context)


@login_required(login_url="/users/login/")
@api_view(["POST", "GET"])
@renderer_classes([JSONRenderer, TemplateHTMLRenderer])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def categories_add_view(request: Request) -> Response:

    if request.method == "GET":
        context = {
            "category_status": Category.status.field.choices,
        }
        if request.accepted_renderer.format == "html":
            return render(request, "products/categories_add.html", context=context)
        else:
            return Response(context, status=200)

    if request.method == "POST":
        # Save the POST arguments
        data = request.data

        attributes = {
            "name": data.get("name", ""),
            "status": data.get("status", ""),
            "description": data.get("description", ""),
        }

        serializer = CategorySerializer(data=attributes)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Category created successfully!"}
            )
        else:
            return Response(
                {"status": "error", "message": serializer.errors}, status=400
            )


@login_required(login_url="/users/login/")
@api_view(["POST", "GET"])
def categories_update_view(request: HttpRequest, category_id: str) -> HttpResponse:
    if request.method == "GET":

        category = get_object_or_404(Category, id=category_id)
        serializer = CategorySerializer(instance=category)
        context = {
            "category_status": Category.status.field.choices,
            "category": serializer.data,
        }

        return render(request, "products/categories_update.html", context)

    if request.method == "POST":
        try:

            data = request.data

            attributes = {
                "name": data.get("name", ""),
                "status": data.get("status", ""),
                "description": data.get("description", ""),
            }
            Category.objects.filter(id=category_id).update(**attributes)

            return Response(
                {"status": "success", "message": "Category updated successfully!"}
            )

        except Exception as e:
            return Response({"status": "error", "message": str(e)})


@login_required(login_url="/users/login/")
def categories_delete_view(request: HttpRequest, category_id: str) -> HttpResponse:
    """
    Args:
        request: HttpRequest
        category_id : The category's ID that will be deleted
    """
    try:
        # Get the category to delete
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(
            request, "¡Category: " + category.name + " deleted!", extra_tags="success"
        )
        return redirect("products:categories_list")
    except Exception as e:
        messages.success(
            request,
            "That category cannot be deleted as some products are associated with it",
            extra_tags="danger",
        )

        return redirect("products:categories_list")


@login_required(login_url="/users/login/")
def products_list_view(request: HttpRequest) -> HttpResponse:
    context = {"products": Product.objects.all()}
    company = Company.objects.first()
    if company:
        context["currency_symbol"] = company.currency_symbol
    else:
        context["currency_symbol"] = "Ksh"

    return render(request, "products/products.html", context=context)


@login_required(login_url="/users/login/")
def products_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # Save the POST arguments
        data = request.POST

        try:
            track_inventory = data["track_inventory"]
        except:
            track_inventory = "off"
        if track_inventory == "on":
            track_inventory = True
        else:
            track_inventory = False

        attributes = {
            "name": data["name"],
            "status": data["state"],
            "description": data["description"],
            "category": data["category"],
            "price": data["price"],
            "track_inventory": track_inventory,
        }

        serializer = ProductSerializer(data=attributes)
        if serializer.is_valid():
            serializer.save()
            if track_inventory:
                inventory = Inventory.objects.create(
                    product=serializer.instance, quantity=1
                )
                inventory.save()
            return JsonResponse(
                {"status": "success", "message": "Product created successfully!"}
            )
        else:
            return JsonResponse(
                {"status": "error", "message": serializer.errors}, status=400
            )

    elif request.method == "GET":
        context = {
            "product_status": Product.status.field.choices,
            "categories": Category.objects.all().filter(status="ACTIVE"),
        }
        return render(request, "products/products_add.html", context=context)

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@login_required(login_url="/users/login/")
@api_view(["POST", "GET"])
@renderer_classes([JSONRenderer, TemplateHTMLRenderer])
def products_update_view(request, product_id: str):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "GET":
        context = {
            "product_status": Product.status.field.choices,
            "product": product,
            "categories": [
                category.to_json()
                for category in Category.objects.all().filter(status="ACTIVE")
            ],
        }

        # Check if the request is for HTML or JSON
        if request.accepted_renderer.format == "html":
            return render(request, "products/products_update.html", context)
        else:
            return Response(context)

    if request.method == "POST":
        serializer = ProductSerializer(
            data=request.data, instance=product, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"status": "success", "message": "Product updated successfully!"}
            )
        else:
            return Response(
                data={"status": "error", "message": serializer.errors}, status=400
            )


@login_required(login_url="/users/login/")
def products_delete_view(request: HttpRequest, product_id: str) -> HttpResponse:
    """
    Args:
        request:HttpRequest
        product_id : The product's ID that will be deleted
    """
    product = get_object_or_404(Product, id=product_id)
    try:
        # TODO: Migrate response to JsonResponse
        product.delete()
        messages.success(
            request, "¡Product: " + product.name + " deleted!", extra_tags="success"
        )
        return redirect("products:products_list")
    except Exception as e:
        messages.success(
            request,
            "An error occurred while deleting that product. It is already associated with a sale record.",
            extra_tags="danger",
        )

        return redirect("products:products_list")


def is_ajax(request: HttpRequest) -> bool:
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


@login_required(login_url="/users/login/")
@api_view(["GET"])
def get_products_ajax_view(request: Request) -> Response:
    query = request.query_params.dict().get("term", "")
    products = Product.objects.filter(name__icontains=query)
    serializer = ProductSerializer(products, many=True)
    return Response(data=serializer.data, status=200)


@login_required(login_url="/users/login/")
def upload_excel_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":

        categories = Category.objects.all()
        context = {"categories": categories}
        return render(request, "products/upload_csv_excel.html", context=context)
    elif request.method == "POST":

        try:
            excel_file = request.FILES["excel_file"]
            if not excel_file.name.endswith(".xlsx"):
                messages.error(request, "File is not Excel type")
                return redirect("products:upload_excel")
            # if the file is too large, return
            if excel_file.multiple_chunks():
                messages.error(
                    request,
                    "Uploaded file is too big (%.2f MB)."
                    % (excel_file.size / (1000 * 1000),),
                    extra_tags="warning",
                )
                return redirect("products:upload_excel")

            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb.active
            for row in worksheet.iter_rows(
                min_row=2, max_row=worksheet.max_row, min_col=1, max_col=6
            ):

                # Coca Cola A nice soft drink 250 1 1

                product = Product()
                product.name = row[0].value
                product.description = row[1].value
                product.price = row[2].value
                if row[3].value == 1:
                    product.track_inventory = True
                else:
                    product.track_inventory = False
                if row[5].value == 1:
                    product.status = "ACTIVE"
                else:
                    product.status = "INACTIVE"
                categ = row[4].value
                try:
                    category = Category.objects.get(id=categ)
                except Exception as e:
                    category = Category.objects.first()
                product.category = category
                product.save()
                # add to if specified
                if product.track_inventory:
                    inv = Inventory.objects.filter(product=product)
                    if inv.exists():
                        inv = inv.first()
                        inv.quantity += 1
                        inv.save()
                    else:
                        inv = Inventory.objects.create(product=product, quantity=1)
                        inv.save()

                return JsonResponse(
                    {
                        "status": "success",
                        "message": "Processing complete. All products have been added to the database.",
                    },
                    safe=True,
                )
        except Exception as e:

            return JsonResponse(
                {
                    "status": "error",
                    "message": "An error occurred while processing the file. The file did not meet the required format or it is corrupted.",
                }
            )


@login_required(login_url="/users/login/")
def download_template(request: HttpRequest):
    file_path = "static/upload_products.xltx"
    with open(file_path, "rb") as file:
        response = HttpResponse(file, content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="upload_products.xltx"'
        return response


@login_required(login_url="/users/login/")
def product_detail_view(request: HttpRequest, product_id: str) -> HttpResponse:
    product = get_object_or_404(Product, id=product_id)
    context = {
        "product": product,
    }
    return render(request, "products/product_details.html", context=context)
