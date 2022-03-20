import numpy as np
import scipy as sp
from inspect import signature
import quantumrandom as qrand

#Seed = int(t.time())
Seed = 22061910

#vars()['Force_'+str(x)]

SFC64 = np.random.Generator(np.random.SFC64(seed=np.random.SeedSequence(Seed)))


#Will sqaure a list of arrays for all arrays in the list
def SqList(listIn):
    listOut = [i**2 for i in listIn]
    return listOut

#Integrand
def Integrand(DataIn):

    x = DataIn[0]
    y = DataIn[1]

    return x + y

def nDcube(DataIn):
    return DataIn

#Named after the car that won the 1983 Monte-Carlo rally

NoSamples = 10000
NoDims = 3

def Lancia037(NoSamples,Integrand,NoDims):
    
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
        samples = SFC64.uniform(Lims[i][0],Lims[i][1],NoSamples)
        SampleBox[i] = samples
        
    
    Ssum = Integrand(SampleBox)
    SsumSq = Ssum**2
    
    ExpectSsum = sum(Ssum) / NoSamples
    ExpectSsumSq = sum(SsumSq) / NoSamples
    
    Var = ((ExpectSsumSq) - (ExpectSsum)**2)
    
    Std = (Var)**0.5
    
    Coef = np.prod(np.diff(Lims))
    
    Total = np.sum(Ssum)
    
    Final = (Coef / NoSamples) * Total
    
    error = Coef * Std / (NoSamples)**0.5
    
    return Lims,SampleBox,Final, error


#Lims,SampleBox,Result,Error,Error2,coef,one = Lancia037(1000000,nDcube,2)

#This car has won several monte carlo rallies
def AudiQuattroA2(Samples,Lims):
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