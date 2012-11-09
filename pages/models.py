from django.db import models

class HomePage(models.Model):
    homecopy    = models.TextField()   # so this holds the text you entered via admin interface

    def __unicode__(self):
        return 'Home Page Copy'  # (every instance of) this model calls itself 'Home Page Copy'... but we'll only have one instance of this so that's ok
