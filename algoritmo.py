# Password generator
# Author: Cesare Francesco Gigliuto 
# Author: Ciro Cozzolino
# Version: 1.0

# imports
import itertools
import sys
import os
import itertools
from datetime import datetime as dt
import random
from random import randint 
import string

dictionary = ['a','s','d','f','g','h','j', 'k']
random.seed(dt.now())


def generapassword(leng):
    b = ""

    for i in range(0,leng):
        r = randint(0,len(dictionary)-1)
        b = b + dictionary[r]
    return b
def creapassword():
    a = int(input("inserire la lunghezza della password da generare: "))

    if a == 0 :
        print("input non valido") 
        return ""

    b = generapassword(a)
    return b

def get_random_string(length, dicti):
    # choose from all lowercase letter
    return ''.join(random.choice(dicti) for i in range(length))

def creaCampione(password, elements):
    out = []
    for i in range(1,elements):
        out.append(get_random_string(len(password), dictionary))

    return out

def decriptapassword(password):
    iterations = pow(len(dictionary),len(password)) 
    campione = creaCampione(password, 1000000)
    checker = get_random_string(len(password), [' '])
    begin = dt.now()
    for i in range(0,len(campione)):
        checker == campione[i]
    end = dt.now()

    msec = (end-begin).microseconds
    print ("msec: {}".format(msec))
    total_time = msec*iterations/1000000
    return total_time

if __name__ == "__main__":

    print('\n\n*** GENERATORE DI PASSWORD CASUALI *** \n')
    password = creapassword()

    print('\nla tua password generata è: ' + password + '\n')


    if password != "" :
        tot=decriptapassword(password)
        print("Il tempo di bruteforce per trovare la seguente password e': {} milliseconds".format(tot))

    else :
        print("la password non è stata generata, riprova per una password piu' sicura")
