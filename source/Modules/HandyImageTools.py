import os, cv2, imutils

def resize(cv2Image, desiredWidth=None):
    if not desiredWidth:
        desiredWidth = 300
    resized= imutils.resize(cv2Image, desiredWidth)
    return resized

def displayImage(image, name=None):
    name = 'Image' if not name else name
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def resizeSaveManyImages(listOfPaths, desiredWidth = None):
    for path in listOfPaths:
        img = cv2.imread(path)
        rs = self.resize(img,desiredWidth)
        root, ext = os.path.splitext(path)
        newPath = "{}{}{}".format(root,'_resized',ext)
        cv2.imwrite(newPath,rs)

def getFilesInDirectory(directory,fileType):
    fileList=[]
    for item in os.listdir(directory):
        if item.lower().endswith(fileType):
            fileList.append("{}{}".format(directory,item))
    return fileList