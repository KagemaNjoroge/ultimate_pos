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


from django.contrib.auth.decorators import user_passes_test


def is_admin_user(user):
    return user.is_superuser  # or user.is_superuser


User = get_user_model()


@require_http_methods(["GET"])
@login_required()
def no_permission_view(request: HttpRequest) -> HttpResponse:
    user_permissions = request.user.permissions.all()

    return render(
        request=request,
        template_name="accounts/no_permission.html",
        status=403,
        context={
            "permissions": user_permissions,
        },
    )


@require_http_methods(["GET", "POST"])
@login_required()
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("authentication:login")


@login_required()
@require_http_methods(["GET"])
@user_passes_test(is_admin_user)
def index(request: HttpRequest) -> HttpResponse:
    # for users management
    users = User.objects.all()
    return render(request, "accounts/index.html", {"users": users})


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


@require_http_methods(["GET", "POST"])
@user_passes_test(is_admin_user)
@login_required()
def register_user(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {"message": "User registered successfully", "status": "success"},
                status=201,
            )
        else:
            return JsonResponse(
                {
                    "message": "Error registering user",
                    "status": "error",
                    "errors": form.errors,
                },
                status=400,
            )

    elif request.method == "GET":
        return render(
            request,
            "accounts/register.html",
        )
