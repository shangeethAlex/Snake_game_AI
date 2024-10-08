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
        self.epsilon = 0 #randomness
        self.gamma = 0.9 
        self.memory = deque(maxlen=MAX_MEMORY) #pop left
        self.model = None #TODO
        self.trainer = None #TODO
   
        
        
    def get_state(self, game):
        head = game.snake[0] #head
        point_l = Point(head.x-20,head.y)
        point_r = Point(head.x+20,head.y)
        point_u = Point(head.x,head.y-20)
        point_d = Point(head.x,head.y+20)
    
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN
        
        state = [
            #Danger straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),
    
            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),
            
            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            #move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            #food location
            game.food.x < game.head.x,  # Food is to the left
            game.food.x > game.head.x,  # Food is to the right
            game.food.y < game.head.y,  # Food is above
            game.food.y > game.head.y   # Food is below
            
        ]
        
        return np.array(state,dtype=int)
            
    
    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done)) #pop left if MAX_MEMORY is reached
    

    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory,BATCH_SIZE) #list of tuples
        else:
            mini_sample = self.memory
            
        states,actions,rewards,next_states,dones = zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards,next_states,dones)
        
        
        self.trainer.train_step(states,actions,rewards,next_states,dones)
    
    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)
        
    
    #responsible for determining the next move for the AI agent
    #This function uses a combination of exploration (random moves) and 
    # exploitation (using the model's predictions) to decide the agent's next move. 
    def get_action(Self,state):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        
        #deciding whether to explore or exploit
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1
        
        else:
            state0 = torch.tensor(state,dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move
    
    
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    
    while True:
        #get old state
        state_old = agent.get_state(game)
        
        #get move
        final_move = agent.get_action(state_old)
        
        #perform move and get new state
        reward,done,score = game.play_step(final_move)
        state_new = agent.get_state(game)
        
        #train short memory 
        agent.train_short_memory(state_old,final_move,reward,state_new,done)
        
        #remember
        agent.remember(state_old,final_move,reward,state_new,done)
        
        if done:
            #train long memory /replay memory
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            
            if score > record:
                record = score
                # agent.model.save()
                
            print('Gmae',agent.n_games,'Score',score,'Record:',record)
            
            #TODO: plot
            
            

if __name__ =="__main__":
    train()
    
    
        
    