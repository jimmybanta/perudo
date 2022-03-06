import random

from aitest import AITest, AITest_Round, NO_DICE
from ai_gen_zero import ai_gen_zeropointzero, ai_gen_zeropointone, ai_gen_zeropointtwo, ai_gen_zeropointthree, ai_gen_zeropointfour



class AIGame(AITest):
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
        
        self.total_dice = sum(self.players.values())
        
        self.results = {}
        for player in self.players:
            self.results[player] = 0


    
    def play(self, games):
        input('Welcome to perudo! ')
        game_num = 0

        for _ in range(games):
            game_num += 1

            for player in self.players:
                self.order.append(player)
            random.shuffle(self.order)

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
                round = AIGame_Round(self.players, order)
                

                if straight and self.total_dice > 2:
                    round.straight_run()
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

            if game_num % 1000 == 0:
                print('Game {} complete'.format(game_num))

            self.check_winner()
            self.results[self.winner] += 1

    def print_results(self):
        print('')
        print('Results: ')
        print('')
        for player in self.results:
            print('{} --- {} wins'.format(str(player), self.results[player]))
        print('')









class AIGame_Round(AITest_Round):
    def run(self):
        betting_player = self.order[0]
        first_bet = self.start()
        
        self.bets.append(first_bet)

        turn = 1

        calling_player = self.order[turn % len(self.order)]
        bet = calling_player.bet(first_bet)
        

        while bet:
            self.bets.append(bet)
            betting_player = calling_player
            
            turn += 1

            calling_player = self.order[turn % len(self.order)]
            bet = calling_player.bet(bet)
        
            
        bet = self.bets[-1]
    
        self.final_loser = self.loser(bet, calling_player, betting_player)
    

    def straight_run(self):
        betting_player = self.order[0]
        first_bet = self.start(straight=True)
        
        self.bets.append(first_bet)

        turn = 1

        calling_player = self.order[turn % len(self.order)]
        bet = calling_player.straight_bet(first_bet)

        while bet:
            self.bets.append(bet)
            betting_player = calling_player
            
            turn += 1

            calling_player = self.order[turn % len(self.order)]
            bet = calling_player.straight_bet(bet)
            

        
        bet = self.bets[-1]

        self.final_loser = self.loser(bet, calling_player, betting_player)





if __name__ == '__main__':

    game = AIGame()


    game.play(1000)

    game.print_results()



