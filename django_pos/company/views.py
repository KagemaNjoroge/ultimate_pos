from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Branch, Company
from .serializers import CompanySerializer
from rest_framework.views import APIView
from rest_framework.response import Response


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
def index(request: HttpRequest) -> HttpResponse:
    company = Company.objects.first()

    if company != None:
        company = company.to_dict()

    return render(
        request,
        template_name="company/settings.html",
        context={"active_icon": "settings", "company": company},
    )


@login_required(login_url="/users/login/")
def branches(request: HttpRequest) -> HttpResponse:
    all_branches = Branch.objects.all()
    return render(request, "company/branches.html", {"branches": all_branches})


@login_required(login_url="/users/login/")
def invoice_design(request: HttpRequest) -> HttpResponse:
    return render(request, "company/invoice_design.html")
