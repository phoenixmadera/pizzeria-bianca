from django.contrib import admin
from addresses.models import *
from models import *

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Neighborhood)
admin.site.register(NeighborhoodRate)