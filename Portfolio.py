import os
import pickle
 
import Creation

class Portfolio(object):
    """ Class that handles multiple created creations over time """
    storedcreations = "storedcreations.pkl"
    creations = []

    def __init__(self):
        # could call self.load_older()
        pass

    def load_older(self):
        """ Load the previous mixes with their meta-data """
        # cf ../CC2015Goal3Month1/BlendMeAPicture.py using pickle
        if os.path.isfile(self.storedcreations):
            with open(self.storedcreatiions, 'rb') as inputfile:
                self.creations = pickle.load(inputfile)

    def make_new(self):
        """ Generate a new creation """
        pass

    def save_new(self):
        """ Save the new creation with its meta-data in order
            to make sure the next execution will make something different """
        # cf ../CC2015Goal3Month1/BlendMeAPicture.py using pickle
        with open(self.storedcreations, 'wb') as output:
            pickle.dump(self.creations, output, pickle.HIGHEST_PROTOCOL)
