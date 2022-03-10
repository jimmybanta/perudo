import random
import itertools as it
import csv

from hand import Hand
from dice import D6

DICE = [1,2,3,4,5,6]

class Player:
    def __init__(self, name=False, dice=5, ai=False, gen='human'):
        self.name = name
        self.dice = dice
        self.ai = ai
        self.gen = gen
    
    def roll(self, *args):
        if args:
            self.hand = Hand(*args, size=self.dice)
        else:
            self.hand = Hand(size=self.dice)
    
    def lose_turn(self):
        self.dice -= 1
    
    @property
    def one_left(self):
        return True if self.dice == 1 else False
    
    def __str__(self):
        return self.name

    

class AIPlayer(Player):
    def __init__(self, name=False, gen='ai', dice=5):
        super().__init__(name=name, gen=gen, dice=dice, ai=True)
    
    def retrieve_probability(self, quantity, total_dice, jessies=False, straight=False):
        '''Retrieves probability that there are [quantity] dice among [total_dice] dice.
        
        Uses normal_probs unless value = 1 or it's straight - in which case it uses straight_probs'''

        if jessies or straight:
            with open('probs/straight_probs.csv', 'r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if row['number_of_dice'] != str(total_dice):
                        continue
                    return round(float(row[str(quantity)]), 4)
        else:
            with open('probs/normal_probs.csv', 'r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if row['number_of_dice'] != str(total_dice):
                        continue
                    return round(float(row[str(quantity)]), 4)
    
    
    
    
if __name__ == '__main__':
    player = Player()

    



