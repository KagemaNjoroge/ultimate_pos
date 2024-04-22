from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "reports/index.html", context={"active_icon": "reports"})
