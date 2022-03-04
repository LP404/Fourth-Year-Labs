import numpy as np
import scipy as sp
from inspect import signature
import quantumrandom as qrand

#Integrand
def func():
    return 2
    

#Named after driver that won the 1983 Monte-Carlo rally 
def WalterRohl(Integrad):
    Dims = len(signature(func).parameters)
    
    #This is for the edge case of an integrand that consists of one or more constants
    if Dims == 0:
        Dims = 1
    else:
        pass
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
def Lancia037(Samples,Dims,Lims):
        
        
        
    return



Lancia037(WalterRohl(func()))

