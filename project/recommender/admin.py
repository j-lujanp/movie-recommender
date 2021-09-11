from django.contrib import admin

from .models import Rater, Rating

admin.site.register(Rater)
admin.site.register(Rating)