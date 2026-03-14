Custom Reinforcement Learning agent for a simplified Pacman maze built with pygame.

### Core Features
- Custom Q-Table implementation using NumPy  
- ε-greedy action selection with automatic cool-down (0.45 → 0.075)  
- TD(0) update with discount factor γ = 0.8 and learning rate α = 0.25  
- Smart state encoding (ghost direction, nearest cookie direction, scaled distance, position)

### Technologies
Python • NumPy • Pygame • Matplotlib (win-rate plot)

**Result:** The agent learns to win consistently after ~7,000 episodes (win rate rises from 0 % to >76 %).

Full code + training visualization available in the repository.
