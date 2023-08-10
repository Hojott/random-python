import random
import math

def roll_dice():
    roll = math.ceil(random.random()*6)
    return roll

def eka_heitto():
    r1 = roll_dice()
    r2 = roll_dice()
    if r1 > r2:
        return r1
    else:
        return r2

def toka_heitto():
    og_roll = eka_heitto()
    r3 = roll_dice()
    return r3 < og_roll

def n_kertaa(n):
    oikein = 0
    for i in range (n):
        if toka_heitto():
            oikein +=1
    return oikein

print(n_kertaa(1000000)/1000000)
