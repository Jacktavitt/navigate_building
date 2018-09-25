'''
9-22: placeholder
'''

class SlamOutput(object):
    '''
    Wrapper for whatever output comes from the SLAM we use for the project.
    Should have:
        pose_info: unique location in space
        image: image associated to current pose
    '''
    def __init__(self, *, image, pose_info):
        self.image = 'some image thing' if not image else image
        self.pose_info = 'some unique number' if not pose_info else pose_info

    def __str__(self):
        return f'image:{self.image}, pose:{self.pose_info}'