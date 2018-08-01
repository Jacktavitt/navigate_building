from PIL import Image
import cv2
import CustomImage as CIM
import pytesseract

image = CIM.Image.open(r"C:\Users\TJAMS002\Documents\ComputerScience\Thesis\RoomFinder\source\ImageGeneration\SNAPS\test_hallway_2_25p_10.png")
image.gray()
# image.blur()
image.show()

text=pytesseract.image_to_string(image.image)
print(text)