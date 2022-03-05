import random

from hand import Hand

class Player:
    def __init__(self, name, dice=5, ai=False, gen='human'):
        self.name = name
        self.dice = dice
        self.ai = ai
        self.gen = gen
        self.one_left = True if self.dice == 1 else False
    
    def roll(self):
        self.hand = Hand(size=self.dice)
    
    def lose_turn(self):
        self.dice -= 1
    
    def __str__(self):
        return self.name


class AIPlayer(Player):
    def __init__(self, name, gen='ai', dice=5):
        self.name = 'Player {}'.format(name)
        super().__init__(name=self.name, ai=True, gen=gen, dice=dice)
    
    
    
    