import numpy as np
from inspect import signature
import IntegralFunctions as IF

Seed = 22061910
SFC64 = np.random.Generator(np.random.SFC64(seed=np.random.SeedSequence(Seed)))


def Integrand(DataIn):
    x = DataIn[0]
    return 2*np.exp((-x**2))

#The metropolis alrotithim necessistaes the inclusion of the if statment
#This is because the metropolis algorithim was developed a little while after the MC Integrator and it does not use a list to store the dimentions
#I know it's a little janky but this is my solution to the problem
def WeightFunc(DataIn):
    if type(DataIn) == list:
        x = DataIn[0]
    else:
        x = DataIn
    
    return np.exp(-abs(x)) 

# def FiveB(DataIn):
#     x = DataIn[0]
#     return (1.5 * np.sin(x))

# def FiveBWeight(DataIn):
#     if type(DataIn) == list:
#         x = DataIn[0]
#     else:
#         x = DataIn
        
#     return ((4 / np.pi**2) * x * (np.pi - x))   


def metropolis(x0, delta, n, Integrand):
    
    #Opens a txt using the current UNIX time as a unique identifier
    #Since there will be only two outputs in a given run of the simulation it should be trivial to disinguish what txts belong to what answers

    
    #Initilises the Metropolis algorithim
    x = np.zeros(n)
    x[0] = x0
    
    #Initilise loop
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
 
    return out

# #Creates a pesudo log spaced NoSamples
# Order = np.logspace(1, 6, 6)
# #BaseNo = np.array([1,2.5,5,7.5])
# BaseNo = np.arange(1,10,1)
# NoSamples = np.outer(Order,BaseNo).flatten()
# NoSamples = np.array([1000000])

#Converts all the values in NoSamples to integers if they are not already
# NoSamples = NoSamples.astype(int)

delta = 0.2

DoingNBall = False
Dims = 3

Lims = [[-10,10]]
# Lims = [[0,np.pi]]
Lim6 = [[-2,2],[-2,2],[-2,2]]
n = 500000

initGuess = np.array([1])
# initGuess = np.array([1.5])
    
    

Out = IF.MCIntegratorFindConst(initGuess, 0.2, n, WeightFunc, 1, Lims)

 
# #Monte Carlo Integrator with importance sampeling
    
# #Will check if there are any unspecified dimentions
# #If there are any the function will abort and send an error message
# DimsCheck = len(signature(Integrand).parameters)
# if DimsCheck > Dims:
#     print('There are dimentions that have no limits assigned to them')
#     #return
# else:
#     pass
    
# #Creates a list to hold all randomly generated points for the integrator
# SampleBox = [[] for _ in range(0,Dims)]


# #Generates samples via the metropolis algorithim
# #Puts them in the same sample box list
# for i in range(Dims):
#     SampleBox[i] = metropolis(initGuess[i], delta, n, WeightFunc)
 

# else:

#     #Generates the output of the function(s) for the importance sampling method
#     Ssum = (Integrand(SampleBox) / WeightFunc(SampleBox))


#     #Generates the normalisation coeffiecnet, exists as an array now but will be summed
#     Norm = (1 / WeightFunc(SampleBox))


            
#     #Finds the values squared for the variance
#     SsumSq = Ssum**2
#     NormSq = Norm**2
    
    
#     #Calcaultes the expectation values for finding the total and the squared values for the variance
#     ExpectVal = sum(Ssum) / sum(Norm)
#     ExpectValSq = sum(SsumSq) / sum(NormSq)
    
    
#     #Find the variance
#     Var = ((ExpectValSq) - (ExpectVal)**2)
    
#     #Find the standard deviation
#     Std = (Var)**0.5
    
#     #Calcualtes the difference between the limits for the coefficent that will be multipled by the expectation value
#     Coef = np.prod(np.diff(Lims))
    
#     # Generates final answer
#     Final = Coef * ExpectVal
    
#     #Error is generated in accorance with the monte carlo importance sampling error
#     error = Coef * Std / n**0.5
        
        
    
