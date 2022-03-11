import random
import pdb

from game import Game, Round
from ai_gen_zero import ai_gen_test, ai_gen_zeropointzero, ai_gen_zeropointone, ai_gen_zeropointtwo, ai_gen_zeropointthree, ai_gen_zeropointfour
from ai_gen_zero import ai_gen_zeropointfive, ai_gen_zeropointsix, ai_gen_zeropointseven, ai_gen_zeropointeight
from ai_gen_one import ai_gen_onepointzero, ai_gen_onepointone

NO_DICE = 3

AIS = [ai_gen_onepointone(dice=NO_DICE),
        ai_gen_onepointzero(dice=NO_DICE),
        ai_gen_onepointone(dice=NO_DICE),
        ai_gen_onepointzero(dice=NO_DICE), 
        ai_gen_onepointone(dice=NO_DICE),
        ai_gen_onepointzero(dice=NO_DICE)]



class AITest(Game):
    '''So that I can watch AI's play a game'''
    def __init__(self):
        self.players = {}
        self.order = []
        self.winner = None
        self.winner_dice = 0

        self.ais = AIS
            
        for player in self.ais:
            self.players[player] = NO_DICE
            self.order.append(player)
        
        random.shuffle(self.order)

        self.temp_order = self.order.copy()
        
        self.total_dice = sum(self.players.values())

    
    def play(self):
        input('Welcome to perudo! ')
        round_num = 0
        print('Global order: {}'.format(self.print(self.order)))
        print('')

        first_player = None
        straight = False

        print('')

        while not self.check_end():
            round_num += 1
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
            round = AIRound(self.players, order)
            
            print('')
            print('Round order: {}'.format(self.print(order)))
            print('')
            
            print('Dice: {}'.format(round.all_dice))

            if straight and self.total_dice > 2:
                round.run(straight=True, test=True)
                straight = False
            else:
                round.run(test=True)

            loser = round.final_loser
            print('Loser: {}'.format(loser))
            self.end_round(loser)

            if loser.dice == 0:
                temp_order = self.set_order(loser, direction=direction)[0]
                first_player = temp_order[1]
            elif loser.dice == 1:
                straight = True
                first_player = loser
            else:
                first_player = loser
            

            self.update_order()
            print('')

        print('Game Over!')
        winner = self.check_winner()
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
        for item in self.players.items():
            print('{} -- {} dice'.format(str(item[0]), item[1]))



class AIRound(Round):

    def run(self, straight=False, test=False):

        betting_player = self.order[0]
        first_bet = self.start()

        if test:
            print("First bet: {} {}'s".format(first_bet[0], first_bet[1]))
            print('by {}'.format(str(betting_player)))
            input('')
        self.bets.append(first_bet)

        turn = 1

        calling_player = self.order[turn % len(self.order)]
        bet = calling_player.bet(first_bet, self.total_dice, straight=straight)

        while bet:
            self.bets.append(bet)
            betting_player = calling_player
            if test:
                print("Current bet: {} {}'s".format(bet[0], bet[1]))
                print('by {}'.format(str(betting_player)))
                input('')
            turn += 1

            calling_player = self.order[turn % len(self.order)]
            bet = calling_player.bet(bet, self.total_dice, straight=straight)
            
        
        bet = self.bets[-1]

        if test:
            input('Call! ')
            print('')
            print('Betting player: {}'.format(str(betting_player)))
            print('Calling player: {}'.format(str(calling_player)))
            print('')
            print('Bet is {}'.format(self.score(bet, straight=straight)))

        self.final_loser = self.loser(bet, calling_player, betting_player)
    



if __name__ == "__main__":
    game = AITest()

    game.play()



