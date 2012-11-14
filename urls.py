from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
#from pages.views import *
#from beer.views import *
#from drinker.views import *
from djukebox import views   
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # If just want a simple page, don't need to access db, etc:
    # so don't need to write your own view; this will just call list.html
#    url(r'^$', direct_to_template, {'template': 'list.html'} ), # so don't need to write your own view; this will just call list.html
    url(r'^$', direct_to_template, {'template': 'song_list.html'} ), # so don't need to write your own view; this will just call song_list.html
    #url(r'^$', MainHomePage), # so don't need to write your own view; this will just call index.html
    #######  how do I stick Songs in here??????????   
    #url(r'^$', direct_to_template, {'template': 'list.html', 'extra_context': Songs objects.....????} ), 

#    url(r'^list/$', show_list),
    url(r'^list/$', 'djukebox.views.the_songs'),
    #url(r'^covers/$', show_covers),

    ###############################################################
    # djukebox controls 
    ###############################################################
    #  these need to be consistent!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!  fix !!!!!!!!!!!!!!!!!!!!!!!!
    url(r'play/$', views.increment_playcount),
    url(r'add_album/$', views.add_album),
    url(r'list/remove_album/$', views.remove_album),
    url(r'/block_song/$', views.block_song),
    url(r'/unblock_song/$', views.unblock_song),

    ###############################################################
    #  login/out/register/user profile 
    ###############################################################
    url(r'^login/$',views.loginRequest), 
    url(r'^logout/$', views.logoutRequest),
    url(r'^register/$', views.ownerRegistration),  
#    url(r'^profile/$', direct_to_template, {'template': 'profile.html'} ),
    (r'^profile/$', views.profile),

    ###############################################################
    #  password resetting 
    ###############################################################
    url(r'^resetpassword/passwordsent/$','django.contrib.auth.views.password_reset_done'), 
    url(r'^resetpassword/$','django.contrib.auth.views.password_reset'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),  # token gets passed to password_reset_confirm that's generated from password reset and emailed to the user... how we validate that the user is able to reset password for a given account
    url(r'^reset/done/$','django.contrib.auth.views.password_reset_complete'),  #shows page to tell user that their password has been reset. 



    ###############################################################
    # admin stuff 
    ###############################################################
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    ###############################################################
    # ignore us
    ###############################################################
    #(r'search/$', views.search),
    #(r'^tinymce', include('tinymce.urls')),
    #(r'^login/$', views.login_user),
    #(r'^logout/$', views.logout_user),
    #(r'^thing_that_requires_login/$', views.thing_that_requires_login),  #  playing with new login
    #(r'^new_login/$', 'django.contrib.auth.views.login'),  #  playing with new login
    #(r'^logout/$', 'django.contrib.auth.views.logout', { 'next_page': '/songs/'}   ),  
    #(r'^logout/$', 'django.contrib.auth.views.logout'), 
    #url(r'^beers/$', BeerAll),  # associates BeersAll view with this URL
    #url(r'^beers/(?P<beerslug>.*)/$', SpecificBeer),  # associates BeersAll view with this URL
    #url(r'^brewery/(?P<breweryslug>.*)/$', SpecificBrewery),
)
