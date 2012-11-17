######  from the youtube tutorial... not sure if I need this for now ............

from django.contrib import admin
from beer.models import Beer, Brewery

class BeerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}  # slug will be automatically pre-filled with name field
    list_display = ('name', 'brewery', 'locality')  # will be able to sort on these
    search_fields = ['name']  # search field now shows up for admin; can search on name only

class BreweryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}  # slug will be automatically pre-filled with name field

admin.site.register(Beer, BeerAdmin)  # BeerAdmin knows about.. stuff
admin.site.register(Brewery, BreweryAdmin)
