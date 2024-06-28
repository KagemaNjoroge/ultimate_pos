import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .forms import SignUpForm
from .serializers import CustomUserSerializer

# get_user_model
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required(login_url="/users/login/")
def index(request: HttpRequest) -> HttpResponse:
    # for users management
    users = User.objects.all()
    return render(request, "accounts/index.html", {"users": users})


@login_required(login_url="/users/login/")
@api_view(["GET", "POST"])
def logout_view(request) -> Response:
    if request.method == "POST":
        logout(request)
        return Response({"message": "success"})
    else:
        return render(request, "accounts/logout.html")


@login_required(login_url="/users/login/")
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


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("/")
    else:

        if request.method == "GET":
            return render(request, "accounts/signin.html")
        elif request.method == "POST":
            print(request.body)
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                try:
                    send_mail(
                        "Account Login Notification",
                        "You have successfully logged in to your account. If you did not perform this action, please contact us immediately.",
                        "reecejames934@gmail.com",
                        [
                            user.email,
                        ],
                        fail_silently=False,
                    )
                except Exception as e:
                    pass

                return JsonResponse({"message": "success"})
            else:
                return JsonResponse({"message": "Invalid email or password!"})
        else:
            return JsonResponse({"message": "Invalid request method"}, status=405)


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
