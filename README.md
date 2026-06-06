# 🟡 Micro-Pacman Reinforcement Learning Agent

## Introduction

This project implements a simplified version of Pacman using Python and Pygame. The goal is to train an autonomous agent that learns to collect all cookies in a maze while avoiding a ghost that actively pursues it.

The agent is trained using **Q-Learning**, a model-free reinforcement learning algorithm. Through repeated interactions with the environment, the agent learns which actions maximize its long-term reward and develops a strategy for surviving and collecting cookies efficiently.

---

# 🎥 Demo

## RESULT

## PRE TRAINING Results




https://github.com/user-attachments/assets/019a350b-c221-4038-89c2-1d5b1577f3db


## POST TRAINING RESULTS 



https://github.com/user-attachments/assets/916bd62a-34df-44ee-8a07-a70f37144689




---

# 🚀 Features

* Custom Pacman environment built with Pygame
* Q-Learning based reinforcement learning agent
* ε-greedy exploration strategy
* Dynamic ghost opponent
* Reward-based learning
* State-space compression
* Automatic training over thousands of episodes
* Training progress visualization using Matplotlib
* Randomized starting positions
* Cookie collection objective

---

# 🕹️ Environment

The game is played inside a small maze:

```text
##########
#........#
#.##..##.#
#........#
##########
```

### Symbols

| Symbol | Meaning     |
| ------ | ----------- |
| #      | Wall        |
| .      | Cookie      |
| Space  | Empty field |

---

# 🤖 Agent Design

The agent is implemented in `Agent.py` and uses a Q-table to estimate the value of actions in different states.

Possible actions:

* LEFT
* RIGHT
* UP
* DOWN

The agent follows an ε-greedy strategy:

* With probability ε: explore randomly
* Otherwise: choose the currently best action

The exploration rate gradually decreases during training.

---

# 📊 State Representation

To keep the state space manageable, the environment is encoded using a small set of features.

The state consists of:

| Feature          | Description                               |
| ---------------- | ----------------------------------------- |
| Ghost Direction  | Direction of the ghost relative to Pacman |
| Cookie Direction | Direction of the nearest cookie           |
| Ghost Distance   | Scaled Manhattan distance                 |
| Pacman X         | Horizontal position                       |
| Pacman Y         | Vertical position                         |

The state is converted into a unique integer index that is used to access the Q-table.

---

## Ghost Direction Encoding

| Value | Direction |
| ----- | --------- |
| 1     | Left      |
| 2     | Right     |
| 3     | Up        |
| 4     | Down      |

---

## Distance Scaling

The Manhattan distance between Pacman and the ghost is compressed into three categories:

| Distance | Encoded Value |
| -------- | ------------- |
| < 2      | 0             |
| 2 – 3    | 1             |
| ≥ 4      | 2             |

This reduces the size of the state space and improves learning speed.

---

# 🎯 Reward Function

The reward function guides the learning process.

| Event            | Reward |
| ---------------- | ------ |
| Every step       | -0.1   |
| Cookie collected | +0.25  |
| Win game         | +1     |
| Caught by ghost  | -1     |

### Motivation

* Small negative rewards encourage shorter solutions.
* Positive rewards encourage cookie collection.
* Winning is strongly rewarded.
* Collisions with the ghost are punished.

---

# 📚 Learning Algorithm

The agent learns using Temporal Difference Learning (TD Learning).

Q-values are updated according to:

Q(s,a) ← Q(s,a) + α · [r + γ · max(Q(s',a')) − Q(s,a)]

Where:

| Symbol | Meaning         |
| ------ | --------------- |
| α      | Learning Rate   |
| γ      | Discount Factor |
| r      | Reward          |
| s      | Current State   |
| s'     | Next State      |

---

## Hyperparameters

| Parameter                    | Value |
| ---------------------------- | ----- |
| Learning Rate (α)            | 0.25  |
| Discount Factor (γ)          | 0.8   |
| Initial Exploration Rate (ε) | 0.45  |
| Minimum ε                    | 0.075 |

Exploration decays after every episode:

```python
epsilon *= 0.9995
```

---

# 👻 Ghost Behavior

The ghost follows a simple chasing strategy.

Every third game iteration it moves one step toward Pacman:

* Horizontal movement has priority.
* Vertical movement is used when horizontal movement is not possible.
* Walls cannot be crossed.

This creates a moving threat that the agent must learn to avoid.

---

# 🏆 Winning Condition

Pacman wins when all cookies have been collected.

The game ends immediately when:

1. All cookies are eaten.
2. The ghost catches Pacman.

---

# 📈 Training Process

Training consists of approximately 6000 episodes.

For each episode:

1. The maze is reset.
2. Pacman starts at a random valid position.
3. The ghost starts in the lower-right corner.
4. The agent interacts with the environment.
5. Rewards are collected.
6. The Q-table is updated.

During training, the cumulative number of wins is tracked and plotted.

---

# 📁 Project Structure

```text
Micro-Pacman/
│
├── main.py
├── Agent.py
├── paci_demox.mp4
├── README.md
└── requirements.txt
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/micro-pacman.git
cd micro-pacman
```

Install dependencies:

```bash
pip install pygame numpy matplotlib
```

---

# ▶️ Running the Project

Start the training process:

```bash
python main.py
```

The first few games and the final trained games will be rendered using Pygame.

A graph showing the cumulative number of wins will be displayed after training.

---

# 📈 Example Learning Outcome

After several thousand training episodes the agent learns to:

* Move efficiently toward cookies.
* Avoid direct collisions with the ghost.
* Finish games faster.
* Increase its overall win rate.

The cumulative win count steadily increases as training progresses.

---

# 🔮 Possible Improvements

Future extensions could include:

* Deep Q-Networks (DQN)
* Multiple ghosts
* Larger mazes
* Power pellets
* Better pathfinding ghosts
* Experience replay
* Double DQN
* Policy Gradient methods
* Procedurally generated maps

---

# 🛠️ Technologies Used

* Python 3
* Pygame
* NumPy
* Matplotlib
* Reinforcement Learning (Q-Learning)

---

# 👨‍💻 Author

**Samroy Gilbert**

B.Sc. Wirtschaftsinformatik

University Student focusing on:

* Machine Learning
* Data Science
* Reinforcement Learning
* Artificial Intelligence

---

# 📄 License

This project is provided for educational and research purposes.

Feel free to use, modify and extend the code for learning and experimentation.

