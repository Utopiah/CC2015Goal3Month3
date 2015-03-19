""" Module to make new personnalized mix for focus """

from __future__ import unicode_literals
from random import shuffle
import os
import requests
import json
import youtube_dl
from glob import glob
from pydub import AudioSegment
import argparse

# Youtube dl code form https://github.com/rg3/youtube-dl/blob/master/README.md#readme
class YTDL_MyLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)

def YTDL_Hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    #server blocked on ipv6 must force ipv4
    'source_address' : '5.39.79.30',
    #'nocheckcertificate': True,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': YTDL_MyLogger(),
    'progress_hooks': [YTDL_Hook],
}

def download_item_from_id(item_id):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['http://www.youtube.com/watch?v=' + item_id])

def fake_download_item_from_id(item_id):
    print "Fake download of", item_id

def item_sort(my_items):
    shuffle(my_items)
    return my_items
    # use instead heuristics 
    # e.g. average song BPM peak at 70% of target time then slow down

def get_related(item_id):
    related_items_ids = []
    req = requests.get("http://gdata.youtube.com/feeds/api/videos/" + item_id + "/related?v=2&alt=jsonc")
    data = json.loads(req.text)
    for item in data['data']['items']:
        related_items_ids.append(item['id'])
    return related_items_ids

def item_details(item):
    detailed_item = {}
    for element in item:
        if element == 'title':
            print element, item[element].encode('ascii', 'ignore')
            detailed_item['title'] = item[element].encode('ascii', 'ignore') 
        if element == 'id':
            print element, item[element]
            detailed_item['id'] = item[element]
        if element == 'duration':
            print element, item[element]
            detailed_item['duration'] = item[element]
        # problem with recorded
        """
        if element == 'recorded':
            pass
        if element == 'title' or element == 'description':
            print element, last[element].encode('ascii', 'ignore')
        else:
            print element, last[element]
        """
    return detailed_item

def item_details_by_id(item_id):
    req = requests.get("http://gdata.youtube.com/feeds/api/videos/" + item_id + "?v=2&alt=jsonc")
    data = json.loads(req.text)
    return item_details(data['data'])

def not_dupe(item_id):
    # assuming files are download in the current directory
    # and contain the id in their filename
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if item_id in f:
            return False
    return True

def mix_songs_by_id(mymix,i):
    print "mixing %s with %s" % (mymix, i)
    mixed = mymix + "/" + i
    return mixed

class Creations(object):
    """ Class that handles the creations of new mix """

    def __init__(self):
        pass

    def load_older(self):
        """ Load the previous mixes with their meta-data """
        # cf ../CC2015Goal3Month1/BlendMeAPicture.py using pickle
        pass

    def make_new(self):
        """ Generate a new creation """
        pass

    def respect_structure(self):
        """ Verify that a creation follows a set of predefined patterns """
        pass

    def save_new(self):
        """ Save the new creation with its meta-data in order
            to make sure the next execution will make something different """
        # cf ../CC2015Goal3Month1/BlendMeAPicture.py using pickle
        pass

