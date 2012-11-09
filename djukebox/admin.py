from django.contrib import admin
from djukebox.models import Song, Artist, Album

class SongAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # slug will be automatically pre-filled with name field
    list_display =  ('name',) # will be able to sort on these
    search_fields = ['name']  # seach field now shows up for admin; can search on name only

class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',) }

class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Song, SongAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
