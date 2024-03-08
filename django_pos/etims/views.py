from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def etims(request: HttpRequest) -> HttpResponse:
    return render(request, "etims/etims.html", {"active_icon": "etims"})
