from django.contrib.auth.models import User, Group
from django.db import models


# Users

class Centre(models.Model):
    owner = models.ForeignKey(User, related_name="owned_centre", on_delete=models.CASCADE)
    name = models.TextField(max_length=100)
    location = models.TextField(max_length=500)
    setters = models.ManyToManyField("Climber", related_name="employers", blank=True)
    image = models.ImageField(upload_to="media/centres", blank=True)

    def serialise(self):
        data = {
            "id": self.id,
            "owner": self.owner.id,
            "name": self.name,
            "location": self.location,
            "setters": [{"id": climber.id, "username": climber.user.username} for climber in self.setters.order_by("user__username")],
            "walls_num": self.walls.count(),
            "routes_num": None,
            "image_url": None,
        }
        total = 0
        for w in self.walls.all():
            total += w.routes.count()
        data["routes_num"] = total

        if self.image:
            data["image_url"] = self.image.url

        return data

    class Meta:
        app_label = "tracker"


class Climber(models.Model):
    user = models.ForeignKey(User, related_name="climber", on_delete=models.CASCADE)
    following = models.ManyToManyField("Centre", related_name="followers", blank=True)

    class Meta:
        app_label = "tracker"


# Route information
class Route(models.Model):
    wall = models.ForeignKey("Wall", related_name="routes", on_delete=models.CASCADE)
    number = models.IntegerField(blank=True)

    class Meta:
        app_label = "tracker"


class Wall(models.Model):
    centre = models.ForeignKey(Centre, related_name="walls", on_delete=models.CASCADE, blank=True)

    class Meta:
        app_label = "tracker"


# Reviews
class Review(models.Model):
    writer = models.ForeignKey("Climber", related_name="reviews", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "tracker"
