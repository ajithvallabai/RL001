from collections import deque
from gym import Env, spaces
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

BUFFER_MEMORY = 30
XDIM = 84
YDIM = 84
class CarEnv(Env):
    """Car Environment that follows gym interface"""

    def __init__(self):
        super(CarEnv, self).__init__()
        # Define action and observation space
        # Using discrete action
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=255, shape=(XDIM,YDIM,3*BUFFER_MEMORY), dtype=np.uint8)

    def step(self, action):
        cv.imshow("The Car Dot game", self.img)
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
        destReached = False
        if dtDestination(self.dot) == True:
            self.score += 1
            destReached = True
            self.done = True
            print("Destination reached")

        self.img = getDisplay(self.dot)
        cv.waitKey(150)

        # Using distance parameters and awarding reward
        # distance between a line and point
        # d = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)
        currDistToDest = np.linalg.norm(
            np.cross( (self.destPts[1]-self.destPts[0]),(self.destPts[1]-np.array(self.dot) ) )
            )/ np.linalg.norm(self.destPts[1] - self.destPts[0])

        prevDistToDest = np.linalg.norm(
            np.cross( (self.destPts[1]-self.destPts[0]),(self.destPts[1]-np.array(previousArr) ) )
            )/ np.linalg.norm(self.destPts[1] - self.destPts[0])

        if self.done and (destReached==False):
            # For colliding with boundaries
            self.reward -= 200
        elif self.done and destReached:
            # Fetching current food
            self.reward += (self.score * 1000)
        elif currDistToDest < prevDistToDest:
            # staying alive and moving towards from food
            self.reward += 3
        else:
            # staying alive and moving away from food
            self.reward -= 2
        print("#######Reward########", self.reward)

        self.destPts = np.array([[40, 70], [160, 70]],
                np.int32)
        # head_x = self.dot[0]
        # head_y = self.dot[1]
        # # Using change towards midpoint as a observation(p1.x+p2.x)/2, (p1.y+p2.y)/2
        # dest_delta_x = head_x - ((self.destPts[0][0] + self.destPts[1][0])/2)
        # dest_delta_y = head_y - ((self.destPts[0][1] + self.destPts[1][1])/2)
        self.previousFrames = self.previousFrames[1:] #poping first frame

        currFrame = self.img[(92-42): (92 + 42), (427-42): (427+42)]
        self.previousFrames.append(currFrame)
        # print(self.previousFrames[0].shape)
        # print(self.previousFrames[3].shape)
        # self.observation = np.concatenate([self.previousFrames[3],
        #                      self.previousFrames[2],self.previousFrames[1],self.previousFrames[0]],axis=-1)
        self.observation = np.swapaxes(self.previousFrames,2,1).reshape(84,84,90)
        info = {}
        return self.observation, self.reward, self.done, info

    def reset(self):
        self.done = False
        self.dot = [92,427]
        self.img = getDisplay(self.dot)

        self.score = 0
        self.reward = 0
        self.key = 0 # default key left

        # observation
        # previous move frames
        self.destPts = np.array([[40, 70], [160, 70]],
                np.int32)
        # head_x = self.dot[0]
        # head_y = self.dot[1]
        # # Using change towards midpoint as a observation(p1.x+p2.x)/2, (p1.y+p2.y)/2
        # dest_delta_x = head_x - ((self.destPts[0][0] + self.destPts[1][0])/2)
        # dest_delta_y = head_y - ((self.destPts[0][1] + self.destPts[1][1])/2)

        self.previousFrames = []
        for _ in range(BUFFER_MEMORY):
            self.previousFrames.append(np.zeros((XDIM, YDIM, 3),dtype=np.uint8))

        self.observation = np.swapaxes(self.previousFrames,2,1).reshape(84,84,90)
        #print(self.observation.shape)
        return self.observation
