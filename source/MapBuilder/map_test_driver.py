# test map making with default plaque output
import NodeMap
import HandyTools as HT

SAMPLE_OUTPUT = ['248', '248', '248', '248', None, None, None, None, None, None, '250', '250', '250', '250', None, None, None, None, None, None, '252', '252', '252', '252', None, None, None, None, None, None, '254', '254', '254', '254', None, None, None, None, None, None, '256', '256', '256', '256', None, None, None, None, None, None, 'EXIT', 'EXIT', 'EXIT', 'EXIT', None, None, None, '257', '257', '257', '257', None, None, None, None, None, None, '255', '255', '255', '255', None, None, None, None, None, None, '253', '253', '253', '253', None, None, None, None, None, None, '251', '251', '251', '251', None, None, None, None, None, None, '249', '249', '249', '249', None, None, None, None, None, 'EXIT', 'EXIT', 'EXIT', 'EXIT', None, None, None, None, None, '248', '248', '248', '248']
SIMPLE_SAMPLE_OP = ['4', '4', '4', '6', '6', '6', 'EXIT', 'EXIT', 'EXIT', '5', '5', '5', '3', '3', '3', '1', '1', '1', 'EXIT', 'EXIT', 'EXIT', '2', '2', '2', '4', '4', '4']
SIMPLE_NORM_SAMPLE = ['4', '6', 'EXIT', '5', '3', '1', 'EXIT', '2', '4']
ALFA_NUM_SAMPLE = ['B','A','EXIT','4','3','2','1','EXIT','D','C','B']
if __name__=="__main__":
    the_map = NodeMap.NodeMap()
    sample = HT.distill_list(SIMPLE_NORM_SAMPLE)
    # the_map.build_simple_map(SAMPLE_OUTPUT, 4)
    # the_map.build_simple_map(SIMPLE_SAMPLE_OP, 3)
    the_map.add_hallway(sample)
    # print(the_map)
    # the_map.add_hallway(ALFA_NUM_SAMPLE)
    # print(the_map)
    for hall in the_map.map:
        for value in hall:
            print(f"{value}: {hall[value]}")