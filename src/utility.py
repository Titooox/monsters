import random
import math

def reduceNumber(number):
    temp = number/2
    if random.randint(0,1) == 0:
        temp = math.floor(temp)
    else:
        temp = math.ceil(temp)
    return int(temp)
