import random
import pdb
import matplotlib.pyplot as plt
from numpy import true_divide

from aitest import AITest, AIRound, NO_DICE, AIS
from ai_gen_zero import ai_gen_zeropointzero, ai_gen_zeropointone, ai_gen_zeropointtwo, ai_gen_zeropointthree, ai_gen_zeropointfour


class GameSet:
    def __init__(self, number):
        self.number = number
        self.results = {}

        for ai in AIS:
            self.results[ai] = 0
    

    def run(self):

        game_num = 0

        for _ in range(self.number):
            game_num += 1

            game = AIGame()
            game.play()
            winner = game.check_winner()
            self.results[winner] += 1

            if game_num % 100 == 0:
                print('Game {} complete'.format(game_num))
                print('')
            

    def print_results(self):
        print('')
        print('Results: ')
        print('')
        for player in self.results:
            print("{} --- {} wins --- Won {}% of games".format(str(player), 
                                                self.results[player], 
                                                round((self.results[player] / self.number) * 100), 2))
        print('')

    def analyze(self):
        x = []
        y = []
        for player in self.results:
            x.append(player.prob * 100)
            y.append(round((self.results[player] / self.number), 3) * 100)

        plt.scatter(x,y)
        plt.xlabel('Percentage Chance of Calling')
        plt.ylabel('Percentage of Games Won')
        plt.title('Gen 0 - Starting Bet = 2 Above Average')

        plt.show()

           


        




class AIGame(AITest):
    def __init__(self):
        self.players = {}
        self.order = []
        
        self.ais = AIS
            
        for player in self.ais:
            self.players[player] = NO_DICE
            player.dice = NO_DICE
            self.order.append(player)
            
        random.shuffle(self.order)
        
        self.total_dice = sum(self.players.values())
        

    
    def play(self):
        round_num = 0
        
        first_player = None
        straight = False

        while not self.check_end():
            round_num += 1
            
            if not first_player:
                order = self.order
                direction = 'right'
            else:
                new_order = self.set_order(first_player)
                direction = new_order[1]
                order = new_order[0]
                
            round = AIRound(self.players, order)
            
            

            if straight and self.total_dice > 2:
                round.run(straight=True)
                straight = False
            else:
                round.run()

            loser = round.final_loser
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
            
    






class AIGame_Round(AIRound):

    def run(self, straight=False):
        betting_player = self.order[0]
        first_bet = self.start()
        
        self.bets.append(first_bet)

        turn = 1

        calling_player = self.order[turn % len(self.order)]
        bet = calling_player.bet(first_bet, self.total_dice)
        

        while bet:
            self.bets.append(bet)
            betting_player = calling_player
            
            turn += 1

            calling_player = self.order[turn % len(self.order)]
            bet = calling_player.bet(bet, self.total_dice)
        
            
        bet = self.bets[-1]
    
        self.final_loser = self.loser(bet, calling_player, betting_player)
    

    def straight_run(self):
        betting_player = self.order[0]
        first_bet = self.start(straight=True)
        
        self.bets.append(first_bet)

        turn = 1

        calling_player = self.order[turn % len(self.order)]
        bet = calling_player.straight_bet(first_bet, self.total_dice)

        while bet:
            self.bets.append(bet)
            betting_player = calling_player
            
            turn += 1

            calling_player = self.order[turn % len(self.order)]
            bet = calling_player.straight_bet(bet, self.total_dice)
            

        
        bet = self.bets[-1]

        self.final_loser = self.loser(bet, calling_player, betting_player)





if __name__ == '__main__':

    game_set = GameSet(500)

    game_set.run()

    game_set.print_results()
