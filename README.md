Dungeon Escape 

 # Overview

Dungeon Escape is a multi-agent reinforcement learning simulation where three agents collaborate to escape a dungeon. The agents must eliminate a dragon to obtain a key, unlock the door, and escape. If they take too long, the dragon escapes through a portal and the environment resets.

# Objective
One agent sacrifices itself to defeat the dragon
Dragon drops a key
Remaining agents pick the key
Unlock the door and escape

# Agents
Total: 3 agents
Behavior:
Learn using Q-learning (basic RL)
Move randomly until goal appears
Move toward key when visible
Move toward door after picking key

# Dragon
Moves in semi-random pattern
If agents delay:
Dragon escapes via portal
Game resets

# Key
Appears only after dragon is defeated
Must be picked by any alive agent

# Door
Final exit point
Agent with key must reach here to win

# Portal
Dragon escape point
Triggered after time limit

# Reward System
Event	Reward
Agent escapes successfully	+1
No escape / timeout	0


# How to Run
1. Install dependencies
pip install pygame
2. Run the project
    python main.py
   
# Controls
Click START → begin simulation
Click RESTART → reset after game ends

# Expected Behavior
Scenario 1 (Success)
Agent kills dragon
Key appears
Agent picks key
Reaches door

# Output:
AGENT WINS!
Reward: 1
Scenario 2 (Failure)
Agents take too long
Dragon escapes through portal
Game resets automatically

# Features
Multi-agent system
Basic reinforcement learning (Q-learning)
Dynamic environment reset
Obstacle navigation
Interactive UI (Start/Restart)

# Author
Lakshman

# Summary
This project demonstrates a hybrid approach combining:

Reinforcement Learning
Rule-based AI
Multi-agent coordination
to solve a cooperative escape problem.
