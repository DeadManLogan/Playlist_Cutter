from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint
import csv
import os
import sys

'''
Inside the code I will have some basic comments in English.For more information read the
tutorial (how-to-use) on the repository, which is also in English. The code's main purpose is to 
create new smaller playlists from a "parent" playlist on Spotify. The user gives the name of an artist and the
code creates a new playlist with artist's name as playlist name. As you guessed the new playlist's
content is all the artist's songs that were found in the "parent" playlist.

DISCLAIMER: This is not the most efficient, quickest or best overall way to do it, but is my way, in my style.
I am not an experienced programmer and I'm sure it can be improved in many ways, but if we always try to
improve a project we will never stop.
'''

'''
When you open the terminal, before you run this script, type the following commands:
$ bash
$ export SPOTIPY_CLIENT_ID='xxx'
$ export SPOTIPY_CLIENT_SECRET='xxx'
$ export SPOTIPY_REDIRECT_URI='https://xxx'
for more information check the how-to-use
Also before starting you have to provide the code with a new token. You can find such token in Spotify API.
You onle need playist-modify-private and playlist-modify-public scopes. COpy it ad put it in line 100 at the
token variable. Token expires after 1 hour.
'''


'''
At this part of the code is where the user gives the artist's name. Then we scan the "parent" Spotify
playlist for items that have the given artist as creator. Then we isolate the track uri and we print it inside
the uris.csv we opened.
'''

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())     # helps us authorise through the variables we set before running

with open('uris.csv', 'w', newline = '', encoding = 'utf-8')as ofp:     # we create a csv so we can write inside it
    ow = csv.writer(ofp)        # converts the data we provide to strings for the csv    

    pl_id = 'spotify:playlist:xxx'       # the "parent" playlist's uri
    offset = 0

    ar = input("Give the name of the artist's song's uris you want: ")

    while True:
        response = sp.playlist_tracks(pl_id,        # here we ask for some items in fields=, from our playlist pl_id
                                    offset=offset,      # we can ask for many things here but right now we only need artist, track's name and uri
                                    fields='items.track.artists,items.track.name,items.track.uri,total')    # another way to format is fields='items[track][id]'
        #pprint(response["items"])      # here we can print all the response items
        offset = offset + len(response['items'])
        print(offset, "/", response['total'])

        if len(response['items']) == 0:     # we stop the response process
            break

        '''
        In the following for loop we take the response and for every item in there we can isolate and use many information. In our case we only need
        the artist's info and the track uri for each song. Then we take from the artist's info only his/her name and we check if it is the one the user
        provided us with. If it is we save the track's uri to our uris.csv.
        Any line of code you see in comments it is not mandatory for this code, but it can help you understand the code better if you decide to try yourself.
        '''

        for item in response["items"]:      # for loop for each response item,which means for each track in the parent playlist
            artist_info = item["track"]["artists"]      # we save to artist_info the artist's information about the particular song
            #track_name = item["track"]["name"]
            track_uri = item["track"]["uri"]        # we save each track's uri to the track_uri value
            for name in artist_info:        # for loop for each artist_info, we try to access each info item 
                artist = name["name"]       # we isolate the artist's name from the rest info
                if artist == ar:        # we check if it's the desirable artist name
                    print([track_uri])      #here we print the songs of a certin artist
                    ow.writerow([track_uri])        #we print the track's uri into our csv
                #print([artist])     # here we print only the name of the artists section of response['items']
            #pprint([artist_info])        # here we print only the artists section of response['items']
            #pprint([track_name])       #here we print all the track names
            #pprint([track_uri])

# makes the csv uris into a cleaner format so we can use them
word_delete = 'spotify:track:'      # here you type the word or phrase you want to delete
with open('uris.csv', 'r') as ifp:        # we open the file for read
    lines = ifp.readlines()     # organise our lines into a list
    newlines = []       # we put here our new lines
    for line in lines:
        newline = line.replace(word_delete, '')     # here we replace the word that we want to delete with nothing
        newlines.append(newline)        # we add the edited lines
with open('uris.csv', 'w') as ifp:        # we open the file for write
    ifp.writelines(newlines)        # write the new lines to csv

