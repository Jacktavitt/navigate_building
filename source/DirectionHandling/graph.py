import sys
import time

# this class uses the concepts of supernodes for direction generation, not path traversal
class AllNodes(object):
    '''
    simpler node structure with 'supernode' meta data instead of logical hierarchy. 
    '''
    # def __init__(self):
        # self.generateDB()
    

    __nodes__= {
        100:{'N':0,'adj':{0:1},'S':None,'E':None,'W':None, 'type':'intersection'},
        101:{'N':10,'S':7,'adj':{7:1,10:1,40:1,30:1},'W':40,'E':30,'type':'intersection'},
        102:{'N':20,'S':17,'adj':{17:1,20:1},'E':None,'W':None,'type':'intersection'},
        103:{'N':None,'S':25,'adj':{25:1},'E':None,'W':None,'type':'intersection'},
        104:{'N':None,'S':None,'E':35,'adj':{35:1},'W':None,'type':'intersection'},
        105:{'N':None,'S':None,'E':None,'W':45,'adj':{45:1},'type':'intersection'}, 
        0: {'E': None,'W': None,'N':1,'S': 100,'adj':{1:1,100:1},'name': 0,'type': 'exit', 'hall':1000},
        1: {'E': '242', 'N': 2, 'S': 0, 'W': '241','adj':{2:1,0:1}, 'name': 1, 'type': 'node', 'hall':1000},
        2: {'E': '244', 'N': 3, 'S': 1, 'W': '243','adj':{ 3:1,1:1},'name': 2, 'type': 'node', 'hall':1000},
        3: {'E': '246', 'N': 4,'S': 2, 'W': '245', 'adj':{4:1,2:1}, 'name': 3, 'type': 'node', 'hall':1000},
        4: {'E': None, 'N': 5, 'S': 3, 'W': '247','adj':{5:1,3:1}, 'name': 4, 'type': 'node', 'hall':1000},
        5: {'E': '248', 'N': 6,'S': 4, 'W': '249', 'adj':{6:1,4:1}, 'name': 5, 'type': 'node', 'hall':1000},
        6: {'E': '250', 'N': 7, 'S': 5, 'W': '251', 'adj':{7:1,5:1},'name': 6, 'type': 'node', 'hall':1000},
        7: {'E':None,'W':None,'S':6,'N':101,'adj':{ 6:1,101:1},'name': 7, 'type': 'exit', 'hall':1000},
        10: {'E':None,'W':None,'N':11,'S':101,'adj':{11:1,101:1},'name': 10,'type': 'exit', 'hall':1001},
        11: {'E': '262', 'N': 12, 'S': 10, 'W': '263', 'adj':{12:1,10:1},'name': 11, 'type': 'node', 'hall':1001},
        12: {'E': '260', 'N': 13, 'S': 11, 'W': '261', 'adj':{13:1,11:1},'name': 12, 'type': 'node', 'hall':1001},
        13: {'E': '258', 'N': 14, 'S': 12, 'W': '259', 'adj':{14:1,12:1},'name': 13, 'type': 'node', 'hall':1001},
        14: {'E': '256', 'N': 15, 'S': 13, 'W': '257', 'adj':{15:1,13:1},'name': 14, 'type': 'node', 'hall':1001},
        15: {'E': '254', 'N': 16, 'S': 14, 'W': None,'adj':{ 16:1,14:1},'name': 15, 'type': 'node', 'hall':1001},
        16: {'E': '252', 'N': 17, 'S': 15, 'W': '255', 'adj':{17:1,15:1},'name': 16, 'type': 'node', 'hall':1001},
        17: {'E':None,'W':None,'S':16, 'N':102,'adj':{16:1,102:1},'name': 17, 'type': 'exit', 'hall':1001},
        20: {'E':None,'W':None,'N':21,'S':102,'adj':{21:1,102:1},'name': 20,'type': 'exit', 'hall':1002},
        21: {'E': '264', 'N': 22, 'S': 20, 'W': '265', 'adj':{22:1,20:1},'name': 21, 'type': 'node', 'hall':1002},
        22: {'E': '266', 'N': 23, 'S': 21, 'W': '267', 'adj':{23:1,21:1},'name': 22, 'type': 'node', 'hall':1002},
        23: {'E': '268', 'N': 24, 'S': 22, 'W': None, 'adj':{24:1,22:1},'name': 23, 'type': 'node', 'hall':1002},
        24: {'E': '270', 'N': 25, 'S': 23, 'W': '269','adj':{ 25:1,23:1},'name': 24, 'type': 'node', 'hall':1002},
        25: {'E':None,'W':None,'S':24,'N':103,'adj':{24:1,103:1},'name': 25, 'type': 'exit', 'hall':1002},
        30: {'E':None,'W':None,'N':31,'S':101,'adj':{31:1,101:1},'name': 30,'type': 'exit', 'hall':1003},
        31: {'E': '274', 'N': 32, 'S': 30, 'W': '275', 'adj':{32:1,30:1},'name': 31, 'type': 'node', 'hall':1003},
        32: {'E': '276', 'N': 33, 'S': 31, 'W': '277','adj':{ 33:1,31:1},'name': 32, 'type': 'node', 'hall':1003},
        33: {'E': '278', 'N': 34, 'S': 32, 'W': None, 'adj':{34:1,32:1},'name': 33, 'type': 'node', 'hall':1003},
        34: {'E': '280', 'N': 35, 'S': 33, 'W': '279', 'adj':{35:1,33:1},'name': 34, 'type': 'node', 'hall':1003},
        35: {'E':None,'W':None,'S':34,'N':104, 'adj':{34:1,104:1},'name': 35, 'type': 'exit', 'hall':1003},
        40: {'E':None,'W':None,'N':41,'S':101,'adj':{41:1,101:1},'name': 40,'type': 'exit', 'hall':1004},
        41: {'E': '284', 'N': 42, 'S': 40, 'W': '285', 'adj':{42:1,40:1},'name': 41, 'type': 'node', 'hall':1004},
        42: {'E': '286', 'N': 43, 'S': 41, 'W': '287', 'adj':{43:1,41:1},'name': 42, 'type': 'node', 'hall':1004},
        43: {'E': '288', 'N': 44, 'S': 42, 'W': None, 'adj':{44:1,42:1},'name': 43, 'type': 'node', 'hall':1004},
        44: {'E': '290', 'N': 45, 'S': 43, 'W': '289', 'adj':{45:1,43:1},'name': 44, 'type': 'node', 'hall':1004},
        45: {'E':None,'W':None,'S':44,'N':105, 'adj':{44:1,105:1},'name': 45, 'type': 'exit', 'hall':1004}
    }
    __bug__=False
    
    CARDINALS = ('N','S','E','W')
    LONG_CARDINALS = {'E': 'East', 'N': 'North', 'S': 'South', 'W': 'West'}
    SOUTH_WAY = {'E': 'left', 'N': 'backward', 'S': 'forward', 'W': 'right'}
    NORTH_WAY={'W': 'left', 'S': 'backward', 'N': 'forward', 'E': 'right'}
    EAST_WAY={'N': 'left', 'W': 'backward', 'E': 'forward', 'S': 'right'}
    WEST_WAY={'E': 'left', 'S': 'backward', 'W': 'forward', 'N': 'right'}
    
    DB={'241': 1,
        '242': 1,
        '243': 2,
        '244': 2,
        '245': 3,
        '246': 3,
        '247': 4,
        '248': 5,
        '249': 5,
        '250': 6,
        '251': 6,
        '252': 16,
        '254': 15,
        '255': 16,
        '256': 14,
        '257': 14,
        '258': 13,
        '259': 13,
        '260': 12,
        '261': 12,
        '262': 11,
        '263': 11,
        '264': 21,
        '265': 21,
        '266': 22,
        '267': 22,
        '268': 23,
        '269': 24,
        '270': 24,
        '274': 31,
        '275': 31,
        '276': 32,
        '277': 32,
        '278': 33,
        '279': 34,
        '280': 34,
        '284': 41,
        '285': 41,
        '286': 42,
        '287': 42,
        '288': 43,
        '289': 44,
        '290': 44,
        }
    
    def expandNode(self, node, side = 'W'):
        '''
        get the room information from the node. assumes west side.
        '''
        graphNode = self.__nodes__[node][side]
        
    def getNodeFromRoom(self, room):
        '''
        returns node of a room
        '''
        return self.DB[room]
    
    def generateDB(self):
        for node in self.__nodes__:
            if self.__nodes__[node]['W']:
                self.DB[self.__nodes__[node]['W']]=node
            if self.__nodes__[node]['E']:
                self.DB[self.__nodes__[node]['E']]=node
        print(self.DB)

    def debugPrint(self,something):
        if self.__bug__:
            print(something)
    
    def doDijkstra(self, origin, destination):
        '''
        origin and destination are the node IDS of the rooms we are after.
        sys.maxsize is used for 'inf' as lists cannot be sorted when they have a Nonetype
        '''
        Q=[n for n in self.__nodes__]
        dist={n: sys.maxsize for n in self.__nodes__}
        prev={n: None for n in self.__nodes__}


        dist[origin]=0

        while Q:
            # get guy with smallest distance value
            if self.__bug__:
                time.sleep(1)
            curN = min(Q, key=dist.get)
            self.debugPrint(str("Smallest guy in Q: {}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~".format(curN)))
            # remove him from Q
            Q.remove(curN)
            # if we've reached goal, break loop
            if curN == destination:
                self.debugPrint("destination reached!\n")
                break
            
            for node, cNdist in self.__nodes__[curN]['adj'].items():
                self.debugPrint('In adjacent nodes. Node: {}'.format(node))
                if node in Q:
                    currDist=dist[curN]+cNdist
                    self.debugPrint('Node is in Q. Current distance: {}'.format(currDist))
                    if currDist < dist[node]:
                        self.debugPrint('Updating {}. New parent is {}, new dist is {}.\n'.format(node, curN, currDist))
                        dist[node]=currDist
                        prev[node]=curN
        return dist, prev
            
    def breakPathUp(self, path):
        '''
        breaks simple path (i.e., [21, 20, 102, 17, 16, 15, 14, 13, 12, 11, 10, 101, 7, 6, 5, 4]) into nodes in hallways, and interNodes.
        returns dictionary, where keys are the steps, and values are hallways or interNodes
        '''
        newPath=[]
        interNodes=[n for n in self.__nodes__ if self.__nodes__[n]['type']=='intersection']
        splitIdxs=[path.index(n) for n in interNodes if n in path]
        # splitIdxs.append(len(splitIdxs)-1)
        splitIdxs.sort()
        idx=-1
        for s in splitIdxs:
            newPath.append(path[idx+1:s])
            newPath.append(path[s])
            idx=s
        newPath.append(path[idx+1:len(path)])
        self.debugPrint(newPath)
        dijkstraPacket={
            'oHall':newPath[0],
            'dHall':newPath[-1]
        }
        for n in range(len(newPath)):
            dijkstraPacket[n]=newPath[n]
        return dijkstraPacket
                    
    def getDirectionsFromEdsger(self, dijkPac, oRm, Drm):
        dPli = [n for n in list(dijkPac.keys()) if type(n)==int] # create list of integer keys
        dPli.sort() # sort it
        oNode= dijkPac['oHall'][0]
        dNode= dijkPac['dHall'][-1]
        # get side of room from origin to generate room near ext
        # do the same for destination
        
        # get the number of doors to pass from origin to first exit, and from last exit to destination
        
        # get directions for each intersection (right, left, etc)
        
        
        
        

        