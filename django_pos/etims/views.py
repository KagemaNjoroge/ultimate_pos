from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


@login_required(login_url="/users/login/")
@api_view(["GET"])
def get_etims_server_status(request) -> Response:
    # hardcoding the server address for now
    return Response({
        "status":"success",
    })


@login_required(login_url="/users/login/")
def etims(request: HttpRequest) -> HttpResponse:
    return render(request, "etims/etims.html", {"active_icon": "etims"})

