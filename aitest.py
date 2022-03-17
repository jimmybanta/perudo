import random
import pdb

from game import Game, Round
from ai_gen_zero import ai_gen_test, ai_gen_zeropointzero, ai_gen_zeropointone, ai_gen_zeropointtwo, ai_gen_zeropointthree, ai_gen_zeropointfour
from ai_gen_zero import ai_gen_zeropointfive, ai_gen_zeropointsix, ai_gen_zeropointseven, ai_gen_zeropointeight
from ai_gen_one import ai_gen_onepointfour, ai_gen_onepointzero, ai_gen_onepointone, ai_gen_onepointtwo, ai_gen_onepointthree
from ai_gen_two import ai_gen_twopointzero, ai_gen_twopointone, ai_gen_twopointtwo, ai_gen_twopointthree
from ai_gen_two import ai_gen_twopointthreepointone, ai_gen_twopointthreepointtwo, ai_gen_twopointthreepointthree, ai_gen_twopointthreepointfour
from ai_gen_two import ai_gen_twopointfour, ai_gen_twopointfourpointone, ai_gen_twopointfourpointtwo, ai_gen_twopointfourpointthree, ai_gen_twopointfourpointfour
from ai_gen_two import ai_gen_twopointfourpointfive, ai_gen_twopointfourpointsix
from ai_gen_two import ai_gen_twopointfivepointone, ai_gen_twopointfivepointtwo, ai_gen_twopointfivepointthree, ai_gen_twopointfivepointfour, ai_gen_twopointfivepointfive


NO_DICE = 5


AI = ai_gen_twopointfivepointfive(dice=NO_DICE)

CONTROL_GROUP = [ai_gen_twopointtwo(dice=NO_DICE),
            ai_gen_onepointtwo(dice=NO_DICE), 
            ai_gen_onepointzero(dice=NO_DICE),
            ai_gen_zeropointsix(dice=NO_DICE)]





class AITest(Game):
    '''So that I can watch AI's play a game'''
    def __init__(self):
        super().__init__()
            
        for player in CONTROL_GROUP:
            self.players[player] = NO_DICE
            self.order.append(player)
            player.dice = NO_DICE

        self.players[AI] = NO_DICE
        self.order.append(AI)
        AI.dice = NO_DICE
        
        random.shuffle(self.order)
        
        self.total_dice = sum(self.players.values())

        self.test = True


    
    def play(self):
        round_num = 0

        if self.test:
            input('Welcome to perudo! ')
            print('Global order: {}'.format(self.print(self.order)))
            print('')

        first_player = None
        straight = False

        while not self.check_end():
            round_num += 1
            if self.test:
                input('Start of Round {}... '.format(round_num))
                if straight:
                    print('STRAIGHT ROUND')
                print('')
                self.print_players()
                print('')
            
            if not first_player:
                order = self.order
                direction = 'right'
            else:
                order, direction = self.set_order(first_player)
            round = AIRound(self.players, order, test=self.test, straight=straight)
            
            if self.test:
                print('')            
                print('Dice: {}'.format(round.all_dice))

            round.run()

            loser = round.final_loser
            if self.test:
                print('Loser: {}'.format(loser))
            self.end_round(loser)

            if loser.dice == 0:
                temp_order = self.set_order(loser, direction=direction)[0]
                first_player = temp_order[1]
            elif loser.dice == 1 and self.total_dice > 2:
                straight = True
                first_player = loser
            else:
                first_player = loser
            

            self.update_order()

        if self.test:
            winner = self.check_winner()
            print('Game Over!')
            print('Winner: {} with {} dice'.format(winner, self.winner_dice))
    
    def set_order(self, player, direction=False):
        # sets the order for a round, given the first player
        round_order = []
        if not direction:
            direction = player.choose_direction()

        start = self.order.index(player)
    
        length = len(self.order)
        if direction == 'right':
            round_order = self.order[start:] + self.order[:start]
        else:
            temp = self.order.copy()
            temp.reverse()
            round_order = temp[length - (start + 1):] + temp[:length - (start + 1)]
        return round_order, direction

    def print(self, order):
        print([str(player) for player in order])
    
    def print_players(self):
        for player in self.players:
            print('{} -- {} dice'.format(str(player), player.dice))

        #for item in self.players.items():
         #   print('{} -- {} dice'.format(str(item[0]), item[1]))



class AIRound(Round):
    def __init__(self, players, order, test=False, straight=False):
        super().__init__(players, order)
        self.test = test
        self.straight = straight

    def run(self):

        betting_player = self.order[0]
        first_bet = self.start(straight=self.straight)

        if self.test:
            print("First bet: {} {}'s".format(first_bet[0], first_bet[1]))
            print('Hand: {}'.format(betting_player.hand))
            print('by {}'.format(str(betting_player)))
            input('')
        self.bets.append(first_bet)

        turn = 1

        calling_player = self.order[turn % len(self.order)]
        bet = calling_player.bet(first_bet, self.total_dice, straight=self.straight)

        while bet:
            self.bets.append(bet)
            betting_player = calling_player
            if self.test:
                print("Current bet: {} {}'s".format(bet[0], bet[1]))
                print('Hand: {}'.format(betting_player.hand))
                print('by {}'.format(str(betting_player)))
                input('')
            turn += 1

            calling_player = self.order[turn % len(self.order)]
            bet = calling_player.bet(bet, self.total_dice, straight=self.straight)
            
        
        bet = self.bets[-1]

        if self.test:
            input('Call! ')
            print('Hand: {}'.format(calling_player.hand))

            print('')
            print('Betting player: {}'.format(str(betting_player)))
            print('Calling player: {}'.format(str(calling_player)))
            print('')
            print('Bet is {}'.format(self.score(bet, straight=self.straight)))

        self.final_loser = self.loser(bet, calling_player, betting_player, straight=self.straight)
    



if __name__ == "__main__":
    game = AITest()

    game.play()



