import numpy as np
from inspect import signature
import quantumrandom as qrand
from functools import reduce 
from operator import mul

#Seed = int(t.time())
Seed = 22061910
SFC64 = np.random.Generator(np.random.SFC64(seed=np.random.SeedSequence(Seed)))

#Reshapes a list
def reshape(ListIn, shape):
    if len(shape) == 1:
        return ListIn
    n = reduce(mul, shape[1:])
    return [reshape(ListIn[i*n:(i+1)*n], shape[1:]) for i in range(len(ListIn)//n)]


def MCIntegrator(NoSamples,Integrand,NoDims):
    
    DimsCheck = len(signature(Integrand).parameters)
    Dims = NoDims
    
    if DimsCheck > Dims:
        print('There are dimentions that have no limits assigned to them')
        #return
    else:
        pass
    
    Lims = [[] for _ in range(0,Dims)]
    SampleBox = [[] for _ in range(0,Dims)]
    
    for i in range(Dims):
        while True:   
            try:
                lower = float(input('Value of lower limit for dimention '+str(i+1)+' : '))
                upper = float(input('Value of upper limit for dimention '+str(i+1)+' : '))
                print('\n')
                break
            except ValueError:
                print("Value is not a real number, try again")
        Lims[i].insert(0,lower)
        Lims[i].insert(1,upper)
    
    
    for i in range(Dims):
        SampleBox[i] = SFC64.uniform(Lims[i][0],Lims[i][1],NoSamples)
        
    
    Ssum = Integrand(SampleBox)
    SsumSq = Ssum**2
    
    ExpectSsum = sum(Ssum) / NoSamples
    ExpectSsumSq = sum(SsumSq) / NoSamples
    
    Var = ((ExpectSsumSq) - (ExpectSsum)**2)
    
    Std = (Var)**0.5
    
    Coef = np.prod(np.diff(Lims))
    
    Final = Coef * ExpectSsum
    
    error = Coef * Std / (NoSamples)**0.5
    
    return Lims,SampleBox,Final, error


#Lims,SampleBox,Result,Error,Error2,coef,one = Lancia037(1000000,nDcube,2)

#This car has won several monte carlo rallies
def nBallVolume(Samples,Lims):
    #checks if the limits pretaine to a n ball, by checking if they are all the same length in each axis and occupy the same respective coorsinates in each axis
    check = True
    for i in range(1,len(Lims)):
        if Lims[i] == Lims[i-1]:
            pass
        else:
            check = False
    
    if check == False:
        print('nBall calcualtion is not possible, check limits')
        return
    else:
        pass
    
    #we know that the equation for an n ball is dim1**2 + dim2**2 + ... + dimN**2 = radius**2
    #Factor in center points
    
    
    rsq = (np.diff(Lims)[0][0]/2)**2
    
    InSphere = 0
    
    for i in range(0,len(Samples[0])):
        total = 0
        for j in range(0,len(Lims)):
            total += ([row[i] for row in Samples][j] - np.mean(Lims[0]))**2
        
        
        if total <= rsq:
            InSphere += 1
        else:
            pass
    
    Volume = np.prod(np.diff(Lims)) * (InSphere / len(Samples[0]))
    
    
    return InSphere ,Volume

def metropolis(x0, delta, n, Integrand):
    x = np.zeros(n)
    x[0] = x0
    i = 1
    while x[-1] == 0:
        xCurrent = x[i-1]
        xTemp = xCurrent + SFC64.uniform(-delta,delta)
        w = Integrand(xTemp) / Integrand(xCurrent)
        if w <= 1:
            xCurrent = xTemp
            x[i-1] = xCurrent
            i+=1
        else:
            r = SFC64.uniform(0,1)
            if r <= w:
                xCurrent = xTemp
                x[i-1] = xCurrent
                i+=1  
            else:
                pass  
    return x[int(n/10)::2]

def MCISIntegrator(delta,n,Integrand,WeightFunc,Dims):
    
    DimsCheck = len(signature(Integrand).parameters)
    
    if DimsCheck > Dims:
        print('There are dimentions that have no limits assigned to them')
        #return
    else:
        pass
    
    Lims = [[] for _ in range(0,Dims)]
    SampleBox = [[] for _ in range(0,Dims)]
    initGuess = np.zeros(Dims)
    
    for i in range(Dims):
        while True:   
            try:
                lower = float(input('Value of lower limit for dimention '+str(i+1)+' : '))
                upper = float(input('Value of upper limit for dimention '+str(i+1)+' : '))
                initGuess[i] = float(input('Inital guess value for dimention '+str(i+1)+' : '))
                print('\n')
                break
            except ValueError:
                print("Value is not a real number, try again")
        Lims[i].insert(0,lower)
        Lims[i].insert(1,upper)
    
    for i in range(Dims):
        SampleBox[i] = metropolis(initGuess[i], delta, n, Integrand)
        
    
    Norm = 1 / WeightFunc(SampleBox)
    
    Ssum = (Integrand(SampleBox) / WeightFunc(SampleBox))
    
    SsumSq = Ssum**2
    
    ExpectSsum = sum(Ssum) / sum(Norm)
    ExpectSsumSq = sum(SsumSq) / sum(Norm)
    
    Var = ((ExpectSsumSq) - (ExpectSsum)**2)
    
    Std = (Var)**0.5
    
    Coef = np.prod(np.diff(Lims))
    
    Final = Coef * ExpectSsum
    
    error = Coef * Std / (n)**0.5
    
    return Lims,SampleBox,Final, error

def main():
    print('Oh, you\'re actually running this file directly?\nHave a cookie -> 🍪 ')
    return

if __name__ == '__main__':
    main()