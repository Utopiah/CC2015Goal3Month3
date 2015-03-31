import os
from random import shuffle
from glob import glob
from pydub import AudioSegment
from pydub.silence import detect_nonsilent 

class Creation(object):
    """ Class that handles the creation itself """

    def __init__(self, library):

        # should be conditional
        library.extend()
        # should sort a library or part of it
        self.item_sort(library)
    
        library.blends_items()

    def item_sort(my_items):
        shuffle(my_items)
        return my_items
        # use instead heuristics 
        # e.g. average song BPM peak at 70% of target time then slow down
    
    def respect_structure(self):
        """ Verify that a creation follows a set of predefined patterns """
        pass

    def verify_novelty(self):
        """ verify that a creation is truly novel compared to other creations in the portfolio
            and outside of the portfolio """
        pass

    def normalize_multiple_songs(self):
    #    https://github.com/jiaaro/pydub/issues/90
    #    cf http://normalize.nongnu.org/ or https://gist.github.com/slhck/99020a1a54e59cf94042
    #    because of http://productionadvice.co.uk/youtube-loudness/
        pass

    def blends_items(self):
        """ Blends multiple items from the library to make a new creation """
        # TODO use dedicated dir
        ItemsDir = "ItemsLibrary"
        # TODO use only files from playlist
        # check http://stackoverflow.com/questions/26363558/pydub-concatenate-mp3-in-a-directory
        playlist_filenames = glob("*.mp3")
        playlist_songs = [AudioSegment.from_mp3(mp3_file) for mp3_file in playlist_filenames]
        # TODO check total length, limit to +/-10% of aimed duration
        first_song = playlist_songs.pop(0)
        # let's just include the first 30 seconds of the first song (slicing
        # is done by milliseconds)
        beginning_of_song = first_song[:60*1000]
        playlist = beginning_of_song
        durationsofar = 60
        comment = ""
        for i, song in enumerate(playlist_songs):
            # We don't want an abrupt stop at the end, so let's do a 10 second crossfades
            if args.test:
                print "Not actually mixing any song"
            else:
                playlist = playlist.append(song[10*1000:-20*1000], crossfade=(10 * 1000))
            # TODO detect silences in beginning and ends
            durationsofar += int(song.duration_seconds)
            filename = playlist_filenames[i]
            comment += filename[:-16] + "; "
            if args.verbose:
                print "Mixing ", filename[:-16]
                print "BPM ", get_bpm(song)
                print durationsofar, args.duration * 60
            if durationsofar > (args.duration * 60) :
                break
        # let's fade out the end of the last song
        playlist = playlist.fade_out(30)
        # hmm I wonder how long it is... ( len(audio_segment) returns milliseconds )
        playlist_length = len(playlist) / (1000*60)
        # lets save it!
        # TODO use dedicated dir
        SavingDir = "Creations"
        if args.test:
            print "File of duration %s not saved" % playlist_length
            print comment
        else:
            out_f = open("%s_minute_playlist.mp3" % playlist_length, 'wb')
            playlist.export(out_f, format='mp3',  tags={'artist': 'CC2015Goal3', 'album': 'March 2015 mix', 'comments': comment} )

    def not_dupe(item_id):
        # assuming files are download in the current directory
        # and contain the id in their filename
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            if item_id in f:
                return False
        return True
