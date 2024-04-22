from django.contrib.auth.models import AbstractUser, Group
from django.db import models


# Users
class Centre(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='centres_groups')
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='centres_user_permissions'
    )

    location = models.TextField(max_length=500)
    setters = models.ManyToManyField("Climber", related_name="employers")

    class Meta:
        app_label = "tracker"


class Climber(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='climber_groups')
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='climber_user_permissions'
    )

    following = models.ManyToManyField("Centre", related_name="followers")

    class Meta:
        app_label = "tracker"


# Route information
class Route(models.Model):
    wall = models.ForeignKey("Wall", related_name="routes", on_delete=models.CASCADE)
    number = models.IntegerField()

    class Meta:
        app_label = "tracker"


class Wall(models.Model):
    centre = models.ForeignKey("Centre", related_name="walls", on_delete=models.CASCADE)

    class Meta:
        app_label = "tracker"


# Reviews
class Review(models.Model):
    writer = models.ForeignKey("Climber", related_name="reviews", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "tracker"
