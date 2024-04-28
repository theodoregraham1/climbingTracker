from django.contrib import admin

from tracker.models import Climber, Centre, Wall, Route, Review

# Register your models here.
admin.site.register(Climber)
admin.site.register(Centre)
admin.site.register(Wall)
admin.site.register(Route)
admin.site.register(Review)