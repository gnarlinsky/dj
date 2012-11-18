#!/usr/bin/env python
from django import forms
from djukebox.models import Song, Album, Artist, Owner
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  render_to_response
from djukebox.forms import RegistrationForm, LoginForm
from django.views.generic import list_detail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def increment_playcount(request,next= '/list/'):
    """ Increment the playcount of a song. Also increment the playcounts of
        the associated album and artist. 
    """
    if request.GET.has_key('next'):  next = request.GET['next'] #  see if GET request included a next key to indicate where to redirect successful logins and to set the next variable accordingly:
    if "song_id" in request.GET:
        s = Song.objects.get(id=int(request.GET["song_id"]))
        ar = s.get_artist()
        al = s.album
        s.playcount = s.playcount + 1;  s.save() # update the song's playcount
        ar.playcount = ar.playcount+1;  ar.save() # update the artist's playcount
        al.playcount = al.playcount+1;  al.save() # update the album's playcount
    return HttpResponseRedirect(next) 




#############################################################################################################
# Tollowing four views are for the buttons on song_list. 
# ... Or should I have one big remove/add/block/unblock view and just check value of request.POST["submit"]?
#############################################################################################################

@login_required()     # but... they wouldn't even see block_song if they weren't
        # logged in.. why am I even providing a login url here...?   
        # Is it a security thing, in case this could be faked? 
def block_song(request, next='/list/'):
    if request.GET.has_key('next'):  next = request.GET['next']
    if request.method == "POST":
        if request.POST["submit"] == "Block song":
            if "song_id" in request.POST:
                s = Song.objects.get(id=int(request.POST["song_id"]))
                s.blocked = True; s.save()
    return HttpResponseRedirect(next) 


# GET vs POST ?
@login_required()     
def unblock_song(request, next='/list/'):
    if request.GET.has_key('next'):  next = request.GET['next']
    if request.method == "GET":
        if request.GET["submit"] == "Unblock song":
            if "song_id" in request.GET:
                s = Song.objects.get(id=int(request.GET["song_id"]))
                s.blocked = False; s.save()
    return HttpResponseRedirect(next) 


# GET vs POST ?
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


# if not logged in, send to login page that's defined in settings,
# then bring them back
############  Wait, no, that doesn't work for me right here.......  I'm seeing this http://localhost:8080/login/?next=/profile/, but after submit it does NOT go to profile... but it HAS registered them. 
@login_required
def send_to_profile(request):
    if not request.user.is_authenticated():  # if not logged in... not required, sort of a safety net thing (right?)
        return HttpResponseRedirect('/login/')
    owner = request.user.get_profile   # will return an Owner object
    context = {'owner': owner}
    return render_to_response('profile.html', context, context_instance=RequestContext(request))





##############################################################################
# Following:login/out/registration views 
##############################################################################

def ownerRegistration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/') # send user to profile if they're already registered

    if request.method == 'POST': # if they're submitting the form...
        form = RegistrationForm(request.POST) # fill out registration form with what's been posted

        if form.is_valid():   # remember our custom validation in forms.py! [update: well... not anymore] 
            # so at this point we know everything in the form is good
            user = User.objects.create_user(username = form.cleaned_data['username'], \
                    email = form.cleaned_data['email'], \
                    password = form.cleaned_data['password'])
            user.save()  # save user object

            ##################################################################
            # so setting owner = user.get_profile() -- this is what ties 
            # together the User and the Owner...right?
            ##################################################################
#            owner =user.get_profile()  # Can call this method against a user to get their owner object that's attached
                    # remember AUTH_PROFILE_MODULE='owner.Owner' in settings.py..... 
                
   #         user = request.user.get_profile()   # set user attached to the owner that's logged in according to the request
   #         owner.name = form.cleaned_data['name']
   #         owner.birthday = form.cleaned_data['birthday']
            owner = Owner(user=user, name=form.cleaned_data['name'], birthday=form.cleaned_data['birthday'])
            owner.save()     # so this is in place of automatically creating the profile...  we have to set birthday when we create the object ??????????????
            return HttpResponseRedirect('/profile/')  # or just HttpResponse????
                    # to do: just return "hi, you're registered, ______"; log them in already.   

        else:  # form doesn't validate
            return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))

    else: # user is not trying to submit the form, show them a blank registration form
        form = RegistrationForm()
        context = {'form':form}
        return render_to_response('register.html',context,context_instance=RequestContext(request))


def loginRequest(request):
    # when this is called via url, not through trying to submit the form (right?)
    if request.user.is_authenticated():
     #   return HttpResponseRedirect('/profile/') # so can't login twice
        return HttpResponseRedirect('/')   # don't go anywhere new.....   How do you just ... stay there?

    # unlike above, this would happen when actual button-clickage is happening
    if request.method == 'POST':  # if user is trying to log in right now
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # when you log someone in:  (1) call authenticate, then (2) call login
            owner = authenticate(username =username, password=password)   # return a user object if 
                            #password is valid, otherwise returns null
            if owner is not None:   # authentication succeeded
                login(request, owner)
                # returning this way below because already logged in... although this shouldn't actually happen, because 
                #   there's no form/submit button available to someone who is already logged in 
                #   (although I think this could be faked)
                #return HttpResponseRedirect('/profile/')   
                return HttpResponseRedirect('/')  # no, not to "/"... stay .. "there" 
            else: #authentication failed
                #return HttpResponseRedirect('/login/')
                # Commenting out above because you're going to go back and actually show the error, not just redirect to
                return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request)) # login

        else:  # form not valid
            return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))

    else:  # user is not submitting the form, show the login form
        # So this wouldn't be happening through button clickage, but via url, like the first above
        #   (if request.user_is_authenticated() except that this time user is NOT authenticated.....
        form = LoginForm()
        context = {'form':form}
        return render_to_response('login.html', context, context_instance=RequestContext(request))


def logoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/')
