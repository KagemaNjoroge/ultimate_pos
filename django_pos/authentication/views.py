from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import (
    CustomUserSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
)
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods


from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


User = get_user_model()


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


@require_http_methods(["GET"])
def no_permission_view(request: HttpRequest) -> HttpResponse:
    return Response(
        {"detail": "You do not have permission to access this resource."},
        status=403,
    )


@api_view(["GET", "POST"])
def profile(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        user = User.objects.get(pk=request.user.id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=200)
    elif request.method == "POST":
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Profile updated successfully", "status": "Ok"},
                status=200,
            )
        else:
            return Response(
                data={
                    "errors": serializer.errors,
                    "status": "error",
                    "detail": "An error occurred",
                },
                status=400,
            )
