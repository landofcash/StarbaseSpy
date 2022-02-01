import cv2
import numpy as np


def green_mask(inputImage, inputGray, name):
    # Convert the BGR image to HSV:
    hsvImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV)

    # Create the HSV range for the blue ink:
    # [128, 255, 255], [90, 50, 70] ,
    lowerValues = np.array([36, 15, 15])
    upperValues = np.array([70, 255,255])

    # Get binary mask of the blue ink:
    greenMask = cv2.inRange(hsvImage, lowerValues, upperValues)
    # Use a little bit of morphology to clean the mask:
    # Set kernel (structuring element) size:
    kernelSize = 1
    # Set morph operation iterations:
    opIterations = 2
    # Get the structuring element:
    morphKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelSize, kernelSize))
    # Perform closing:
    mask = cv2.morphologyEx(greenMask, cv2.MORPH_CLOSE, morphKernel, None, None, opIterations, cv2.BORDER_REFLECT101)

    colorMask = cv2.add(inputGray, greenMask)
    _, binaryImage = cv2.threshold(colorMask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    thresh, im_bw = cv2.threshold(binaryImage, 210, 230, cv2.THRESH_BINARY)
    kernel = np.ones((1, 1), np.uint8)
    imgfinal = cv2.dilate(im_bw, kernel=kernel, iterations=1)
    cv2.imwrite(name+".png", imgfinal)
    return imgfinal