class Library(object):
    """ Class that handles songs that will be part of a mix """

    def __init__(self):
        pass

    def load_items_from(self):
        """ Load the songs that were already used before in a library """
        # cf ../CC2015Goal3Month1/BlendMeAPicture.py using pickle
        pass

    def extend(self):
        """ Use multiple sources with several criteria
            to find a song not yet present in the library and add it """
        pass

    def blend_items_from(self):
        """ Blend sequentially two songs from the library based on meta-data of both
            and of the expected structure of the overall mix """
        pass

    def find_similar_item_from(self):
        """ Find anoter song from the library similar to a providing song
            and a similarity criteria """
        pass

    def modify_item_from(self):
        """ Modify a song in order to make it better fix
            within surrounding songs and overall mix """
        pass

    def save_items_to(self):
        """ Save items to library after it has been extended """
        # cf ../CC2015Goal3Month1/BlendMeAPicture.py using pickle
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Module to make new personnalized mix for focus")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose, display plenty of debugging and testing information")
    parser.add_argument("-d", "--duration", type=int, default=25,
                        help="Duration of the mix in minutes, e.g. 25 (Default)")
    parser.add_argument("-t", "--theme", default="focus",
                        help="Theme of the mix, e.g. focus (default)")
    parser.add_argument("-ms", "--music-style", default="minimal",
                        help="Style of the music, e.g. minimal (default)")
    parser.add_argument("-ft", "--favourite-tune", default="Anja Schneider - Cascabel",
                        help="Favourite tune used a seed to search for similar songs, e.g. Anja Schneider - Cascabel (default)")
    parser.add_argument("-vl", "--veto-list", default="Bieber, Vivaldi",
                        help="Lists of songs that must be excluded separated by coma, e.g. Bieber, Vivaldi (default)")
    args = parser.parse_args()
    if args.verbose:
        print "We picked a duration of %d" % args.duration
        print "We picked a theme of %s" % args.theme
        print "We picked a music style of %s" % args.music_style
        print "We picked a favourite tune of %s" % args.favourite_tune
        print "We picked a veto list of %s" % args.veto_list

    duration = 15
    # shorter for testse
    favouritetune = args.favourite_tune
    url_top10_for_search_text = "http://gdata.youtube.com/feeds/api/videos?max-results=10&orderby=viewCount&v=2&alt=jsonc&q=" + favouritetune
    # would be safer to remove very long songs wihch are most likely mix
    # https://developers.google.com/youtube/2.0/developers_guide_protocol#durationsp
    req = requests.get(url_top10_for_search_text)
    data = json.loads(req.text)
    
    """
    idtoexplorefrom = 0
    for item in data['data']['items']:
        if favouritetune in item['title']:
            idtoexplorefrom = item['id']
        if idtoexplorefrom == 0:
            idtoexplorefrom = item['id']
    mysongs = get_related(idtoexplorefrom)
    for song_id in mysongs:
        detailed_item = item_details_by_id(song_id)
        #title = "this is - mysong"
        #currentitle = "this is - another of mysong"
        #all(wordfromtitle in currentitle.split() for wordfromtitle in title.split())
        # remove songs that are dupe based on title
        # remove songs when a same artist threshold is passed (e.g. 30% from same artist)
        if not_dupe(song_id) or detailed_item['duration'] > 3*60 or detailed_item['duration'] < 9*60 :
        # remove song too short (duration < 3*60
            # fake_download_item_from_id(song_id)
            download_item_from_id(song_id)
    mixorder = item_sort(mysongs)
    mymix = mixorder[0]
    for i in range(1,len(mixorder)):
        mymix = mix_songs_by_id(mymix,mixorder[i])
    """

    playlist_songs = [AudioSegment.from_mp3(mp3_file) for mp3_file in glob("*.mp3")]
    first_song = playlist_songs.pop(0)
    # let's just include the first 30 seconds of the first song (slicing
    # is done by milliseconds)
    beginning_of_song = first_song[:30*1000]
    playlist = beginning_of_song
    for song in playlist_songs:
        # We don't want an abrupt stop at the end, so let's do a 10 second crossfades
        playlist = playlist.append(song, crossfade=(10 * 1000))
    # let's fade out the end of the last song
    playlist = playlist.fade_out(30)
    # hmm I wonder how long it is... ( len(audio_segment) returns milliseconds )
    playlist_length = len(playlist) / (1000*60)
    # lets save it!
    out_f = open("%s_minute_playlist.mp3" % playlist_length, 'wb')
    playlist.export(out_f, format='mp3')

# TODO rebind
# def debug(self, msg):
# def warning(self, msg):
# def error(self, msg):
# def YTDL_Hook(d):
# def download_item_from_id(item_id):
# def fake_download_item_from_id(item_id):

# def item_sort(my_items):
# def get_related(item_id):
# def item_details(item):
# def item_details_by_id(item_id):
# def not_dupe(item_id):
# def mix_songs_by_id(mymix,i):

# PROPER CLASSES
# class Creations(object):
# def __init__(self):
# def load_older(self):
# def make_new(self):
# def respect_structure(self):
# def save_new(self):

# class Library(object):
# def __init__(self):
# def load_items_from(self):
# def extend(self):
# def blend_items_from(self):
# def find_similar_item_from(self):
# def modify_item_from(self):
# def save_items_to(self):

# class songformix(object)
# def get_avg_bpm()
#    cf analysis.tempo() http://atl.me/overvie
# def normalize_multiple_songs()
#    https://github.com/jiaaro/pydub/issues/90
#    cf http://normalize.nongnu.org/ or https://gist.github.com/slhck/99020a1a54e59cf94042
#    because of http://productionadvice.co.uk/youtube-loudness/

# NO, to be done AFTER the result is sold!
# class item
#   (abstract)
# class songformix(inherit from class item)

#url_details_by_id = "http://gdata.youtube.com/feeds/api/videos/" + item_id + "?v=2&alt=jsonc"
#url_related_by_id = "http://gdata.youtube.com/feeds/api/videos/" + item_id + "/related?v=2&alt=jsonc"
#url_top10_for_search_text = "http://gdata.youtube.com/feeds/api/videos?max-results=10&orderby=viewCount&v=2&alt=jsonc&q=" + searchtext
#url_top_rated_global = "http://gdata.youtube.com/feeds/api/standardfeeds/top_rated?v=2&alt=jsonc"
# url = "http://gdata.youtube.com/feeds/api/videos?orderby=viewCount&v=2&alt=jsonc"
# from https://github.com/jiaaro/pydub#installation
