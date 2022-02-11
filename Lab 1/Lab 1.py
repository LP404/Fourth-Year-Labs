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

TotalNum = int(input("How many random numbers would you like to generate? : "))

#RandomSeed = t.time()
#Set Seed = 1337

Seed = int(t.time())

PCG64 = np.random.Generator(np.random.PCG64(seed=np.random.SeedSequence(Seed)))
SFC64 = np.random.Generator(np.random.SFC64(seed=np.random.SeedSequence(Seed)))

PCRand = PCG64.random(TotalNum)
SFRand = SFC64.random(TotalNum)

#ChiSQ Test

#Probability of exceeding chi squadred with 9 degrees of freedom and alpha = 0.05 is 16.92
#Probability of exceeding chi squadred with 9 degrees of freedom and alpha = 0.05 is 16.92


PCRand25, PCRand75 = np.percentile(PCRand, [25, 75])
SFRand25, SFRand75 = np.percentile(SFRand, [25, 75])

PCRandBinWidth = 2 * (PCRand75 - PCRand25) * len(PCRand) ** (-1/3)
SFRandBinWidth = 2 * (SFRand75 - SFRand25) * len(SFRand) ** (-1/3)

PCRandBins = round((PCRand.max() - PCRand.min()) / PCRandBinWidth)
SFRandBins = round((SFRand.max() - SFRand.min()) / SFRandBinWidth)


plt.hist(PCRand, bins=PCRandBins)
plt.hist(SFRand, bins=SFRandBins)


PCRandChiSQ = chiSQ(PCRand,PCRandBins)
SRRandChiSQ = chiSQ(SFRand,SFRandBins)




#Correlations


PCRandAutoCorrelate = np.correlate((PCRand-np.mean(PCRand)) / (np.std(PCRand) * len(PCRand)),(PCRand-np.mean(PCRand)) / (np.std(PCRand)),mode = 'full')
SFRandAutoCorrelate = np.correlate((SFRand-np.mean(SFRand)) / (np.std(SFRand) * len(SFRand)),(SFRand-np.mean(SFRand)) / (np.std(SFRand)),mode = 'full')   


Xaxis = np.arange(1,len(PCRandAutoCorrelate) + 1,1)
ShiftedXaxis = Xaxis - Xaxis[int((len(Xaxis)-1)/2)]

PCRandLooperCorrelate = SFRandLooperCorrelate = np.zeros(TotalNum)

for i in range(0,TotalNum):
    PCRandLooperCorrelate[i] = np.correlate(PCRand,shiftFunc(PCRand,i),mode='valid')
    SFRandLooperCorrelate[i] = np.correlate(SFRand,shiftFunc(SFRand,i),mode='valid')







#Tasks 2-4
TotalParticles = int(input("How many particles are in the box? : ")) 
TotalEvents = int(input("How many events will the particles in the box experiance? : ")) 

Timeaxis = np.arange(0,TotalEvents + 1,1)

PCRandBox = PCG64.random(TotalParticles)
SFRandBox = SFC64.random(TotalParticles)

PCRandParticleLocY = PCRandParticleLocYBox2 = np.zeros((len(PCRandBox),len(Timeaxis)))
SFRandParticleLocY = SFRandParticleLocYBox2 = np.zeros((len(SFRandBox),len(Timeaxis)))

for i in range(0,len(PCRandBox)):
    PCRandParticleLocY[i][0] =  PCRandParticleLocYBox2[i][0] = PCRandBox[i]
    SFRandParticleLocY[i][0] = SFRandParticleLocYBox2[i][0] = (SFRandBox[i] + 1)
    


for i in range(0,len(Timeaxis)-1):
    
    #Picks a random particle from each partition
    Index1 = PCG64.integers(0,TotalParticles,1)[0]
    Index2 = SFC64.integers(0,TotalParticles,1)[0]
    
    Index3 = PCG64.integers(0,TotalParticles,1)[0]
    Index4 = SFC64.integers(0,TotalParticles,1)[0]
    
    Particle1 = PCRandParticleLocY[Index1][i]
    Particle2 = SFRandParticleLocY[Index2][i]
    
    Particle3 = PCRandParticleLocY[Index1][i]
    Particle4 = SFRandParticleLocY[Index2][i]
    
    #Picks a random particle in each partition and moves it to the oppostie parition
    if Particle1 <= 1:
        Particle1 = Particle1 + 1
    else:
        Particle1 = Particle1 - 1
    
    if Particle2 >= 1:
        Particle2 = Particle2 - 1
    else:
        Particle2 = Particle2 + 1
     
    
    if Particle3 <= 1:
        if PCG64.integers(0,4,1)[0] < 3:
            Particle3 = Particle3 + 1
    else:
        if PCG64.integers(0,4,1)[0] < 1:    
            Particle3 = Particle3 - 1
        
    if Particle4 >= 1:
        if SFC64.integers(0,4,1)[0] < 3:
            Particle4 = Particle4 - 1
    else:
        if SFC64.integers(0,4,1)[0] < 1:
            Particle4 = Particle4 + 1
        
    PCRandParticleLocY[:,i+1:i+2] = PCRandParticleLocY[:,i:i+1]
    SFRandParticleLocY[:,i+1:i+2] = SFRandParticleLocY[:,i:i+1]
    
    PCRandParticleLocYBox2[:,i+1:i+2] = PCRandParticleLocYBox2[:,i:i+1]
    SFRandParticleLocYBox2[:,i+1:i+2] = SFRandParticleLocYBox2[:,i:i+1]
    
    PCRandParticleLocY[Index1][i] = Particle1
    SFRandParticleLocY[Index2][i] = Particle2
    
    PCRandParticleLocYBox2[Index3][i] = Particle3
    SFRandParticleLocYBox2[Index4][i] = Particle4