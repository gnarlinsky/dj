from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Drinker(models.Model):
    user        = models.OneToOneField(User)  # every user account will be associated with one of the built-in Django objects; and this will provide the authentication
    birthday    = models.DateField()
    name        = models.CharField(max_length=100)
#    user_pic    = models.ImageField(upload_to='user_pics/') #nk
                    # Django will automatically use the MEDIA root specified in settings.py here

    def __unicode__(self):
        return self.name    # not the user name, actually, it's provided by the user object....  wait.... what? 

# create our user object to attach to our drinker object
#########################  not really sure what's going on here, though............... ###################
def create_drinker_user_callback(sender, instance, **kwargs):
    drinker, new = Drinker.objects.get_or_create(user=instance) # returns True if created, False if it already exists


##### some birthday stuff kept getting screwed up here because something was being called before something else blah blah 
#post_save.connect(create_drinker_user_callback, User)   # when user object is created, register the post_save, and will call this function
