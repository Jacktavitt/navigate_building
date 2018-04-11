import math
import time
import random
import nodes
import argparse
    
parser=argparse.ArgumentParser()
parser.add_argument("o", type=str, help="Room closest to origin")
parser.add_argument("d", type=str, help="Destination room")
args=parser.parse_args()

origin = args.o
destination = args.d
    
def getID(NODE,name):
    id=NODE.getIDFromName(name)
    if not id:
        print("name not in database. Exiting...")
        return False
    return id
    
def mainSecond(origin, desination):   
    SSN = nodes.SecondStateNode()
    # get id for origin and destin from a database structure
    oID=getID(SSN, origin)
    dID=getID(SSN, destination)
    path=[]
    oHall,dHall = SSN.getContainingHallways(oID,dID,SSN.__sampleGraph__)
    currHall=oHall
    hpath=[currHall]
    while currHall != dHall: # first traverse hallways
        # expand its hallways to find which hallway is closer to dest Hallway
        # assuming only 2 adjacent hallways
        h1,h2=SSN.__sampleGraph__[currHall]['adj']
        better=SSN.performHeuristic(dHall,h1,h2)
        hpath.append(better)
        currHall=better
        
    # now we should be at the destination hallway
    # must get directions from origin to best exit
    # find exit between origin and destination
    firstExit = SSN.findBestExit(oHall, hpath[1])
    currNode = oID
    fnpath={
        'orig': origin, 
        'hall': oHall,
        'path': [currNode]
    }
    # this is for origin to correct exit
    while currNode != firstExit:
        next = SSN.traverse2ndStateNodes(oHall, currNode,firstExit)
        currNode = next
        fnpath['path'].append(currNode)
    # now we should be to the correct exit.
    # must find the same deal for the destination hallway
    currNode = SSN.findBestExit(dHall, hpath[-2])
    dnpath={
        'destin': destination,
        'hall': dHall,
        'path':[currNode]
    }
    while currNode != dID:
        next = SSN.traverse2ndStateNodes(dHall, currNode, dID)
        currNode = next
        dnpath['path'].append(currNode)       
    # once in goal hallway, generate directions
    print(SSN.generate2ndStateDirections(fnpath, hpath,dnpath))
    
def mainThird(origin,desination):
    TSN=nodes.ThirdStateNode()
    oID=getID(TSN, origin)
    dID=getID(TSN, destination)
    path=[]
    oHall,dHall = TSN.getContainingHallways(oID,dID,TSN.__sampleGraph__)
    currHall=oHall
    hpath=[currHall]
    
    while currHall != dHall: # first traverse hallways
        print(currHall) 
        adjs=TSN.__sampleGraph__[currHall]['adj']
        better=TSN.performHeuristic(dHall,adjs)
        hpath.append(better)
        currHall=better
   
    print(hpath)
    
    iNodePath=TSN.traverseThirdStatePath(origin, oID, destination,dID,hpath)
    print(iNodePath)
    # now we have a path, must generate directions between hallways
    firstInterNode = TSN.findBestExit(oHall, hpath[1])
    currNode = oID
    fnpath={
        'orig': origin, 
        'hall': oHall,
        'path': [currNode]
    }
    
# mainSecond(origin, destination)
mainThird(origin, destination)