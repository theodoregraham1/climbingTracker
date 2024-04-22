from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    # Display all centres

    return render(request, "tracker/index.html")


def login_view(request):
    # Login the user

    if request.method != "POST":
        return render(request, "tracker/login.html", {
            "username": ""
        })

    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        messages.error(request, "Invalid username and/or password")
        return render(request, "tracker/login.html", {
            "username": username
        })
