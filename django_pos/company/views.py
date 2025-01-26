from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Branch, Company
from .serializers import CompanySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django_countries import countries


@require_http_methods(["GET"])
def set_up_company(request):
    company = Company.objects.first()
    context = {
        "company": company,
        "countries": countries,
    }
    return render(request, "company/setup.html", context)


class CompanyView(APIView):
    def get(self, request, id: int = None):

        if id:
            company = get_object_or_404(Company, pk=id)
            return Response(company.to_dict())
        else:
            company = Company.objects.first()
            if company == None:
                return Response({})
            return Response(company.to_dict())

    def delete(self, request, id: int):
        company = get_object_or_404(Company, pk=id)
        try:
            company.delete()
            return Response({"message": "Company deleted successfully"})
        except Exception as e:
            return Response(
                {"message": f"Error deleting company: {str(e)}"}, status=400
            )

    def put(self, request, id: int):
        company = get_object_or_404(Company, pk=id)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
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
