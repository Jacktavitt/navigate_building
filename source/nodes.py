import math
import time
import random
from bisect import bisect_left
    
class SimpleNode(object):

    def __init__(self):
        self.makeGraph()
        pass
        
    def makeNodes(self):
        Oberlist={}
        for n in self.POSE_INFO:
            Oberlist[n] = self.genSimpleNode(n)
        return Oberlist
            
    
    def getAdjacent(self,id):
        '''
        assumes no cycle.
        '''
        place= self.ID_LIST.index(id)
        a1 = None if place == 0 else self.ID_LIST[place-1] 
        a2 = None if place == len(self.ID_LIST)-1 else self.ID_LIST[place+1] 
        return [a1,a2]
    
    def genSimpleNode(self,id):
        return {
            'name': id,
            'holds': self.POSE_INFO[id],
            'adj': self.getAdjacent(id)
        }
        
    def getNodeFromName(self,name):
        return self.GRAPH[name]
        
    def getNodeFromHolds(self,name):
        for n in self.GRAPH:
            if name in self.GRAPH[n]['holds']:
                return self.GRAPH[n]
                
    def traverse(self, origin, destin):
        '''
        assuming both destin and origin are in graph
        '''
        path=[]
        currN= origin
        while currN != destin:
            # expand neighbors
            n1,n2 = self.getAdjacent(currN['name'])
            currN = self.closerNode(self.getNodeFromName(n1),self.getNodeFromName(n2),destin)
            path.append(currN)
        return path

        
    def closerNode(self,node1, node2, dNode):
        '''
        uses simple heuristic
        '''
        closer = node1 if (abs(dNode['name']-node1['name']) < abs(dNode['name']-node2['name'])) else node2
        return closer
        
    def makeGraph(self):
        '''
        POSE_INFO consists of tuples of adjacent rooms.
        rooms at index 0 are on one side of the hall, index 1 are the other. (subject to change)
        '''
        self.GRAPH = self.makeNodes()
        
    def calcNumDoors(self,path,side):
        dCount = 0
        for n in path:
            if n['holds'][side] != None:
                dCount +=1
        return dCount
        
    def genDirString(self, destination, dSideDist, sideChange):
        sc = "Go to the other side of the hallway. " if sideChange else ''
        dstr = "{}Proceed {} doors down the hallway and arrive at your destination, room {}.".format(sc, dSideDist, destination)
        return dstr
        
    # POSE_INFO holds ids for the room(s) found and the node ID for that spot... maybe gen from pose    
    POSE_INFO = {
        0:('exit',None), # do this for other pose infos
        1:('262','263'),
        2:('260','261'),
        3:('258','259'),
        4:('256','257'),
        5:('254',None),
        6:('252','255'),
        7:('exit',None)
        }
     # sample with four: 7:('intersection')
    ID_LIST = list(POSE_INFO.keys())
    GRAPH = None

