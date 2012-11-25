from django.db import models
from django.contrib.auth.models import User
#from django.db.models.signals import post_save



class Artist(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)   # so can query object based on a URL; will give error if trying to create same slug (because unique=True)
    playcount = models.IntegerField()
 
    def __unicode__(self):
        return self.name

    def get_albums(self):
        return self.album_set.all()
    
    # deal with this more intelligently, have to loop through albums and songs
    #def get_albums(self):
    def get_songs(self):   # had get_albums, but this should be get_songs, right? 
        return self.album_set.all().song_set.all()

    class Meta:
        ordering = ['name']


class Album(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)   
    artist = models.ForeignKey(Artist)
    playcount = models.IntegerField()
    removed = models.BooleanField() 
    
    def __unicode__(self):
        return self.name

    def get_songs(self):
        return self.song_set.all()

    class Meta:
        ordering = ['name']


###########################################################################
# a song may have more than one artist IRL.  But for the sake of simplicity, 
# assuming this does not occur here (avoiding many-to-many relationship)
###########################################################################
class Song(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)   
    album = models.ForeignKey(Album) 
    playcount = models.IntegerField()
    blocked = models.BooleanField() 
            # note - only individual songs may be blocked. 
   
    # hmm, not sure if this makes sense in terms of consistency/design:
    def get_removed_status(self):
        """ Removal is associated with Albums, not Songs """
        return self.album.removed   
   
    # Is this the best way to get artist? 
    def get_artist(self):
        return self.album.artist

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        

class Owner(models.Model):
    user        = models.OneToOneField(User)  # every user account will be associated with one of the built-in Django objects; and this will provide the authentication
    birthday    = models.DateField()
    name        = models.CharField(max_length=100)
#    slug        = models.SlugField(unique=True)
#    user_pic    = models.ImageField(upload_to='user_pics/') # Django will automatically use the MEDIA root specified in settings.py here

    def __unicode__(self):
        return self.name   

    # create our user object to attach to our Owner object
    #################  is this even used????????????????????????  ################
    def create_owner_user_callback(sender, instance, **kwargs):
        owner, new = Owner.objects.get_or_create(user=instance) # returns True if created, False if it already exists

    #post_save.connect(create_owner_user_callback, User)   # when user object is created, register the post_save, and will call this function
