from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from djukebox import views   
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ############ test ##############

    # If just want a simple page, don't need to access db, etc:
    # so don't need to write your own view; this will just call song_list.html
    url(r'^$', direct_to_template, {'template': 'index.html'} ), 

    url(r'^list/$', 'djukebox.views.the_songs'),
    url(r'^simtags/$', 'djukebox.views.find_similar_songs_by_tag'),
    #url(r'^covers/$', show_covers),
    #url(r'/(?P<song_slug>.*)/$', Song),  

    ###############################################################
    # djukebox controls 
    ###############################################################
    url(r'play/$', views.increment_playcount),
    #url(r'song_change/(?P<song_id>)/$', 'djukebox.views.song_change'),  
    url(r'song_change/(\d+)/$', 'djukebox.views.song_change'),
    # following four views phased out in favor of above 
    #url(r'add_album/$', views.add_album),
    #url(r'remove_album/$', views.remove_album),
    #url(r'unblock_song/$', views.unblock_song), # Since these are checked in 
        # order, unblock_song has to come before block_song, otherwise "unblock_song" will  match on "block_song"    
    #url(r'block_song/$', views.block_song),

    ###############################################################
    #  login/out/register/user profile 
    ###############################################################
    url(r'login/$',views.loginRequest),
    url(r'logout/$', views.logoutRequest),
    #url(r'^logout/$', 'django.contrib.auth.views.logout', { 'next_page': '/list/'}   ),  
    url(r'register/$', views.ownerRegistration),
    url(r'profile/$', views.send_to_profile),
    # note - changed all these from r'^login/$', etc.

    ###############################################################
    #  password resetting 
    ###############################################################
    url(r'^resetpassword/passwordsent/$','django.contrib.auth.views.password_reset_done'), 
    url(r'^resetpassword/$','django.contrib.auth.views.password_reset'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', \
                    'django.contrib.auth.views.password_reset_confirm'),  # token gets passed to 
                    # password_reset_confirm that's generated from password reset and emailed to 
                    # the user -- which is how you validate that the user is able to reset 
                    # password for their account)
    # shows page to tell user that their password has been reset:
    url(r'^reset/done/$','django.contrib.auth.views.password_reset_complete'),  

    ###############################################################
    # admin stuff 
    ###############################################################
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
