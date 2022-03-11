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



class ai_gen_onepointone(ai_gen_onepointzero):
    '''Uses probabilities to call AND make bets.'''
    
    def __init__(self, name='Gen 1.1', gen='1.1', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
    
    def possible_bets(self, bet, straight=False, jessies=False):
        '''Given a current_bet, returns all possible bets under a max quantity'''
        quantity, value = bet

        straight_bets = []
        normal_bets = []

        if straight:
            if self.one_left:
                for i in range(value + 1, 7):
                    straight_bets.append((quantity, i))
                for j in range(1, value + 1):
                    straight_bets.append((quantity + 1, j))
            else:
                straight_bets.append((quantity + 1, value))
        else:
            if jessies:
                straight_bets.append((quantity + 1, 1))

                for k in range(2,7):
                    normal_bets.append(((quantity * 2) + 1,k))
            else:
                straight_bets.append((math.ceil(quantity / 2), 1))
                
                for i in range(value + 1, 7):
                    normal_bets.append((quantity, i))

                for j in range(2, value + 1):
                    normal_bets.append((quantity + 1, j))
                
        return straight_bets, normal_bets

    def bet(self, current_bet, total_dice, straight=False):
        '''Returns False if it decides to call, otherwise returns a bet.
        
            Makes a bet by choosing the highest-probability possible bet.'''

        value = current_bet[1]
        jessies = True if value == 1 else False

        if self.prob(current_bet, total_dice, straight=straight, jessies=jessies)  < .5:
            return False

        straight_bets, normal_bets = self.possible_bets(current_bet, straight=straight, jessies=jessies)

        straight_probs = [self.prob(bet, total_dice, straight=True) for bet in straight_bets]
        normal_probs = [self.prob(bet, total_dice) for bet in normal_bets]

        final = list(zip(straight_bets, straight_probs)) + list(zip(normal_bets, normal_probs))

        max_prob = max([x[1] for x in final])

        final = [x for x in final if x[1] == max_prob]

        return random.choice([x[0] for x in final])



class ai_gen_onepointtwo(ai_gen_onepointzero):
    def __init__(self, name='Gen 1.2', gen='1.2', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
    


    def starting_bet(self, total_dice, straight=False):
    
        bets = self.possible_starting_bets(total_dice, straight=straight)

        probs = [self.prob(bet, total_dice, straight=straight) for bet in bets]

        final = list(zip(bets, probs))
        final = [x for x in final if x[1] >= .66]

        final.sort(key=lambda x:x[0], reverse=True)

        while not final:
            total_dice -= 1
            return self.starting_bet(total_dice, straight=straight)

        return final[0][0]
    



    def possible_starting_bets(self, total_dice, straight=False):
        bets = []

        if straight:
            average = total_dice // 6
            for i in range(average - 1, average + 2):
                for j in range(1,7):
                    bets.append((i, j))
        else:
            average = total_dice // 3
            for i in range(average - 1, average + 2):
                for j in range(2,7):
                    bets.append((i, j))
        
        
        return bets





        

    



if __name__ == "__main__":

    player = ai_gen_onepointtwo()
    player.roll()
    
    print(player.starting_bet(18))
    


    