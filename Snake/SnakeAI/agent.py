import torch
import random
import numpy as np
from collections import deque
from snakeai import SnakeGameAI, Direction, Point, BLOCK_SIZE

# Defining constants
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

class Agent:
    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0 # randomness
        self.discount_rate = 0 
        self.memory = deque(maxlen=MAX_MEMORY) # If we exceed max memory it will automatically call popleft()
        self.model = None
        self.trainer = None

    def get_state(self, game):
        head = game.snake[0]
        # Calculating points around snake head
        point_left = Point(head.x - BLOCK_SIZE, head.y)
        point_right = Point(head.x + BLOCK_SIZE, head.y)
        point_up = Point(head.x, head.y - BLOCK_SIZE)
        point_down = Point(head.x, head.y + BLOCK_SIZE)
        # Calculating current direction of snake in game: One hot
        is_left_direction = game.direction == Direction.LEFT
        is_right_direction = game.direction == Direction.RIGHT
        is_up_direction = game.direction == Direction.UP
        is_down_direction = game.direction == Direction.DOWN
        # List with 11 attributes completely describing state of game for agent to process
        state = [ 
            # Danger straight/ahead
            (is_right_direction and game.is_collision(point_right)) or
            (is_left_direction and game.is_collision(point_left)) or
            (is_up_direction and game.is_collision(point_up)) or
            (is_down_direction and game.is_collision(point_down)),

            # Danger right
            (is_up_direction and game.is_collision(point_right)) or
            (is_down_direction and game.is_collision(point_left)) or
            (is_left_direction and game.is_collision(point_up)) or
            (is_right_direction and game.is_collision(point_down)),

            # Danger left
            (is_down_direction and game.is_collision(point_right)) or
            (is_up_direction and game.is_collision(point_left)) or
            (is_right_direction and game.is_collision(point_up)) or
            (is_left_direction and game.is_collision(point_down)),

            # Change direction
            is_left_direction,
            is_right_direction,
            is_up_direction,
            is_down_direction,

            # Food location
            game.food.x < game.head.x, # Food left
            game.food.x > game.head.x, # Food right
            game.food.y < game.head.y, # Food up
            game.food.y > game.head.y, # Food down
        ]
        return np.array(state, dtype=int) # Convert list to numpy array and set data type as int

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over)) # popleft automatically if MAX_MEMORY reached
         
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            # Generate random sample
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples of size BATCH_SIZE
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        """Method to train agent for one game_iteration/frame_iteration"""
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        """Method to perform random moves as tradeoff between exploration and exploitation"""
        # In the beginning we will be exploring more than exploting, later on it becomes the opposite
        self.epsilon = 80 - self.number_of_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            # Explore: Make a random move
            move_index = random.randint(0, 2)
            final_move[move_index] = 1
        else:
            # Exploit: Make a move based on our model
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model.predict(state0) # Makes prediciton based on one state
            move_index = torch.argmax(prediction).item()
            final_move[move_index] = 1
        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    best_score = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # Get current state
        current_state = agent.get_state(game)
        # Get move based on current state
        final_move = agent.get_action(current_state)
        # Perform move and get new state
        reward, game_over, score = game.play_step(final_move)
        new_state = agent.get_state(game)
        # Train short memory
        agent.train_short_memory(current_state, final_move, reward, new_state, game_over)
        # Store in memory
        agent.remember(current_state, final_move, reward, new_state, game_over)
        if game_over:
            # Train the long memory/experience replay, plot results
            game.reset()
            agent.number_of_games += 1
            agent.train_long_memory()
            # Set new high score if achieved
            if score > best_score:
                best_score = score
                # agent.model.save()
            print('Game', agent.number_of_games, 'Score', score, 'High Score:', best_score)

if __name__ == '__main__':
    train()