#!/usr/bin/env python
from djukebox.models import Song, Album, Artist, Owner
from django.template import Context, RequestContext, Template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  redirect,render_to_response
from djukebox.forms import RegistrationForm, LoginForm
from django.views.generic import list_detail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import time    # for timer
import urllib

def increment_playcount(request):
    """ Increment the playcount of a song. Also increment the playcounts of
        the associated album and artist.  """
    # get: QueryDict method for getting value for key (first arg); second arg 
    # is a Django hook with default value in case key doesn't exist
    # next: indicate where to redirect successful logins and to set the next variable accordingly
    s = ""
    if "song_id" in request.GET:
        s = Song.objects.get(id=int(request.GET["song_id"]))
        ar = s.get_artist()
        al = s.album
        s.playcount  += 1;  s.save() # update the song's playcount
        ar.playcount += 1;  ar.save() # update the artist's playcount
        al.playcount += 1;  al.save() # update the album's playcount

    #next = request.GET.get('next', '/list/') 
    #return HttpResponseRedirect(next) 

    # extra context here until playing a song is an actual action
    sort_by = request.GET.get("sort_by", "-playcount" ) 
    return list_detail.object_list( request, 
                            queryset = Song.objects.all().order_by(sort_by),
                            template_name= 'song_list.html',
                             #'template_object_name'= 'Song',
                             extra_context = {'just_played':s},
                             #'extra_context'= {'song_list': song.objects.all}
                             )

@login_required()   # What the user sees *is* restricted at the template level, 
    # but if someone knows the URL, they could still access this without being
    # logged in. Hence the login_required decorator. 
def song_change(request, song_id): 
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
    # get: QueryDict method for getting value for key (first arg); second arg 
    # is a Django hook with default value in case key doesn't exist
    return list_detail.object_list( request, 
                            queryset = Song.objects.all().order_by(sort_by),
                            template_name= 'song_list.html',
                             #'template_object_name'= 'Song',
                             #'extra_context'= {'song_list': song.objects.all}
                             )

def find_similar_songs_by_tag(request):
    """ User selects song and/or tags; djukebox returns songs with semantically similar tags """


    # hardcoding some tags in for now, while testing this.......
    # similarities among tags below:
    #  types: punk/classical
    #  my own: eargasm/ugh 
    #  sleep/chill
    #  sad/depressing/melancholy    .... so tag 'sad' is more similar to 'melancholy' than to 'depressing,' I guess. 
    #  happy/energizing
    #  opposites: chill, energizing

    tags_songs = { 
        "song1name":"punk",\
        "song2name":"classical", \
        "song3name":"ugh", \
        "song4name":"eargasm",\
        "song5name":"sleep",\
        "song6name":"chill",\
        "song7name":"depressing",\
        "song8name":"sad",\
        "song9name":"melancholy",\
        "song10name":"happy",\
        "song11name":"energizing",\
        "a": "inspiring",\
        "b": "joyful",\
        "c": "soothing",\
        "d": "dark",\
        "e": "moody",\
        "f": "boring",\
        "g": "acoustic",\
        "h": "discordant",\
        "i": "up-tempo",\
        "j": "indie",\
        "k": "alternative",\
        }


    # commenting out below for now, just want the above to show up on the page
    """
    with Timer():
        res = {}
        for tag_word1 in tags_songs.values():
            for tag_word2 in tags_songs.values():
                # if tags are not same and this pair has not been compared already
                if (tag_word1 != tag_word2) and ((tag_word1,tag_word2) not in tags_songs.keys()):
                    print "........ comparing %s and %s: " % (tag_word1, tag_word2)
                    # store results in res dict, where keys are word1,word2(in alpha order) tuple pairs and vals are scores
                    # (so this is pretty terrible, overwriting prev vals, etc. )

                    t = tuple(sorted([tag_word1,tag_word2]))
                    #print "here's t and its type: ",t,"-----------", type(t)
                    if t not in res.keys():
                        # commenting out hso -hso does not give results as good as vector_pairs!
                        #measure = measure_from_web_interface(tag_word1,tag_word2,"hso")  
                        measure = measure_from_web_interface(tag_word1,tag_word2,"vector_pairs")
                        if measure:
                            res[t] = measure
                print "-------------- end for loop in main ---------------------------------------------------------"

        # sort on score
        l = sorted( (float(res[key]),key) for key in res.keys())

        return HttpResponse(l)
        """

    # get chosen tags and pass them along
    chosen_tags = None
    if request.POST:
        if 'tagSelectionField' in request.POST:
            chosen_tags = request.POST.getlist('tagSelectionField')  # do getlist - otherwise you'll only get the first val...
    return render_to_response('sim_tags.html', {'tags_songs': tags_songs, 'chosen_tags':chosen_tags}, context_instance=RequestContext(request))

