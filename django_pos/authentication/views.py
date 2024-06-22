import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from django.core.mail import send_mail
from authentication.utils import get_all_permissions
from .forms import SignUpForm

# get_user_model
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required(login_url="/users/login/")
def index(request: HttpRequest) -> HttpResponse:
    # for users management
    users = User.objects.all()
    return render(request, "accounts/index.html", {"users": users})


def request_is_ajax(request: HttpRequest) -> bool:
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return JsonResponse(
        {"message": "Logged out successfully", "status": "Ok"}, status=200
    )


@login_required(login_url="/users/login/")
@require_http_methods(["GET", "POST"])
def profile(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "accounts/profile.html")
    elif request.method == "POST":

        email = request.POST.get(key="email").lower()
        first_name = request.POST.get(key="first_name").title()
        last_name = request.POST.get(key="last_name").title()
        user = request.user
        if email == "":
            email = None
        if first_name == "":
            first_name = None
        if last_name == "":
            last_name = None

        user.email = email or user.email
        user.first_name = first_name or user.first_name
        user.last_name = last_name or user.last_name

        user.save()

        return JsonResponse(
            {"message": "Profile updated successfully", "status": "Ok"}, status=200
        )

    else:
        # method isn't allowed
        return JsonResponse({"message": "Invalid request method"}, status=405)


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("/")
    else:

        if request.method == "GET":
            return render(request, "accounts/signin.html")
        elif request.method == "POST":

            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                try:
                    print(user.email)
                    # send email to user
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

    # all permissions available in the system.
    perms = get_all_permissions()

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
            {"perms": perms, "msg": msg, "success": success},
        )
    else:
        # not allowed
        return JsonResponse({"message": "Invalid request method"}, status=405)
