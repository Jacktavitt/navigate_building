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
import PoseAndImage as PAI # really necessary?


class NodeMap(object):
    ''' map class. contains functions to interact with map, to save and open it.'''

    def __init__(self, *,map=None, backupFile=None):
        # can initialize with an existing map
        self.map = map if map else {}
        self.backupFile = backupFile if backupFile else 'buildingmap.pkl'

    def __str__(self):
        return str(self.map)

    def build_simple_map(self, footage_output, look_back=4):
        ''' Reads through results of plaque-detection system and generates an
            adjacency list
            Args:
                look_back:
                    how far to look back for dup;licates. Number is 4 for the sample list
                footage_output:
                    result of simple palque detection, a list of values either None or a string value of a room number
                    sample: 
                        ['EXIT', 'EXIT', 'EXIT', 'EXIT', None, None, None, '248', '248', '248', '248', None, None, None, None, None, None, '250', '250', '250', '250', None, None, None, None, None, None, '252', '252', '252', '252', None, None, None, None, None, None, '254', '254', '254', '254', None, None, None, None, None, None, '256', '256', '256', '256', None, None, None, None, None, None, 'EXIT', 'EXIT', 'EXIT', 'EXIT', None, None, None, '257', '257', '257', '257', None, None, None, None, None, None, '255', '255', '255', '255', None, None, None, None, None, None, '253', '253', '253', '253', None, None, None, None, None, None, '251', '251', '251', '251', None, None, None, None, None, None, '249', '249', '249', '249', None, None, None, None, None, 'EXIT', 'EXIT', 'EXIT', 'EXIT', None, None, None, None, None, '248', '248', '248', '248']
                    assumes that values are normalized, i.e. no spelling errors ('EXIT', 'HXIT', etc)
        '''
        # need to look back some number to see if we are at a new node yet
        prev_room = None
        for index, value in enumerate(footage_output):
            if index < look_back:
                lb_slice = 0
            else:
                lb_slice = index-look_back
            # either this value is in the map or is not in the map
            if value in self.map:
                # either it has been recently added or is the closing of a loop or an exit
                if value in footage_output[lb_slice:index]:
                    # this room was in the last few frames, still new
                    continue
                elif value not in footage_output[lb_slice:index]:
                    # either we are closing the loop on a no-exit room or it is an exit
                    if value is 'EXIT':
                        self.name_exit(footage_output)
                    else:
                        # must close the loop JGL
                        self.map[value]['before'] = prev_room
            elif value: # not in map yet and is not None
                # must add it to the map
                if prev_room:
                    # this is not the first room
                    # but, does it matter? value of 'before' will either be the prev room or the defualt None value
                    pass
                self.map[value] = {}
                self.map[value]['before'] = prev_room
                if prev_room:
                    self.map[prev_room]['after'] = value
                prev_room = value



    def name_exit(self, footage_output):
        '''
        must rename the previous exit found in the map since we're at the other exit now
        '''
        room_before = self.map['EXIT']['before']
        room_after = self.map['EXIT']['after']
        self.map[f"{'EXIT'}-{room_before}-{room_after}"] = self.map.pop('EXIT')

    def close_loop(self, footage_output):
        '''
        complete 'hallway' by joining the duplicate room with what came before
        '''
        pass