# create playlist
# below we use curl for new playlist which was found in Spotify api.for more info read how-to-use
# We break the curl in several pieces so we can add the artist's name inside as playlist's name.
# originally the curl from the api has "" at the start and end of each field. We changed the into '' so it can work in our code
curl1_pl = "curl -X POST 'https://api.spotify.com/v1/users/xxx/playlists' --data '{\"name\":\""       # first part of the curl. the important part is the user id
name_pl = ar        # here we set the artist's name the user gave us to playlist's name
curl2_pl = "\",\"description\":\"\",\"public\":true}' -H 'Accept: application/json' -H 'Content-Type: application/json' -H 'Authorization: Bearer "     # here we specify many things as playlist's description, if it's public or not and give some access to our account
token = "BQBgPboQ29wldtGiBFrkNs9s6vjC1zvbsPnh6suOi8EuRONCHSlofeDF5cDgfd3Jyom-YEFzsOs3L-pZ4muujP0gV9vBgbVKoYKO8LX2ydAYRSrZ36Rxq-HI3rplM9NxcdctHpoeGm9uqtNZwtgCJpBXd5_NQWXjBGJNpbPlKz2y0aBWRli0MmmLyGV2O2Fkeo0IYaddm9NevuwNNILVVy5PfCrzLRfVgcRyAdUVW-r6kP9q1AcfGo_CCiqMcyWstqinl63Ecjr-7IQE_qUDWNXLGLMWRA'"
x = (curl1_pl +
    name_pl +
    curl2_pl +
    token)      # here we build our playlist curl

curlOut01 = os.system(x)        # here we run the curl using variable x on the terminal.we create our playlist

'''
In the next part of the code we get access to users public playlists. Our goal is to find the uri of the previously created playlist.
Then we isolate each playlist's uri and store it inside playlist_uri.csv.
To get the correct playlist we check if the name of the laylist is the same from the playlist we created before.
'''

with open('playlist_uri.csv', 'w', newline = '', encoding = 'utf-8')as ofp:     # we open a new playlist_uri csv, in which we store all the uri of the public playlists of the user
    ow = csv.writer(ofp)        # converts the data we provide to strings for the csv

    user = 'xxx'      # we need to specify which user's account we will be granted access to

    if len(sys.argv) > 1:
        user = sys.argv[1]

    playlists = sp.user_playlists(user)     # we store info for user's public playlists

    while playlists:        # the following code is executed for each playlist item we got before (number of public playlists)
        for i, playlist in enumerate(playlists['items']):       # for each item in a playlist's info
            if(playlist['name'] == name_pl):        # here we check if we got the correct playlist
                print(playlist['uri'])      # we print playlist's uri on terminal
                ow.writerow([playlist['uri']])      # we store the playist's uri in csv
            print(
                "%4d %s %s" %
                (i +
                1 +
                playlists['offset'],
                playlist['uri'],
                playlist['name']))      # we print playlist's info. It is not mandatory
        if playlists['next']:
            playlists = sp.next(playlists)      # gets the next public playlist
        else:
            playlists = None        # stops if no more public playlists can be found

# makes the csv uris into a cleaner format so we can use them
word_delete = 'spotify:playlist:'       # here you type the word or phrase you want to delete
with open('playlist_uri.csv', 'r') as ifp:        # we open the file for read
    lines = ifp.readlines()     # organise our lines into a list
    newlines = []       # we put here our new lines
    for line in lines:
        newline = line.replace(word_delete, '')     # here we replace the word that we want to delete with nothing
        newlines.append(newline)        # we add the edited lines
with open('playlist_uri.csv', 'w') as ifp:        # we open the file for write
    ifp.writelines(newlines)        # write the new lines to csv

'''
Below we open the csv which contains playlist's uri and store it to a variable
'''

with open('playlist_uri.csv', 'r', newline = '',encoding = 'utf-8') as ifp:     # open the file for reading
    ir = csv.reader(ifp)

    for i, row in enumerate(ir):
        pl_uri = ', '.join(row)     # we store the csv's line of uri to pl_uri without the quotes
    print(pl_uri)       # we print the uri


# here we have the curl for adding items (tracks) to our playlist
# of course we break it into pieces for better handling
curl1 = "curl -X POST 'https://api.spotify.com/v1/playlists/"
pl_curl = pl_uri        # playlist's uri where we will add our tracks
curl2 = "/tracks?uris=spotify%3Atrack%3A"       # the prefix of curl's for each track
curl3 = "' -H 'Accept: application/json' -H 'Content-Type: application/json' -H 'Authorization: Bearer "

with open('uris.csv', 'r', newline = '',encoding = 'utf-8') as ifp:     # we open uris.csv for reading. we have finally use our uris and fill our playlist
    ir = csv.reader(ifp)

    for i, row in enumerate(ir):        # we do the next lines of code for each row
        v = (curl1 + 
            pl_curl +
            curl2 +
            ', '.join(row)+
            curl3 +
            token + '\n')       # we assemble the curl for adding tracks to playlist
        curlOut02 = os.system(v)        # we call the curl
        print(v)        # we print the curl and get the snapshot of it on the terminal