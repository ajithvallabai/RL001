import cv2 as cv
import numpy as np
import random
import copy

def carBody(arr, img):
    cv.rectangle(img, arr, arr, (255,255,255), 5)
    return img

def dtCollisionBoundaries(arr):
    if (arr[0] >= 155) or (arr[0] <= 45):
        return True
    if (arr[1] >= 465):
        return True
    return False

def dtDestination(arr):
    if (arr[1] <= 75):
        return True
    return False

def getDisplay(arr):
    img = np.zeros((512, 512, 3), dtype="uint8")
    img = carBody(arr, img)
    boundaryPts = np.array([[40, 70], [40, 470],
                    [160, 470], [160, 70]],
                np.int32)
    boundaryPts = boundaryPts.reshape((-1, 1, 2))

    destPts = np.array([[40, 70], [160, 70]],
                np.int32)
    destPts = destPts.reshape((-1, 1, 2))
    isClosed = True
    thickness = 8
    img = cv.polylines(img, [boundaryPts],
                        isClosed, (0, 255, 0),
                        thickness)
    img = cv.polylines(img, [destPts],
                        isClosed, (0, 0, 255),
                        thickness)
    return img

if __name__ == "__main__":
    arr = [92,427]
    img = getDisplay(arr)
    key = 97

    while True:
        done = False
        cv.imshow("The Car Dot game", img)

        if key == ord('a'):
            arr[0] = arr[0] - 5
        elif key == ord('d'):
            arr[0] = arr[0] + 5
        elif key == ord('w'):
            arr[1] = arr[1] - 5
        elif key == ord('s'):
            arr[1] = arr[1] + 5
        elif key == ord('q'):
            break

        # detect collision with boudaries
        if dtCollisionBoundaries(arr) == True:
            print("collision with boundaries")
            break

        # # check if snake has found the food
        if dtDestination(arr) == True:
            print("Reached destination")
            break

        img = getDisplay(arr)
        k = cv.waitKey(400)
        if k != -1:
            key = copy.deepcopy(k)