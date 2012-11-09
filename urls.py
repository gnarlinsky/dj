from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
#import pages
#import beer 
#from pages.views import *
from beer.views import *
from pages.views import *
from drinker.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


###############  from the older one ##############
#from django.conf.urls.defaults import *    # watch it, combine with above maybe
from djukebox import views   

urlpatterns = patterns('',
    (r'^songs/$', views.the_songs),  # commenting out for now while redoing login

#    (r'^login/$', views.login_user),
    #(r'^logout/$', views.logout_user),
    #(r'^thing_that_requires_login/$', views.thing_that_requires_login),  #  playing with new login
    #(r'^new_login/$', 'django.contrib.auth.views.login'),  #  playing with new login
    #(r'^logout/$', 'django.contrib.auth.views.logout', { 'next_page': '/songs/'}   ),  
    #(r'^logout/$', 'django.contrib.auth.views.logout'), 

    (r'play/$', views.increment_playcount),
    (r'songs/add_album/$', views.add_album),
    (r'songs/remove_album/$', views.remove_album),
    (r'songs/block_song/$', views.block_song),
    (r'songs/unblock_song/$', views.unblock_song),
    #(r'search/$', views.search),


    url(r'^tinymce', include('tinymce.urls')),
    url(r'^register/$', 'drinker.views.DrinkerRegistration'),  #!!! wait! why didn't this complain but beer.views.BeerAll complains!!  Is it because of the quotes?????????????
    url(r'^login/$','drinker.views.LoginRequest'), 
    url(r'^logout/$', 'drinker.views.LogoutRequest'),
    url(r'^resetpassword/passwordsent/$','django.contrib.auth.views.password_reset_done'),
    url(r'^resetpassword/$','django.contrib.auth.views.password_reset'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^reset/done/$','django.contrib.auth.views.password_reset_complete'),
    url(r'^profile/$', direct_to_template, {'template': 'profile.html'} ),

    # If just want a simple page, don't need to access db, etc:
    # so don't need to write your own view; this will just call list.html
#    url(r'^$', direct_to_template, {'template': 'list.html'} ), # so don't need to write your own view; this will just call list.html
    url(r'^$', direct_to_template, {'template': 'song_list.html'} ), # so don't need to write your own view; this will just call list.html
    #######  how do I stick Songs in here??????????   
    #url(r'^$', direct_to_template, {'template': 'list.html', 'extra_context': Songs objects.....????} ), 



    #url(r'^$', MainHomePage), # so don't need to write your own view; this will just call index.html

    url(r'^beers/$', BeerAll),  # associates BeersAll view with this URL
    url(r'^beers/(?P<beerslug>.*)/$', SpecificBeer),  # associates BeersAll view with this URL
    url(r'^brewery/(?P<breweryslug>.*)/$', SpecificBrewery),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

##############  hmmm  why does he capitalize the views again?  aren't those... just methods...? #####

#    url(r'^list/$', show_list),
    url(r'^list/$', 'djukebox.views.the_songs'),
    url(r'^covers/$', show_covers),
)
