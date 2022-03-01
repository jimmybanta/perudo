from hand import Hand

class Player:
    def __init__(self, name, dice=5):
        self.name = name
        self.dice = dice
    
    def roll(self):
        self.hand = Hand(size=self.dice)
    
    def lose_turn(self):
        self.dice -= 1
    


joe = Player('joe')



print(joe.name)
print(joe.dice)

joe.lose_turn()
print(joe.dice)