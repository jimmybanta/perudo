

from player import AIPlayer

class ai_gen_onepointone(AIPlayer):
    def __init__(self, name='Gen 1.0', gen='1.0', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
    

    def starting_bet(self, average):
        pass

    def bet(self, current_bet, total_dice):
        hand = self.hand

        quantity = current_bet[0]
        value = current_bet[1]

        total_needed = quantity
        unknown_dice = total_dice - len(hand)

        for die in hand:
            if die == value:
                total_needed -= 1
        
    
    


        
        
        




    def straight_bet(self, current_bet, total_dice):
        pass


if __name__ == "__main__":
    player = ai_gen_onepointone()
    player.roll()
    print(player.name)
    print(player.hand)

    player.bet((1,1), 5)
    