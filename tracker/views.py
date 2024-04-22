from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from tracker.models import Climber, Centre


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

    messages.error(request, "Invalid username and/or password")
    return render(request, "tracker/login.html", {
        "username": username
    })


def register(request):
    if request.method != "POST":
        return render(request, "tracker/register.html", {
            "username": "",
            "email": ""
        })

    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    confirmation = request.POST["confirmation"]

    if Climber.objects.get(username=username) is not None or Centre.objects.get(username=username) is not None:
        messages.error(request, "Username is already used")
        return render(request, "tracker/register.html", {
            "username": username,
            "email": email
        })

    if password != confirmation:
        messages.error(request, "Password is not the same as the confirmation")
        return render(request, "tracker/register.html", {
            "username": username,
            "email": email
        })

    new_user = Climber.objects.create_user(username, email, password)

    if new_user is not None:
        new_user.save()
        login(request, new_user)

        messages.success(request, "Logged in successfully")
        return HttpResponseRedirect(reverse("index"))

    return render(request, "tracker/register.html", {
        "username": username,
        "email": email
    })


def add_centre(request):
    if request.method != "POST":
        return render(request, "tracker/add_centre.html")

    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    confirmation = request.POST["confirmation"]
    location = request.POST["location"]

    if Climber.objects.get(username=username) is not None or Centre.objects.get(username=username) is not None:
        messages.error(request, "Username is already used")
        return render(request, "tracker/add_centre.html", {
            "username": username,
            "email": email,
            "location": location
        })

    if password != confirmation:
        messages.error(request, "Password is not the same as the confirmation")
        return render(request, "tracker/add_centre.html", {
            "username": username,
            "email": email,
            "location": location
        })

    new_centre = Centre(username=username, email=email, password=password, location=location)

    if new_centre is not None:
        new_centre.save()
        login(request, new_centre)

        messages.success(request, "Centre registered successfully")
        return HttpResponseRedirect(reverse("index"))

    return render(request, "tracker/add_centre.html", {
        "username": username,
        "email": email,
        "location": location
    })


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return HttpResponseRedirect(reverse("index"))





