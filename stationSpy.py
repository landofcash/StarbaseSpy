import asyncio

from skimage.metrics import structural_similarity
import screenshot
import cv2
import numpy as np
import winsound
import config


async def act(t, window_name="starbase"):
    images_folder="img"

    screenshot.make_screenshot(window_name, f"{images_folder}/1")
    await asyncio.sleep(5)  # Sleep for 5 seconds
    screenshot.make_screenshot(window_name, f"{images_folder}/2")

    # load images
    before = cv2.imread(f"{images_folder}/1.png")
    after = cv2.imread(f"{images_folder}/2.png")
    #crop
    y = config.settings["sstop"]
    x = config.settings["ssleft"]#150
    h = 200
    w = 500
    before = before[y:y + h, x:x + w]
    after = after[y:y + h, x:x + w]
    cv2.imwrite(f'{images_folder}/cut-before.png', before)
    cv2.imwrite(f'{images_folder}/cut-after.png', after)
    # Convert images to grayscale
    before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    (score, diff) = structural_similarity(before_gray, after_gray, full=True)
    print("Image similarity:", score)

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type in the range [0,1]
    # so we must convert the array to 8-bit unsigned integers in the range
    # [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(before.shape, dtype='uint8')
    filled_after = after.copy()
    alarm = False
    for c in contours:
        area = cv2.contourArea(c)
        if area > 200:
            print("Countour area:", area)
            alarm = True
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(before, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.rectangle(after, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
            cv2.drawContours(filled_after, [c], 0, (0, 255, 0), -1)
    if alarm:
        winsound.Beep(2500, 1000)
        print("ALARM")
        cv2.imwrite(f'{images_folder}/before{t}.png', before)
        cv2.imwrite(f'{images_folder}/after{t}.png', after)
        #cv2.imwrite(f'{images_folder}/diff{t}.png', diff)
        #cv2.imwrite(f'{images_folder}/mask{t}.png', mask)
        return 1
    #cv2.imwrite(f'{images_folder}/before{t}.png', before)
    #cv2.imwrite(f'{images_folder}/after{t}.png', after)
    return 0