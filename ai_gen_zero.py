import random
import math

from player import AIPlayer

# starting bet is 2 less than average, 33% chance of calling, next bet is one up the line
class ai_gen_zeropointzero(AIPlayer):
    def __init__(self, name='Gen 0.0', gen='0.0', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.prob = .33


    def starting_bet(self, average):
        quantity = math.floor(average - 2)
        if quantity < 1:
            quantity = 1
        value = random.randint(2,6)
        return (quantity, value)

    def bet(self, current_bet):
        # any subsequent bet (that isn't the first)
        # return a bet
        quantity = current_bet[0]
        value = current_bet[1]

        d = [2,3,4,5,6,2]

        if random.random() < self.prob:
            return False
        else:
            if value == 6:
                quantity += 1
            return (quantity, d[d.index(value) + 1])
    
    def straight_bet(self, current_bet):
        quantity = current_bet[0]
        value = current_bet[1]

        d = [2,3,4,5,6,2]

        if random.random() < self.prob:
            return False

        elif self.one_left:
            if value == 6:
                quantity += 1
            return (quantity, d[d.index(value) + 1])
        else:
            return (quantity + 1, value)
    
    def choose_direction(self):
        # True = right, False = left
        return 'right' if random.random() < .5 else 'left'
            

class ai_gen_zeropointone(ai_gen_zeropointzero):
    def __init__(self, name='Gen 0.1', gen='0.1', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.prob = .25

class ai_gen_zeropointtwo(ai_gen_zeropointzero):
    def __init__(self, name='Gen 0.2', gen='0.2', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.prob = .50

class ai_gen_zeropointthree(ai_gen_zeropointzero):
    def __init__(self, name='Gen 0.3', gen='0.3', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.prob = .75

class ai_gen_zeropointfour(ai_gen_zeropointzero):
    def __init__(self, name='Gen 0.4', gen='0.4', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.prob = .90


if __name__ == '__main__':
    ai = ai_gen_zeropointzero('joe')

    current_bet = ai.starting_bet(8)
    print(current_bet)

    for _ in range(10):
        current_bet = ai.bet(current_bet)
        print(current_bet)