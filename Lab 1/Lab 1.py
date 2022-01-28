import numpy as np
from numpy import random as nprnd
import random as rnd
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import shift
import time as t

def shiftFunc(array,shiftVal):
    
    if shiftVal > len(array):
        print('Length of shift cannot exceed length of array')
        return
    
    else:
        
        array1 = array[int(shiftVal-1):]
        shiftedArray = shift(array,shiftVal,cval=0)
        for i in range(0,len(array1)):
            shiftedArray[i] = array1[i]
            
        return shiftedArray


TotalNum = int(input("How many random numbers would you like to generate? : "))

Seed = int(t.time())

PCG64 = np.random.Generator(np.random.PCG64(seed=np.random.SeedSequence(Seed)))
SFC64 = np.random.Generator(np.random.SFC64(seed=np.random.SeedSequence(Seed)))

PCRand = PCG64.random(TotalNum)
SFRand = SFC64.random(TotalNum)

Cor1 = np.correlate(PCRand,PCRand,mode = 'same')
Cor2 = np.correlate(SFRand,SFRand,mode = 'same')


Cor3 = np.correlate(PCRand,PCRand,mode = 'full')
Cor4 = np.correlate(SFRand,SFRand,mode = 'full')   

Xaxis = np.arange(1,TotalNum + 1,1)
Xaxis3 = Xaxis - Xaxis[int((len(Xaxis)-1)/2)]

Xaxis2 = np.arange(1,len(Cor3) + 1,1)
Xaxis4 = Xaxis2 - Xaxis2[int((len(Xaxis2)-1)/2)]



TotalParticles = int(input("How many particles are in the box? : "))
ParticleLocX = nprnd.rand(TotalParticles)
ParticleLocX-=1 
ParticleLocY = nprnd.rand(TotalParticles)