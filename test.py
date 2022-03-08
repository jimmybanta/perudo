
import datetime as dt
import itertools as it


DICE = [1,2,3,4,5,6]

d = {}

for i in range(1,40):
    start = dt.datetime.now()
    it.product(DICE, repeat=i)
    end = dt.datetime.now()

    time = end - start 
    d[i] = time

total = 0

iter = it.product(DICE, repeat=10)
for combo in iter:
    total += 1

print(total)
