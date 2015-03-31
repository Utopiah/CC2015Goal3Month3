""" Module to make new personnalized mix for focus """

import argparse

from Portfolio import *
from Creation import *
from Library import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Module to make new personnalized mix for focus")
    parser.add_argument("-v", "--verbose", action="store_true", default = False, 
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
    parser.add_argument("-g", "--grabber", action="store_true", default = False,
                        help="Grabber, only download songs, do not mix them together")
    parser.add_argument("-m", "--mixer", action="store_true", default = False,
                        help="Mixer, only mix songs together, do not download more")
    parser.add_argument("-tst", "--test", action="store_true", default = False,
                        help="Test, no download, no saved mixing")
    args = parser.parse_args()

    # args.duration = 15
    # shorter for tests

    if args.verbose:
        print "We picked a duration of %d" % args.duration
        print "We picked a theme of %s" % args.theme
        print "We picked a music style of %s" % args.music_style
        print "We picked a favourite tune of %s" % args.favourite_tune
        print "We picked a veto list of %s" % args.veto_list

    if args.grabber:
        if args.verbose:
            print "Grabber only, no mixing involved"
        mixer = False
    if args.mixer:
        if args.verbose:
            print "Mixing only, no grabbing involved"
        grabber = False

    # Prototype of what the class based versions could be used as
    MyPortfolio = Portfolio()
    # MyPortfolio.loadPastCreations() should be done during __init__
    # should load automatically previous creations
    MyLibrary = Library()
    # MyLibrary.loadItems() should be done during __init__
    MyCreation = Creation(MyLibrary)
    while not MyCreation.verify_novelty():
        # TODO basically the ONLY function used in this month work
        # no library proper, no portfolio proper unlike previous months
        MyCreation = Creation(MyLibrary)
        # MyLibrary.extend() called internally if not enough appropriate items
    else:
        MyPortfolio.save(MyCreation)
