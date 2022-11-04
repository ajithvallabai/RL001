import cv2 as cv
import numpy as np
import random
import copy

def carBody(arr, img):
    cv.rectangle(img, arr, arr, (255,255,255), 5)
    return img

def dtCollisionBoundaries(arr):
    if (arr[0] <= 45):
        return True
    if (arr[1] <= 75) or (arr[1] >= 475):
        return True
    return False

def dtDestination(arr):
    if (arr[0] >= 835):
        return True
    return False

def getDisplay(arr):
    img = np.zeros((512, 900, 3), dtype="uint8")
    img = carBody(arr, img)
    boundaryPts = np.array([[40, 70], [40, 470],
                    [840, 470], [840, 70]],
                np.int32)
    boundaryPts = boundaryPts.reshape((-1, 1, 2))

    destPts = np.array([[840, 470], [840, 70]],
                np.int32)
    destPts = destPts.reshape((-1, 1, 2))

    hindPts1 = np.array([[194, 474], [194, 304]],
                np.int32)
    hindPts1 = hindPts1.reshape((-1, 1, 2))

    hindPts2 = np.array([[408, 474], [408, 304]],
                np.int32)
    hindPts2 = hindPts2.reshape((-1, 1, 2))

    hindPts3 = np.array([[682, 474], [682, 304]],
                np.int32)
    hindPts3 = hindPts3.reshape((-1, 1, 2))

    hindPts4 = np.array([[281, 69], [281, 231]],
                np.int32)
    hindPts4 = hindPts4.reshape((-1, 1, 2))

    hindPts5 = np.array([[541, 69], [541, 231]],
                np.int32)
    hindPts5 = hindPts5.reshape((-1, 1, 2))

    isClosed = True
    thickness = 8
    img = cv.polylines(img, [boundaryPts],
                        isClosed, (0, 255, 0),
                        thickness)
    img = cv.polylines(img, [destPts],
                        isClosed, (0, 0, 255),
                        thickness)
    img = cv.polylines(img, [hindPts1],
                        isClosed, (120, 120, 0),
                        thickness)
    img = cv.polylines(img, [hindPts2],
                        isClosed, (120, 120, 0),
                        thickness)
    img = cv.polylines(img, [hindPts3],
                        isClosed, (120, 120, 0),
                        thickness)
    img = cv.polylines(img, [hindPts4],
                    isClosed, (120, 120, 0),
                    thickness)
    img = cv.polylines(img, [hindPts5],
                    isClosed, (120, 120, 0),
                    thickness)
    return img

def collisionWithHind(arr):
    #[194, 474], [194, 304]
    if (190 <= arr[0] <= 199) and (304 <= arr[1] <= 474):
        return True

    #[408, 474], [408, 304]
    if ((408-5) <= arr[0] <= (408+5)) and (304 <= arr[1] <= 474):
        return True

    #[682, 474], [682, 304]
    if ((682-5) <= arr[0] <= (682+5)) and (304 <= arr[1] <= 474):
        return True
    #[281, 69], [281, 231]
    if ((281-5) <= arr[0] <= (281+5)) and (69 <= arr[1] <= 231):
        return True

    #[541, 69], [541, 231]
    if ((541-5) <= arr[0] <= (541+5)) and (69 <= arr[1] <= 231):
        return True
    return False

if __name__ == "__main__":
    arr = [59,268]
    img = getDisplay(arr)
    key = 100

    while True:
        done = False
        cv.imshow("The Bird Dot game", img)
        #key = cv.waitKey(0)
        if key == ord('a'):
            arr[0] = arr[0] - 5
        elif key == ord('d'):
            arr[0] = arr[0] + 5
        elif key == ord('w'):
            arr[1] = arr[1] - 5
        elif key == ord('s'):
            arr[1] = arr[1] + 5
        elif key == ord('e'):
            arr[0] = arr[0] + 5
            arr[1] = arr[1] - 5
        elif key == ord('z'):
            arr[0] = arr[0] + 5
            arr[1] = arr[1] + 5
        elif key == ord('q'):
            break

        if dtCollisionBoundaries(arr) == True:
            print("Collided")
            break
        if dtDestination(arr) == True:
            print("Reached destination")
            break
        if collisionWithHind(arr) == True:
            print("Collided with hinderance")
            break
        img = getDisplay(arr)
        k = cv.waitKey(400)
        if k != -1:
            key = copy.deepcopy(k)