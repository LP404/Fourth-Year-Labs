import numpy as np
import scipy as sp
import quantumrandom as qrand

#Named after driver that won the 1983 Monte-Carlo rally 
def WalterRohl():
    while True:
        try:
            Dims = int(input('Number of dimensions : '))
            if Dims > 0:
                break
            else:
                print("Number of dimensions amount can't be less than zero, try again")
        except ValueError:
            print("Number of dimensions amount must be a number, try again")
    
    Lims = [[] for _ in range(0,Dims)]
    
    for i in range(Dims):
        while True:   
            try:
                upper = float(input('Value of upper limit : '))
                lower = float(input('Value of lower limit : '))
                break
            except ValueError:
                print("Value is not a real number, try again")
        Lims[i].insert(0,upper)
        Lims[i].insert(1,lower)
    
    
    return Dims, Lims


#Named after the car that won the 1983 Monte-Carlo rally
def Lancia037(Samples,Dims):
    
    
    
    return





