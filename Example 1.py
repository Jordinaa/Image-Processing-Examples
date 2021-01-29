import cv2
import numpy as np
import time

start = time.time()

print(f'To end program hit the "b" key')
# Path to the image
imagePath = 'Lego.png'



# Function passed into argument for creating trackbars 
def empty(x):
    pass

# Function I use for troubleshooting
# This function takes an array of images and stacks them rows x columns
# It is used inside of a while loop with trackbars so I can manipulate images in real time
def imageStacked(scale, arrayImages):

    rows = len(arrayImages)
    columns = len(arrayImages[0])
    rowsAvailable = isinstance(arrayImages[0], list)
    
    width = arrayImages[0][0].shape[1]
    height = arrayImages[0][0].shape[0]
    
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, columns):
                if arrayImages[x][y].shape[:2] == arrayImages[0][0].shape[:2]:
                    arrayImages[x][y] = cv2.resize(arrayImages[x][y], (0, 0), None, scale, scale)
                else:
                    arrayImages[x][y] = cv2.resize(arrayImages[x][y], (arrayImages[0][0].shape[1], arrayImages[0][0].shape[0]), None, scale, scale)
                if len(arrayImages[x][y].shape) ==2: arrayImages[x][y] = cv2.cvtColor(arrayImages[x][y], cv2.COLOR_GRAY2BGR)
        blankImage = np.zeros((height, width, 3), np.uint8)
        horizantal = [blankImage] * rows
        horizantal_con = [blankImage] * rows
        for x in range(0, rows):
            horizantal[x] = np.hstack(arrayImages[x])
        vertical = np.vstack(horizantal)
        
    else:
        for x in range(0, rows):
            if arrayImages[x].shape[:2] == arrayImages[0].shape[:2]:
                arrayImages = cv2.resize(arrayImages[x], (0, 0), None, scale, scale)
            else:
                arrayImages[x] = cv2.resize(arrayImages[x], (arrayImages[0].shape[1], arrayImages[0].shape[0]), None, scale, scale)
            if len(arrayImages[x].shape) == 2: arrayImages[x] = cv2.cvtColor(arrayImages[x], cv2.COLOR_GRAY2BGR)
        horizantal = np.hstack(arrayImages)
        vertical = horizantal

    return vertical

# This function performs basic image manipulation such as thresholding, gaussianblur, and image dilation
def basic(inputimage):

    gray = cv2.cvtColor(inputimage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1)

    minThresh = cv2.getTrackbarPos('Minimum Threshold', 'Parameters')
    maxThresh = cv2.getTrackbarPos('Maximum Threshold', 'Parameters')
    ret, threshold = cv2.threshold(blur, minThresh, maxThresh, cv2.THRESH_BINARY_INV)

    kernel = np.ones((5,5))
    dilation = cv2.dilate(threshold, kernel, iterations=1)

    return dilation, blur

# This function draws contours based on the area of the object 
def areaFilter(dilatedImage, imageContour):

    contours, hierarchy = cv2.findContours(dilatedImage, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    for countofContours in contours:
        area = cv2.contourArea(countofContours)

        areaMin = cv2.getTrackbarPos('AreaMin', 'Parameters')
        areaMax = cv2.getTrackbarPos('AreaMax', 'Parameters')
        if areaMin < area < areaMax:

            drawing = cv2.drawContours(imageContour, countofContours, -1, (0, 70, 255), 7)
            peri = cv2.arcLength(countofContours, True)
            approx = cv2.approxPolyDP(countofContours, 0.02 * peri, True)

            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imageContour, (x , y ), (x + w , y + h ), (255, 0, 0), 5)
            cv2.putText(imageContour, "Area of contour:" + str(int(area)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 0), 2)

    return imageContour

# This gives you the XY coordinates of where you clicked in pixels
def clickXY(event, x, y, flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
        cv2.putText(image, 'XY ' + str(x) + ',' + str(y), (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2) 
        cv2.imshow('Click for XY', image) 

    if event == cv2.EVENT_RBUTTONDOWN: 
        print(x, ' ', y) 
        b = image[y, x, 0] 
        g = image[y, x, 1] 
        r = image[y, x, 2] 
        cv2.putText(image, 'RGB Value: ' + str(b) + ',' + str(g) + ',' + str(r), (x,y),  cv2.FONT_HERSHEY_COMPLEX, 1, (0, 70, 255), 2) 
        cv2.imshow('Click for XY', image) 

print(f'The left click returns the XY in pixels\nThe right click will return the RGB value of the current pixel')

# First window
image = cv2.imread(imagePath, 1) 
cv2.namedWindow('Click for XY', cv2.WINDOW_FREERATIO)
cv2.resizeWindow('Click for XY', 1080, 720)
cv2.imshow('Click for XY', image) 
cv2.setMouseCallback('Click for XY', clickXY) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 

#############################################################################
# Second window 

# Creates parameters window
cv2.namedWindow('Parameters')
cv2.resizeWindow('Parameters', 640, 240)

# Inside basic function / affects threshold
cv2.createTrackbar('Minimum Threshold', 'Parameters', 75, 255, empty)
cv2.createTrackbar('Maximum Threshold', 'Parameters', 255, 255, empty)

# Inside areaFilter Function / affects minimum and maximum area of contour being drawn over
cv2.createTrackbar('AreaMin', 'Parameters', 5000, 50000, empty)
cv2.createTrackbar('AreaMax', 'Parameters', 7500, 50000, empty)

image = cv2.imread(imagePath)

while True:

    # Creates a copy of the image and overlays contours
    imageCopy = image.copy()

    # Basic function
    dilatedImage, blur = basic(image)

    area = areaFilter(dilatedImage, imageCopy)


    stack = imageStacked(0.8, ([image, dilatedImage], [area, area]))
    cv2.namedWindow('ImageIX', cv2.WINDOW_FREERATIO)
    cv2.resizeWindow('ImageIX', 1280, 720)
    cv2.imshow('ImageIX', stack)

    if cv2.waitKey(1) & 0xFF == ord('b'):
        end = time.time()
        time = round((start - end), 3)
        print(f'This program ran for a total of: {-(time)} seconds')
        break
