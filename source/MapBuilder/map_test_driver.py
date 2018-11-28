# test map making with default plaque output
import NodeMap
SAMPLE_OUTPUT = ['248', '248', '248', '248', None, None, None, None, None, None, '250', '250', '250', '250', None, None, None, None, None, None, '252', '252', '252', '252', None, None, None, None, None, None, '254', '254', '254', '254', None, None, None, None, None, None, '256', '256', '256', '256', None, None, None, None, None, None, 'EXIT', 'EXIT', 'EXIT', 'EXIT', None, None, None, '257', '257', '257', '257', None, None, None, None, None, None, '255', '255', '255', '255', None, None, None, None, None, None, '253', '253', '253', '253', None, None, None, None, None, None, '251', '251', '251', '251', None, None, None, None, None, None, '249', '249', '249', '249', None, None, None, None, None, 'EXIT', 'EXIT', 'EXIT', 'EXIT', None, None, None, None, None, '248', '248', '248', '248']

if __name__=="__main__":
    the_map = NodeMap.NodeMap()
    the_map.build_simple_map(SAMPLE_OUTPUT, 4)
    print(the_map)