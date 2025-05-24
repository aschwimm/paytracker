from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from payplan.models import Sale, Payplan, UserModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum
from payplan.forms import RegisterUserForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    account_info = UserModel.objects.filter(username=request.user.username)
    return render(request, "users/index.html", {
        "account_info": account_info
    })
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:index"))
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
    
        if user:
            login(request, user)
            if Payplan.objects.filter(user_id=user).exists():
                return HttpResponseRedirect(reverse("saletracker:index"))
            else:
                return HttpResponseRedirect(reverse("payplan:index"))
        else:
            return render(request, "users/login.html", {
                "message": "invalid login"
            })
 
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "logged out"
    })

def register_view(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            store_code = form.cleaned_data['store_code']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration successful"))
            user_entry = UserModel(username=username, first_name=first_name, last_name=last_name, email=email, store_code=store_code)
            user_entry.save()
            return HttpResponseRedirect(reverse("payplan:index"))
    else:
        form = RegisterUserForm()
    return render(request, "users/register.html", {
        "form": form
    })
