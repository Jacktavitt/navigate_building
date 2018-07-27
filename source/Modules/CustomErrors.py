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

class PlaqueFontError(Exception):
    '''Exception for feeding too many letters or too big
        a sign into the ADA font getter.
    Attributes:
        message: keyword for catcher
    '''
    errCodes ={
        1: "Too many letters!",
        2: "Sign too big!"
    }
    def __init__(self, message):
        self.message = self.errCodes[message]