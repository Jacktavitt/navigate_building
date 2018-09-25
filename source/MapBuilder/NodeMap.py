''' 
This will handle the logic for determining the dictionary 'map' of the rooms in a building.
Things to do:
  > Generate a dictionary of nodes, including room number and adjacent nodes.
        on exit or exception, write dictionary to a pkl file and exit.
        Should match sample dictionary from DirectionHandling/graph.py
    
'''

import pickle
import PoseAndImage as PAI


class NodeMap(object):
    ''' map class. contains functions to interact with map, to save and open it.'''

    def __init__(self, *,map=None):
        # can initialize with an existing map
        self.map = map if map else {}

    def __str__(self):
        return f'{str(self.map.keys())}'