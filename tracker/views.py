from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from tracker.models import Climber, Centre


def index(request):
    # Display all centres, paginated
    return render(request, "tracker/index.html")


def get_centres(request):
    paginator = Paginator(Centre.objects.all().order_by("name"), request.POST["page_size"])
    page_num = request.POST["page_num"]

    centres = [centre.serialise() for i, centre in enumerate(paginator.get_page(page_num))]

    return JsonResponse(centres, status=201, safe=False)


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
        if user.owned_centre is not None:
            request.session["type"] = "Centre"
        else:
            request.session["type"] = "Climber"

        messages.success(request, "Logged in successfully")
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

    if User.objects.filter(username=username).exists():
        messages.error(request, "Username is already taken")
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

    new_user = User.objects.create_user(username=username, email=email, password=password)

    if new_user is not None:
        new_user.save()

        try:
            new_climber = Climber(user=new_user)
            new_climber.save()
        except Exception:
            new_user.delete()
            new_user.save()

        login(request, new_user)
        request.session["type"] = "Climber"

        messages.success(request, "Registered successfully")
        return HttpResponseRedirect(reverse("index"))

    messages.error(request, "An unknown error occurred, login unsuccessful")
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

    if User.objects.filter(username=username).exists():
        messages.error(request, "Username is already used")
        return render(request, "tracker/add_centre.html", {
            "username": "",
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

    new_user = User.objects.create_user(username=username, email=email, password=password)

    if new_user is not None:
        new_user.save()

        try:
            new_centre = Centre(owner=new_user)
            new_centre.save()
        except Exception:
            new_user.delete()
            messages.error(request, "An unknown error occurred, login unsuccessful")

            return render(request, "tracker/add_centre.html", {
                "username": username,
                "email": email
            })

        login(request, new_user)
        request.session["type"] = "Centre"

        messages.success(request, "Centre registered successfully")
        return HttpResponseRedirect(reverse("index"))

    messages.error(request, "An unknown error occurred, login unsuccessful")
    return render(request, "tracker/add_centre.html", {
        "username": username,
        "email": email,
        "location": location
    })


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return HttpResponseRedirect(reverse("index"))


def account_centre(request):
    if request.method != "post":
        return render(request, "tracker/account_centre.html", {

        })
