import numpy as np
import matplotlib.pyplot as plt
import time as t

#Basic function that shifts all the values in an array x number of indices 'to the right'.
def shiftFunc(Array,Shift):
    # A quick check to see if the desired shift length exceeds the length of the array
    if Shift > len(Array):
        print('Array Shift exceeds length of array. Function will return input Array')
        return Array
    else:
        #Seperates the Array into two parts at the point where it is to be shifted the second part is then moved to be infront and the arrays are concatenated together to make a shifted array
        ArrayFront, ArrayBack = Array[0:int(Shift)],Array[int(Shift):len(Array)]
        ShiftedArray = np.concatenate([ArrayBack,ArrayFront])
    return ShiftedArray


#Function that performs a chi squared test using the chi squared formula
def chiSQ(TotalNum,Observed,binNo):
    #Observed corresponds to the number of counts in a given bin, this has already been calcauted by plt.hist
    
    #This is the expected number of counts of values that fall within a given bin
    Expected = TotalNum / binNo

    #Peforms the final summation to attain the chi sqaured value
    ChiSq = np.sum((Observed - Expected)**2 / Expected)
    
    return ChiSq


#A function that performs calculations relevant to the Freedman–Diaconis rule, which is used to find the number of bins in a histogram should use for a given dataset

def FDBinFinder(RandArray):
    
    #Gets the lower and upper quartiles for the input array
    RandArray25, RandArray75 = np.percentile(RandArray, [25, 75])
    
    #The calcualtion that is the Freedman–Diaconis rule is performed
    BinWidth = 2 * (RandArray75 - RandArray25) * len(RandArray) ** (-1/3)
    
    #Calcualtes number of bins from bin width
    BinNum = round((RandArray.max() - RandArray.min()) / BinWidth)
    
    return BinNum


#All input variables for all tasks are delclared here
TotalNum = 20000
TotalParticles = 10
TotalEvents = 5

#Seed is set using the t.time() function, returns the current time in Unix time, which is seconds since 01/01/1970 00:00 (UTC)
#Seed could also be set with a integer value

#Seed = int(t.time())
Seed = 22061910

#The Bit Generators PCG64 and SFC64 were chosen for this script
PCG64 = np.random.Generator(np.random.PCG64(seed=np.random.SeedSequence(Seed)))
SFC64 = np.random.Generator(np.random.SFC64(seed=np.random.SeedSequence(Seed)))

#Generates an array of n lengths filled with random numbers from 0 to 1
PCRand = PCG64.random(TotalNum)
SFRand = SFC64.random(TotalNum)

#Next section of code will:
#- Generate the number of bins needed for the histograms
#- Create and plot the histograms
#- Calcaulted the chi sqaured values for the histograms

PCRandBinNum = FDBinFinder(PCRand)
SFRandBinNum = FDBinFinder(SFRand)

plt.figure(1)
PCRandHistOut = plt.hist(PCRand, bins = PCRandBinNum, alpha=0.5,edgecolor='black',color='navy')
plt.title(f'BitGenrator PCG64 Uniform Distributions with {TotalNum} samples \n Seed = {Seed}')
plt.xlabel('Random Values')
plt.ylabel('Occurance of Random values')


plt.figure(2)
SFRandHistOut = plt.hist(SFRand, bins = SFRandBinNum, alpha=0.5,edgecolor='black',color='navy')
plt.title(f'BitGenrator SFC64 Uniform Distributions with {TotalNum} samples \n Seed = {Seed}')
plt.xlabel('Random Values')
plt.ylabel('Occurance of Random values')

PCRandChiSQ = chiSQ(TotalNum,PCRandHistOut[0],PCRandBinNum)
SRRandChiSQ = chiSQ(TotalNum,SFRandHistOut[0],SFRandBinNum)

print(f'Chi-Squared for PCG64 for {TotalNum} samples with {PCRandBinNum - 1} degress of freedom is {np.around(PCRandChiSQ,2)}')
print(f'Chi-Squared for SFC64 for {TotalNum} samples with {SFRandBinNum - 1} degress of freedom is {np.around(PCRandChiSQ,2)}')

