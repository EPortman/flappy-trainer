# Train an AI Model to play Flappy Bird

### High Level Overview:
1. **ai_trainer.py**
    - Orchestrates the training of the RL agent
2. **reinforcement_learning_agent.py**
    - Contains the NN Model that learns how to play flappy bird

## The RL Agent aims to match an input with an output

### Input = numpy tensor representing the game state
  1. **Bird Vertical Position:** [0 -> 1]  
  2. **Bird Vertical Velocity:** [-1 -> 1]  
  3. **Pipe Velocity:** [0 -> 1]  
  4. **Next Pipe Distance:** [0 -> 1] (1 if none)  
  5. **Next Pipe Gap Position:** [0 -> 1] (0.5 if none)  
  6. **Next Pipe Gap Height:** [0 -> 1] (0.25 if none)  
  7. **Second Pipe Distance:** [0 -> 1] (1 if none)  
  8. **Second Pipe Gap Position:** [0 -> 1] (0.5 if none)  
  9. **Second Pipe Gap Height:** [0 -> 1] (0.25 if none)  

### Output = Whether to flap or not

## The RL agent learns via Q-Learning on previous gameplay examples
1. Whenever the agent makes an action, the state at which the action happened and action is stored
2. Once a period of time has passed since the action, the post state is captured and reward for that action is calculated
3. The pre-state, action, post-state, and reward are then stored as knowledge
4. Periodically, the agent replays the knowledge to better match the pre-states so their actions yield greater reward
5. This repeats helping the agent make better decisions in the future



## The AI Trainer orchestratess the game and RL agents interactions with the game
- Controls the game with a copy of the Game Manager
- Controls the agent with a copy of the RL agent

### The AI Trainer splits training into curricula
1. Makes the training more efficient as the agent does not have to learn everything all at once
2. Starts the training with no pipes and gradually gets more difficult

### The AI Trainer runs each curriculum until the Agent gets it
```
action_tick = 1/4 sec
replay_interval = action_tick * 2

for every episode in curricula:
   start_game()
   current_tick = 0
   pending_actions = []
   while bird is alive:
     update_game(1)
     current_tick += 1
     if current_tick % action_tick == 0:
        pre_state = get_current_state()
        action = agent.choose_action(pre_state)
        apply_action(action)
        for action_made in pending_actions:
          if current_tick - action_made.tick >= action_tick:
             post_state = get_current_state()
             reward = 1 if post_state.is_alive else -1
             knowledge = action_made.state, action, reward, post_state
             agent.remember(knowledge)
        if current_tick % replay_interval == 0
           agent.replay()
     if bird is alive for a long time:
        agent gets it and can move on to next curriculum
```
