from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import JsonResponse

from company.utils.branch_utils import ensure_default_branch, set_current_branch
from .models import Branch, Company
from .serializers import CompanySerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CompanySerializer


@require_http_methods(["GET", "POST"])
@login_required()
def select_current_branch(request: HttpRequest) -> HttpResponse:
    """
    View to select the current branch for the user.
    """
    # Ensure there's at least one branch available
    ensure_default_branch()

    branches = Branch.objects.all()

    if request.method == "POST":
        branch_id = request.POST.get("branch_id")
        if branch_id:
            try:
                branch = Branch.objects.get(id=branch_id)

                # Use utility function to set current branch
                if set_current_branch(request, branch):
                    messages.success(
                        request,
                        f"Successfully switched to branch: {branch.branch_name}",
                    )

                    # Redirect to POS dashboard or appropriate page
                    return redirect("pos:index")
                else:
                    messages.error(request, "Failed to set current branch.")

            except Branch.DoesNotExist:
                messages.error(request, "Selected branch does not exist.")
                return render(
                    request, "company/select_branch.html", {"branches": branches}
                )
        else:
            messages.error(request, "Please select a branch to continue.")
            return render(request, "company/select_branch.html", {"branches": branches})

    # GET request - show branch selection page
    return render(request, "company/select_branch.html", {"branches": branches})


@require_http_methods(["GET", "POST"])
def set_up_company(request):
    if request.method == "GET":
        # Check if company already exists and redirect if so
        existing_company = Company.objects.first()
        if existing_company:
            messages.info(
                request=request,
                message="Company has already been set up. You can edit settings below.",
                extra_tags="info",
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


@login_required()
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


@login_required()
@require_http_methods(["GET"])
def branches(request: HttpRequest) -> HttpResponse:
    all_branches = Branch.objects.all()
    return render(request, "company/branches.html", {"branches": all_branches})


@login_required()
@require_http_methods(["GET"])
def add_branch(request):
    company = Company.objects.first()

    return render(
        request,
        "company/add_branch.html",
        context={"company": company},
    )


@login_required()
@require_http_methods(["POST"])
def switch_branch(request: HttpRequest) -> HttpResponse:
    """
    API endpoint to quickly switch branches via AJAX.
    """

    try:
        branch_id = request.POST.get("branch_id", None)
        if not branch_id:
            return JsonResponse({"success": False, "message": "Branch ID is required."})

        branch = Branch.objects.get(id=branch_id)

        if set_current_branch(request, branch):
            return JsonResponse(
                {
                    "success": True,
                    "message": f"Switched to {branch.branch_name}",
                    "branch": {
                        "id": branch.id,
                        "name": branch.branch_name,
                        "address": branch.address,
                        "phone": branch.phone_number,
                        "is_headquarter": branch.is_headquarter,
                    },
                }
            )
        else:
            return JsonResponse(
                {"success": False, "message": "Failed to switch branch."}
            )

    except Branch.DoesNotExist:
        return JsonResponse({"success": False, "message": "Branch not found."})
    except Exception as e:
        # Prevent exposing sensitive error details
        return JsonResponse({"success": False, "message": "Error"})
