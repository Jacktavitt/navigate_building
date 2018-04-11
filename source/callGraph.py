import graph
import sys

if __name__ =='__main__':
    if len(sys.argv) <3:
        print("Please include origin and destination ID numbers.")
        raise SystemExit(1)
        
    G=graph.AllNodes()
    originRm=sys.argv[1]
    destinRm=sys.argv[2]
    origin=G.getNodeFromRoom(sys.argv[1])
    destination=G.getNodeFromRoom(sys.argv[2])
    if len(sys.argv) == 4:
        G.__bug__ = True
    dist,prev=G.doDijkstra(origin,destination)
    # print(str(dist)+'\n'+str(prev))
    
    nPath=[]
    
    curN=destination
    while prev[curN]:
        nPath.insert(0,curN)
        curN=prev[curN]
    nPath.insert(0,curN)
    dijkPak=G.breakPathUp(nPath)
    dirs=G.getDirectionsFromEdsger(dijkPak,originRm,destinRm)