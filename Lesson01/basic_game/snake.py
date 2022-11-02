import cv2 as cv
import numpy as np
import random
import copy

def snakeBody(arr, img):
    cv.rectangle(img, arr, arr, (255,255,255), 5)
    return img

def dtCollisionBoundaries(arr):
    if (arr[0] >= 512) or (arr[0] <= 0):
        return True
    if (arr[1] >= 512) or (arr[1] <= 0):
        return True
    return False

def dtFood(arr, arrFood):
    if np.linalg.norm(np.array(arr)-np.array(foodArr)) < 14:
        return True
    return False

img = np.zeros((512, 512, 3), dtype="uint8")

# Food
foodArr = [random.randint(1, 511), random.randint(1, 511)]
cv.rectangle(img, foodArr, foodArr, (0,255,0), 10)

arr = [410,320]
img = snakeBody(arr, img)
key = 97 # default key left

while True:
    done = False
    cv.imshow("The Slytherin Dot game", img)
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

    # check if snake has found the food
    if dtFood(arr, foodArr) == True:
        foodArr = [random.randint(1, 511), random.randint(1, 511)]
        print("Food fetched")

    img = np.zeros((512, 512, 3), dtype="uint8")
    cv.rectangle(img, foodArr, foodArr, (0,255,0), 10)

    img = snakeBody(arr, img)
    k = cv.waitKey(400)
    if k != -1:
        key = copy.deepcopy(k)
