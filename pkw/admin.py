from django.contrib import admin

# Register your models here.

from models import *

admin.site.register(Voivodeship)
admin.site.register(City)
admin.site.register(County)
admin.site.register(Commission)
