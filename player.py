import random
import itertools as it

from hand import Hand

DICE = [1,2,3,4,5,6]

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
    
    def calc_prob(self, quantity, value, total_dice):
        """Calculates the probability that there are 
            [quantity] dice of [value] in [total_dice] number of dice, 
            taking jessies into account"""
        times_true = 0
        total_options = 0

        options = it.product(DICE, repeat=total_dice)
        for option in options:
            if option.count(1) + option.count(value) >= quantity:
                times_true += 1
            total_options += 1

        print('Times true: {}'.format(times_true))
        print('Total options: {}'.format(total_options))
        
        print('Prob: {}'.format(times_true / total_options)) 



    def calc_prob(self, quantity, value, total_dice):
        """Calculates the probability that there are 
            [quantity] dice of a value [value] in [total_dice] number of dice, 
            taking jessies into account"""
        times_true = 0
        total_rolls = 0

        rolls = it.product(DICE, repeat=total_dice)
        for roll in rolls:
            if roll.count(1) + roll.count(value) >= quantity:
                times_true += 1
            total_rolls += 1

        return times_true / total_rolls
        


    

    def calc_prob_straight(self, quantity, value, total_dice):
        times_true = 0
        total_options = 0

        options = it.product(DICE, repeat=total_dice)
        for option in options:
            if option.count(value) >= quantity:
                times_true += 1
            total_options += 1

        print('Times true: {}'.format(times_true))
        print('Total options: {}'.format(total_options))
        
        print('Prob: {}'.format(times_true / total_options)) 


    



class AIPlayer(Player):
    def __init__(self, name=False, gen='ai', dice=5):
        super().__init__(name=name, gen=gen, dice=dice, ai=True)
    
    
    
    
if __name__ == '__main__':
    player = Player()

    prob = player.calc_prob_straight(3,3,5)

    



