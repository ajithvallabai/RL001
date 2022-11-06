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
                        isClosed, (0, 0, 255),
                        thickness)
    img = cv.polylines(img, [destPts],
                        isClosed, (0, 255, 0),
                        thickness)
    return img

BUFFER_MEMORY = 20

class CarEnv(Env):
    """Car Environment that follows gym interface"""

    def __init__(self):
        super(CarEnv, self).__init__()
        # Define action and observation space
        # Using discrete action
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=-500, high=500, shape=((4+BUFFER_MEMORY),), dtype=np.float64)

    def step(self, action):
        self.prev_actions.append(action)
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

        # check if dest is reached
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
            self.reward -= 20
        elif self.done and destReached:
            # Fetching current food
            self.reward += (self.score * 100)
        elif currDistToDest < prevDistToDest:
            # staying alive and moving towards from food
            self.reward += 1
        else:
            # staying alive and moving away from food
            self.reward -= 1
        print("#######Reward########", self.reward)

        # head_x, heady_y,  dest_delta_x, dest_delta_y + previous_moves
        self.destPts = np.array([[40, 70], [160, 70]],
                np.int32)
        head_x = self.dot[0]
        head_y = self.dot[1]
        # Using change towards midpoint as a observation(p1.x+p2.x)/2, (p1.y+p2.y)/2
        dest_delta_x = head_x - ((self.destPts[0][0] + self.destPts[1][0])/2)
        dest_delta_y = head_y - ((self.destPts[0][1] + self.destPts[1][1])/2)

        self.observation = [head_x, head_y, dest_delta_x, dest_delta_y] + list(self.prev_actions)
        self.observation = np.array(self.observation)

        info = {}
        return self.observation, self.reward, self.done, info

    def reset(self):
        self.done = False
        self.dot = [92,427]
        self.img = getDisplay(self.dot)

        # Food
        self.score = 0
        self.reward = 0
        self.key = 0 # default key left

        # observation
        # head_x, heady_y,  dest_delta_x, dest_delta_y + previous_moves
        self.destPts = np.array([[40, 70], [160, 70]],
                np.int32)
        head_x = self.dot[0]
        head_y = self.dot[1]

        # Using change towards midpoint as a observation(p1.x+p2.x)/2, (p1.y+p2.y)/2
        dest_delta_x = head_x - ((self.destPts[0][0] + self.destPts[1][0])/2)
        dest_delta_y = head_y - ((self.destPts[0][1] + self.destPts[1][1])/2)

        self.prev_actions = deque(maxlen=BUFFER_MEMORY)
        for _ in range(BUFFER_MEMORY):
            self.prev_actions.append(-1)

        self.observation = [head_x, head_y, dest_delta_x, dest_delta_y] + list(self.prev_actions)
        self.observation = np.array(self.observation)
        return self.observation
