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
    '''Comes with a prob method that, passed a bet and the total dice, returns the prob of that bet.'''
    def __init__(self, name=False, gen='ai', dice=5):
        super().__init__(name=name, gen=gen, dice=dice, ai=True)


    def dice_needed(self, current_bet, total_dice, straight=False, jessies=False):
        '''Determines how many dice are needed, and how many unknown dice there are.
        
        Ex. A call of (3,3) out of 6 dice, when you have a hand of [1,2,3], would return 
        total_needed = 1, unknown_dice = 3 if straight=False
        or total_needed = 1, unknown_dice = 3 if straight=True'''

        hand = self.hand

        quantity, value = current_bet

        total_needed = quantity
        unknown_dice = total_dice - len(hand)

        for die in hand:
            if straight or jessies:
                if die.value == value:
                    total_needed -= 1
            else:
                if die.value == value or die.value == 1:
                    total_needed -= 1
        
        return total_needed, unknown_dice

    def retrieve_probability(self, total_needed, unknown_dice, straight=False, jessies=False):
        '''Retrieves probability of a [bet] among [total_dice] dice, given your current hand.
        
        Uses normal_probs unless value = 1 or it's straight - in which case it uses straight_probs'''

        if jessies or straight:
            with open('probs/straight_probs.csv', 'r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if row['number_of_dice'] != str(unknown_dice):
                        continue
                    return round(float(row[str(total_needed)]), 4)
        else:
            with open('probs/normal_probs.csv', 'r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if row['number_of_dice'] != str(unknown_dice):
                        continue
                    return round(float(row[str(total_needed)]), 4)
    
    def prob(self, bet, total_dice, straight=False, jessies=False):
        '''Given a bet, determines the probability of it GIVEN THE CURRENT HAND'''

        total_needed, unknown_dice = self.dice_needed(bet, total_dice, straight=straight, jessies=jessies)

        if total_needed > 0 and total_needed <= unknown_dice:
            return self.retrieve_probability(total_needed, unknown_dice, straight=straight, jessies=jessies)
        elif total_needed > unknown_dice:
            return 0
        else:
            return 1

    


    
    
if __name__ == '__main__':
    player = AIPlayer()

    player.roll()
    print(player.hand)


    print(player.prob((3,6), 10))



