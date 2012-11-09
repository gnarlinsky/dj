#!/usr/bin/env python

import argparse # new in 2.7 (optparse deprecated now) 
import random
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jukebox.settings")  # management.py does this
from djukebox.models import Song, Album, Artist

from nkDebugser import DebugserColors  # mine, to print colors
########################################################
#  later do all this verbose shit when you're not on a deadline 
#  (i.e. debugser only when args.verbose == True)







if __name__ == "__main__":
    d = DebugserColors() # for printing in color
    
    ########################################################
    # Define arguments
    ########################################################
    my_parser = argparse.ArgumentParser(description="Backs up previous db; populates new  db with Owner names and passwords, songs, artists, and albums)")
       # How to describe positional arguments   e.g. myprog.py 3 2 64 "hello" or some shit like that
    #   Note that the type is specified
    my_parser.add_argument("new_db_name", help="new name for backed up db (e.g. db.archive.3)", type=str)
#    my_parser.add_argument("num_owners", help="how many owners", type=int) # user should specify number of owners with an int
    my_parser.add_argument("num_artists", help="how many artists", type=int)

    # How to describe an optional argument that requires value(s) e.g.  myprog.py --thing1 3 --thing2 54354 --thing3 fu
    #   Note that the first argument is the short version of the option
    #   Note that if the song and/or album counts are specified, they refer not to the total number of songs and/or albums
    #       in the db, but PER EACH. 
    my_parser.add_argument("-al", "--num_albums",   help="how many albums PER EACH ARTIST", type=int)
    my_parser.add_argument("-s", "--num_songs",  help="how many songs PER EACH ALBUM", type=int)
    # Above, making num_songs and num_albums optional; if they're not specified, 
    # the script should just calculate these values as multiples of num_artists). 

    # How to describe an optional argument that's just a flag (e.g. -h, but that comes 'free') 
    #   This necessitates an *action*. Here, we just want to remember that the verbose option
    #   was turned on, hence "store_true"
#    my_parser.add_argument("--verbosity", help="turn on more verbose output", action="store_true")
    #   in the helper script, -v is actually for turning on debugging statements

    ################################################################
    #  HOW TO GET AT THE ARGUMENTS
    ################################################################
    # parse_args() inspects command line arguments from sys.argv; converts each arg to the right type (i.e. not strings, hello!), 
    #   and does whatever action 
    args = my_parser.parse_args() # Now args holds all the arguments, converted to the type you specified when defining the arguments above

    ########################################################
    # back up previous db; create new one
    ########################################################
   # d.dPrint("....... backup db..........","blueHilite")
   # os.system("mv db.db db_archives/%s" % args.new_db_name)  # later use sqlite backup 
    # below doing fixture crap for some reason.........