#def covers(request):
    """ Cover flow """

# if not logged in, send to login page that's defined in settings,
@login_required
def send_to_profile(request):
    if not request.user.is_authenticated():  # if not logged in... not required, sort of a safety net thing (right?)
        return HttpResponseRedirect('login/')
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
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username =username,email = email, password = password)
            user.save()  # save user object

            ##################################################################
            # so setting owner = user.get_profile() -- this is what ties 
            # together the User and the Owner...right?
            ##################################################################
#            owner =user.get_profile()  # Can call this method against a user to get their owner object that's attached
                    # remember AUTH_PROFILE_MODULE='owner.Owner' in settings.py..... 

            owner = Owner(user=user, name=form.cleaned_data['name'], birthday=form.cleaned_data['birthday'])
            owner.save()     # so this is in place of automatically creating the profile...  we have to set birthday when we create the object ??????????????
            #########################################################################
            # after sucessfully registering, get logged in --  and go back, or home
            #########################################################################
            this_owner = authenticate(username =username, password=password)
            login(request, this_owner)    # Is this okay?   Secure??????
            go_back = request.path_info.rsplit("/",2)[0]  # get everything but last element of the URL + trailing "/",
            #####################################################################
            # TO DO -- that trailing slash may not be there!!!  Do this smarter.
            #####################################################################
            if not go_back:
                go_back = "/" # go home, or you just came from home  (so this is in case there's no initial forward slash)
            return redirect(go_back)
            #return HttpResponseRedirect('/profile/')
        else:  # form doesn't validate
            return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
    else: # user is not trying to submit the form, show them a blank registration form
        form = RegistrationForm()
        context = {'form':form}
        return render_to_response('register.html',context,context_instance=RequestContext(request))


