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
NoDims = 2

#def Lancia037(NoSamples,Integrand,NoDims):
DimsCheck = len(signature(Integrand).parameters)
Dims = NoDims

if DimsCheck > Dims:
    print('There are dimentions that have no limits assigned to them')
    #return
else:
    pass

Lims = [[] for _ in range(0,Dims)]
SampleBox = [[] for _ in range(0,Dims)]
SampleBoxSq = [[] for _ in range(0,Dims)]

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
    SampleBoxSq[i] = samples**2


Ssum = Integrand(SampleBox)
SsumSq = Integrand(SampleBoxSq)

Total = sum(Ssum)
TotalSq = sum(SsumSq)

Var = ((TotalSq) - (Total)**2) / NoSamples

Std = (Var)**0.5

Coef = np.prod(np.diff(Lims))

error = Coef * (np.std(Ssum) / (NoSamples)**0.5)

error2 = Coef * Std / (NoSamples)**0.5
    
    #return Lims,SampleBox, (Coef / NoSamples) * Total, error,error2, Coef, Std


#Lims,SampleBox,Result,Error,Error2,coef,one = Lancia037(1000000,nDcube,2)

#This car has won several monte carlo rallies
def AudiQuattroA2(Samples,Lims):
    
    return