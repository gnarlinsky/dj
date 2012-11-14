#!/usr/bin/env python
from djukebox.models import Song, Album, Artist
from django.views.generic import list_detail
#from django.template.loader import get_template
from django.template import Context#, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  render_to_response
#from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms

# ... or in models ....? 
def increment_playcount(request,next= '/list/'):
    #  see if GET request included a next key to indicate where to redirect successful logins and to set the next variable accordingly:
    if request.GET.has_key('next'):  next = request.GET['next']
    if "song_id" in request.GET:
        s = Song.objects.get(id=int(request.GET["song_id"]))
        ar = s.get_artist()
        al = s.album
       # message = "BEFORE updated i guess: %d, %d, %d" % (ar.playcount, al.playcount, s.playcount)
        s.playcount = s.playcount + 1;  s.save() # update the song's playcount
        ar.playcount = ar.playcount+1;  ar.save() # update the artist's playcount
        al.playcount = al.playcount+1;  al.save() # update the album's playcount
       # message+= "<a href = 'http://127.0.0.1:8000/songs/'>/songs/</a>"
    return HttpResponseRedirect(next) 

@login_required()     # but... they wouldn't even see block_song if they weren't logged in.. why am I even providing a login url here...?   Is it a security thing, in case this could be faked? 
def block_song(request, next='/list/'):
    if request.GET.has_key('next'):  next = request.GET['next']
    if request.method == "POST":
        if request.POST["submit"] == "Block song":
            if "song_id" in request.POST:
                s = Song.objects.get(id=int(request.POST["song_id"]))
                s.blocked = True; s.save()
    return HttpResponseRedirect(next) 



# uhhh wtf?  this USED to work when it was using POST, like remove_album below, but then ... 
#   it stopped working. Now just using GET, not even checking value of 'submit'
@login_required()     # but... they wouldn't even see block_song if they weren't logged in.. why am I even providing a login url here...?   Is it a security thing, in case this could be faked? 
def unblock_song(request, next='/list/'):
    if request.GET.has_key('next'):  next = request.GET['next']
    if request.method == "GET":
#        if request.GET["submit"] == "Unblock song":
        if "song_id" in request.GET:
            s = Song.objects.get(id=int(request.GET["song_id"]))
            s.blocked = False; s.save()
    return HttpResponseRedirect(next) 


######## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
################ !!!!!!!!!!!!!!!!!!!  different login_url !!!!!!!!!!!!!!!!!!!!!!
######## !!!!!!!!!!!!!!!!!  or just don't put the login_url ?????!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required()
def remove_album(request, next='/list/'):
    if request.GET.has_key('next'):  next = request.GET['next']
    if request.method == 'POST':
        if request.POST['submit'] == "Remove album":
            if "song_id" in request.POST:
                s = Song.objects.get(id=int(request.POST["song_id"]))
                al = s.album
                al.removed = True; al.save()
    return HttpResponseRedirect(next) 



################################  so why get vs post here.........  anywhere ...............########################
#  i.e. why not doing everything like /play/? 
#  why not retrieve song id from url?   like,put it in Url when submit form (so would have to be get, not post, right? and then url conf can take
#  it from there............)
@login_required()
def add_album(request, next='/list/'):
    if request.GET.has_key('next'):  next = request.GET['next']
    if request.method == 'POST':
        if request.POST['submit'] == "Add album":
            if "song_id" in request.POST:
                s = Song.objects.get(id=int(request.POST["song_id"]))
                al = s.album
                al.removed = False; 
                al.save()
    return HttpResponseRedirect(next) 




def the_songs(request):
    """ Sort column depending on which header cell's link was clicked. 
        
        (Note on playcount sort order: will come in as "-playcount," 
        so  *descending* order is taken care of.
    """
    default_sort_order = "-playcount"
    sort_by = request.GET.get("sort_by", default_sort_order ) 
    return list_detail.object_list( request, 
                                queryset = Song.objects.all().order_by(sort_by),
                                template_name= 'song_list.html',
                                 #'template_object_name'= 'Song',
                                 #  'extra_context'= {'song_list': Song.objects.all}
                                 )




#def search(request, next='/songs'):
#    """ A pretty dumb 'search': determine *exact* matches for artist/album/song name """
#    pass
#    #  see if the GET request included a next key to indicate where to redirect successful logins and to set the next variable accordingly:
#    if request.GET.has_key('next'):  next = request.GET['next']
#    if "search_for" in request.GET:
#        name_to_search_for = request.GET["search_for"]
#    
#    return list_detail.object_list( request, 
#                               queryset = Song.objects.filter(name__icontains=search_for),
#                                template_name= 'song_list.html',
#
#


##################################################################################################
#    THE FOLLOWING IS THE ENTIRE VIEWS.PY THAT WAS IN DRINKER APP
##################################################################################################
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from drinker.forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User
from drinker.models import Drinker
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



# if not logged in, send to login page that's defined in settings,
# then bring them back
@login_required
def Profile(request):
    if not request.user.is_authenticated():  # if not logged in... not required, sort of a safety net thing (right?)
        return HttpResponseRedirect('/login/')
    drinker = request.user.get_profile   # will return a drinker object
    context = {'drinker': drinker}
    return render_to_response('profile.html', context, context_instance=RequestContext(request))

def DrinkerRegistration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/') # send user to profile if they're already registered

    if request.method == 'POST': # if they're submitting the form...
        form = RegistrationForm(request.POST) # fill out registration form with what's been posted

        if form.is_valid():   # remember our custom validation in forms.py!
            # so at this point we know everything in the form is good
            user = User.objects.create_user(username = form.cleaned_data['username'], \
                    email = form.cleaned_data['email'], \
                    password = form.cleaned_data['password'])
            user.save()  # save user object

            ###############################################################################
            # so setting drinker = user.get_profile() -- this is what ties together the User and the Drinker...right?
            ###############################################################################
#            drinker=user.get_profile()  # remember AUTH_PROFILE_MODULE='drinker.Drinker' in settings.py 
                # So can call this method against a user to get their drinker object that's attached
                # to their user. Will come in handly later on, when we do: 
                
###############  note commenting out below because some shit broke with post_blah blah (video 7).....   and adding the line below
   #         user = request.user.get_profile()   # set user attached to the drinker that's logged in according to the request
   #         drinker.name = form.cleaned_data['name']
   #         drinker.birthday = form.cleaned_data['birthday']
   #         drinker.save()  # save drinker object     ....... uhhh  he had this twice in the video?????
            drinker = Drinker(user=user, name=form.cleaned_data['name'], birthday=form.cleaned_data['birthday'])
            drinker.save()     # so this is in place of automatically creating the profile...  we have to set birthday when we create the object because of the blah blah is NULL error. So this is MANUAL, keep that in mind...  nk
            return HttpResponseRedirect('/profile/')  # or just HttpResponse????
