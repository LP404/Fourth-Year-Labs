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
def chiSQ(Observed,binNo):
    #Observed corresponds to the number of counts in a given bin, this has already been calcauted by plt.hist
    
    #This is the expected number of counts of values that fall within a given bin
    Expected = len(Observed) / binNo

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


#Script prompts user input, it could be a decalred variable but I like the interactivity
TotalNum = int(input("How many random numbers would you like to generate? : "))


#Seed is set using the t.time() function, returns the current time in Unix time, which is seconds since 01/01/1970 00:00 (UTC)
#Seed could also be set with a integer value

Seed = int(t.time())
#Seed = 1337

#The Bit Generators PCG64 and SFC64 were chosen for this script
PCG64 = np.random.Generator(np.random.PCG64(seed=np.random.SeedSequence(Seed)))
SFC64 = np.random.Generator(np.random.SFC64(seed=np.random.SeedSequence(Seed)))

#Generates an array of n lengths filled with random numbers from 0 to 1
PCRand = PCG64.random(TotalNum)
SFRand = SFC64.random(TotalNum)

#ChiSQ Test


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