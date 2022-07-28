import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
# https://stackoverflow.com/questions/12876177/how-to-create-a-tuple-with-only-one-element

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, filename='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        filename = os.path.join(model_folder_path, filename)
        torch.save(self.state_dict(), filename)

class QTrainer:
    def __init__(self, model, learning_rate, discount_rate):
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def train_step(self, current_state, action, reward, new_state, game_over):
        # Convert parameters to pytorch tensors
        current_state = torch.tensor(current_state, dtype=torch.float)
        new_state = torch.tensor(new_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # Handle parameters of varying length
        if len(current_state.shape) == 1:
            # Single value: (1, x), Multiple values: (n, x)
            current_state = torch.unsqueeze(current_state, 0)
            new_state = torch.unsqueeze(new_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            game_over = (game_over, ) # Creates a tuple with a single element, without the comma this would be converted to a string
        # 1. Predicted Q values with current state
        prediction = self.model(current_state)
        target = prediction.clone()
        for index in range(len(game_over)):
            Q_new = reward[index]
            if not game_over[index]:
                Q_new = reward[index] + self.discount_rate * torch.max(self.model(new_state[index]))
            target[index][torch.argmax(action).item()] = Q_new
        # 2. q_new = reward + discount_rate * max(next_predicted_q_value) -> only do this if not game_over
        # prediction.clone()
        # predictions[argmax(action)] = q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, prediction)
        loss.backward()
        self.optimizer.step()