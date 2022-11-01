import cv2 as cv
import numpy as np
import random
import time
import copy

def snakeBody(arrOld1, arrNew1, img):
    for each in arrOld1:
        cv.rectangle(img, each[0], each[1], (0,0,0), 5)
    for each in arrNew1:
        cv.rectangle(img, each[0], each[1], (255,255,255), 5)
    return img
img = np.zeros((512, 512, 1), dtype="uint8")


arrOld = [[[410,320],[410,320]], [[415,320],[415,320]]]
arrNew = [[[410,320],[410,320]], [[415,320],[415,320]]]
img = snakeBody(arrOld, arrNew, img)


while True:
    # snake body
    cv.imshow("Single channel window", img)
    #make snake to roll
    print("hi")
    if cv.waitKey(0) == ord('a'):
        for each in range(0,2):
            arrNew[each][0][0] = arrOld[each][0][0]-5
            arrNew[each][1][0] = arrOld[each][1][0]-5
        print(arrOld)
        print(arrNew)
        img = snakeBody(arrOld, arrNew, img)
        time.sleep(0.5)
        cv.imshow("Single channel window", img)
        arrOld = copy.deepcopy(arrNew)
    print("after loop")
    #cv.waitKey(0)

    cv.destroyAllWindows()