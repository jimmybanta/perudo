import math
import random

from ai_gen_zero import ai_gen_zeropointzero
from player import AIPlayer

class ai_gen_onepointzero(ai_gen_zeropointzero):
    '''Uses probabilities to call. Doesn't use it to make any bets.'''
    def __init__(self, name='Gen 1.0', gen='1.0', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)


    def bet(self, current_bet, total_dice):
        '''If prob of bet is less than 50%, it calls. Otherwise it sends it up the line'''
        hand = self.hand

        quantity = current_bet[0]
        value = current_bet[1]

        total_needed = quantity
        unknown_dice = total_dice - len(hand)

        for die in hand:
            if die.value == value or die.value == 1:
                total_needed -= 1
        
        
        if total_needed > 0 and total_needed <= unknown_dice:
            prob = self.retrieve_probability(total_needed, unknown_dice)
        elif total_needed > unknown_dice:
            prob = 0
        else:
            prob = 1
        

        if prob < .5:
            return False
        
        else:
            d = [2,3,4,5,6,2]
            if value == 6:
                quantity += 1
            return (quantity, d[d.index(value) + 1])


    def straight_bet(self, current_bet, total_dice):
        hand = self.hand

        quantity, value = current_bet

        total_needed = quantity
        unknown_dice = total_dice - len(hand)

        for die in hand:
            if die.value == value or die.value == 1:
                total_needed -= 1
        
        if total_needed > 0 and total_needed <= unknown_dice:
            prob = self.retrieve_probability(total_needed, unknown_dice, straight=True)
        elif total_needed > unknown_dice:
            prob = 0
        else:
            prob = 1
    

        if prob < .5:
            return False
        elif self.one_left:
            d = [2,3,4,5,6,2]
            if value == 6:
                quantity += 1
            return (quantity, d[d.index(value) + 1])
        else:
            return (quantity + 1, value)






class ai_gen_onepointone(ai_gen_onepointzero):
    '''Uses probabilities to call. And uses it to make bets.'''
    def __init__(self, name='Gen 1.1', gen='1.1', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
    

    def dice_needed(self, current_bet, total_dice, straight=False):
        hand = self.hand

        quantity, value = current_bet

        total_needed = quantity
        unknown_dice = total_dice - len(hand)

        for die in hand:
            if straight:
                if die.value == value:
                    total_needed -= 1
            else:
                if die.value == value or die.value == 1:
                    total_needed -= 1
        
        return total_needed, unknown_dice

    def call(self, current_bet, total_dice, straight=False):
        '''Returns True if the AI decides to call, False if it wants to bet'''

        total_needed, unknown_dice = self.dice_needed(current_bet, total_dice, straight=straight)
        
        if total_needed > 0 and total_needed <= unknown_dice:
            prob = self.retrieve_probability(total_needed, unknown_dice)
        elif total_needed > unknown_dice:
            prob = 0
        else:
            prob = 1
        
        return True if prob < .5 else False

    def calc_prob(self, move, total_dice, straight=False):
        total_needed, unknown_dice = self.dice_needed(move, total_dice, straight=straight)

        if total_needed > unknown_dice:
            return 0
        elif total_needed <= 0:
            return 1
        else:
            return self.retrieve_probability(total_needed, unknown_dice, straight=straight)

    def bet(self, current_bet, total_dice, straight=False, jessies=False):
        '''Calls if it decides to call, otherwise bets.
        
            Makes a bet by choosing the highest-probability possible move.'''

        if self.call(current_bet, total_dice, straight=straight):
            return False
        else:

            straight_moves, normal_moves = self.possible_moves(current_bet, 2, straight=straight)

            straight_probs = [self.calc_prob(move, total_dice, straight=True) for move in straight_moves]
            normal_probs = [self.calc_prob(move, total_dice) for move in normal_moves]

            final = list(zip(straight_moves, straight_probs)) + list(zip(normal_moves, normal_probs))

            max_prob = max([x[1] for x in final])

            final = [x for x in final if x[1] == max_prob]

            return random.choice([x[0] for x in final])

            
        
    

    def possible_moves(self, current_bet, look_ahead, straight=False):
        '''Given a current_bet, returns all possible bets under a max quantity'''
        look_ahead += 1
        quantity, value = current_bet

        straight_moves = []
        normal_moves = []

        if straight:
            max = quantity + look_ahead 
            if self.one_left:
                for i in range(value + 1, 7):
                    straight_moves.append((quantity, i))
                for j in range(quantity + 1, max):
                    for k in range(1,7):
                        straight_moves.append((j,k))
            else:
                for j in range(quantity + 1, max):
                    straight_moves.append((j, value))
        else:
            if value == 1:
                max1 = quantity + look_ahead 
                maxnormal = (quantity * 2) + 1 + look_ahead 

                for i in range(quantity + 1, max1):
                    straight_moves.append((i, 1))
                for j in range((quantity * 2) + 1, maxnormal):
                    for k in range(2,7):
                        normal_moves.append((j,k))
            else:
                max = quantity // 2 + look_ahead
                for l in range(math.ceil((quantity / 2)), max):
                    straight_moves.append((l, 1))
                

                max = quantity + look_ahead 
                for i in range(value + 1, 7):
                    normal_moves.append((quantity, i))
                for j in range(quantity + 1, max):
                    for k in range(2,7):
                        normal_moves.append((j,k))
                
        return straight_moves, normal_moves

                






if __name__ == "__main__":
    player = ai_gen_onepointone()
    player.roll()
    print(player.hand)

    print(player.bet((4,6), 10))

    player.retrieve_probability

    