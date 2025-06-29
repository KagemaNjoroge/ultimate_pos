import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .forms import SignUpForm
from .serializers import CustomUserSerializer
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.utils.http import url_has_allowed_host_and_scheme

User = get_user_model()


def logout_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        logout(request)
        return redirect("/login/")
    else:
        return redirect("/login/")


@login_required()
def index(request: HttpRequest) -> HttpResponse:
    # for users management
    users = User.objects.all()
    return render(request, "accounts/index.html", {"users": users})


@login_required()
@api_view(["GET", "POST"])
def logout_view(request) -> Response:
    if request.user.is_authenticated:
        logout(request)
        return redirect("/login/")
    else:
        return redirect("/login/")


@login_required()
@api_view(["GET", "POST"])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def profile(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.accepted_renderer.format == "html":
            return render(request, "accounts/profile.html")
        else:
            user = User.objects.get(pk=request.user.id)
            serializer = CustomUserSerializer(user)
            return Response(
                serializer.data, status=200, template_name="accounts/profile.html"
            )
    elif request.method == "POST":
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Profile updated successfully", "status": "Ok"},
                status=200,
                template_name="accounts/profile.html",
            )
        return Response(
            data={
                "errors": serializer.errors,
                "status": "error",
                "message": "An error occurred",
            },
            status=400,
            template_name="accounts/profile.html",
        )


@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
    next_url = request.GET.get("next", "/")
    # Ensure next_url is safe
    if (
        not url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        )
        or next_url.startswith("//")
        or "\\" in next_url
    ):
        # Default to home page if validation fails:
        next_url = "/"
    if request.user.is_authenticated:
        return redirect(next_url)
    else:

        if request.method == "GET":
            return render(request, "accounts/signin.html", {"next": next_url})
        elif request.method == "POST":

            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return JsonResponse({"message": "success", "next": next_url})
            else:
                return JsonResponse(
                    {"message": "Invalid email or password!", "status": "error"},
                    status=401,
                )


def register_user(request: HttpRequest) -> HttpResponse:
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            authenticate(username=username, password=raw_password)
            return redirect("/login/")
        # TODO: Return error message as json response

    elif request.method == "GET":
        return render(
            request,
            "accounts/register.html",
            {"msg": msg, "success": success},
        )
    else:
        # not allowed
        return JsonResponse({"message": "Invalid request method"}, status=405)
