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
        self.map = map if map else []
        self.backupFile = backupFile if backupFile else 'buildingmap.pkl'

    def __str__(self):
        return str(self.map)

    def __build_simple_map(self, door_list):
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
                        self.map[prev_room]['after'] = value
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


    def add_hallway(self, door_list):
        ''' Reads through results of plaque-detection system and generates an
            adjacency list
            Args:
                door_list:
                    result of simple palque detection, a list of values either None or a string value of a room number
                    sample: 
                        ['EXIT', 'EXIT', 'EXIT', 'EXIT', None, None, None, '248', '248', '248', '248', None, None, None, None, None, None, '250', '250', '250', '250', None, None, None, None, None, None, '252', '252', '252', '252', None, None, None, None, None, None, '254', '254', '254', '254', None, None, None, None, None, None, '256', '256', '256', '256', None, None, None, None, None, None, 'EXIT', 'EXIT', 'EXIT', 'EXIT', None, None, None, '257', '257', '257', '257', None, None, None, None, None, None, '255', '255', '255', '255', None, None, None, None, None, None, '253', '253', '253', '253', None, None, None, None, None, None, '251', '251', '251', '251', None, None, None, None, None, None, '249', '249', '249', '249', None, None, None, None, None, 'EXIT', 'EXIT', 'EXIT', 'EXIT', None, None, None, None, None, '248', '248', '248', '248']
                    assumes that values are normalized, i.e. no spelling errors ('EXIT', 'HXIT', etc)
                pointer_room:
                    name of room from prvious hallway. None defualt value indicates that this is one
                    end of the sausage link.
        '''
        hallway = {}
        # need to look back some number to see if we are at a new node yet
        prev_room = None
        for index, value in enumerate(door_list):
            # either this value is in the map or is not in the map
            if value in hallway:
                # either it has been recently added or is the closing of a loop or an exit
                ## removing code below as form of room_list should not have dupicates other than EXIT and the origin room
                # if value is prev_room:
                #     # this room was in the last few frames, still new
                #     continue
                # if value not in door_list[lb_slice:index]:
                    # either we are closing the loop on a no-exit room or it is an exit
                if value is 'EXIT':
                    self.name_exit(hallway)
                else:
                    # must close the loop JGL
                    hallway[value]['before'] = prev_room
                    hallway[prev_room]['after'] = value
                    # hallway[value]['after'] = 
            if value and not value in hallway: # not in map yet and is not None
                # must add it to the map
                # if prev_room:
                #     # this is not the first room
                #     # but, does it matter? value of 'before' will either be the prev room or the defualt None value
                #     pass
                hallway[value] = {}
                hallway[value]['before'] = prev_room
                if prev_room:
                    hallway[prev_room]['after'] = value
                    # print(f"DEBUG --> rm: {value} prev: {prev_room}")
                    # print(f"DEBUG --> map at {prev_room}: {hallway[prev_room]}")
                prev_room = value
        # TODO: compare the time required to do this once and memory to add it to list
        # versus just looking in the dynamically-generated list of keys
        # the goal of this is quick checking for hallway search when moving through
        hallway['rooms']=[list(hallway.keys())]

    # while contemplating the reworking needed to accomplish this,
    #  it occurs to me that with the same amount of work I could add "pose information"
    #  to the map, which would be closer to my desired goal.

        # # now to connect hallways
        # # TODO: this is for sausage-link hallways.
        # # this is also assuming that each hallway has a "pointer room" which is hand-labelled, that
        # # denotes a room in the previous hallway. Each time a hallway is added, look for the pointer room
        # # and set up the 'linked list' style relationship
        # # now look for a hallway with the pointer-room in its list
        # if pointer_room is None:
        #     hallway['previous hallway'] = None
        # else:
        #     for hallway in self.map:
        #         if pointer_room in hallway['rooms']:
        #             hallway['previous hallway'] = 


        # stick in the map
        self.name_exit(hallway)
        self.map.append(hallway)



    def name_exit(self, hallway):
        '''
        must rename the previous exit found in the map since we're at the other exit now
        '''
        # save the data for the old exit
        room_before = hallway['EXIT']['before']
        room_after = hallway['EXIT']['after']
        new_exit_name = f"{'EXIT'}-{room_before}-{room_after}"
        hallway[new_exit_name] = hallway.pop('EXIT')
        hallway[room_before]['after'] = new_exit_name
        hallway[room_after]['before'] = new_exit_name
