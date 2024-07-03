import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
    
    def __len__(self):
        return len(self.buffer)

class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(32, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 16)
        self.relu = nn.ReLU()
        
        self.optimizer = optim.Adam(self.parameters())
        self.loss_fn = nn.MSELoss()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def get_move(self, board_state, legal_moves, epsilon=0.1):
        legal_indices = [i for i, move in enumerate(legal_moves) if move == 1]
        
        if not legal_indices:
        	#print("No legal moves availible!")
        	#print("Board state:", board_state)
        	#print("Legal moves:", legal_moves)
        	raise ValueError("No legal moves available")
        	
        if random.random() < epsilon:
        	return random.choice(legal_indices)
            
        state = torch.FloatTensor(board_state)
        with torch.no_grad():
            q_values = self(state)
        
        masked_q_values = q_values.clone()
        masked_q_values[torch.tensor(legal_moves) == 0] = float('-inf')
        
        return masked_q_values.argmax().item()

    def update(self, replay_buffer, batch_size, gamma): 
        if len(replay_buffer) < batch_size:
            return
        
        batch = replay_buffer.sample(batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)
        
        current_q_values = self(states).gather(1, actions.unsqueeze(1))
        next_q_values = self(next_states).max(1)[0]
        target_q_values = rewards + (gamma * next_q_values * (1 - dones))
        
        loss = self.loss_fn(current_q_values, target_q_values.unsqueeze(1))
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item()

