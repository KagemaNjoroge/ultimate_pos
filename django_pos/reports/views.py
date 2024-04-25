from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from pos.views import check_subscription
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="/accounts/login/")
@check_subscription
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "reports/index.html", context={"active_icon": "reports"})
