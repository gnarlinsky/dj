from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from drinker.forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User
from drinker.models import Drinker
from django.contrib.auth import authenticate, login, logout

def DrinkerRegistration(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/') # send user to profile if they're already registered

    if request.method == 'POST': # if they're submitting the form...
        form = RegistrationForm(request.POST) # fill out registrationform with what's been posted

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

        else:  # form doesn't validate
            return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))

    else: # user is not trying to submit the form, show them a blank registration form
        form = RegistrationForm()
        context = {'form':form}
        return render_to_response('register.html',context,context_instance=RequestContext(request))


def LoginRequest(request):
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
            drinker = authenticate(username =username, password=password)   # return a user object if 
                            #password is valid, otherwise returns null
            if drinker is not None:   # authentication succeeded
                login(request, drinker)
                # returning this way below because already logged in... although this shouldn't actually happen, because 
                #   there's no form/submit button available to someone who is already logged in (although I think this could be faked)
                #return HttpResponseRedirect('/profile/')   
                return HttpResponseRedirect('/')  # no, not to "/"... stay .. "there" 
            else: #authentication failed
                #return HttpResponseRedirect('/login/')
                # why above no good?  Because you're going to go back and actually show the error, not just redirect to
                # login
                return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
        else:  # form not valid
            return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))

    else:  # user is not submitting the form, show the login form
            # So this wouldn't be happening through button clickage, but via url, like the first thign above, except that this time user is NOT
            # authenticated.....
            # yeah you might want to reorder these three things here... 
        form = LoginForm()
        context = {'form':form}
        return render_to_response('login.html', context, context_instance=RequestContext(request))


def LogoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/')
