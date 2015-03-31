from __future__ import unicode_literals
import requests
import json
import youtube_dl

import Item

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

class Library(object):
    """ Class that handles songs that will be part of a mix """
    storeditemsinlibrary = "itemsinlibrary.pkl"
    items = []

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

    def __init__(self):
        # should call self.load_items_from() except if ones wants to start fro scratch
        pass

    def download_item_from_id(item_id):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download(['http://www.youtube.com/watch?v=' + item_id])
    
    def fake_download_item_from_id(item_id):
        print "Fake download of", item_id
    
    def load_items_from(self):
        """ Load the songs that were already used before in a library """
        # cf ../CC2015Goal3Month1/BlendMeAPicture.py using pickle
        if os.path.isfile(self.storeditemsinlibrary):
            with open(self.storeditemsinlibrary, 'rb') as inputfile:
                self.items = pickle.load(inputfile)

    def extend(self):
        """ Use multiple sources with several criteria
            to find a song not yet present in the library and add it """
        #url_details_by_id = "http://gdata.youtube.com/feeds/api/videos/" + item_id + "?v=2&alt=jsonc"
        #url_related_by_id = "http://gdata.youtube.com/feeds/api/videos/" + item_id + "/related?v=2&alt=jsonc"
        #url_top10_for_search_text = "http://gdata.youtube.com/feeds/api/videos?max-results=10&orderby=viewCount&v=2&alt=jsonc&q=" + searchtext
        #url_top_rated_global = "http://gdata.youtube.com/feeds/api/standardfeeds/top_rated?v=2&alt=jsonc"
        # url = "http://gdata.youtube.com/feeds/api/videos?orderby=viewCount&v=2&alt=jsonc"
        # from https://github.com/jiaaro/pydub#installation
        url_top10_for_search_text = "http://gdata.youtube.com/feeds/api/videos?max-results=10&orderby=viewCount&v=2&alt=jsonc&q=" + args.favourite_tune
        req = requests.get(url_top10_for_search_text)
        data = json.loads(req.text)
        
        idtoexplorefrom = 0
        for item in data['data']['items']:
            if args.favourite_tune in item['title']:
                idtoexplorefrom = item['id']
            if idtoexplorefrom == 0:
                idtoexplorefrom = item['id']
        mysongs = self.get_related(idtoexplorefrom)
        for song_id in mysongs:
            detailed_item = item_details_by_id(song_id)
            if args.verbose:
                print detailed_item
            #title = "this is - mysong"
            #currentitle = "this is - another of mysong"
            #all(wordfromtitle in currentitle.split() for wordfromtitle in title.split())
            # remove songs that are dupe based on title
            # remove songs when a same artist threshold is passed (e.g. 30% from same artist)
            # drop lives
            if (    not_dupe(song_id)
                and (detailed_item['duration'] > 3*60 and detailed_item['duration'] < 9*60)
                and not "live" in detailed_item['title']
               ):
            # remove song too short (duration < 3*60
                # fake_download_item_from_id(song_id)
                if args.test:
                    fake_download_item_from_id(song_id)
                else:
                    download_item_from_id(song_id)
        self.items.extend(mysongs)

    def get_related(item_id):
        related_items_ids = []
        req = requests.get("http://gdata.youtube.com/feeds/api/videos/" + item_id + "/related?v=2&alt=jsonc")
        data = json.loads(req.text)
        for item in data['data']['items']:
            related_items_ids.append(item['id'])
        return related_items_ids

    def blend_items_from(self):
        """ Blend sequentially two songs from the library based on meta-data of both
            and of the expected structure of the overall mix """
        pass

    def find_similar_item_from(self):
        """ Find anoter song from the library similar to a providing song
            and a similarity criteria """
        # cf get_related()
        pass

    def modify_item_from(self):
        """ Modify a song in order to make it better fix
            within surrounding songs and overall mix """
        pass

    def save_items_to(self):
        """ Save items to library after it has been extended """
        # cf ../CC2015Goal3Month1/BlendMeAPicture.py using pickle
        with open(self.storeditems, 'wb') as output:
            pickle.dump(self.items, output, pickle.HIGHEST_PROTOCOL)
