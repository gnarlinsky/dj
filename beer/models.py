from django.db import models

# in db, will just use the one character
BEER_CHOICES = (
    ('D','Domestic'),
    ('I','Import'),
)

class Beer(models.Model):
    name        = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True)     # gives ability to query object based on a URL
        # will give error if trying to create same slug (unique=True)
    brewery     = models.ForeignKey("Brewery")
    locality    = models.CharField(max_length=1, choices=BEER_CHOICES)
    description = models.TextField(blank=True)  # blank=True  means  optional
    image1      = models.ImageField(upload_to='beerthumbs/') # Django will automatically use the MEDIA root here; also this folder must be writable...???

    def __unicode__(self):
        return self.name    # object will always return its name field as def of itself
                            # this is what this object will be called in, for example, admin interface    


class Brewery(models.Model):
    name        = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name
