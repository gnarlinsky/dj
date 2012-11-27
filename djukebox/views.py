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
        the associated album and artist.  """
    next = request.GET.get('next', '/list/') 
    # get: QueryDict method for getting value for key (first arg); second arg 
    # is a Django hook with default value in case key doesn't exist
    # next: indicate where to redirect successful logins and to set the next variable accordingly
    if "song_id" in request.GET:
        s = Song.objects.get(id=int(request.GET["song_id"]))
        ar = s.get_artist()
        al = s.album
        s.playcount  += 1;  s.save() # update the song's playcount
        ar.playcount += 1;  ar.save() # update the artist's playcount
        al.playcount += 1;  al.save() # update the album's playcount
    return HttpResponseRedirect(next) 


@login_required()   # What the user sees *is* restricted at the template level, 
    # but if someone knows the URL, they could still access this without being
    # logged in. Hence the login_required decorator. 
def song_change(request, song_id, next='/list/'): # ??  need to specify next here? 
    """ Actions available to Owners: block/unblock songs, add/remove album
        song_id comes from URL
    """
    next = request.GET.get('next', '/list')
    s = Song.objects.get(id=song_id)   # weird, didn't complain that not int  ?
    if request.POST:
        if 'block_song' in request.POST:
            block_song(s)
        elif 'unblock_song' in request.POST:
            unblock_song(s)
        elif 'remove_album' in request.POST:
            remove_album(s)
        elif 'add_album' in request.POST:
            add_album(s)
        # else: 
        #   something went wrong.........
    return HttpResponseRedirect(next)


def block_song(song_object):
   song_object.blocked = True
   song_object.save()

def unblock_song(song_object):
    song_object.blocked = False 
    song_object.save()

def remove_album(song_object):
    al = song_object.album
    al.removed = True
    al.save()

def add_album(song_object):
    al = song_object.album
    al.removed = False; 
    al.save()

def the_songs(request):
    """ Sort column depending on which header cell's link was clicked. 
        
        (Note on playcount sort order: will come in as "-playcount," 
        so  *descending* order is taken care of.

        To do: When coming back from block/unblock, etc. maintain previous 
            sort order, i.e. don't use the default_sort_order

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
