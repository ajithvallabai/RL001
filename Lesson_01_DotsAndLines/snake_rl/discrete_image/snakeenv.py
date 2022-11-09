from collections import deque
from gym import Env, spaces
import cv2 as cv
import numpy as np
import random
import copy

FOOD_FETCH_GOAL = 15

def snakeBody(dot, foodLoc):
    img = np.zeros((632, 632, 3), dtype="uint8")
    # Add border
    boundaryPts = np.array([[30, 30], [30, 542],
                    [542, 542], [542, 30]],
                np.int32)
    boundaryPts = boundaryPts.reshape((-1, 1, 2))
    isClosed = True
    thickness = 8
    img = cv.polylines(img, [boundaryPts],
                        isClosed, (0, 0, 255),
                        thickness)
    cv.rectangle(img, foodLoc, foodLoc, (0,255,0), 10)
    cv.rectangle(img, dot, dot, (255,255,255), 5)
    return img

def dtCollisionBoundaries(dot):
    if (dot[0] >= 542) or (dot[0] <= 30):
        return True
    if (dot[1] >= 542) or (dot[1] <= 30):
        return True
    return False

def dtFood(dot, arrFood):
    if np.linalg.norm(np.array(dot)-np.array(arrFood)) < 14:
        return True
    return False

BUFFER_MEMORY = 50
XDIM = 40
YDIM = 40
class SnakeEnv(Env):
    """Snake Environment that follows gym interface"""

    def __init__(self):
        super(SnakeEnv, self).__init__()
        # Define action and observation space
        # Using discrete action
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=255, shape=(XDIM,YDIM,3*BUFFER_MEMORY), dtype=np.uint8)

    def step(self, action):
        #self.prev_actions.append(action)
        #cv.imshow("The Slytherin Dot game", self.img)
        self.key = action
        previousArr = copy.deepcopy(self.dot)

        # Actions possible
        if self.key == 0:
            self.dot[0] = self.dot[0] - 10
        elif self.key == 1:
            self.dot[0] = self.dot[0] + 10
        elif self.key == 2:
            self.dot[1] = self.dot[1] - 10
        elif self.key == 3:
            self.dot[1] = self.dot[1] + 10

        # detect collision with boudaries
        if dtCollisionBoundaries(self.dot) == True:
            self.done = True
            print("collision with boundaries")

        # check if snake has found the food
        currFoodFetch = False
        if dtFood(self.dot, self.foodLoc) == True:
            self.foodLoc = [random.randint(31, 540), random.randint(31, 540)]
            self.score += 1
            currFoodFetch = True
            print("Food fetched")

        self.img = snakeBody(self.dot, self.foodLoc )
        #cv.waitKey(150)

        # Using distance parameters and awarding reward
        currDistToFood = np.linalg.norm(np.array(self.dot)-np.array(self.foodLoc))
        prevDistToFood = np.linalg.norm(np.array(previousArr)-np.array(self.foodLoc))

        if self.done:
            # For colliding with boundaries
            self.reward -= 200
        elif currFoodFetch:
            # Fetching current food
            self.reward += (self.score * 1000)
        elif currDistToFood < prevDistToFood:
            # staying alive and moving towards from food
            self.reward += 3
        else:
            # staying alive and moving away from food
            self.reward -= 1

        self.previousFrames = self.previousFrames[:, :, 3:] #poping first frame

        currFrame = self.img[(self.dot[1]-(YDIM//2)): (self.dot[1]+(YDIM//2)), (self.dot[0]-(XDIM//2)): (self.dot[0] + (XDIM//2))]
        # cv.imshow("The frame ", currFrame)
        # cv.waitKey(0)
        self.previousFrames = np.dstack((self.previousFrames, currFrame))
        self.observation = copy.deepcopy(self.previousFrames)
        # cv.imshow("The frame ", self.observation[:,:, :3])
        # cv.waitKey(0)
        info = {}
        return self.observation, self.reward, self.done, info

    def reset(self):
        self.done = False
        #self.img = np.zeros((512, 512, 3), dtype="uint8")

        # Food
        self.foodLoc = [random.randint(31, 540), random.randint(31, 540)]
        #cv.rectangle(self.img, self.foodLoc, self.foodLoc, (0,255,0), 10)
        self.score = 0
        self.reward = 0
        self.dot = [410,320]
        self.img = snakeBody(self.dot, self.foodLoc)
        self.key = 0 # default key left

        # observation
        self.previousFrames = np.zeros((XDIM, YDIM, 3),dtype=np.uint8)
        b = np.zeros((XDIM, YDIM, 3),dtype=np.uint8)

        for _ in range(BUFFER_MEMORY-1):
            self.previousFrames = np.dstack((self.previousFrames, b))

        self.observation = copy.deepcopy(self.previousFrames)
        return self.observation
