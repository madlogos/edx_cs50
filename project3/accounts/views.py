from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegisterForm, LoginForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return login_view(request)
    return HttpResponseRedirect(reverse("menu"), content={"user": request.user})

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("menu"), content={"user": request.user})
    try:
        if request.method == "POST":
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get("username")
                password = login_form.cleaned_data.get("password")
            else:
                return render(request, "accounts/login.html", 
                    {"message": ["danger", str(login_form.errors.values())], "form": LoginForm()})
            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"), content={"user": request.user})
            else:
                return render(request, "accounts/login.html", 
                    {"message": ["danger", "Invalid credentials."], "form": login_form})
        else:
            login_form = LoginForm()
            return render(request, "accounts/login.html", {"message": None, "form": login_form})
    except Exception as e:
        return render(request, "accounts/login.html", {"message": ["danger", str(e)]})

def logout_view(request):
    logout(request)
    return render(request, "accounts/login.html", {"message": ["success", "Logged out."]})

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("menu"), content={"user": request.user})
    try:
        if request.method == "POST":
            reg_form = RegisterForm(request.POST)
            if reg_form.is_valid():
                username = reg_form.cleaned_data.get("username")
                password = reg_form.cleaned_data.get("password")
                first_name = reg_form.cleaned_data.get("first_name")
                last_name = reg_form.cleaned_data.get("last_name")
                email = reg_form.cleaned_data.get("email")
            else:
                return render(request, "accounts/register.html", 
                    {"message": ["danger", str(reg_form.errors.values())], "form": RegisterForm()})
            
            user = User.objects.create_user(
                username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            user.save()
            user.is_active = True
            user.success = True

            return render(request, "accounts/login.html", 
                {"message": ["success", "New account %s has been created. Log in now." % (username)], "form": LoginForm()})
        else:
            return render(request, "accounts/register.html", {"message": None, "form": RegisterForm()})
    except Exception as e:
        return render(request, "accounts/register.html", 
            {"message": ["danger", str(e)], "form": RegisterForm()})
