# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignUpForm
from django.views.decorators.http import require_http_methods
from django.contrib import messages




def logout_view(request:HttpRequest)->HttpResponse:

    logout(request)
    return redirect('/')

@login_required(login_url="/accounts/login/")
@require_http_methods(['GET', 'POST'])
def profile(request:HttpRequest)->HttpResponse:
    if request.method == 'GET':
        return render(request, "accounts/profile.html")
    else:
        
        email=request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user = request.user   
        # if email != '' and first_name != '' and last_name != '':
            
        #     user.email = email
        #     user.first_name = first_name
        #     user.last_name = last_name

        #     user.save()
        #     messages.add_message(request=request, message='Profile updated successfully', level=messages.SUCCESS)
        #     return redirect('/accounts/profile')
        if email == '':
            email = None
        if first_name== '':
            first_name = None
        if last_name=='':
            last_name=None
        
        user.email = email or user.email
        user.first_name = first_name or user.first_name
        user.last_name = last_name or user.last_name

        user.save()
        messages.add_message(request=request, message='Profile updated successfully', level=messages.SUCCESS)
        return redirect('/accounts/profile')
        

        


        
def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid username or password!'
        else:
            msg = 'An error ocurred!.'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
