from django.contrib import admin

from .models import Fighter, Event, Match

# Register your models here.
admin.site.register(Fighter)
admin.site.register(Event)
admin.site.register(Match)

