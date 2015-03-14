""" Module to make new personnalized mix for focus """

import argparse

class Creations(object):
    """ Class that handles the creations of new mix """

    def __init__(self):
        pass

    def load_past_creations(self):
        """ Load the previous mixes with their meta-data """
        pass

    def make_new_creation(self):
        """ Generate a new creation """
        pass

    def creation_respect_structure(self):
        """ Verify that a creation follows a set of predefined patterns """
        pass

    def save_new_creations(self):
        """ Save the new creation with its meta-data in order
            to make sure the next execution will make something different """
        pass

class Library(object):
    """ Class that handles songs that will be part of a mix """

    def __init__(self):
        pass

    def load_items_from_library(self):
        """ Load the songs that were already used before in a library """
        pass

    def extend_library(self):
        """ Use multiple sources with several criteria
            to find a song not yet present in the library and add it """
        pass

    def blend_items_from_library(self):
        """ Blend sequentially two songs from the library based on meta-data of both
            and of the expected structure of the overall mix """
        pass

    def find_similar_item_from_library(self):
        """ Find anoter song from the library similar to a providing song
            and a similarity criteria """
        pass

    def modify_item_from_library(self):
        """ Modify a song in order to make it better fix
            within surrounding songs and overall mix """
        pass

    def save_items_to_library(self):
        """ Save items to library after it has been extended """
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
