import random

class Die:
    def __init__(self, sides, value=None):
        self.sides = sides if isinstance(sides, int) else False

        if value and self.sides:
            self.value = value
        elif self.sides:
            self.value = random.randint(1, sides)
    
    def __eq__(self, other):
        if self.value == other.value:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.value < other.value:
            return True
        else:
            return False
    
    def __le__(self, other):
        if self < other or self == other:
            return True
        else:
            return False
    
    def __gt__(self, other):
        if self.value > other.value: 
            return True
        else:
            return False
    
    def __ge__(self, other):
        if self > other or self == other:
            return True
        else:
            return False



class D6(Die):
    def __init__(self, value=None):
        super().__init__(6, value=value)

