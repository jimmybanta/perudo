import itertools as it
import csv
import pdb
import datetime as dt
from math import comb


DICE = [1,2,3,4,5,6]

NAMES = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
        'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
        'seventeen', 'eighteen', 'nineteen', 'twenty', 'twenty-one', 'twenty-two', 'twenty-three', 'twenty-four',
        'twenty-five', 'twenty-six', 'twenty-seven', 'twenty-eight', 'twenty-nine', 'thirty']

class Brute_Generator_Straight:
    def __init__(self, start, end=False):
        self.start = start
        self.times = []
        self.time_diffs = []
        
        self.end = self.start if not end else end


        # each list - index 0 is the total options,
        #  index 1 is the total times there's at least 1 6,
        #  index 2 is the total times there's at least 2 6's, etc.
        for i, name in enumerate(NAMES):
            setattr(self, name, [0] * (i + 2))



    def generate_probs(self):

        for i in range(self.start, self.end + 1):
            start = dt.datetime.now()
            iter = it.product(DICE, repeat=i)

            for combo in iter:
                for k in range(1, i + 1):
                    if combo.count(6) >= k:
                        getattr(self, NAMES[i - 1])[k] += 1

                getattr(self, NAMES[i - 1])[0] += 1
            
            end = dt.datetime.now()
            diff = end - start
            print('Done with {} dice'.format(i))
            print('Took {}'.format(diff))
            
            # self.write_probs(NAMES[i - 1])
                        
        for name in NAMES[self.start - 1:self.end]:
            print('{}: {}'.format(name, getattr(self, name)))


    def write_probs(self, name):
        fieldnames = ['number_of_dice'] + NAMES

        with open('straight_probs.csv', 'a') as file:
            writer = csv.DictWriter(file, fieldnames)

            i = NAMES.index(name) + 1

            d = {}
            att = getattr(self, name)
            total = att[0]
            d['number_of_dice'] = i

            for k in range(1, i + 1):
                prob = round((att[k] / total), 8)
                d[NAMES[k - 1]] = prob

            writer.writerow(d)
            
    def calc_diffs(self):
        for i, timedelta in enumerate(self.times):
            if i == 0:
                continue
            self.time_diffs.append(timedelta / self.times[i - 1])


class Brute_Generator_Normal(Brute_Generator_Straight):
    def generate_probs(self):

        for i in range(self.start, self.end + 1):
            start = dt.datetime.now()
            iter = it.product(DICE, repeat=i)

            for combo in iter:
                for k in range(1, i + 1):
                    if combo.count(6) + combo.count(1) >= k:
                        getattr(self, NAMES[i - 1])[k] += 1

                getattr(self, NAMES[i - 1])[0] += 1
            
            end = dt.datetime.now()
            diff = end - start
            self.times.append(diff)
            print('Done with {} dice'.format(i))
            print('Took {} seconds'.format(diff.seconds))
            print('')


            # self.write_probs(NAMES[i - 1])
                        

        for name in NAMES[self.start - 1:self.end]:
            print('{}: {}'.format(name, getattr(self, name)))
                    



    def write_probs(self, name):
        fieldnames = ['number_of_dice'] + NAMES

        with open('normal_probs.csv', 'a') as file:
            writer = csv.DictWriter(file, fieldnames)

            i = NAMES.index(name) + 1

            d = {}
            att = getattr(self, name)
            total = att[0]
            d['number_of_dice'] = i

            for k in range(1, i + 1):
                prob = round((att[k] / total), 8)
                d[NAMES[k - 1]] = prob

            writer.writerow(d)
                    

class Math_Generator_Straight(Brute_Generator_Straight):
    def generate_probs(self):

        for i in range(self.start, self.end + 1):
            getattr(self, NAMES[i - 1])[0] = 6 ** i

            for k in range(1, i + 1):
                value = comb(i,k) * (5 ** (i - k))
                getattr(self, NAMES[i - 1])[k] = value

        for name in NAMES:
            l = getattr(self, name)
            length = len(l)
            temp = l.copy()
            temp[0] = l[0]
            for i in range(1, NAMES.index(name) + 2):
                temp[i] = sum(l[i:length + 1])
            setattr(self, name, temp)
                
            
        '''
        for name in NAMES[self.start - 1:self.end]:
            print('{}: {}'.format(name, getattr(self, name)))
            '''
        

    def write_probs(self):
        fieldnames = ['number_of_dice'] + NAMES

        with open('test_probs.csv', 'a') as file:
            writer = csv.DictWriter(file, fieldnames)
            writer.writeheader()

            for name in NAMES:
                i = NAMES.index(name) + 1

                d = {}
                att = getattr(self, name)
                total = att[0]
                d['number_of_dice'] = i

                for k in range(1, i + 1):
                    prob = round((att[k] / total), 8)
                    d[NAMES[k - 1]] = prob

                writer.writerow(d)

                    
class Math_Generator_Normal(Brute_Generator_Straight):
    def generate_probs(self):

        for i in range(self.start, self.end + 1):
            getattr(self, NAMES[i - 1])[0] = 6 ** i

            for k in range(1, i + 1):
                value = comb(i,k) * (4 ** (i - k)) * (2 ** k)
                getattr(self, NAMES[i - 1])[k] = value

        for name in NAMES:
            l = getattr(self, name)
            length = len(l)
            temp = l.copy()
            temp[0] = l[0]
            for i in range(1, NAMES.index(name) + 2):
                temp[i] = sum(l[i:length + 1])
            setattr(self, name, temp)
                
            
        
        for name in NAMES[self.start - 1:self.end]:
            print('{}: {}'.format(name, getattr(self, name)))
        
        

    def write_probs(self):
        fieldnames = ['number_of_dice'] + NAMES

        with open('normal_probs.csv', 'a') as file:
            writer = csv.DictWriter(file, fieldnames)
            writer.writeheader()

            for name in NAMES:
                i = NAMES.index(name) + 1

                d = {}
                att = getattr(self, name)
                total = att[0]
                d['number_of_dice'] = i

                for k in range(1, i + 1):
                    prob = round((att[k] / total), 8)
                    d[NAMES[k - 1]] = prob

                writer.writerow(d)



p = Math_Generator_Normal(1,30)
p.generate_probs()
p.write_probs()