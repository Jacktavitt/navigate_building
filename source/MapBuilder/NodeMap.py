#!/usr/bin/env python3
''' 
This will handle the logic for determining the dictionary 'map' of the rooms in a building.
Things to do:
  > Generate a dictionary of nodes, including room number and adjacent nodes.
        on exit or exception, write dictionary to a pkl file and exit.
        Should match sample dictionary from DirectionHandling/graph.py
    
'''

import pickle
import cv2
import PoseAndImage as PAI


class NodeMap(object):
    ''' map class. contains functions to interact with map, to save and open it.'''

    def __init__(self, *,map=None, backupFile=None):
        # can initialize with an existing map
        self.map = map if map else {}
        self.backupFile = backupFile if backupFile else 'buildingmap.pkl'

    def __str__(self):
        return f'{str(self.map.keys())}'

    def buildMap(self, image):
        ''' Checks image for a labelled plaque.
            If contains a plaque, and label is novel, add a new node.
            if an error occurs, pickle the map and save to backup file.
            Args:
                image: cv2-style numpy array image
        '''
        pass

