import numpy as np 
import random as rd

class Agent:

    actions = ["LEFT", "RIGHT", "UP", "DOWN"]

    
    
    @staticmethod
    def init_q_table(dim_x, dim_y):
        return np.zeros((dim_x, dim_y))

    def __init__(self, state_num, learning=0.15, gamma=0.8,epsilon=0.4):
        self.actions = Agent.actions
        self.learning_rate = learning
        self.gamma = gamma
        self.epsilon = epsilon
        self.qtable = Agent.init_q_table(state_num, len(self.actions))

    def choose_action_greedy(self, state):
        if rd.random() < self.epsilon:  # Exploration
            choice = rd.choice(self.actions)
        else:  # Exploitation
            best_action_index = np.argmax(self.qtable[state])
            choice = self.actions[best_action_index]
        return choice

    def TD_update(self, action, state, reward, future_state):
        action_index = self.actions.index(action)
        old_value = self.qtable[state][action_index]
        
        best_future_q = np.max(self.qtable[future_state])  # richtiger Wert
        
        new_q = old_value + self.learning_rate * ((reward + self.gamma * best_future_q ) - old_value)
        self.qtable[state][action_index] = new_q
        
    def cool_down(self):
        if self.epsilon > 0.075:
            self.epsilon *= 0.9995
            print(self.epsilon)


    def print_q_table(self):
        for i in range(len(self.qtable)):
            for y in range(len(self.qtable[i])):
                print(f"{self.qtable[i][y]:.3f}", end="\t")  # schön formatiert
            print() 

            


        








