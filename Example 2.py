import cv2
import numpy as np 

image = cv2.imread('Lego.png')
imageCopy = image.copy()

cropping = False

# Inside mouseCrop function
xStart, xEnd, yStart, yEnd = 0, 0, 0, 0

# This lets you crop an image with your mouse
def mouseCrop(event, x, y, flags, param):

    # References globalk variables 
    global xStart, xEnd, yStart, yEnd, cropping

    # If left MSB is down start recording
    if event == cv2.EVENT_LBUTTONDOWN:
        xStart, yStart, xEnd, yEnd = x, y, x, y
        cropping = True

    # Mouse is moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            xEnd, yEnd = x, y

    # If the left mouse button is released
    elif event == cv2.EVENT_LBUTTONUP:
        # Record the ending (x, y) coordinates
        xEnd, yEnd = x, y
        # Cropping is finished
        cropping = False 

        referencePoint = [(xStart, yStart), (xEnd, yEnd)]

        if len(referencePoint) == 2:
            regionofInterest = imageCopy[referencePoint[0][1]:referencePoint[1][1], referencePoint[0][0]:referencePoint[1][0]]
            print(referencePoint)
            cv2.imshow("Region of Interest", regionofInterest)

cv2.namedWindow("Original Image", cv2.WINDOW_FREERATIO)
cv2.resizeWindow("Original Image", 1280, 720)
cv2.setMouseCallback("Original Image", mouseCrop)

while True:

    copiedImage = image.copy()

    if not cropping:
        cv2.imshow("Original Image", image)

    elif cropping:
        cv2.rectangle(copiedImage, (xStart, yStart), (xEnd, yEnd), (0, 0, 0), 2)
        cv2.imshow("Original Image", copiedImage)

    if cv2.waitKey(1) & 0xFF == ord('b'):
        break

cv2.destroyAllWindows()