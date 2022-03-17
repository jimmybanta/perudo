import random
import math


from ai_gen_one import ai_gen_onepointfour


class ai_gen_twopointzero(ai_gen_onepointfour):
    '''Combines the starting bet mechanism of Gen 1.2, and betting mechanism of Gen 1.3'''
    def __init__(self, name='Gen 2.0', gen='2.0', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.starting_prob = .66

    def starting_bet(self, total_dice, straight=False):
    
        bets = self.possible_starting_bets(total_dice, straight=straight)

        probs = [self.prob(bet, total_dice, straight=straight) for bet in bets]

        final = list(zip(bets, probs))
        final = [x for x in final if x[1] >= self.starting_prob]

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
    
    def bet(self, current_bet, total_dice, straight=False):
        '''Returns False if it decides to call, otherwise returns a bet.
        
            Decides to call or bet based off which has the best chance of working.'''

        value = current_bet[1]
        jessies = True if value == 1 else False

        first_prob = self.prob(current_bet, total_dice, straight=straight, jessies=jessies)

        # make first_prob the probability that you would be correct in calling
        first_prob = 1 - first_prob

        straight_bets, normal_bets = self.possible_bets(current_bet, straight=straight, jessies=jessies)

        straight_probs = [self.prob(bet, total_dice, straight=True) for bet in straight_bets]
        normal_probs = [self.prob(bet, total_dice) for bet in normal_bets]

        final = list(zip(straight_bets, straight_probs)) + list(zip(normal_bets, normal_probs))

        second_prob = max([x[1] for x in final])

        if first_prob >= second_prob:
            return False
        else:
            final = [x for x in final if x[1] == second_prob]
            return random.choice([x[0] for x in final])
    

class ai_gen_twopointone(ai_gen_twopointzero):
    def __init__(self, name='Gen 2.1', gen='2.1', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.starting_prob = .5
        self.starting_straight_prob = .7

    def starting_bet(self, total_dice, straight=False):
    
        bets = self.possible_starting_bets(total_dice, straight=straight)

        probs = [self.prob(bet, total_dice, straight=straight) for bet in bets]

        final = list(zip(bets, probs))
        if straight:
            final = [x for x in final if x[1] >= self.starting_straight_prob]
        else:
            final = [x for x in final if x[1] >= self.starting_prob]

        final.sort(key=lambda x:x[0], reverse=True)

        while not final:
            return self.starting_bet(total_dice - 1, straight=straight)

        return final[0][0]
    
    def possible_starting_bets(self, total_dice, straight=False):
        bets = []

        if straight:
            average = total_dice // 6
            for i in range(average - 1, average + 3):
                for j in range(1,7):
                    bets.append((i, j))
        else:
            average = total_dice // 3
            for i in range(average - 1, average + 4):
                for j in range(2,7):
                    bets.append((i, j))
        
        return bets

class ai_gen_twopointtwo(ai_gen_twopointone):
    def __init__(self, name='Gen 2.2', gen='2.2', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.starting_prob = .4
        self.starting_straight_prob = .7

class ai_gen_twopointthree(ai_gen_twopointone):
    def __init__(self, name='Gen 2.3', gen='2.3', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.starting_prob = .8
        self.starting_straight_prob = .9


class ai_gen_twopointthreepointone(ai_gen_twopointone):
    def __init__(self, name='Gen 2.3.1', gen='2.3', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.starting_prob = .6
        self.starting_straight_prob = .6

class ai_gen_twopointthreepointtwo(ai_gen_twopointone):
    def __init__(self, name='Gen 2.3.2', gen='2.3', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.starting_prob = .7
        self.starting_straight_prob = .7

class ai_gen_twopointthreepointthree(ai_gen_twopointone):
    def __init__(self, name='Gen 2.3.3', gen='2.3', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.starting_prob = .9
        self.starting_straight_prob = .9

class ai_gen_twopointthreepointfour(ai_gen_twopointone):
    def __init__(self, name='Gen 2.3.4', gen='2.3', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        self.starting_prob = .95
        self.starting_straight_prob = .95
    

class ai_gen_twopointfour(ai_gen_twopointone):
    def __init__(self, name='Gen 2.4', gen='2.4', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        # the probability any of your bets need to have to be eligible
        self.betting_prob = .5
        # the probability that an incoming bet has to clear for you to raise the bet
        self.calling_prob = .5

        self.starting_prob = .95
        self.starting_straight_prob = .95

        self.look_ahead = 3

    def possible_bets(self, bet, straight=False, jessies=False):
        '''Given a current_bet, returns all possible bets under a max quantity'''
        look_ahead = self.look_ahead + 1
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
        
            Decides to call useing self.calling_prob (if a bet is less than that, it calls). 
            Decides a bet by choosing the highest up the line bet over self.betting_prob.'''

        value = current_bet[1]
        jessies = True if value == 1 else False

        first_prob = self.prob(current_bet, total_dice, straight=straight, jessies=jessies)

        if first_prob <= self.calling_prob:
            return False

        straight_bets, normal_bets = self.possible_bets(current_bet, straight=straight, jessies=jessies)

        straight_probs = [self.prob(bet, total_dice, straight=True) for bet in straight_bets]
        normal_probs = [self.prob(bet, total_dice) for bet in normal_bets]

        final = list(zip(straight_bets, straight_probs)) + list(zip(normal_bets, normal_probs))

        final_one = [x for x in final if x[1] >= self.betting_prob]

        if not final_one:
            max_prob = max([x[1] for x in final])

            final_two = [x for x in final if x[1] == max_prob]
            return random.choice([x[0] for x in final_two])
        else:
            final_one.sort(key= lambda x:x[0], reverse=True)
            return final_one[0][0]


class ai_gen_twopointfourpointone(ai_gen_twopointfour):
    def __init__(self, name='Gen 2.4.1', gen='2.4.1', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        # the probability any of your bets need to have to be eligible
        self.betting_prob = .5
        # the probability that an incoming bet has to clear for you to raise the bet
        self.calling_prob = .3

        self.starting_prob = .95
        self.starting_straight_prob = .95

        self.look_ahead = 3

class ai_gen_twopointfourpointtwo(ai_gen_twopointfour):
    def __init__(self, name='Gen 2.4.2', gen='2.4.2', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        # the probability any of your bets need to have to be eligible
        self.betting_prob = .5
        # the probability that an incoming bet has to clear for you to raise the bet
        self.calling_prob = .4
        
        self.starting_prob = .95
        self.starting_straight_prob = .95

        self.look_ahead = 3

class ai_gen_twopointfourpointthree(ai_gen_twopointfour):
    def __init__(self, name='Gen 2.4.3', gen='2.4.3', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        # the probability any of your bets need to have to be eligible
        self.betting_prob = .5
        # the probability that an incoming bet has to clear for you to raise the bet
        self.calling_prob = .6
        
        self.starting_prob = .95
        self.starting_straight_prob = .95

        self.look_ahead = 3

class ai_gen_twopointfourpointfour(ai_gen_twopointfour):
    def __init__(self, name='Gen 2.4.4', gen='2.4.4', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        # the probability any of your bets need to have to be eligible
        self.betting_prob = .5
        # the probability that an incoming bet has to clear for you to raise the bet
        self.calling_prob = .7
        
        self.starting_prob = .95
        self.starting_straight_prob = .95

        self.look_ahead = 3

class ai_gen_twopointfourpointfive(ai_gen_twopointfour):
    def __init__(self, name='Gen 2.4.5', gen='2.4.5', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        # the probability any of your bets need to have to be eligible
        self.betting_prob = .5
        # the probability that an incoming bet has to clear for you to raise the bet
        self.calling_prob = .2
        
        self.starting_prob = .95
        self.starting_straight_prob = .95

        self.look_ahead = 3

class ai_gen_twopointfourpointsix(ai_gen_twopointfour):
    def __init__(self, name='Gen 2.4.6', gen='2.4.6', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        # the probability any of your bets need to have to be eligible
        self.betting_prob = .5
        # the probability that an incoming bet has to clear for you to raise the bet
        self.calling_prob = .1
        
        self.starting_prob = .95
        self.starting_straight_prob = .95

        self.look_ahead = 3


class ai_gen_twopointfivepointone(ai_gen_twopointfour):
    def __init__(self, name='Gen 2.5.1', gen='2.5.1', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        # the probability any of your bets need to have to be eligible
        self.betting_prob = .3
        # the probability that an incoming bet has to clear for you to raise the bet
        self.calling_prob = .3
        
        self.starting_prob = .95
        self.starting_straight_prob = .95

        self.look_ahead = 3

class ai_gen_twopointfivepointtwo(ai_gen_twopointfour):
    def __init__(self, name='Gen 2.5.2', gen='2.5.2', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        # the probability any of your bets need to have to be eligible
        self.betting_prob = .4
        # the probability that an incoming bet has to clear for you to raise the bet
        self.calling_prob = .3
        
        self.starting_prob = .95
        self.starting_straight_prob = .95

        self.look_ahead = 3

class ai_gen_twopointfivepointthree(ai_gen_twopointfour):
    def __init__(self, name='Gen 2.5.3', gen='2.5.3', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        # the probability any of your bets need to have to be eligible
        self.betting_prob = .5
        # the probability that an incoming bet has to clear for you to raise the bet
        self.calling_prob = .3
        
        self.starting_prob = .95
        self.starting_straight_prob = .95

        self.look_ahead = 3

class ai_gen_twopointfivepointfour(ai_gen_twopointfour):
    def __init__(self, name='Gen 2.5.4', gen='2.5.4', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        # the probability any of your bets need to have to be eligible
        self.betting_prob = .6
        # the probability that an incoming bet has to clear for you to raise the bet
        self.calling_prob = .3
        
        self.starting_prob = .95
        self.starting_straight_prob = .95

        self.look_ahead = 3

class ai_gen_twopointfivepointfive(ai_gen_twopointfour):
    def __init__(self, name='Gen 2.5.5', gen='2.5.5', dice=5):
        super().__init__(name=name, gen=gen, dice=dice)
        # the probability any of your bets need to have to be eligible
        self.betting_prob = .7
        # the probability that an incoming bet has to clear for you to raise the bet
        self.calling_prob = .3
        
        self.starting_prob = .95
        self.starting_straight_prob = .95

        self.look_ahead = 3





if __name__ == '__main__':
    print("")
    print('Gen 2.4')
    p1 = ai_gen_twopointfour()
    p1.roll()
    print('Hand: {}'.format(p1.hand))

    print('Bet: {}'.format(p1.bet((8,3), 24)))

    print('')

    print('Gen 1.4: ')
    p2 = ai_gen_onepointfour()
    p2.hand = p1.hand
    print('Hand: {}'.format(p2.hand))

    print('Bet: {}'.format(p2.bet((8,3), 24)))
    print('')