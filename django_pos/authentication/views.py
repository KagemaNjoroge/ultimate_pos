from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from .forms import SignUpForm
from .serializers import (
    CustomUserSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
)
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import user_passes_test


from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


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


@api_view(["GET"])
@permission_classes([AllowAny])
def logout_api_view(request: HttpRequest) -> HttpResponse:
    """
    API endpoint to log out a user.
    """
    logout(request)
    return Response({"message": "Logged out successfully"}, status=200)


@login_required()
@require_http_methods(["GET"])
@user_passes_test(is_admin_user)
def index(request: HttpRequest) -> HttpResponse:
    # for users management
    users = User.objects.all()
    return render(request, "accounts/index.html", {"users": users})


@api_view(["GET", "POST"])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def profile(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.accepted_renderer.format == "html":
            # available roles
            roles = User.role.field.choices
            return render(request, "accounts/profile.html", {"roles": roles})
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
