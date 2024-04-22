from django.contrib.auth.models import AbstractUser
from django.db import models


# Users
class User(AbstractUser):
    pass


class Centre(User):
    pass


class Climber(User):
    pass


# Route information
class Route(models.Model):
    pass


class Wall(models.Model):
    pass


# Reviews
class Review(models.Model):
    pass
