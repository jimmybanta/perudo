import random
import math

from ai_gen_zero import ai_gen_zeropointzero


from player import Player, AIPlayer

NO_DICE = 5

class Game:
    def __init__(self, num_players, human=True):
        self.players = {}
        self.order = []
        
        if human:
            for i in range(num_players - 1):
                ai_player = ai_gen_zeropointzero(i + 1)
                self.players[ai_player] = NO_DICE
                self.order.append(ai_player)
            name = input('What is your name? ')
            human_player = Player(name)
            self.players[human_player] = NO_DICE
            self.order.append(human_player)
            
            
        else:
            for i in range(num_players):
                ai_player = ai_gen_zeropointzero(i + 1)
                self.players[ai_player] = NO_DICE
                self.order.append(ai_player)
        
        random.shuffle(self.order)
        
        self.total_dice = sum(self.players.values())

    
    def play(self):
        input('Welcome to perudo! You know the rules...')
        input('Rolling... ')

        while self.check_end == False:
            
            pass



    def check_end(self):
        players = [x for x in self.players if self.players[x] != 0]
        return False if len(players) >= 2 else True
        
    def update_players(self):
        # run at the end of each round to clear out any players with no more dice
        # add something about keeping track of who loses, for the purposes of data

        self.players = {key:value for key, value in self.players.items() if value > 0}
        self.order = [player for player in self.order if player.dice > 0]



class Round:
    def __init__(self, players, order):
        self.players = players
        self.order = order
        for player in self.order:
            player.roll()

        self.total_dice = sum(self.players.values())
        self.all_dice = []
        for player in self.order:
            for die in player.hand:
                self.all_dice.append(die.value)
        self.all_dice.sort()

        self.average = self.total_dice / 3

        # keep track of bets - to be used later
        self.bets = []

    def start(self):
        first = self.order[0]
        if first.ai:
            return(first.starting_bet(6.66))
        else:
            quantity = int(input('What quantity do you choose? '))
            value = int(input('what value do you choose? '))
            return (quantity, value)
    
    def run(self):
        betting_player = self.order[0]
        first_bet = self.start()
        print("First bet: {} {}'s".format(first_bet[0], first_bet[1]))
        print(str(betting_player))
        print('')
        self.bets.append(first_bet)

        turn = 1

        calling_player = self.order[turn % len(self.order)]
        if not calling_player.ai:
            quantity = int(input('What quantity do you choose? '))
            value = int(input('what value do you choose? '))
            bet = (quantity, value)
        else:
            bet = calling_player.bet(first_bet)

        while bet:
            self.bets.append(bet)
            betting_player = calling_player
            print("Current bet: {} {}'s".format(bet[0], bet[1]))
            print(str(betting_player))
            print('')
            turn += 1

            calling_player = self.order[turn % len(self.order)]
            if not calling_player.ai:
                quantity = int(input('What quantity do you choose? '))
                value = int(input('what value do you choose? '))
                bet = (quantity, value)
            else:
                bet = calling_player.bet(bet)
            

        print('Call! ')
        print('')
        bet = self.bets[-1]
        print('Betting player: {}'.format(str(betting_player)))
        print('Calling player: {}'.format(str(calling_player)))

        print('Bet is {}'.format(self.score(bet)))
        
        print('Loser: {}'.format(self.loser(bet, calling_player, betting_player)))

    def score(self, bet):
        # returns if a bet is true
        quantity, value = bet[0], bet[1]

        ones = self.all_dice.count(1)
        others = self.all_dice.count(value)
        
        return True if ones + others >= quantity else False
    
    def legal_move(self, current, next):
        # returns whether a move is legal or not
        current_quantity, current_value = current[0], current[1]
        next_quantity, next_value = next[0], next[1]

        if current_value == 1:
            if next_value > 1:
                return True if next_quantity >= ((current_quantity * 2) + 1) else False
            elif next_value == 1:
                return True if next_quantity >= (current_quantity + 1) else False
            
        elif current_value > 1:
            if next_value == 1:
                return True if next_quantity >= (math.ceil(current_quantity / 2)) else False
            elif next_value > 1:
                if next_value > current_value:
                    return True if next_quantity >= current_quantity else False
                elif next_value <= current_value:
                    return True if next_quantity > current_quantity else False


    def test_moves(self, move1=False, move2=False):
        if move1 and move2:
            current_move = (move1[0], move1[1])
            next_move = (move2[0], move2[1])
        else:
            current_move = (random.randint(1,6), random.randint(1,6))
            next_move = (random.randint(1,6), random.randint(1,6))

        print("Current move: {} {}'s".format(current_move[0], current_move[1]))
        print("Next move: {} {}'s".format(next_move[0], next_move[1]))

        truth = True if self.legal_move(current_move, next_move) else False

        print('Legal!') if truth else print('ILLEGAL')
        print('')



    def loser(self, bet, calling_player, betting_player):
        return calling_player if self.score(bet) else betting_player

    
    def check_winner_turn(self, betting_player, calling_player):
        pass
        



if __name__ == '__main__':

    game = Game(5)
    round = Round(game.players, game.order)
    
    for _ in range(20):
        round.test_moves()
