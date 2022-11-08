from collections import deque
from gym import Env, spaces
import cv2 as cv
import numpy as np
import random
import copy

FOOD_FETCH_GOAL = 15

def snakeBody(dot, img):
    cv.rectangle(img, dot, dot, (255,255,255), 5)
    return img

def dtCollisionBoundaries(dot):
    if (dot[0] >= 512) or (dot[0] <= 0):
        return True
    if (dot[1] >= 512) or (dot[1] <= 0):
        return True
    return False

def dtFood(dot, arrFood):
    if np.linalg.norm(np.array(dot)-np.array(arrFood)) < 14:
        return True
    return False


class SnakeEnv(Env):
    """Snake Environment that follows gym interface"""

    def __init__(self):
        super(SnakeEnv, self).__init__()
        # Define action and observation space
        # Using discrete action
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=-500, high=500, shape=((5+FOOD_FETCH_GOAL),), dtype=np.float64)

    def step(self, action):
        self.prev_actions.append(action)
        cv.imshow("The Slytherin Dot game", self.img)
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
            # Todo: Add time limit for food fetch
            self.score += 1
            currFoodFetch = True
            print("Food fetched")

        self.img = np.zeros((512, 512, 3), dtype="uint8")
        cv.rectangle(self.img, self.foodLoc, self.foodLoc, (0,255,0), 10)

        self.img = snakeBody(self.dot, self.img)
        cv.waitKey(150)

        # Using distance parameters and awarding reward
        currDistToFood = np.linalg.norm(np.array(self.dot)-np.array(self.foodLoc))
        prevDistToFood = np.linalg.norm(np.array(previousArr)-np.array(self.foodLoc))

        if self.done:
            # For colliding with boundaries
            self.reward -= 20
        elif currFoodFetch:
            # Fetching current food
            self.reward += (self.score * 100)
        elif currDistToFood < prevDistToFood:
            # staying alive and moving towards from food
            self.reward += 1
        else:
            # staying alive and moving away from food
            self.reward -= 1

        # head_x, heady_y, apple_x, apple_y, snake_score, previous_moves
        head_x = self.dot[0]
        head_y = self.dot[1]
        apple_delta_x = head_x - self.foodLoc[0]
        apple_delta_y = head_y - self.foodLoc[1]
        snake_score = self.score
        self.observation = [head_x, head_y, apple_delta_x, apple_delta_y, snake_score] + list(self.prev_actions)
        self.observation = np.array(self.observation)
        if currFoodFetch:
            self.foodLoc = [random.randint(1, 511), random.randint(1, 511)]
        info = {}
        return self.observation, self.reward, self.done, info

    def reset(self):
        self.done = False
        self.img = np.zeros((512, 512, 3), dtype="uint8")

        # Food
        self.foodLoc = [random.randint(1, 511), random.randint(1, 511)]
        cv.rectangle(self.img, self.foodLoc, self.foodLoc, (0,255,0), 10)
        self.score = 0
        self.reward = 0
        self.dot = [410,320]
        self.img = snakeBody(self.dot, self.img)
        self.key = 0 # default key left

        # observation
        # head_x, heady_y, apple_x, apple_y, snake_score, previous_moves
        head_x = self.dot[0]
        head_y = self.dot[1]
        apple_delta_x = head_x - self.foodLoc[0]
        apple_delta_y = head_y - self.foodLoc[1]
        snake_score = self.score
        self.prev_actions = deque(maxlen=FOOD_FETCH_GOAL)
        for _ in range(FOOD_FETCH_GOAL):
            self.prev_actions.append(-1)

        self.observation = [head_x, head_y, apple_delta_x, apple_delta_y, snake_score] + list(self.prev_actions)
        self.observation = np.array(self.observation)
        return self.observation
