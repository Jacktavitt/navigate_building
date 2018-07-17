# import Exception

class NoImageError(Exception):
    '''Custom exception for missing images.
    Attributes:
        message: keyword for catcher
    '''
    def __init__(self, message):
        self.message = message