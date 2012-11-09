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
def increment_playcount(request,next= '/songs/'):

    #  see if GET request included a next key to indicate where to redirect successful logins and to set the next variable accordingly:
    if request.GET.has_key('next'):  
        next = request.GET['next']
    if "song_id" in request.GET:
        s = Song.objects.get(id=int(request.GET["song_id"]))
        ar = s.get_artist()
        al = s.album
        message = "BEFORE updated i guess: %d, %d, %d" % (ar.playcount, al.playcount, s.playcount)
        s.playcount = s.playcount + 1;  s.save() # update the song's playcount
        ar.playcount = ar.playcount+1;  ar.save() # update the artist's playcount
        al.playcount = al.playcount+1;  al.save() # update the album's playcount
        message+= "<a href = 'http://127.0.0.1:8000/songs/'>/songs/</a>"
    return HttpResponseRedirect(next) 

"""
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())


def logout_user(request, next= '/songs/'):   #Hmm, I don't think "next" should be hardcoded in here
    if request.GET.has_key('next'):  next = request.GET['next']
    logout(request)
    return HttpResponseRedirect(next)
"""

@login_required(login_url="/new_login/")
def unblock_song(request, next='/songs/'):
    if request.GET.has_key('next'):  next = request.GET['next']
    if request.method == 'POST':
        if request.POST['submit'] == "UNblock SONG":
            if "song_id" in request.POST:
                s = Song.objects.get(id=int(request.POST["song_id"]))
                s.blocked = False; s.save()
    return HttpResponseRedirect(next) 

@login_required(login_url="/new_login/")
def remove_album(request, next='/songs/'):
    if request.GET.has_key('next'):  next = request.GET['next']
    if request.method == 'POST':
        if request.POST['submit'] == "Remove ALBUM":
            if "song_id" in request.POST:
                s = Song.objects.get(id=int(request.POST["song_id"]))
                al = s.album
                al.removed = True; al.save()
    return HttpResponseRedirect(next) 

@login_required(login_url="/new_login/")
def add_album(request, next='/songs/'):
    if request.GET.has_key('next'):  next = request.GET['next']
    if request.method == 'POST':
        if request.POST['submit'] == "Add ALBUM":
            if "song_id" in request.POST:
                s = Song.objects.get(id=int(request.POST["song_id"]))
                al = s.album
                al.removed = False; al.save()
    return HttpResponseRedirect(next) 

@login_required(login_url="/new_login/")     # but... they wouldn't even see block_song if they weren't logged in.. why am I even providing a login url here...?   Is it a security thing, in case this could be faked? 
def block_song(request, next='/songs/'):
    if request.GET.has_key('next'):  next = request.GET['next']
    if request.method == "POST":
        if request.POST["submit"] == "Block SONG":
            if "song_id" in request.POST:
                s = Song.objects.get(id=int(request.POST["song_id"]))
                s.blocked = True; s.save()
    return HttpResponseRedirect(next) 


"""

# testing new login instead of login_user below
def new_login(request):
    html = "lemme print the request........"
    return HttpResponse(html+str(request))

@login_required(login_url="/new_login/")
def thing_that_requires_login(request):
    html = "using the login required decorator....  do I still return whatever with HttpResponse? Is it just that a login will be required for that? "
    return HttpResponse(html)



def login_user(request, next= '/songs/'):   
    if request.GET.has_key('next'):  next = request.GET['next']
    message = 'Login User'
    lForm = LoginForm()

    if request.method == 'POST':
        if request.POST['submit'] == 'Login':
            postDict = request.POST.copy()
            lForm = LoginForm(postDict)
            if lForm.is_valid():
                uName = request.POST['username']
                uPass = request.POST['password']
                user = authenticate(username=uName, password=uPass)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        message = 'Logged in: %s' % uName
                        return HttpResponseRedirect(next) 
                        #assert False
                        #return render_to_response('song_list.html',{'message': message })  
                    else:
                        message = 'Account Deactivated'
                        return HttpResponseRedirect(next) 
                else:
                    message = 'Login Incorrect'
                    return render_to_response('song_list.html',{
                        'lForm': lForm,
                        'message': message })


    return render_to_response('song_list.html',{
                'lForm': lForm,
                'message': message })
"""




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
