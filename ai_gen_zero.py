import random
import math

from player import AIPlayer


# starting bet is average - 1, 33% chance of calling, next bet is one up the line
class ai_gen_zeropointzero(AIPlayer):
    def __init__(self, name='Gen 0.0', gen='0.0', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.probability = .33

    def starting_bet(self, total_dice, straight=False):
        average = total_dice / 3
        quantity = math.floor(average - 2)
        if quantity < 1:
           quantity = 1

        value = random.randint(2,6)
        return (quantity, value)

    def bet(self, current_bet, total_dice, straight=False):
        # any subsequent bet (that isn't the first)
        # return a bet
        quantity, value = current_bet
        jessies = True if value == 1 else False

        d = [2,3,4,5,6,2]

        if random.random() < self.probability:
            return False
        else:
            return self.up_the_line(current_bet, total_dice, straight=straight, jessies=jessies)
    
    def up_the_line(self, current_bet, total_dice, straight=False, jessies=False):
        '''Returns a bet 1 up the line.
        
        ex. if the bet is (2,3), it returns (2,4)'''
        
        quantity, value = current_bet

        if straight:
            if self.one_left:
                d = [1,2,3,4,5,6,1]
                if value == 6:
                    quantity += 1
                return (quantity, d[d.index(value) + 1])
            else:
                return (quantity + 1, value)
        else:
            d = [2,3,4,5,6,2]
            if jessies:
                return (quantity + 1, value)
            elif value == 6:
                quantity += 1
            return (quantity, d[d.index(value) + 1])

    def choose_direction(self):
        # True = right, False = left
        return 'right' if random.random() < .5 else 'left'
            

class ai_gen_zeropointone(ai_gen_zeropointzero):
    def __init__(self, name='Gen 0.1', gen='0.1', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.probability = .25

class ai_gen_zeropointtwo(ai_gen_zeropointzero):
    def __init__(self, name='Gen 0.2', gen='0.2', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.probability = .50

class ai_gen_zeropointthree(ai_gen_zeropointzero):
    def __init__(self, name='Gen 0.3', gen='0.3', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.probability = .75

class ai_gen_zeropointfour(ai_gen_zeropointzero):
    def __init__(self, name='Gen 0.4', gen='0.4', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.probability = .90

class ai_gen_zeropointfive(ai_gen_zeropointzero):
    def __init__(self, name='Gen 0.5', gen='0.5', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.probability = .15

class ai_gen_zeropointsix(ai_gen_zeropointzero):
    def __init__(self, name='Gen 0.6', gen='0.6', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.probability = .07

class ai_gen_zeropointseven(ai_gen_zeropointzero):
    def __init__(self, name='Gen 0.7', gen='0.7', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.probability = .01

class ai_gen_zeropointeight(ai_gen_zeropointzero):
    def __init__(self, name='Gen 0.8', gen='0.8', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.probability = 0


class ai_gen_test(ai_gen_zeropointzero):
    def __init__(self, name='test_gen', gen='test', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.probability = 0


    def starting_bet(self, average):
        quantity = int((average * 10) - 1)
        value = random.randint(2,6)
        return (quantity, value)

    def bet(self, current_bet, average):
        # any subsequent bet (that isn't the first)
        # return a bet
        quantity = int((average * 10) - 1)
        value = random.randint(2,6)
        return (quantity, value)
    
    def straight_bet(self, current_bet, average):
        quantity = int((average * 4) - 1)
        value = random.randint(2,6)
        return (quantity, value)



if __name__ == '__main__':
    ai = ai_gen_zeropointzero('joe')

    