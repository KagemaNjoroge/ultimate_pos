from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="/users/login/")
def etims(request: HttpRequest) -> HttpResponse:
    return render(request, "etims/etims.html", {"active_icon": "etims"})
