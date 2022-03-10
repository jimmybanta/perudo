

from ai_gen_zero import ai_gen_zeropointzero
from player import AIPlayer





class ai_gen_onepointzero(ai_gen_zeropointzero):
    '''Uses probabilities to call. Doesn't use it to make any bets.'''
    def __init__(self, name='Gen 1.0', gen='1.0', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
    

    def call(self, current_bet, total_dice, straight=False):
        '''Returns True if the AI decides to call, False if it wants to bet'''
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
        
        
        if total_needed > 0 and total_needed <= unknown_dice:
            prob = self.retrieve_probability(total_needed, unknown_dice)
        elif total_needed > unknown_dice:
            prob = 0
        else:
            prob = 1
        
        return True if prob < .5 else False


    def bet(self, current_bet, total_dice, straight=False, jessies=False):
        '''Calls if it decides to call, otherwise bets.
        
            Makes a bet by choosing the highest-probability possible move.'''

        if self.call(current_bet, total_dice, straight=straight):
            return False
        else:
            quantity, value = current_bet





            d = [2,3,4,5,6,2]
            quantity, value = current_bet
            if value == 6:
                quantity += 1
            return (quantity, d[d.index(value) + 1])
        
    

    def possible_moves(self, current_bet, look_ahead, straight=False):
        '''Given a current_bet, returns all possible bets under a max quantity'''
        look_ahead += 1
        quantity, value = current_bet

        moves = []

        if straight:
            max = quantity + (look_ahead // 2) 
            if self.one_left:
                for i in range(value + 1, 7):
                    moves.append((quantity, i))
                for j in range(quantity + 1, max):
                    for k in range(1,7):
                        moves.append((j,k))
            else:
                for j in range(quantity + 1, max):
                    moves.append((j, value))
        else:
            if value == 1:
                max1 = quantity + look_ahead 
                maxnormal = (quantity * 2) + 1 + look_ahead 

                for i in range(quantity + 1, max1):
                    moves.append((i, 1))
                for j in range((quantity * 2) + 1, maxnormal):
                    for k in range(2,7):
                        moves.append((j,k))
            else:
                max = quantity + look_ahead 
                
                for i in range(value + 1, 7):
                    moves.append((quantity, i))
                for j in range(quantity + 1, max):
                    for k in range(2,7):
                        moves.append((j,k))
        
        return moves

                




        







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










if __name__ == "__main__":
    player = ai_gen_onepointzero()
    player.roll()
    print(player.hand)

    player.bet((9,5), 18)
    