class SecondStateNode(SimpleNode):
    '''
    (N,S,E,W)
    '''
    
    def __init__(self):
        self.makeGraph()
        self.patchExitNode()
        self.distillExits()
        self.genDB()
        
    def makeGraph(self):
        '''
        POSE_INFO consists of tuples of adjacent rooms.
        rooms at index 0 are on one side of the hall, index 1 are the other. (subject to change)
        '''
        id = 0
        for n in self.POSE_COLLECTION:
            namestr = 'h'+str(id)
            self.GRAPH[namestr] = self.makeNodes(n)
            id +=1
        
    def makeNodes(self, POSE_INFO):
        Oberlist={}
        Oberlist['holds'] = list(POSE_INFO.keys())
        for n in POSE_INFO:
            # Oberlist[n] = self.gen2ndStateNode(n,POSE_INFO) if POSE_INFO[n][-1] != 'exit' else self.genExitNode(n, POSE_INFO) 
            Oberlist[n] = self.gen2ndStateNode(n,POSE_INFO)
            if POSE_INFO[n][-1] == 'exit':
                Oberlist[n]['type'] = 'EXIT'
        return Oberlist
        
    def gen2ndStateNode(self,id,POSE_INFO):
        return {
            'name': id,
            'type': 'node',
            'N': POSE_INFO[id][0],
            'S': POSE_INFO[id][1],
            'E': POSE_INFO[id][2],
            'W': POSE_INFO[id][3]
        }
        
    def patchExitNode(self):
        # get a list of all exits, a shallow copy that will change the actual node
        exits=[]
        for h in self.GRAPH:
            for n in self.GRAPH[h]:
                if n != 'holds' and self.GRAPH[h][n]['type'] == 'EXIT':
                    self.GRAPH[h][n]['abuts'] = [h]
                    exits.append(self.GRAPH[h][n])
                    
        # now must set the NSEW to correct hallways, instead of just a room node
        # first pass, as only item in 'abuts' is the hallway itself
        for ex in exits:
            for dir in ('N','S','E','W'):
                if bool(ex[dir]):
                    ex[dir] = ex['abuts']
        
        return exits

    def getContainingHallways(self, oID,dID,aGraph):
        orH = None
        dsH = None
        for n in aGraph:
            if type(n)==int:
                if oID in aGraph[n]['holds']:
                    orH = n
                if dID in aGraph[n]['holds']:
                    dsH = n
        return orH, dsH
        
    '''
    exits are here manually joined, but must be generated automatically in future.
    they are nodes in their own right(???)
    '''
    H1_POSE_INFO = {
        0:(1,None,None,None,'exit'), 
        1:(2,0,'242','241'),
        2:(3,1,'244','243'),
        3:(4,2,'246','245'),
        4:(5,3,None,'247'),
        5:(6,4,'248','249'),
        6:(7,5,'250','251'),
        7:(None,6,None,None,'exit')
        }
    H2_POSE_INFO = {
        10:(11,None,None,None,'exit'), 
        11:(2,0,'262','263'),
        12:(3,1,'260','261'),
        13:(4,2,'258','259'),
        14:(5,3,'256','257'),
        15:(6,4,'254',None),
        16:(7,5,'252','255'),
        17:(None,16,None,None,'exit')
        }
    H3_POSE_INFO = {
        20:(21,None,None,None,'exit'), 
        21:(2,0,'264','265'),
        22:(3,1,'266','267'),
        23:(4,2,'268',None),
        24:(5,3,'270','269'),
        25:(None,24,None,None,'exit')
        }
    
    POSE_COLLECTION = [H1_POSE_INFO,H2_POSE_INFO,H3_POSE_INFO]
    
     # sample with four: 7:('intersection')
    H1_ID_LIST = list(H1_POSE_INFO.keys())
    H2_ID_LIST = list(H2_POSE_INFO.keys())
    H3_ID_LIST = list(H3_POSE_INFO.keys())
    
    GRAPH = {}
    
    # this sample graph is artificially patched to join exits. THIS MUST BE DONE IN SCRiPT!!!
    # this graph acts as a 'floor' and so can be viewed as a node in itself.
    # '100001' are placeholders for none-existent hallways that will fail the simple heuristic.
    # NH vs N: H stands for hallway. Since these are also regular nodes, they have relationship to other nodes in hallway.
    __sampleGraph__= {
        1000:{   
            0: {'EH': None,'E':None,'W':None,'N':1,'S': None,'NH': 1000,'SH': 100001,'WH': None,'name': 0,'type': 'EXIT', 'hall':1000},
            1: {'E': '242', 'N': 2, 'S': 0, 'W': '241', 'name': 1, 'type': 'node', 'hall':1000},
            2: {'E': '244', 'N': 3, 'S': 1, 'W': '243', 'name': 2, 'type': 'node', 'hall':1000},
            3: {'E': '246', 'N': 4, 'S': 2, 'W': '245', 'name': 3, 'type': 'node', 'hall':1000},
            4: {'E': None, 'N': 5, 'S': 3, 'W': '247', 'name': 4, 'type': 'node', 'hall':1000},
            5: {'E': '248', 'N': 6, 'S': 4, 'W': '249', 'name': 5, 'type': 'node', 'hall':1000},
            6: {'E': '250', 'N': 7, 'S': 5, 'W': '251', 'name': 6, 'type': 'node', 'hall':1000},
            7: {'EH': None,'E':None,'W':None,'S':6,'N':None, 'NH': 1001, 'SH': 1000, 'WH': None, 'name': 7, 'type': 'EXIT', 'hall':1000},
            'holds': [0, 1, 2, 3, 4, 5, 6, 7],
            'exits': [0,7],
            'adj': [1001,100001]},
        1001:{
            10: {'EH': None,'E':None,'W':None,'N':11,'S':None,'NH': 1001,'SH': 1002,'WH': None,'name': 10,'type': 'EXIT', 'hall':1001},
            11: {'E': '262', 'N': 12, 'S': 10, 'W': '263', 'name': 11, 'type': 'node', 'hall':1001},
            12: {'E': '260', 'N': 13, 'S': 11, 'W': '261', 'name': 12, 'type': 'node', 'hall':1001},
            13: {'E': '258', 'N': 14, 'S': 12, 'W': '259', 'name': 13, 'type': 'node', 'hall':1001},
            14: {'E': '256', 'N': 15, 'S': 13, 'W': '257', 'name': 14, 'type': 'node', 'hall':1001},
            15: {'E': '254', 'N': 16, 'S': 14, 'W': None, 'name': 15, 'type': 'node', 'hall':1001},
            16: {'E': '252', 'N': 17, 'S': 15, 'W': '255', 'name': 16, 'type': 'node', 'hall':1001},
            17: {'EH': None,'E':None,'W':None,'S':16, 'N':None,'NH': 1000, 'SH': 1001, 'WH': None, 'name': 17, 'type': 'EXIT', 'hall':1001},
            'holds': [16, 17, 10, 11, 12, 13, 14, 15],
            'exits':[10,17],
            'adj': [1000,1002]},
        1002: {
            20: {'EH': None,'E':None,'W':None,'N':21,'S':None,'NH': 1002,'SH': 1001,'WH': None,'name': 20,'type': 'EXIT', 'hall':1002},
            21: {'E': '264', 'N': 22, 'S': 20, 'W': '265', 'name': 21, 'type': 'node', 'hall':1002},
            22: {'E': '266', 'N': 23, 'S': 21, 'W': '267', 'name': 22, 'type': 'node', 'hall':1002},
            23: {'E': '268', 'N': 24, 'S': 22, 'W': None, 'name': 23, 'type': 'node', 'hall':1002},
            24: {'E': '270', 'N': 25, 'S': 23, 'W': '269', 'name': 24, 'type': 'node', 'hall':1002},
            25: {'EH': None,'E':None,'W':None,'S':24,'N':None, 'NH': 100001, 'SH': 1002, 'WH': None, 'name': 25, 'type': 'EXIT', 'hall':1002},
            'holds': [20, 21, 22, 23, 24, 25],
            'exits':[20,25],
            'adj': [1001,100001]}
        }
        
    DB = {}
        
    EXITS_DICT={}
        
    CARDINALS = ('N','S','E','W')
    LONG_CARDINALS = {'E': 'East', 'N': 'North', 'S': 'South', 'W': 'West'}
    SOUTH_WAY = {'E': 'left', 'N': 'backward', 'S': 'forward', 'W': 'right'}
    NORTH_WAY={'W': 'left', 'S': 'backward', 'N': 'forward', 'E': 'right'}
    EAST_WAY={'N': 'left', 'W': 'backward', 'E': 'forward', 'S': 'right'}
    WEST_WAY={'E': 'left', 'S': 'backward', 'W': 'forward', 'N': 'right'}
        
    def genDB(self):
        for h in self.__sampleGraph__:
            kl=[x for x in list(self.__sampleGraph__[h].keys()) if type(x) == int]
            for n in kl:
                for dir in self.CARDINALS:
                    if dir in self.__sampleGraph__[h][n].keys() and type(self.__sampleGraph__[h][n][dir]) == str:
                        self.DB[self.__sampleGraph__[h][n][dir]]=self.__sampleGraph__[h][n]['name']
        
    def getIDFromName(self, name):
        return self.DB[name] if name in self.DB.keys() else False
        
    def percentWords(self, percentage):
        if percentage < .30:
            return 'about a quarter of the way'
        if percentage < .60:
            return 'about halfway'
        if percentage < .85:
            return 'about three quarters of the way'
        else:
            return 'most of the way'
            
    def distillExits(self):
        '''
        grabs all exits in graph. exits are traversed to find path to goal.
        '''
        for n in self.__sampleGraph__:
            if type(n)==int:
                for e in self.__sampleGraph__[n]['exits']:
                    self.EXITS_DICT[e]= self.__sampleGraph__[n][e]
        
    def findClosestExit(self, ID):
        exits=list(self.EXITS_DICT.keys())
        exits.sort()
        return min(exits, key=lambda x: abs(x-ID))
    
    def expandExit(self, exitID):
        '''
        assuming only 2 exits per hallway. next iteration will feature more.
        '''
        e1,e2=self.__sampleGraph__[self.EXITS_DICT[exitID]['hall']]['exits']
        return e1,e2
        
    def expandExitHalls(self, exitID):
        return [self.EXITS_DICT[exitID][n] for n in ('N','S','E','W') if self.EXITS_DICT[exitID][n]]
        
    def performHeuristic(self, dID, ID1, ID2):
        return ID1 if abs(dID - ID1) < abs(dID - ID2) else ID2

    def getBestOfTwoExits(self, dHall,ex1,ex2):
        '''
        assuming 2 exits per hallway, and 2 hallways per exit.
        '''
        e1h1,e1h2=self.expandExitHalls(ex1)
        e1h=self.performHeuristic(dHall,e1h1,e1h2)
        e2h1,e2h2=self.expandExitHalls(ex2)
        e2h=self.performHeuristic(dHall,e2h1,e2h2)
        betterHall = self.performHeuristic(dHall,e1h,e2h)
        better = ex1 if betterHall is e1h else ex2
        return better, betterHall
        
    def traverse(self, oID, dID):
        '''
        assuming both dID and oID are in graph
        in second state, oID is an exit
        '''
        path=[]
        cID=oID
        while cID != dID:
            # expand neighbors
            n1,n2 = self.getAdjacent(currN['name'])
            currN = self.closerNode(self.getNodeFromName(n1),self.getNodeFromName(n2),destin)
            path.append(currN)
        return path
        
    def findBestExit(self, tarHall, otherHall):
        '''
        assumes only 2 exits
        '''
        oExits = self.__sampleGraph__[tarHall]['exits']
        for e in oExits:
            if otherHall in self.__sampleGraph__[tarHall][e].values():
                return e
        
    def traverse2ndStateNodes(self, hall, nID, dID):
        '''
        assuming 'NSEW' layout of nodes
        '''
        theHall = self.__sampleGraph__[hall]
        adj = [theHall[nID][n] for n in ('N','S') if theHall[nID][n] is not None]
        if len(adj) is 1:
            return adj[0]
        return self.performHeuristic(dID, adj[0],adj[1])
        
    def generate2ndStateDirections(self, fnpath, hpath, dnpath):
        dirString=''
        # go (n) nodes to exit by node (fnpath[-1]['N'] or ['S'])
        fstNd=self.__sampleGraph__[fnpath['hall']][fnpath['path'][0]]
        secNd=self.__sampleGraph__[fnpath['hall']][fnpath['path'][1]]
        fex=self.__sampleGraph__[fnpath['hall']][fnpath['path'][-1]]
        rmB4fex = self.__sampleGraph__[fnpath['hall']][fnpath['path'][-2]]
        for n in self.CARDINALS:
            if fstNd[n] == secNd['name']:
                fstDir = n
        # assuming only north or south for now
        way = self.NORTH_WAY if fstDir == 'N' else self.SOUTH_WAY
        # how to do this without throwing error?
        exRm = [rmB4fex[n] for n in ('E','W')]
        firstPart='Proceed from room {} to the {} by room {}.'.format(fnpath['orig'], fex['type'], exRm[0]) 
        # proceed down (len(hpath)-2) hallways.
        numH = len(hpath)-2
        sHall = 'hallways' if numH >1 else 'hallway'
        middlePart='Continue through {} {}.'.format(numH, sHall) if numH >0 else ''
        # go (n)  nodes from exit to destination.
        fstNd=self.__sampleGraph__[dnpath['hall']][dnpath['path'][0]]
        secNd=self.__sampleGraph__[dnpath['hall']][dnpath['path'][1]]
        des=self.__sampleGraph__[dnpath['hall']][dnpath['path'][-1]]
        for n in self.CARDINALS:
            if fstNd[n] == secNd['name']:
                dstDir = n
        # assuming only north or south for now
        way = self.NORTH_WAY if dstDir == 'N' else self.SOUTH_WAY
        goalSide = list(des.keys())[list(des.values()).index(dnpath['destin'])]
        percent = len(self.__sampleGraph__[dnpath['hall']]['holds']) / len(dnpath['path'])
        howFar = self.percentWords(percent)
        lastpart='Proceed {} down the hallway to your destination on the {}.'.format(howFar, way[goalSide])
        dirString = '{} {} {}'.format(firstPart,middlePart,lastpart)
        
        return dirString
    