#Correlations
#Numpy AutoCorrelate

PCRandAutoCorrelate = np.correlate(PCRand,PCRand, mode = 'full')
SFRandAutoCorrelate = np.correlate(SFRand,SFRand, mode = 'full')

PCRandAutoCorrelateNorm = np.correlate((PCRand-np.mean(PCRand)) / (np.std(PCRand) * len(PCRand)),(PCRand-np.mean(PCRand)) / (np.std(PCRand)),mode = 'full')
SFRandAutoCorrelateNorm = np.correlate((SFRand-np.mean(SFRand)) / (np.std(SFRand) * len(SFRand)),(SFRand-np.mean(SFRand)) / (np.std(SFRand)),mode = 'full')   

Xaxis = np.arange(1,len(PCRandAutoCorrelate) + 1,1)
ShiftedXaxis = Xaxis - Xaxis[int((len(Xaxis)-1)/2)]


#'Manual' correlation using loops

PCRandLooperCorrelate = np.zeros(TotalNum)
SFRandLooperCorrelate = np.zeros(TotalNum)
Xaxis2 = np.arange(1,TotalNum + 1,1)

for i in range(0,TotalNum):
    PCRandLooperCorrelate[i] = (np.correlate(PCRand,shiftFunc(PCRand,i)) /  (np.sqrt(np.sum(PCRand**2) * np.sum(shiftFunc(PCRand,i)**2))))
    SFRandLooperCorrelate[i] = (np.correlate(SFRand,shiftFunc(SFRand,i)) /  (np.sqrt(np.sum(SFRand**2) * np.sum(shiftFunc(SFRand,i)**2))))


#All np.correalte arrays share the same index where they reach their maximum
#The purpose of this code block is to remove the central point of no shift as we know that the array will fully corealte with itself
IndexDelete = np.where(PCRandAutoCorrelate == max(PCRandAutoCorrelate))[0][0]
ShiftedXaxis = np.delete(ShiftedXaxis,IndexDelete)
PCRandAutoCorrelate = np.delete(PCRandAutoCorrelate,IndexDelete)
SFRandAutoCorrelate = np.delete(SFRandAutoCorrelate,IndexDelete)
PCRandAutoCorrelateNorm = np.delete(PCRandAutoCorrelateNorm,IndexDelete)
SFRandAutoCorrelateNorm = np.delete(SFRandAutoCorrelateNorm,IndexDelete)



plt.figure(3)
plt.plot(ShiftedXaxis,PCRandAutoCorrelate)
plt.title(f'BitGenrator PCG64 Correlation output\n Seed = {Seed}')
plt.xlabel('x-shift')
plt.ylabel('Correlation')


plt.figure(4)
plt.plot(ShiftedXaxis,SFRandAutoCorrelate)
plt.title(f'BitGenrator SFC64 Correlation output \n Seed = {Seed}')
plt.xlabel('x-shift')
plt.ylabel('Correlation')


plt.figure(5)
plt.scatter(ShiftedXaxis,PCRandAutoCorrelateNorm, s = 1)
plt.title(f'BitGenrator PCG64 Correlation output, Normalised \n Seed = {Seed}')
plt.xlabel('x-shift')
plt.ylabel('Correlation')


plt.figure(6)
plt.scatter(ShiftedXaxis,SFRandAutoCorrelateNorm, s = 1)
plt.title(f'BitGenrator SFC64 Correlation output, Normalised \n Seed = {Seed}')
plt.xlabel('x-shift')
plt.ylabel('Correlation')





plt.figure(7)
plt.plot(Xaxis2,PCRandLooperCorrelate)
plt.title(f'BitGenrator PCG64 Correlation output with manual shift apllied \n Seed = {Seed}')
plt.xlabel('x-shift')
plt.ylabel('Correlation')


plt.figure(8)
plt.plot(Xaxis2,SFRandLooperCorrelate)
plt.title(f'BitGenrator SFC64 Correlation output with manual shift apllied \n Seed = {Seed}')
plt.xlabel('x-shift')
plt.ylabel('Correlation')




