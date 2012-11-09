from django.shortcuts import render_to_response
from django.template import RequestContext # not for this demo, but good practice to use....
from beer.models import Beer, Brewery

# view to spit out all beers in db
def BeerAll(request):
    beers = Beer.objects.all().order_by('name')  # list of all Beer objects in db, order alphabetically
    context = {'beers': beers}   # takes list beers above; puts inside variable 'beers' that will be passed to templates
        # So in template will use 'beers'
    return render_to_response('beersall.html', context, context_instance = RequestContext(request))  
        # variable 'beers' passed to template beersall.html
        # RequestContext: strip the context out of the request, will pass to template
        # So if user is logged in and goes from page to page, everything about the user, what they want, etc.,  
        # passes through the request, across pages, in the background 

def SpecificBeer(request, beerslug):
    beer = Beer.objects.get(slug=beerslug)
    context = {'beer':beer}
    return render_to_response('singlebeer.html',context, context_instance=RequestContext(request))

def SpecificBrewery(request, breweryslug):
    breweryObj = Brewery.objects.get(slug=breweryslug)
    beers = Beer.objects.filter(brewery=breweryObj) # so filtering out only those beers that were made at the specified brewery
    context = {'beers': beers}
    return render_to_response('singlebrewery.html',context, context_instance = RequestContext(request)) 

######## yeah... I don't like how he cap's the views... don't do that in mine......
def show_list(request):
    """ View list of all songs, alphabetized on song name by default """
#    theSongs = Song.objects.all().order_by('name') # list of all Song objects in db, order alphabetically by name
#    context = {'songs': theSongs}  # takes list of Songs above; puts inside variable 'songs', which will be passed to template
    context = {'songs': ['song1', 'song2', 'song3']}
    #return render_to_response('list.html', context, context_instance=RequestContext(request))
    return render_to_response('song_list.html', context, context_instance=RequestContext(request))
        # variable 'songs' passed to template list.html
        # RequestContext: strips the context out of the request, to pass to template --
        #   so if the user is logged in and goes from page to page, their info, what they want, etc
        #   passes through with the request, across pages

def show_covers(request):
    """ View covers flow thing """
    # so there's no separate covers class or anything, right? A Song has an attribute that's the cover/its url, etc. right...
    # return render_to_response('covers.html', context, context_instance=RequestContext(request))
    pass
