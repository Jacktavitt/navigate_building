'''collection of ADA requirements.
ALL IN INCHES
'''
import CustomErrors as CER

def get_font_size(text, signWidth):
    '''returns sign spec from ADA.
    in INCHES!
    usage= sizeChart[signWidth][charnum]
    '''
    charnum = len(text)
    if charnum > 26:
        raise CER.PlaqueFontError(1)
    elif signWidth > 19:
        raise CER.PlaqueFontError(2)

    sizeChart= {
        4:{5: 0.625, 4: 0.75, 3: 1},
        6:{7: 0.625, 6: 0.75, 5: 0.875, 4: 1.25, 3: 1.5},
        8:{11: 0.625, 9: 0.75, 8: 0.875, 7: 1, 5: 1.25, 4: 1.5},
        10:{14: 0.625, 11: 0.75, 10: 0.875, 9: 1, 8: 1.25, 7: 1.5},
        12:{18: 0.625, 14: 0.75, 12: 0.875, 11: 1, 8: 1.25, 7: 1.5},
        18:{25: 0.625, 21: 0.75, 18: 0.875, 16: 1, 13: 1.25, 11: 1.5}
    }
    keys = list(sizeChart.keys())
    chartKey = min(keys, key=lambda x: abs(x-signWidth))
    chartKeyKeys = list(sizeChart[chartKey])
    fontKey = min(chartKeyKeys, key = lambda x: abs(x-charnum))
    return sizeChart[chartKey][fontKey]

def toGray(B,G,R):
    '''converts color value to grayscale via the Limunosity method.
    Args:
        (B,G,R): blue, green, and red colorspace
    '''
    return (R*0.21 + G*0.72 + B*0.07)

DOOR_HT = 80
DOOR_WD = 32
VEIL_HT = 120
PQ_HT = 50
CEIL_HT = 120