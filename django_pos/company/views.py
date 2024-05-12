import os
from django.http import HttpRequest, HttpResponse, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404, render
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.datastructures import MultiValueDict

from company.utils.subscription import check_subscription_in_firebase
from .models import Company, Subscription
from django.views import View
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials


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
        print(request.FILES)

        # Create a QueryDict object
        put_data = QueryDict(request.body, encoding=request._encoding)

        # Create a MultiValueDict for the files
        put_files = MultiValueDict({"logo": []})

        # Check if there's a file in the request
        if "logo" in request.FILES:
            # Wrap the file in an InMemoryUploadedFile object
            logo_file = InMemoryUploadedFile(
                request.FILES["logo"].file,  # file
                "logo",  # field_name
                request.FILES["logo"].name,  # file name
                request.FILES["logo"].content_type,  # content type
                request.FILES["logo"].size,  # file size
                request.FILES["logo"].charset,  # charset
            )

            # Add the file to put_files
            put_files["logo"].append(logo_file)

        # Now you can use put_data and put_files like request.POST and request.FILES
        # print(put_data.dict())
        # print(put_files)

        try:

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

    def post(self, request: HttpRequest):
        data = request.POST.dict()
        logo = request.FILES.get("logo")

        if logo:
            data["logo"] = logo

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
            print(e)
            return JsonResponse(
                {"message": f"Error: {e}", "status": "Failed"}, status=500
            )


def index(request: HttpRequest) -> HttpResponse:
    company = Company.objects.first()

    if company != None:
        company = company.to_dict()

    return render(
        request,
        template_name="company/settings.html",
        context={"active_icon": "settings", "company": company},
    )


def test_firebase(request: HttpRequest) -> HttpResponse:

    subs = Subscription.objects.first()
    # print(save_subscription_to_firebase(subs))
    print(check_subscription_in_firebase(subs))

    return HttpResponse("Firebase test successful")
