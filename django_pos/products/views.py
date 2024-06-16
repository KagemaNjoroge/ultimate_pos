import json

import openpyxl
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from company.models import Company
from inventory.models import Inventory
from pos.views import check_subscription
from .models import Category, Product


@login_required(login_url="/users/login/")
@check_subscription
def categories_list_view(request: HttpRequest) -> HttpResponse:
    context = {
        "active_icon": "products_categories",
        "categories": Category.objects.all(),
    }
    return render(request, "products/categories.html", context=context)


@login_required(login_url="/users/login/")
@check_subscription
def categories_add_view(request: HttpRequest) -> HttpResponse:
    context = {
        "active_icon": "products_categories",
        "category_status": Category.status.field.choices,
    }
    if request.method == "GET":
        return render(request, "products/categories_add.html", context=context)

    if request.method == "POST":
        # Save the POST arguments
        data = json.loads(request.body)

        attributes = {
            "name": data["name"],
            "status": data["status"],
            "description": data["description"],
        }

        # Check if a category with the same attributes exists
        if Category.objects.filter(**attributes).exists():
            return JsonResponse(
                {
                    "status": "error",
                    "message": "A category with those details already exists!",
                }
            )

        try:
            new_category = Category.objects.create(**attributes)
            new_category.save()
            return JsonResponse({"status": "success", "message": "Category created!"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        # method isn't allowed
        return HttpResponse(status=405)


@login_required(login_url="/users/login/")
@check_subscription
def categories_update_view(request: HttpRequest, category_id: str) -> HttpResponse:
    if request.method == "GET":
        category = get_object_or_404(Category, id=category_id)
        context = {
            "active_icon": "products_categories",
            "category_status": Category.status.field.choices,
            "category": category,
        }

        return render(request, "products/categories_update.html", context=context)

    if request.method == "POST":

        try:

            data = json.loads(request.body)

            attributes = {
                "name": data["name"],
                "status": data["status"],
                "description": data["description"],
            }
            Category.objects.filter(id=category_id).update(**attributes)

            return JsonResponse(
                {"status": "success", "message": "Category updated successfully!"}
            )

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        # method isn't allowed
        return HttpResponse(status=405)


@login_required(login_url="/users/login/")
@check_subscription
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
        print(e)
        return redirect("products:categories_list")


@login_required(login_url="/users/login/")
@check_subscription
def products_list_view(request: HttpRequest) -> HttpResponse:
    context = {"active_icon": "products", "products": Product.objects.all()}
    company = Company.objects.first()
    if company:
        context["currency_symbol"] = company.currency_symbol
    else:
        context["currency_symbol"] = "$"

    return render(request, "products/products.html", context=context)


@login_required(login_url="/users/login/")
@check_subscription
def products_add_view(request: HttpRequest) -> HttpResponse:
    context = {
        "active_icon": "products_categories",
        "product_status": Product.status.field.choices,
        "categories": Category.objects.all().filter(status="ACTIVE"),
    }

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
            "category": Category.objects.get(id=data["category"]),
            "price": data["price"],
            "track_inventory": track_inventory,
        }

        # Check if a product with the same attributes exists
        if Product.objects.filter(**attributes).exists():
            messages.error(request, "Product already exists!", extra_tags="warning")
            return redirect("products:products_add")

        try:
            # Create the product
            new_product = Product.objects.create(**attributes)

            # If it doesn't exist, save it
            new_product.save()
            # track inventory
            if track_inventory:
                # if inventory exists, update it
                inventory = Inventory.objects.filter(product=new_product)
                if inventory.exists():
                    inventory = inventory.first()
                    inventory.quantity += 1
                    inventory.save()
                else:
                    inventory = Inventory.objects.create(
                        product=new_product, quantity=1
                    )
                    inventory.save()

            messages.success(
                request,
                "Product: " + attributes["name"] + " created successfully!",
                extra_tags="success",
            )
            return redirect("products:products_list")
        except Exception as e:
            messages.success(
                request, "An error occurred, try again!", extra_tags="danger"
            )

            return redirect("products:products_add")

    return render(request, "products/products_add.html", context=context)


@login_required(login_url="/users/login/")
@check_subscription
def products_update_view(request: HttpRequest, product_id: str) -> HttpResponse:
    if request.method == "GET":

        product = get_object_or_404(Product, id=product_id)

        context = {
            "active_icon": "products",
            "product_status": Product.status.field.choices,
            "product": product,
            "categories": Category.objects.all(),
        }
        return render(request, "products/products_update.html", context=context)

    elif request.method == "POST":

        data = request.body
        data = json.loads(data)

        product = Product.objects.get(id=product_id)
        product.name = data["name"]
        product.description = data["description"]
        product.price = data["price"]
        product.status = data["state"]
        product.category = Category.objects.get(id=data["category"])
        product.track_inventory = data["track_inventory"]
        product.save()

        if product.track_inventory:
            inventory = Inventory.objects.filter(product=product)
            if inventory.exists():
                inventory = inventory.first()
                inventory.quantity = 1
                inventory.save()
            else:
                inventory = Inventory.objects.create(product=product, quantity=1)
                inventory.save()
        return JsonResponse({"message": "Product updated successfully"}, status=200)
    else:  # not allowed
        return JsonResponse({"message": "Method not allowed"}, status=405)


@login_required(login_url="/users/login/")
@check_subscription
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
@check_subscription
def get_products_ajax_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        if is_ajax(request=request):
            data = []

            products = Product.objects.filter(name__icontains=request.POST["term"])
            for product in products[0:10]:
                item = product.to_json()
                data.append(item)

            return JsonResponse(data, safe=False)


@login_required(login_url="/users/login/")
@check_subscription
def upload_excel_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":

        categories = Category.objects.all()
        context = {"active_icon": "products", "categories": categories}
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
@check_subscription
def product_detail_view(request: HttpRequest, product_id: str) -> HttpResponse:
    product = get_object_or_404(Product, id=product_id)
    context = {
        "active_icon": "products",
        "product": product,
    }
    return render(request, "products/product_details.html", context=context)
