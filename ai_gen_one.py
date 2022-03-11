import math
import random

from ai_gen_zero import ai_gen_zeropointzero
from player import AIPlayer

class ai_gen_onepointzero(ai_gen_zeropointzero):
    '''Uses probabilities to call. Doesn't use it to make any bets.'''
    def __init__(self, name='Gen 1.0', gen='1.0', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)


    def bet(self, current_bet, total_dice, straight=False):
        '''If prob of bet is less than 50%, it calls. Otherwise it sends it up the line'''
        hand = self.hand

        quantity, value = current_bet
        jessies = True if value == 1 else False

        if self.prob(current_bet, total_dice, straight=straight, jessies=jessies) < .5:
            return False
        else:
            return self.up_the_line(current_bet, total_dice, straight=straight, jessies=jessies)

    def starting_bet(self, average):
        quantity = math.floor(average - 1)
        if quantity < 1:
           quantity = 1

        value = random.randint(2,6)
        return (quantity, value)

    def choose_direction(self):
        # True = right, False = left
        return 'right' if random.random() < .5 else 'left'



class ai_gen_onepointone(ai_gen_onepointzero):
    '''Uses probabilities to call AND make bets.'''
    
    def __init__(self, name='Gen 1.1', gen='1.1', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
    
    def possible_bets(self, bet, look_ahead, straight=False, jessies=False):
        '''Given a current_bet, returns all possible bets under a max quantity'''
        look_ahead += 1
        quantity, value = bet

        straight_bets = []
        normal_bets = []

        if straight:
            max = quantity + look_ahead 
            if self.one_left:
                for i in range(value + 1, 7):
                    straight_bets.append((quantity, i))
                for j in range(quantity + 1, max):
                    for k in range(1,7):
                        straight_bets.append((j,k))
            else:
                for j in range(quantity + 1, max):
                    straight_bets.append((j, value))
        else:
            if jessies:
                max1 = quantity + look_ahead 
                maxnormal = (quantity * 2) + 1 + look_ahead 

                for i in range(quantity + 1, max1):
                    straight_bets.append((i, 1))
                for j in range((quantity * 2) + 1, maxnormal):
                    for k in range(2,7):
                        normal_bets.append((j,k))
            else:
                max = quantity // 2 + look_ahead
                for l in range(math.ceil((quantity / 2)), max):
                    straight_bets.append((l, 1))
                

                max = quantity + look_ahead 
                for i in range(value + 1, 7):
                    normal_bets.append((quantity, i))
                for j in range(quantity + 1, max):
                    for k in range(2,7):
                        normal_bets.append((j,k))
                
        return straight_bets, normal_bets

    def bet(self, current_bet, total_dice, straight=False):
        '''Returns False if it decides to call, otherwise returns a bet.
        
            Makes a bet by choosing the highest-probability possible bet.'''

        value = current_bet[1]
        jessies = True if value == 1 else False

        if self.prob(current_bet, total_dice, straight=straight, jessies=jessies)  < .5:
            return False


        straight_bets, normal_bets = self.possible_bets(current_bet, 5, straight=straight, jessies=jessies)

        straight_probs = [self.prob(bet, total_dice, straight=True) for bet in straight_bets]
        normal_probs = [self.prob(bet, total_dice) for bet in normal_bets]

        final = list(zip(straight_bets, straight_probs)) + list(zip(normal_bets, normal_probs))

        max_prob = max([x[1] for x in final])

        final = [x for x in final if x[1] == max_prob]

        return random.choice([x[0] for x in final])

    


if __name__ == "__main__":
    player = ai_gen_onepointone()
    player.roll()
    print(player.hand)
    

    print(player.bet((3,4), 10))


    