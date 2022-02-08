import numpy as np
from numpy import random as nprnd
import random as rnd
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import shift
import time as t
#Check time simulation


def shiftFunc(Array,Shift):
    if Shift > len(Array):
        print('Array Shift exceeds length of array. Function will return input Array')
        return Array
    else:
        ArrayFront, ArrayBack = Array[0:int(Shift)],Array[int(Shift):len(Array)]
        ShiftedArray = np.concatenate([ArrayBack,ArrayFront])
    return ShiftedArray

def chiSQ(inputArray,binNo):
    Observed = np.zeros(binNo)
    Expected = len(inputArray) / binNo
    BinBoundary = np.arange(0,1+(1/binNo),(1/binNo))
    for i in range(0,len(Observed)):
        for k in range(0,len(inputArray)):
            if inputArray[k] >= BinBoundary[i] and BinBoundary[i+1] > inputArray[k] :
                Observed[i] += 1
            #The above if statement will not count any instance of the inputArray when it is one, this next line fizes that
            elif  inputArray[k] == 1:
                Observed[i] += 1   
            else:
               #pass is a null operation the IDE kept throwing me an error about the next line and Pass seemed to placate it
               pass
    ChiSq = np.sum((Observed - Expected)**2 / Expected)
    
    return ChiSq

#Probability of exceeding chi squadred with 9 degrees of freedom and alpha = 0.05 is 16.92

TotalNum = int(input("How many random numbers would you like to generate? : "))

#RandomSeed = t.time()
#Set Seed = 1337

Seed = int(1337)

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



TotalEvents = int(input("How many events will the particles in the box experiance? : ")) 
Timeaxis = np.arange(0,TotalEvents + 1,1)
PCRandParticleLocY = np.zeros((len(PCRand),len(Timeaxis)))
SFRandParticleLocY = np.zeros((len(SFRand),len(Timeaxis)))
for i in range(0,len(PCRand)):
    PCRandParticleLocY[i][0] = PCRand
    SFRandParticleLocY[i][0] = (SFRand + 1)


for i in range(0,len(Timeaxis)):
    
    #Picks a random particle from each partition
    Particle1 = PCRandParticleLocY[PCG64.integers(0,TotalNum,1)[0]]
    Particle2 = SFRandParticleLocY[SFC64.integers(0,TotalNum,1)[0]]
    
    #Picks a random particle in each partition and moves it to the oppostie parition
    if Particle1 <= 1:
        Particle1 +=1
    else:
        Particle1 -= 1
    
    if Particle2 >= 1:
        Particle2 -=1
    else:
        Particle2 += 1

plt.scatter(Timeaxis,Particle1)
plt.scatter(Timeaxis,Particle2)