# import Exception

class NoImageError(Exception):
    '''Custom exception for missing images.
    Attributes:
        message: keyword for catcher
    '''
    def __init__(self, message):
        self.message = message

class DumbProgramError(Exception):
    '''Custom exception for overly-simple and frail programs.
    Attributes:
        message: keyword for catcher
    '''
    def __init__(self, message):
        self.message = message
