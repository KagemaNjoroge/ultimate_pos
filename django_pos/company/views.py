from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Branch, Company
from .serializers import CompanySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CompanySerializer


@require_http_methods(["GET", "POST"])
def set_up_company(request):
    if request.method == "GET":
        # Check if company already exists and redirect if so
        existing_company = Company.objects.first()
        if existing_company:
            messages.info(
                request, "Company has already been set up. You can edit settings below."
            )
            return redirect("company:settings")

        return render(request, template_name="company/setup.html")
    else:
        try:
            # Check if company already exists
            if Company.objects.exists():
                messages.info(request, "Company setup has already been completed.")
                return redirect("company:settings")

            # Extract form data
            company_name = request.POST.get("company_name", "").strip()
            phone_number = request.POST.get("phone_number", "").strip()
            email = request.POST.get("email", "").strip()
            city = request.POST.get("city", "").strip()
            address = request.POST.get("address", "").strip()
            currency_symbol = request.POST.get("currency_symbol", "KES").strip()
            tax_registration_number = request.POST.get(
                "tax_registration_number", ""
            ).strip()
            logo = request.FILES.get("logo")

            # Validate required fields
            if not company_name:
                messages.error(request, "Company name is required.")
                return render(request, template_name="company/setup.html")

            # Validate email format if provided
            if email:
                import re

                email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
                if not re.match(email_pattern, email):
                    messages.error(request, "Please enter a valid email address.")
                    return render(request, template_name="company/setup.html")

            # Validate KRA PIN format if provided
            # if tax_registration_number:
            #     if len(tax_registration_number) > 11:
            #         messages.error(request, "KRA PIN cannot exceed 11 characters.")
            #         return render(request, template_name="company/setup.html")

            #     # Basic KRA PIN format validation (alphanumeric)
            #     if not re.match(r"^[A-Z0-9]+$", tax_registration_number.upper()):
            #         messages.error(
            #             request, "KRA PIN should only contain letters and numbers."
            #         )
            #         return render(request, template_name="company/setup.html")

            # Create company instance
            company = Company(
                company_name=company_name,
                phone_number=phone_number if phone_number else None,
                email=email if email else None,
                city=city if city else None,
                address=address if address else None,
                currency_symbol=currency_symbol,
                tax_registration_number=(
                    tax_registration_number.upper() if tax_registration_number else None
                ),
            )

            # Handle logo upload
            if logo:
                # Validate file type
                allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
                if logo.content_type not in allowed_types:
                    messages.error(
                        request,
                        "Please upload a valid image file (JPG, PNG, GIF, WebP).",
                    )
                    return render(request, template_name="company/setup.html")

                # Validate file size (max 5MB)
                if logo.size > 5 * 1024 * 1024:
                    messages.error(request, "Logo file size cannot exceed 5MB.")
                    return render(request, template_name="company/setup.html")

                company.logo = logo

            # Save the company
            company.save()

            messages.success(
                request, f'Company "{company_name}" has been set up successfully!'
            )
            return redirect("company:settings")

        except Exception as e:
            messages.error(
                request, f"An error occurred while setting up the company: {str(e)}"
            )
            return render(request, template_name="company/setup.html")


class CompanyView(APIView):
    def get(self, request, id: int):
        company = get_object_or_404(Company, pk=id)
        serialized_data = CompanySerializer(company).data
        return Response(serialized_data)

    def put(self, request, id: int):
        company = get_object_or_404(Company, pk=id)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@login_required(login_url="/users/login/")
@require_http_methods(["GET"])
def index(request: HttpRequest) -> HttpResponse:
    company = Company.objects.first()

    if not company:
        return redirect("company:setup")

    return render(
        request,
        template_name="company/settings.html",
        context={"company": company.to_dict()},
    )


@login_required(login_url="/users/login/")
@require_http_methods(["GET"])
def branches(request: HttpRequest) -> HttpResponse:
    all_branches = Branch.objects.all()
    return render(request, "company/branches.html", {"branches": all_branches})


@login_required(login_url="/users/login/")
@require_http_methods(["GET"])
def add_branch(request):
    company = Company.objects.first()

    return render(
        request,
        "company/add_branch.html",
        context={"company": company},
    )
