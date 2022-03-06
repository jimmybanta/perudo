import random
import pdb

from game import Game, Round
from ai_gen_zero import ai_gen_zeropointzero, ai_gen_zeropointone, ai_gen_zeropointtwo, ai_gen_zeropointthree, ai_gen_zeropointfour

NO_DICE = 1

class AITest(Game):
    '''So that I can watch AI's play a game'''
    def __init__(self):
        self.players = {}
        self.order = []
        self.winner = None
        self.winner_dice = 0

        self.ais = [ai_gen_zeropointzero(dice=NO_DICE), 
                    ai_gen_zeropointone(dice=NO_DICE), 
                    ai_gen_zeropointtwo(dice=NO_DICE),
                    ai_gen_zeropointthree(dice=NO_DICE), 
                    ai_gen_zeropointfour(dice=NO_DICE)]
            
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
                new_order = self.set_order(first_player)
                direction = new_order[1]
                order = new_order[0]
            round = AITest_Round(self.players, order)
            
            print('')
            print('Round order: {}'.format(self.print(order)))
            print('')
            
            print('Dice: {}'.format(round.all_dice))

            if straight and self.total_dice > 2:
                round.straight_run()
                straight = False
            else:
                round.run()

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
        self.check_winner()
        print('Winner: {} with {} dice'.format(self.winner, self.winner_dice))
    
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
        return [str(player) for player in order]
    
    def print_players(self):
        for item in self.players.items():
            print('{} -- {} dice'.format(str(item[0]), item[1]))



class AITest_Round(Round):
    def run(self):
        betting_player = self.order[0]
        first_bet = self.start()
        print("First bet: {} {}'s".format(first_bet[0], first_bet[1]))
        print('by {}'.format(str(betting_player)))
        input('')
        self.bets.append(first_bet)

        turn = 1

        calling_player = self.order[turn % len(self.order)]
        bet = calling_player.bet(first_bet)

        while bet:
            self.bets.append(bet)
            betting_player = calling_player
            print("Current bet: {} {}'s".format(bet[0], bet[1]))
            print('by {}'.format(str(betting_player)))
            input('')
            turn += 1

            calling_player = self.order[turn % len(self.order)]
            bet = calling_player.bet(bet)
            

        input('Call! ')
        print('')
        bet = self.bets[-1]
        print('Betting player: {}'.format(str(betting_player)))
        print('Calling player: {}'.format(str(calling_player)))
        print('')
        print('Bet is {}'.format(self.score(bet)))

        self.final_loser = self.loser(bet, calling_player, betting_player)
    

    def straight_run(self):
        betting_player = self.order[0]
        first_bet = self.start(straight=True)
        print("First bet: {} {}'s".format(first_bet[0], first_bet[1]))
        print('by {}'.format(str(betting_player)))
        input('')
        self.bets.append(first_bet)

        turn = 1

        calling_player = self.order[turn % len(self.order)]
        bet = calling_player.straight_bet(first_bet)

        while bet:
            self.bets.append(bet)
            betting_player = calling_player
            print("Current bet: {} {}'s".format(bet[0], bet[1]))
            print('by {}'.format(str(betting_player)))
            input('')
            turn += 1

            calling_player = self.order[turn % len(self.order)]
            bet = calling_player.straight_bet(bet)
            

        input('Call! ')
        print('')
        bet = self.bets[-1]
        print('Betting player: {}'.format(str(betting_player)))
        print('Calling player: {}'.format(str(calling_player)))
        print('')
        print('Bet is {}'.format(self.straight_score(bet)))

        self.final_loser = self.loser(bet, calling_player, betting_player)



if __name__ == "__main__":
    game = AITest()

    game.play()