#    d.dPrint("....... syncdb..........","blueHilite")
#    os.system("python manage.py syncdb")

   ########################################################
    # What's going on.....
    ########################################################
    d.dPrint("....... see field names ............","greenHilite")
    d.dPrint("Song.__doc__   -->  ","blue");    print Song.objects.model.__doc__
    d.dPrint("Album.__doc__   -->  ","blue");   print Album.objects.model.__doc__
    d.dPrint("Artist.__doc__   -->  ","blue");  print Artist.objects.model.__doc__
 

    ########################################################
    # populate the database   -- users????????
    #
    #
    # UMMM THAT'S NOT REALLY HOW THAT WORKS. LIKE, CHANGING STUFF
    # HERE WILL OVERRIDE USER STUFF THAT I THOUGHT WAS SPECIFIED 
    # IN THE FIXTURE DB
    ########################################################
    """
    d.dPrint("....... creating users ..........","yellowHilite")
    from django.contrib.auth.models import User
    num_users = args.num_owners
    for i in range(num_users):
        #user_name = "Owner%d" % i
        user_name = "o%d" % i
#        user = User.objects.create_user(user_name, "email@alskdjflsjfsdljslkdemailland.com", "pass"+user_name) 
        password = "p%d" % i
        user = User.objects.create_user(user_name, "email@alskdjflsjfsdljslkdemailland.com", password) 
        print user_name
    # At this point, user is a User object that has already been saved
    # to the database. You can continue to change its attributes
    # if you want to change other fields.
    #>>> user.is_staff = True
    #>>> user.save()
    """

   
    ########################################################
    # (Randomly) populate the database  -- songs, etc.
    ########################################################
    d.dPrint("....... populating with Artists/Albums/Songs..........","blueHilite")

    total_songs = 0
    total_albums= 0
    num_artists = args.num_artists; d.ultPrint("num_artists","red","no_trace",(num_artists))   
    for i in range(num_artists):
        artist_name = "Artist Name %d" % i
        artist_playcount = random.randint(0,500)
        slug = artist_name+"_SLUGGIFIED, LET'S PRETEND"  # somehow slugify(artist_name)
        artistObj = Artist.objects.create(slug=slug, name=artist_name,  playcount = artist_playcount )
        print artist_name 
        
       # If the user specified album count, use that; otherwise, use random multiple 
       #    (remember, the album count for was number of albums PER ARTIST,
       #    not the total number of albums in the db
        if args.num_albums:
            num_albums = args.num_albums
        else: 
            num_albums = random.randint(1,5)
        for j in range(num_albums):
            remove = bool(random.randint(0,1))
            album_playcount = random.randint(0,artist_playcount)
            album_title = "Album Title %d-%d" % (i,j)
            slug = album_title+"_SLUGGIFIED, LET'S PRETEND"  # somehow slugify(artist_name)
            albumObj = Album.objects.create(slug=slug, \
                                            name=album_title, \
                                            artist = artistObj, \
                                            removed=remove, \
                                            playcount = album_playcount)
            total_albums= total_albums+1
            print "\t"+album_title

                            
       # If the user specified song count, use that; otherwise, use random multiple
       #    (remember, the song count for was number of songs PER ALBUM, 
       #    not the total number of songs in the db
            if args.num_songs:
                num_songs= args.num_songs
            else: 
                num_songs = random.randint(5,18)
            for k in range(num_songs):
                block = bool(random.randint(0,1)) 
                #song_name= "Song Name %d.%d.%d (removed:%s; blocked:%s)" % (i,j,k,remove,block)
                song_name= "Song Name %d-%d-%d" % (i,j,k)
                slug = song_name+"_SLUGGIFIED, LET'S PRETEND"  # somehow slugify(artist_name)
                songObj = Song.objects.create(slug = slug, \
                                                name=song_name, \
                                                album = albumObj,\
                                                blocked=block, \
                                                playcount = random.randint(0,album_playcount) )   #obviously these playcounts won't even make sense
                total_songs = total_songs+1
                print "\t\t"+song_name

    d.dPrint("....... done populating db with Song/Album/User..........","blueHilite")
    print "Song.objects: ", str(Song.objects)
    d.dPrint("\n.......<not implemented yet> Reading from actual db now.........","greenHilite")


######  so right now!!!!!!!!
# the crap below ====>  this is what you freaking need for the template, to populate that table that presenting.
#     (so get rid of it after get it together in song_list

################################################################
#       artistObj = Artist.objects.get(name="Artist name 23")
#       songObj = Song.objects.get(id=10)
#       albumObj = Album.objects.get(id=12)
#-------------------------------------------------
#   to get a list of albums for a given artist:
#       artistObj.album_set.all()
#
#   to get a list of songs for a given artist:
#       (artistObj.album_set.all()).song_set.all()
#-------------------------------------------------
#   to get a list of songs for a given album:
#       albumObj.song_set.all()
#
#   to get the artist of a given album:
#       albumObj.artist
#-------------------------------------------------
#  to get the album of a given song
#        songObj.album
#
#  to get the artist of a given song
#       (songObj.album).artist  
################################################################



    #Song.objects.filter(id=2).update(removed=0)
    ########################################################
    # print some info....
    ########################################################
    # later - connect with sqlite3, read, print easy.
    #d.dPrint("Song.objects.model.__doc__   -->  ","blue")
    #d.dPrint(" HOW MANY USERS : "+str(num_users),"redHilite")
    #d.dPrint(" HOW MANY ARTISTS: "+str(num_artists),"redHilite")
    #d.dPrint(" HOW MANY ALBUMS: "+str(total_albums),"redHilite")
    #d.dPrint(" HOW MANY SONGS TOTAL: " + str(total_songs),"redHilite")

    ########################################################
    # runserver
    ########################################################
    d.dPrint("....... runserver ..........","blueHilite")
    os.system("python manage.py runserver 8080")
    
