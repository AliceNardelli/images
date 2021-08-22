#!/usr/bin/env python3.8

# import necessary packages
import cvlib as cv
import cv2
import os 


print("entered3")
# read input image
image = cv2.imread("/root/images/provaimm.jpg")

# apply face detection
faces, confidences = cv.detect_face(image)

print(faces)
print(confidences)

# loop through detected faces
for face,conf in zip(faces,confidences):

    (startX,startY) = face[0],face[1]
    (endX,endY) = face[2],face[3]

    # draw rectangle over face
    cv2.rectangle(image, (startX,startY), (endX,endY), (0,255,0), 2)

# display output
# press any key to close window           
#cv2.imshow("face_detection", image)
#cv2.waitKey()

# save output
cv2.imwrite("/root/images/P3.jpg", image)

# release resources
#cv2.destroyAllWindows()

