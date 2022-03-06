import random

from hand import Hand

class Player:
    def __init__(self, name=False, dice=5, ai=False, gen='human'):
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
    def __init__(self, name=False, gen='ai', dice=5):
        super().__init__(name=name, gen=gen, dice=dice, ai=True)
    
    
    
    