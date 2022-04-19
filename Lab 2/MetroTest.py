#This file merely exists as a testbead for the metropolis algorithim

import numpy as np
import matplotlib.pyplot as plt
import time as t
import os

Seed = 22061910
SFC64 = np.random.Generator(np.random.SFC64(seed=np.random.SeedSequence(Seed)))

n = 1000000
x0 = 0
delta = 0.1

def FDBinFinder(RandArray):
    
    #Gets the lower and upper quartiles for the input array
    RandArray25, RandArray75 = np.percentile(RandArray, [25, 75])
    
    #The calcualtion that is the Freedman–Diaconis rule is performed
    BinWidth = 2 * (RandArray75 - RandArray25) * len(RandArray) ** (-1/3)
    
    #Calcualtes number of bins from bin width
    BinNum = round((RandArray.max() - RandArray.min()) / BinWidth)
    
    return BinNum


# def Integrand(DataIn):
#     if type(DataIn) == list:
#         x = DataIn[0]
#     else:
#         x = DataIn
    
#     return np.exp(-abs(x)) 



def Integrand(DataIn):
    if type(DataIn) == list:
        x = DataIn[0]
    else:
        x = DataIn
        
    return ((4 / np.pi**2) * x * (np.pi - x))   


#Metropolis algorithim

    
#Opens a txt using the current UNIX time as a unique identifier
#Since there will be only two outputs in a given run of the simulation it should be trivial to disinguish what txts belong to what answers
MetroOut = open('Metro\\MetroOut'+str(int(t.time()))+'.txt','w')

#Initlises x arrays and sets the first value to x0
x = np.zeros(n)
x[0] = x0
    
for i in range(1,len(x)):
        
    #Gets current x value from x array
    xCurrent = x[i-1]
    
    #Generates trial value
    xTrial = xCurrent + SFC64.uniform(-delta,delta)
    
    #Finds weght
    w = Integrand(xTrial) / Integrand(xCurrent)
    
    #Check is weight exceeds 1, if so sets new x value to weight        
    if w >= 1:
        x[i] = xTrial 
    
    else:
        #Generates r value
        r = SFC64.uniform(0,1)
        #If r value is less than weight, adopts trial value for new x value
        if r <= w:
            x[i] = xTrial 
            
        #If both previous conditions are new, adopts current x value for new x value
        else:
            x[i] = xCurrent




#Burns 10% of the values and only takes every second remaining value
out = x[int(n/10)::2]

#Writes data to txt
for i in range(len(out)):
    if i == (len(out) - 1):
        MetroOut.write(f"{out[i]}")           
    else:   
        MetroOut.write(f"{out[i]};")

#Closes txt
MetroOut.close()    
