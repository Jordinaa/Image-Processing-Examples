import cv2
import numpy as np
import math

image = cv2.imread('Lego.png')

# Dimensions of image
shapeofImage = np.shape(image)
print(f'The image dimensions are (X, Y, Channels): {shapeofImage}')

backdrop = np.zeros((shapeofImage[0], shapeofImage[1]))
print(backdrop)

def empty(x):
    pass

cv2.namedWindow('Crop Settings')
cv2.resizeWindow('Crop Settings', 640, 240)
cv2.createTrackbar('X', 'Crop Settings', 50, shapeofImage[1], empty)
cv2.createTrackbar('Y', 'Crop Settings', 50, shapeofImage[0], empty)


while True:

    # Creates a copy of the image and overlays contours
    imageCopy = image.copy()
    
    x = cv2.getTrackbarPos('X', 'Crop Settings')
    y = cv2.getTrackbarPos('Y', 'Crop Settings')
    
    cv2.line(imageCopy, pt1 = (x, y), pt2 = (x, 0), color = (0, 0, 0), thickness = 5)
    cv2.line(imageCopy, pt1 = (x, y), pt2 = (0, y), color = (0, 0, 0), thickness = 5)
    # cv2.circle(imageCopy, )

    cv2.namedWindow("Original Image", cv2.WINDOW_FREERATIO)
    cv2.resizeWindow("Original Image", 1280, 720)
    cv2.imshow("Original Image", imageCopy)
    if cv2.waitKey(1) & 0xFF == ord('b'):
        break