ShiftVal = 20
plt.figure(9)
plt.title(f'BitGenrator PCG64 Lag plot with {TotalNum} samples \n Seed = {Seed}')
plt.xlabel('Random Values')
plt.ylabel(f'Random values shifted by + {ShiftVal}')
plt.scatter(PCRand,shiftFunc(PCRand,ShiftVal), s = 1)

plt.figure(10)
plt.title(f'BitGenrator SFC64 Uniform Distributions with {TotalNum} samples \n Seed = {Seed}')
plt.xlabel('Random Values')
plt.ylabel(f'Random values shifted by + {ShiftVal}')
plt.scatter(SFRand,shiftFunc(SFRand,ShiftVal), s = 1)



#Tasks 2-4

Timeaxis = np.arange(0,TotalEvents + 1,1)

PCRandBox = PCG64.random(TotalParticles)
SFRandBox = SFC64.random(TotalParticles)

PCRandParticleLocY = np.zeros((len(PCRandBox),len(Timeaxis)))
PCRandParticleLocYBox2 = np.zeros((len(PCRandBox),len(Timeaxis)))

SFRandParticleLocY = np.zeros((len(SFRandBox),len(Timeaxis)))
SFRandParticleLocYBox2 = np.zeros((len(SFRandBox),len(Timeaxis)))

for i in range(0,len(PCRandBox)):
    PCRandParticleLocY[i][0] = PCRandBox[i]
    PCRandParticleLocYBox2[i][0] = PCRandBox[i]
    SFRandParticleLocY[i][0] = (SFRandBox[i] + 1)
    SFRandParticleLocYBox2[i][0] = (SFRandBox[i] + 1)
    

#Probability for task 4
P = 0.75

for i in range(1,len(Timeaxis)):
    
    #Picks a random particle from each partition
    Index1 = PCG64.integers(0,TotalParticles,1)[0]
    Index2 = SFC64.integers(0,TotalParticles,1)[0]
    
    Index3 = PCG64.integers(0,TotalParticles,1)[0]
    Index4 = SFC64.integers(0,TotalParticles,1)[0]
    
    Particle1 = PCRandParticleLocY[Index1][i-1]
    Particle2 = SFRandParticleLocY[Index2][i-1]
    
    Particle3 = PCRandParticleLocY[Index1][i-1]
    Particle4 = SFRandParticleLocY[Index2][i-1]
    
    
    #Picks a random particle in each partition and moves it to the oppostie parition
    if Particle1 <= 1:
        Particle1 = Particle1 + 1
    else:
        Particle1 = Particle1 - 1
    
    if Particle2 >= 1:
        Particle2 = Particle2 - 1
    else:
        Particle2 = Particle2 + 1
     
    #Picks a random particle in each partition and prepares it to move it to the oppostie parition
    if Particle3 <= 1:
        #A second check occus to see if it makes the transition, if it does it will cross the parition
        if PCG64.random(1)[0] < P:
            Particle3 = Particle3 + 1
    else:
        #A second check occus to see if it makes the transition, if it does it will cross the parition
        if PCG64.random(1)[0] >= P:    
            Particle3 = Particle3 - 1
        
    #This does mean that it is possible for no transition to occur in any given 'timeframe'
        
    if Particle4 >= 1:
        if SFC64.random(1)[0] < P:
            Particle4 = Particle4 - 1
    else:
        if PCG64.random(1)[0] >= P:
            Particle4 = Particle4 + 1
      
    #I understand this is not the most effiecnet or elegant method to do this, but this is the only one that would work
    for k in range(0,len(PCRandBox)):
        PCRandParticleLocY[k][i] = PCRandParticleLocY[k][i-1]
        SFRandParticleLocY[k][i] =  SFRandParticleLocY[k][i-1]
        PCRandParticleLocYBox2[k][i] = PCRandParticleLocYBox2[k][i-1]
        SFRandParticleLocYBox2[k][i] = SFRandParticleLocYBox2[k][i-1]
    
    PCRandParticleLocY[Index1][i] = Particle1
    SFRandParticleLocY[Index2][i] = Particle2
    
    PCRandParticleLocYBox2[Index3][i] = Particle3
    SFRandParticleLocYBox2[Index4][i] = Particle4