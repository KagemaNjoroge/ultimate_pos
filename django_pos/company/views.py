import json
from re import T
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Company
from django.views import View


class CompanyView(View):
    def get(self, request: HttpRequest, id: int = None):

        if id:
            company = get_object_or_404(Company, pk=id)
            return JsonResponse(company.to_dict(), safe=False)
        else:
            company = Company.objects.first()
            if company == None:
                return JsonResponse({}, safe=True)
            return JsonResponse(company.to_dict(), safe=False)

    def delete(self, request: HttpRequest, id: int):
        company = get_object_or_404(Company, pk=id)
        try:
            company.delete()
            return JsonResponse({"message": "Company deleted successfully"})
        except Exception as e:
            return JsonResponse(
                {"message": f"Error deleting company: {str(e)}"}, status=500
            )

    def put(self, request: HttpRequest, id: int):
        company = get_object_or_404(Company, pk=id)
        data = json.loads(request.body)
        try:
            for key, value in data.items():
                setattr(company, key, value)
            company.save()
            return JsonResponse(
                {
                    "message": "Company updated successfully",
                    "company": company.to_dict(),
                    "status": "Okay",
                },
                status=200,
                safe=False,
            )
        except Exception as e:
            return JsonResponse(
                {"message": f"Error: {e}", "status": "Failed"}, status=500
            )

    def post(request: HttpRequest):
        data = json.loads(request.body)
        try:
            company = Company(**data)
            company.save()
            return JsonResponse(
                {
                    "message": "Company added successfully",
                    "company": company.to_dict(),
                    "status": "Okay",
                },
                status=201,
                safe=False,
            )
        except Exception as e:
            return JsonResponse(
                {"message": f"Error: {e}", "status": "Failed"}, status=500
            )


def index(request: HttpRequest) -> HttpResponse:
    company = Company.objects.first()

    if company == None:
        company = {}
    else:
        company = company.to_dict()

    return render(
        request,
        template_name="company/settings.html",
        context={"active_icon": "settings", "company": company},
    )
