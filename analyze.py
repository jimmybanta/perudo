
import matplotlib.pyplot as m 

x = [.9,.75,.5,0,.33,.25,.01,.15,.07]
y = [0,0,2,5,8,14,16,24,30]

m.scatter(x,y)
m.xlabel('Percentage Chance of Calling')
m.ylabel('Percentage of Games Won')
m.title('Generation 0')


m.show()