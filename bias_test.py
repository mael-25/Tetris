import random
import numpy as np

lst = np.zeros((7,7))

a = random.choice([0,1,2,3,4,5,6])
for x in range(1000000):
    b = random.choice([0,1,2,3,4,5,6])
    lst[a,b]+=1
    a=b
# lst[0,4] = 2

print(lst)