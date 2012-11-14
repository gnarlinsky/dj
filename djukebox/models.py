from django.db import models


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

###########################################################################
# a song may have more than one artist IRL.  But for the sake of simplicity, 
# assuming this does not occur here (avoiding many-to-many relationship)
###########################################################################
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



##################################################################################
#  from old drinker app.  Just replacing (D/d)rinker with (O/o)wner
##################################################################################
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Owner(models.Model):
    user        = models.OneToOneField(User)  # every user account will be associated with one of the built-in Django objects; and this will provide the authentication
    birthday    = models.DateField()
    name        = models.CharField(max_length=100)
#    user_pic    = models.ImageField(upload_to='user_pics/') #nk
                    # Django will automatically use the MEDIA root specified in settings.py here

    def __unicode__(self):
        return self.name    # not the user name, actually, it's provided by the user object....  wait.... what? 

# create our user object to attach to our drinker object
#########################  not really sure what's going on here, though............... ###################
def create_owner_user_callback(sender, instance, **kwargs):
    owner, new = Owner.objects.get_or_create(user=instance) # returns True if created, False if it already exists


##### some birthday stuff kept getting screwed up here because something was being called before something else blah blah 
#post_save.connect(create_owner_user_callback, User)   # when user object is created, register the post_save, and will call this function
