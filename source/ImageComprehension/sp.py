import cv2
import numpy as np


image = np.full((500,500),200,dtype=np.uint8)
image=cv2.rectangle(image,(230,230),(300,300),0,-1)


def show(image):
    cv2.imshow("",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def snp(image, amount = .004):
    shapeinfo = image.shape
    row=shapeinfo[0]
    col=shapeinfo[1]
    s_vs_p = 0.5
    out = np.copy(image)
    # Salt mode
    num_salt = np.ceil(amount * image.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt))
    for i in image.shape]
    out[coords] = 255
    # Pepper mode
    num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper))
    for i in image.shape]
    out[coords] = 0
    return out