class ThirdStateNode(SecondStateNode):
    
    __sampleGraph__= {
        'intersections': {
            100:{'N':{'NODE':0,'HALL':1000},'S':{'NODE':None,'HALL':None},'E':{'NODE':None,'HALL':None},'W':{'NODE':None,'HALL':None}},
            101:{'N':{'NODE':10,'HALL':1001},'S':{'NODE':7,'HALL':1000},'W':{'NODE':40,'HALL':1004},'E':{'NODE':30,'HALL':1003}},
            102:{'N':{'NODE':20,'HALL':1002},'S':{'NODE':17,'HALL':1001},'E':{'NODE':None,'HALL':None},'W':{'NODE':None,'HALL':None}},
            103:{'N':{'NODE':None,'HALL':None},'S':{'NODE':25,'HALL':1002},'E':{'NODE':None,'HALL':None},'W':{'NODE':None,'HALL':None}},
            104:{'N':{'NODE':None,'HALL':None},'S':{'NODE':None,'HALL':None},'E':{'NODE':35,'HALL':1003},'W':{'NODE':None,'HALL':None}},
            105:{'N':{'NODE':None,'HALL':None},'S':{'NODE':None,'HALL':None},'E':{'NODE':None,'HALL':None},'W':{'NODE':45,'HALL':1004}}},
        1000:{   
            0: {'E': None,'W': None,'N':1,'S': 100,'name': 0,'type': 'EXIT', 'hall':1000},
            1: {'E': '242', 'N': 2, 'S': 0, 'W': '241', 'name': 1, 'type': 'node', 'hall':1000},
            2: {'E': '244', 'N': 3, 'S': 1, 'W': '243', 'name': 2, 'type': 'node', 'hall':1000},
            3: {'E': '246', 'N': 4, 'S': 2, 'W': '245', 'name': 3, 'type': 'node', 'hall':1000},
            4: {'E': None, 'N': 5, 'S': 3, 'W': '247', 'name': 4, 'type': 'node', 'hall':1000},
            5: {'E': '248', 'N': 6, 'S': 4, 'W': '249', 'name': 5, 'type': 'node', 'hall':1000},
            6: {'E': '250', 'N': 7, 'S': 5, 'W': '251', 'name': 6, 'type': 'node', 'hall':1000},
            7: {'E':None,'W':None,'S':6,'N':101, 'name': 7, 'type': 'EXIT', 'hall':1000},
            'holds': [0, 1, 2, 3, 4, 5, 6, 7],
            'exits': [0,7],
            'adj': [1001,1003,1004]},
        1001:{
            10: {'E':None,'W':None,'N':11,'S':101,'name': 10,'type': 'EXIT', 'hall':1001},
            11: {'E': '262', 'N': 12, 'S': 10, 'W': '263', 'name': 11, 'type': 'node', 'hall':1001},
            12: {'E': '260', 'N': 13, 'S': 11, 'W': '261', 'name': 12, 'type': 'node', 'hall':1001},
            13: {'E': '258', 'N': 14, 'S': 12, 'W': '259', 'name': 13, 'type': 'node', 'hall':1001},
            14: {'E': '256', 'N': 15, 'S': 13, 'W': '257', 'name': 14, 'type': 'node', 'hall':1001},
            15: {'E': '254', 'N': 16, 'S': 14, 'W': None, 'name': 15, 'type': 'node', 'hall':1001},
            16: {'E': '252', 'N': 17, 'S': 15, 'W': '255', 'name': 16, 'type': 'node', 'hall':1001},
            17: {'E':None,'W':None,'S':16, 'N':102,'name': 17, 'type': 'EXIT', 'hall':1001},
            'holds': [16, 17, 10, 11, 12, 13, 14, 15],
            'exits':[10,17],
            'adj': [1000,1002,1003,1004]},
        1002: {
            20: {'E':None,'W':None,'N':21,'S':102,'name': 20,'type': 'EXIT', 'hall':1002},
            21: {'E': '264', 'N': 22, 'S': 20, 'W': '265', 'name': 21, 'type': 'node', 'hall':1002},
            22: {'E': '266', 'N': 23, 'S': 21, 'W': '267', 'name': 22, 'type': 'node', 'hall':1002},
            23: {'E': '268', 'N': 24, 'S': 22, 'W': None, 'name': 23, 'type': 'node', 'hall':1002},
            24: {'E': '270', 'N': 25, 'S': 23, 'W': '269', 'name': 24, 'type': 'node', 'hall':1002},
            25: {'E':None,'W':None,'S':24,'N':103,'name': 25, 'type': 'EXIT', 'hall':1002},
            'holds': [20, 21, 22, 23, 24, 25],
            'exits':[20,25],
            'adj': [1001]},
        1003: {
            30: {'E':None,'W':None,'N':31,'S':101,'name': 30,'type': 'EXIT', 'hall':1003},
            31: {'E': '274', 'N': 32, 'S': 30, 'W': '275', 'name': 31, 'type': 'node', 'hall':1003},
            32: {'E': '276', 'N': 33, 'S': 31, 'W': '277', 'name': 32, 'type': 'node', 'hall':1003},
            33: {'E': '278', 'N': 34, 'S': 32, 'W': None, 'name': 33, 'type': 'node', 'hall':1003},
            34: {'E': '280', 'N': 35, 'S': 33, 'W': '279', 'name': 34, 'type': 'node', 'hall':1003},
            35: {'E':None,'W':None,'S':34,'N':104, 'name': 35, 'type': 'EXIT', 'hall':1003},
            'holds': [30, 31, 32, 33, 34, 35],
            'exits':[30,35],
            'adj': [1001,1004,1000]},
        1004: {
            40: {'E':None,'W':None,'N':41,'S':101,'name': 40,'type': 'EXIT', 'hall':1004},
            41: {'E': '284', 'N': 42, 'S': 40, 'W': '285', 'name': 41, 'type': 'node', 'hall':1004},
            42: {'E': '286', 'N': 43, 'S': 41, 'W': '287', 'name': 42, 'type': 'node', 'hall':1004},
            43: {'E': '288', 'N': 44, 'S': 42, 'W': None, 'name': 43, 'type': 'node', 'hall':1004},
            44: {'E': '290', 'N': 45, 'S': 43, 'W': '289', 'name': 44, 'type': 'node', 'hall':1004},
            45: {'E':None,'W':None,'S':44,'N':105, 'name': 45, 'type': 'EXIT', 'hall':1004},
            'holds': [40, 41, 42, 43, 44, 45],
            'exits':[40,45],
            'adj': [1001,1003,1000]}
        }
        
    def performHeuristic(self, dID, IDlist, resOnly=True):
        '''
        start with assuming that first element in IDlist is best
        '''
        min=abs(dID-IDlist[0])
        res=IDlist[0]
        for h in IDlist:
            dif=abs(dID-h)
            if dif < min:
                res=h
                min=dif
        return res if resOnly else min
        
    def interNodeHeuristic(self, iNList,dHall):
        '''
        returns interNode that has hallway closest to goal
        '''
        results={}
        for n in iNList:
            results[n] = self.performHeuristic(dHall,self.expandIntersection(self.__sampleGraph__['intersections'][n]),False)
        minim=min(list(results.values()))
        minDex=list(results.values()).index(minim)
        return list(results)[minDex]
        
    def getHallIntersections(self,hall):
        interNodes=self.__sampleGraph__['intersections']
        initialNodes=[]
        for n in  interNodes:
            for dir in self.CARDINALS:
                if interNodes[n][dir]['HALL'] == hall:
                    initialNodes.append((n,dir))
        return initialNodes
        
    def expandIntersection(self, interNode):
        hallList=[interNode[dir]['HALL'] for dir in self.CARDINALS if interNode[dir]['HALL'] != None]
        return hallList
            
    def passThroughInterNode(self, starHall, otherHall):
        '''
        starhall is starting hall, other hall is next hall we want to get to
        returns exit direction to take, and the interNode to go through, and the next direction to take
        '''
        sg=self.__sampleGraph__
        oExits = sg[starHall]['exits'] # list of exit nodes
        possibleNodes=[]
        for e in oExits:
            # must look at iNodes to find the one connecting the two hallways
            # so first get the possible nodes
            for dir in self.CARDINALS:
                if sg[starHall][e][dir] in sg['intersections']:
                    possibleNodes.append(sg[starHall][e][dir])
        for iNode in possibleNodes:
            firstIsHere=False
            secondIsHere=False
            for n in sg['intersections'][iNode]:
                if starHall in sg['intersections'][iNode][n].values():
                    firstIsHere=True,n
                if otherHall in sg['intersections'][iNode][n].values():
                    secondIsHere=True,n
            if firstIsHere and secondIsHere:
                # return sg['intersections'][iNode][firstIsHere[1]]['NODE'],iNode,sg['intersections'][iNode][secondIsHere[1]]['NODE']
                return firstIsHere[1],iNode,secondIsHere[1]
        return False # didn't find one, error!        
        
    def traverseThirdStatePath(self,origin,oID,destination,dID, hpath):
        '''
        hpath is path of hallways
        origin is string of origin room
        oID is numerical ID of o.r.
        destination and dID, likewise.
        
        generates a path of interNodes and which entrance/exit are utilized per iNode
        '''
        iNodePath={}
        unmappedHalls=list(hpath)
        while len(unmappedHalls) > 1:
        # while we have more than 2 hallways:   
            # get node and its bridgging exits and generate directions
            passResult=self.passThroughInterNode(unmappedHalls[0],unmappedHalls[1])
            if passResult:
                exitToIN, iNode, exitFromIN= passResult
            else:
                print("ERROR IN MAP")
                return False 
            # pop the beginning hallway
            currHall=unmappedHalls.pop(0)
            iNodePath[currHall]=(exitToIN, iNode, exitFromIN)
        
        return iNodePath
            
    def generateINDirectionString(self, exitToIN, iNode, exitFromIN):
        exitTo = self.__sampleGraph__['intersections'][iNode][exitToIN]
        exitFrom = self.__sampleGraph__['intersections'][iNode][exitFromIN]
        st1= "Go to the {} by room {}. ".format(self.__sampleGraph__[exitTo['HALL']][exitTo['NODE']]['type'],0)

        
        
        