def loginRequest(request):
    # when this is called via url, not through trying to submit the form (right?)
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/') # so can't login twice (although I think registration form will
     # complain about duplicate entries)

    # unlike above, this would happen when actual button-clickage is happening
    if request.method == 'POST':  # if user is trying to log in right now
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # when you log someone in:  (1) call authenticate, then (2) call login
            # return a user object if password is valid, otherwise returns null
            owner = authenticate(username =username, password=password)   

            if owner is not None:   # authentication succeeded
                login(request, owner)

                #############################################################################
                # after logging in, go back to where you came from, or to "/"
                #############################################################################
                go_back = request.path_info.rsplit("/",2)[0]  # get everything but last element of the URL + trailing "/",
                #####################################################################
                # TO DO -- that trailing slash may not be there!!!  Do this smarter.
                #####################################################################
                if not go_back:
                    go_back = "/" # go home, or you just came from home  (so this is in case there's no initial forward slash)
                return redirect(go_back)



                #return HttpResponseRedirect('/')  # no, not to "/"... stay .. "there"
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

    #####################################################################
    # after logging in/out/registering, go back to where you came from.
    #####################################################################
    # Since the login, logout (and other associated) URLs look like this:
    # urls.py:
    #    url(r'^login/$',views.loginRequest),
    # templates:
    #    e.g. href='login/'   (not href='/login/')
    # settings.py:
    #     LOGIN_URL = 'login/'  (vs LOGIN_URL = '/login/')
    # (i.e. to login, the URL just sticks on "login" to the existing URL),
    # we know the path we just came from is this one minus the last element:
    go_back = request.path_info.rsplit("/",2)[0]  # get everything but last element of the URL + trailing "/",
    #####################################################################
    # TO DO -- that trailing slash may not be there!!!  Do this smarter.
    #####################################################################
    if not go_back:
        go_back = "/" # go home, or you just came from home  (so this is in case there's no initial forward slash)
    return redirect(go_back)




#####################################################################
#####################################################################
# testing finding similar songs by comparing tags semantically
#####################################################################
#####################################################################

"""  Go with vector_pairs.   
Getting rid of a bunch of stuff in here; old crap is in archive1.sem_sim_test.py
(comparisons at end of file of archive1.sem_sim_test.py)

http://search.cpan.org/dist/WordNet-Similarity/doc/intro.pod. 
Web interface takes forever.......   52 minutes at one point for hso. only 5 min for vector_pairs, though, but that's still way too long

so ************************** use wordnet_sim_sample.pl ****************************
""" 


class Timer():
    def __enter__(self): self.start = time.time()
    def __exit__(self, *args): 
        sec  = time.time()-self.start
        mins  = sec/60.0
        print "(Timer) That took: %f min (%f sec)" % (mins,sec)


def measure_from_web_interface(word1, word2,method):
    """ Returns hso or vector pairs (Gloss Vector (pairwise))  similarity/relatedness of two words
        The ted pedersen himself said: ' There is also a web interface you could access - you could presumably write a python client to query the web interface to get the lesk or vector values.  You can find those web interfaces here...
http://marimba.d.umn.edu http://talisker.d.umn.edu'

    'This measure (hso) works by finding lexical chains linking the two word senses. There are three classes of relations that are considered: extra-strong, strong, and medium-strong. The maximum relatedness score is 16.'

    method =  currently, specify 'hso' or 'vector_pairs'
    """

    # method must be a specific thing, check for it..........
    
    # build the url 
    # method is 'hso' or 'vector_pairs'
    if method=='hso':  root_node_option='&rootnode=yes'
    elif method=='vector_pairs': root_node_option=''
    url =  "http://talisker.d.umn.edu/cgi-bin/similarity/similarity.cgi?word1=%s&senses1=all&word2=%s&senses2=all&measure=%s%s" % (word1,word2,method,root_node_option)
        
    #
    # tried this assuming that every tag is an adjective for now (%23a)
    #         #   note that I picked hso from results that did NOT specify pos (see the stuff above comparing happy, sad, etc. )
    #             url =
    #             "http://talisker.d.umn.edu/cgi-bin/similarity/similarity.cgi?word1="+word1+"%23a&senses1=all&word2="+word2+"%23a&senses2=all&measure=hso"
    # but.........  that made things worse. 

    #print url,"\n"
    # retrieve the html
    print "...............................  urlopening ...................."
    with Timer():
        h = urllib.urlopen(url)
    print " DONE...............................  urlopening ...................."
    res_html = h.read()
    h.close()


    ######################  ugh. so. slow.  (52 minutes for only about 20 tags!!!!)
    # how long did vector_pairs take?  ______________ (same number of tags)   (but later in the day....  maybe their server load is better right now)
    #  or you could just freaking use the perl module and call it from python. it's not that scary. 
    #  yeah, time to recall perl. 
    #########  so note - see gray sticky -- downloading crap right now for that. ################

    ######## to do #########
    # So this is taking FOREVER. 
    #     How about:  don't just get html every time, SAVE *RESULT* TO DISK.
    #     So check if you already have an hso value for the tag pair. if don't have the results for that one, THEN go out to the web. 
    #     Hey, guess what. nice way to implement memoization, @cached, etc. but first, the ez way: 
    # if (tag1_word,tag2_word) not in result_cache:
    #   same as above, except before returning put the val in the result_cache
    #   return same as above
    # else:
    #   return result_cache[(tag1_word,tag2_word)]
    #   # but actually the @cache thing should be decorating this def, so in main, right?
    #   


    # Just look in the html and find the hso score, which is follows search_str and is followed by a period. 
    search_str = "</a> using %s is " % method
    pos = res_html.find(search_str)
    remainder = res_html[pos:]

    end_pos = remainder.find(".</p>")# look just in remainder of html for the period, which follows the number
    print "\tpos,end_pos:\t\t", pos, end_pos, 
    if (pos != -1) and (end_pos != -1):
        meas=remainder[len(search_str):end_pos] # should pick out the hso number
    else:
        meas = -1
    print "\t%s: \t\t:%s " % (method,meas)
    return meas


