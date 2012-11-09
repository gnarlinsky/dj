from django.db import models

"""
The Jukebox: a web-based application that provides a management and 
operation interface for a jukebox.

Kinds of users:
- Listeners (may be anonymous)
- Owners (named; are also Listeners)

- A Jukebox: has many Albums
- An Album: has many Songs
            belongs to one Artist
- An Artist: has many Albums

"""

class Artist(models.Model):
    slug = models.SlugField(unique=True)   # so can query object based on a URL; will give error if trying to create same slug (because unique=True)
    name = models.CharField(max_length=100)
    playcount = models.IntegerField()
 
    def __unicode__(self):
        return self.name

    def get_albums(self):
        return self.album_set.all()
    
    # deal with this more intelligently, have to loop through albums and songs
    def get_albums(self):
        return self.album_set.all().song_set.all()

    class Meta:
        ordering = ['name']


class Album(models.Model):
    slug = models.SlugField(unique=True)   # so can query object based on a URL; will give error if trying to create same slug (because unique=True)
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist)
    playcount = models.IntegerField()
    removed = models.BooleanField() 
    
    def __unicode__(self):
        return self.name

    def get_songs(self):
        return self.song_set.all()

    class Meta:
        ordering = ['name']

############################################################
# a song may have more than one artist IRL.  But for the sake of simplicity, 
# assuming this does not occur here (avoiding many-to-many relationship)
############################################################
class Song(models.Model):
    slug = models.SlugField(unique=True)   # so can query object based on a URL; will give error if trying to create same slug (because unique=True)
    name = models.CharField(max_length=100)
    album = models.ForeignKey(Album) 
    playcount = models.IntegerField()
    blocked = models.BooleanField() 
            # note - only individual songs may be blocked. 
   
    # hmm, not sure if this makes sense in terms of consistency/design
    def get_removed_status(self):
        return self.album.removed   
   
    def get_artist(self):
        return self.album.artist

    def increment_playcount(self):
        self.playcount = self.playcount + 1

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

