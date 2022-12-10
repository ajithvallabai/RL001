import cv2 as cv
import numpy as np
import random
import copy

def snakeBody(dot, img):
    cv.rectangle(img, dot, dot, (255,255,255), 5)
    return img

def dtCollisionBoundaries(dot):
    if (dot[0] >= 512) or (dot[0] <= 0):
        return True
    if (dot[1] >= 512) or (dot[1] <= 0):
        return True
    return False

def dtFood(dot, foodDot):
    if np.linalg.norm(np.array(dot)-np.array(foodDot)) < 14:
        return True
    return False

if __name__ == "__main__":
    img = np.zeros((512, 512, 3), dtype="uint8")

    # Food
    foodDot = [random.randint(1, 511), random.randint(1, 511)]
    cv.rectangle(img, foodDot, foodDot, (0,255,0), 10)

    dot = [410,320]
    img = snakeBody(dot, img)
    key = 97 # default key left

    while True:
        done = False
        cv.imshow("The Slytherin Dot game", img)
        if key == ord('a'):
            dot[0] = dot[0] - 5
        elif key == ord('d'):
            dot[0] = dot[0] + 5
        elif key == ord('w'):
            dot[1] = dot[1] - 5
        elif key == ord('s'):
            dot[1] = dot[1] + 5
        elif key == ord('q'):
            break

        # detect collision with boudaries
        if dtCollisionBoundaries(dot) == True:
            print("collision with boundaries")
            break

        # check if snake has found the food
        if dtFood(dot, foodDot) == True:
            foodDot = [random.randint(1, 511), random.randint(1, 511)]
            print("Food fetched")

        img = np.zeros((512, 512, 3), dtype="uint8")
        cv.rectangle(img, foodDot, foodDot, (0,255,0), 10)

        img = snakeBody(dot, img)
        k = cv.waitKey(400)
        if k != -1:
            key = copy.deepcopy(k)