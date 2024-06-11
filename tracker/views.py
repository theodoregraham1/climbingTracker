from typing import List

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from tracker.constants import POSSIBLE_GRADES
from tracker.models import Climber, Centre, Wall, Route, Grade


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
        if len(user.owned_centre.all()) > 0:
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
            new_centre = Centre(owner=new_user, location=location, name=username)
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


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return HttpResponseRedirect(reverse("index"))


@login_required
def account(request):
    if request.session["type"] == "Centre":
        return render(request, "tracker/account_centre.html", {
            "centre": Centre.objects.get(owner=request.user).serialise()
        })

    return render(request, "tracker/account_climber.html")


@login_required
def edit_username(request):
    password = request.POST["password"]
    username = request.POST["new-username"]

    status = 202
    success = False

    if not request.user.check_password(password):
        message = {"message": "Password incorrect", "tag": "error"}

    elif User.objects.filter(username=username).exists():
        message = {"message": "Username already taken", "tag": "error"}

    else:
        request.user.username = username
        request.user.save()

        message = {"message": "Username updated", "tag": "success"}
        status = 201
        success = True

    return JsonResponse({"username": request.user.username, "success": success, "message": message}, status=status)


@login_required
def edit_password(request):
    old_password = request.POST["old-password"]
    new_password = request.POST["new-password"]
    confirmation = request.POST["confirmation"]

    status = 202
    success = False

    if new_password != confirmation:
        message = {"message": "Passwords do not match", "tag": "error"}

    elif request.user.check_password(old_password):
        message = {"message": "Password is not correct", "tag": "error"}

    else:
        user = request.user
        request.user.set_password(new_password)
        request.user.save()

        login(request, user)

        message = {"message": "Password updated", "tag": "success"}
        status = 201
        success = True

    return JsonResponse({"success": success, "message": message}, status=status)


@login_required
def edit_centre_attribute(request, attribute):
    centre = Centre.objects.get(owner=request.user)

    if centre is None:
        return JsonResponse({"success": False}, status=500)

    new_attr = request.POST[f"new-{attribute}"]

    setattr(centre, attribute, new_attr)
    centre.save()

    return JsonResponse({
        attribute: new_attr,
        "success": True,
        "message": {"message": f"{attribute.capitalize()} edited successfully", "tag": "success"}
    }, status=201)


@login_required
def edit_centre_image(request):
    centre = Centre.objects.get(owner=request.user)

    if centre is None:
        return JsonResponse({"success": False}, status=500)

    new_image = request.FILES["new-image"]

    status = 202
    success = False

    if new_image.content_type[:5] != "image":
        message = {"message": "Image must be an image file", "tag": "error"}

    else:
        centre.image = new_image
        centre.save()

        status = 201
        success = True
        message = {"message": "Image changed successfully", "tag": "success"}

    return JsonResponse({"success": success, "message": message}, status=status)


@login_required
def edit_setters_list(request):
    # FIXME This is indentation hell
    centre = Centre.objects.get(owner=request.user)

    if centre is None:
        return JsonResponse({"success": False}, status=500)

    status = 202
    success = False

    if request.POST["action"] == "add":
        setter_user = User.objects.get(username=request.POST["new-setter"])
        setter = None

        if setter_user is None:
            message = {"message": "User does not exist", "tag": "error"}

        else:
            setter = Climber.objects.get(user=setter_user)
            if setter is None:
                message = {"message": "Setter must be a climber, not a centre", "tag": "error"}

            elif setter in centre.setters.all():
                message = {"message": "Setter is already registered for this centre", "tag": "primary"}

            else:
                centre.setters.add(setter)
                centre.save()

                status = 201
                success = True
                message = {"message": "Setter added", "tag": "success"}

        return JsonResponse({
            "success": success,
            "message": message,
            "username": request.POST["new-setter"] if setter is not None else None,
            "id": setter.id if setter is not None else None
        }, status=status)

    else:
        centre.setters.remove(Climber.objects.get(id=request.POST["id"]))
        centre.save()

        success = len(centre.setters.filter(id=request.POST["id"])) == 0
        status = 201 if success else 202

        message = {"message": "Setter removed", "tag": "success"}

        return JsonResponse({
            "success": success,
            "message": message,
        }, status=status)


@login_required
def view_wall(request, id):
    wall = Wall.objects.get(id=id)

    owned = False

    if request.session["type"] != "Centre":
        pass

    elif request.user.owned_centre.get() == wall.centre:
        owned = True

    if owned:
        return render(request, "tracker/wall_settings.html", {
            "wall": wall,
            "routes": wall.routes.all(),
            "grades_all": POSSIBLE_GRADES
        })
    else:
        # TODO Allow support for outdoor walls
        return render(request, "tracker/wall.html", {
            "wall": wall,
            "location": wall.centre.get() if wall.centre.get() is not None else None
        })


@login_required
def add_wall(request):
    if request.session["type"] != "Centre":
        return HttpResponseRedirect(reverse("index"))

    if request.method != "POST":
        return HttpResponseRedirect(reverse("account"))

    centre = Centre.objects.get(owner=request.user)
    name = request.POST["new-wall"]

    wall = Wall(centre=centre, name=name)
    wall.save()

    return HttpResponseRedirect(reverse("wall", args=[wall.id,]))


@login_required
def add_route(request, wall_id:int):
    if request.session["type"] != "Centre":
        return HttpResponseRedirect(reverse("index"))

    if request.method != "POST":
        return HttpResponseRedirect(reverse("wall", wall_id))

    centre: Centre = Centre.objects.get(owner=request.user)
    wall: Wall = Wall.objects.get(id=request.POST[wall_id])

    if wall is None:
        return HttpResponseRedirect(reverse("account"))

    if wall.centre != centre:
        return HttpResponseRedirect(reverse("wall", wall_id))

    route: Route = Route(wall=wall, number=request.POST["number"])
    route.save()

    for grade in request.POST["grades"]:
        new_grade: Grade = Grade(route=route, grade=grade)
        new_grade.save()

    message = {"message": "Route added successfully", "tag": "success"}

    return JsonResponse({
        "success": True,
        "message": message,
    }, status=201)


def centre_page(request, centre_id):
    return render(request, "tracker/centre_page.html", {
        "centre": Centre.objects.get(id=centre_id)
    })
