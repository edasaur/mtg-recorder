from django.contrib import admin

from .models import *

admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Tournament)

