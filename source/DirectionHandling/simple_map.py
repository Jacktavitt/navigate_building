# generate a simple 'map' (adj list) of a 'hallway'
import pprint

ROOM_LIST = ['260','LADIES','258','256','254','252','250','248A', '248', '246', 'EXIT', '245','247','249','251','253','255','257','259','261','EXIT','260'] 

def fix_exit_ambiguity(room_list):
    keys = list(range(len(room_list)))
    room_dict = dict(zip(keys, room_list))
    


class SchoolMap(object):
    '''implementation of adj-list based map of rooms'''
    '''
        map: pickled map (in this case already unpickled
            TODO: learn ins and outs of pickling)
        school_map: pickled instance of the class. see TODO above
        map is an adj. list of hallways (??) 
            (might be too complicated for what i actually need but hey)


    '''
    def __init__(self, *, map=None, school_map=None):
        self.map = {} if not map else map

    def __str__(self):
        # textmap = [str(self.map[line])+'\n' for line in self.map]
        return (f"Map:\n {self.map}")

    # def add_hallway_to_map(self):
    #     pass

    def add_node(self, node, prev_node):
        ''' 
        assumes that each new node is sequential to other nodes.
        figures adj. list neighbor and sticks in self map
        TODO: deal with exits. for now just a single hallway
        '''
        # if node is "EXIT":
        #     node = f"EXIT{str(prev_node)}"
        if prev_node is not None:
            self.map[prev_node]["after"] = node
        if node not in self.map:
            node_entry = {"before": prev_node, "after":None}
            self.map[node] = node_entry
        else:
            self.map[node]["before"] = prev_node
        
    
if __name__=="__main__":
    maptastic = SchoolMap()
    prev_room = None
    for rm in ROOM_LIST:
        try:
            maptastic.add_node(rm, prev_room)
        except Exception as e:
            print(f"<<< ERROR >>>\n{e}\n{maptastic}")
        prev_room = rm
    print(maptastic)