import cv2

cap = cv2.VideoCapture(r"hall_vids\my_video-1.mkv")

while True:
    ret, frame = cap.read()
    
    cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()