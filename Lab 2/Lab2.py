import numpy as np
import scipy as sp
from inspect import signature
import quantumrandom as qrand

#Seed = int(t.time())
Seed = 22061910

SFC64 = np.random.Generator(np.random.SFC64(seed=np.random.SeedSequence(Seed)))

#Generates an array of n lengths filled with random numbers from 0 to 1

#Integrand
def func(x):
    return 4*x
   
def circlefunc(x,r):
    return (r**2 - x**2)**0.5

#Named after the car that won the 1983 Monte-Carlo rally
def Lancia037(NoSamples,Integrand):
    Dims = len(signature(Integrand).parameters)
    
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
    
    
    
    
    samples = SFC64.uniform(Lims[0][0],Lims[0][1],NoSamples)
                  
    # for i in range(Dims):
    #     sum()
    
    
    
    
    return samples