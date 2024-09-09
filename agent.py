import torch
import random
import numpy as np
from game import SnakeGameAI,Direction,Point
from collections import deque


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11,256,3)
        self.trainer = QTrainer(self.model,lr = LR,gamma = self.gamma)
    
        
    def get_state(self,game):
        head = game.snake[0]
        
        ponit_l = Point(head.x - 20,head.y)
        point_r = Point(head.x + 20,head.y)
        point_u = Point(head.x,head.y-20)
        point_d = Point(head.x,head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN
        
        state = [
            #Danger straight
            (dir_r and )
        ]
        
        
        
        
        
        
    
    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))
    
    def train_long_memory(self):
        pass
        