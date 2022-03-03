import random
import math

from player import AIPlayer

# starting bet is 1 less than average, 50% chance of calling, next bet is one up the line
class ai_gen_zeropointzero(AIPlayer):
    def __init__(self, name):
        super().__init__(name, gen='0.0')

    def starting_bet(self, average):
        average = math.floor(average - 1)
        value = random.randint(1,6)
        return (average, value)

    def bet(self, current_bet):
        # any subsequent bet (that isn't the first)
        # return a bet
        # TODO: incorporate jessies
        quantity = current_bet[0]
        value = current_bet[1]
        d = [1,2,3,4,5,6,1]
        if random.random() < .2:
            return False
        else:
            if value == 6:
                quantity += 1
            return (quantity, d[d.index(value) + 1])


if __name__ == '__main__':
    ai = ai_gen_zeropointzero('joe')

    current_bet = ai.starting_bet(8)
    print(current_bet)

    for _ in range(10):
        current_bet = ai.bet(current_bet)
        print(current_bet)