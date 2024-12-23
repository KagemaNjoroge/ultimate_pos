from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


@require_http_methods(["POST"])
@login_required(login_url="/users/login/")
@csrf_exempt
def chat(request: HttpRequest):
    return JsonResponse(data={"status": "Under maintenance"})
