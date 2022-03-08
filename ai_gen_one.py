

from ai_gen_zero import ai_gen_zeropointzero
from player import AIPlayer

class ai_gen_onepointzero(ai_gen_zeropointzero):
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

        quantity = current_bet[0]
        value = current_bet[1]

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
    