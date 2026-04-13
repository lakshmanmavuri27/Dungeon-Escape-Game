import numpy as np
from agent import Agent
from dragon import Dragon
from objects import Door, Portal, Key, Pillar
from settings import *

class Environment:
    def __init__(self):
        self.reset()

    def reset(self):
        self.agents = [
            Agent(50,50),
            Agent(100,50),
            Agent(150,50)
        ]

        self.dragon = Dragon()
        self.door = Door()
        self.portal = Portal()
        self.key = Key()

        self.pillars = [
            Pillar(250,200),
            Pillar(450,300),
            Pillar(600,200)
        ]

        self.timer = 0
        return self.get_state()

    # 🔥 STATE (Observation)
    def get_state(self):
        state = []

        for agent in self.agents:
            state.extend([
                agent.rect.x / WIDTH,
                agent.rect.y / HEIGHT,
                int(agent.has_key)
            ])

        # dragon
        state.extend([
            self.dragon.rect.x / WIDTH,
            self.dragon.rect.y / HEIGHT,
            int(self.dragon.alive)
        ])

        # key
        state.append(int(self.key.visible))

        return np.array(state, dtype=float)

    # 🔥 STEP FUNCTION (core RL)
    def step(self, actions):
        reward = 0
        done = False

        self.timer += 1

        self.dragon.move(self.pillars)

        # apply actions
        for i, agent in enumerate(self.agents):
            agent.step(actions[i], self.pillars)

        # sacrifice
        for agent in self.agents:
            if agent.alive and self.dragon.alive:
                if agent.rect.colliderect(self.dragon.rect):
                    agent.alive = False
                    self.dragon.alive = False

                    self.key.visible = True
                    self.key.rect.topleft = self.dragon.rect.topleft

        # key pickup
        if self.key.visible:
            for agent in self.agents:
                if agent.alive and agent.rect.colliderect(self.key.rect):
                    agent.has_key = True
                    self.key.visible = False

        # win condition (GROUP REWARD)
        for agent in self.agents:
            if agent.alive and agent.has_key:
                if agent.rect.colliderect(self.door.rect):
                    reward = 1   # ✅ required
                    done = True
                    return self.get_state(), reward, done

        # timeout reset
        if self.timer > TIMER_LIMIT and self.dragon.alive:
            if self.dragon.rect.colliderect(self.portal.rect):
                done = True
                reward = 0

        return self.get_state(), reward, done

    def draw(self, screen):
        self.door.draw(screen)
        self.portal.draw(screen)
        self.key.draw(screen)

        for p in self.pillars:
            p.draw(screen)

        self.dragon.draw(screen)

        for agent in self.agents:
            agent.draw(screen)