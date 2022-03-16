import random
import pdb
import matplotlib.pyplot as plt
import datetime as dt

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
        start = dt.datetime.now()

        for _ in range(self.number):
            game_num += 1

            game = AIGame()
            game.play()
            winner = game.check_winner()
            self.results[winner] += 1

            if game_num % 100 == 0:
                print('Game {} complete'.format(game_num))
        end = dt.datetime.now()
        print('')
        print('Took {} seconds'.format((end - start).seconds))
            

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
        super().__init__()

        self.test = False


    




if __name__ == '__main__':

    game_set = GameSet(5000)

    game_set.run()

    game_set.print_results()
