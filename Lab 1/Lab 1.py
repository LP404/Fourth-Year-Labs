#Import necessary libraries
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
        #Seperates the Array into two parts at the point where it is to be shifted the second part is then moved to be in front and the arrays are concatenated together to make a shifted array
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


#All input variables for all tasks are declared here
#Number of samples for task 1
TotalNum = 5000
#Number of particles and events for tasks 2-4
TotalParticles = 500
TotalEvents = 1000

#Shift value for lag plot, task 1
ShiftVal = 2000

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


#Generates the number of bins needed for the histograms
PCRandBinNum = FDBinFinder(PCRand)
SFRandBinNum = FDBinFinder(SFRand)

#Create and plot the histograms while obtaning the bin numbers needed for the chi squared test
plt.figure(1)
PCRandHistOut = plt.hist(PCRand, bins = PCRandBinNum, alpha=0.5,edgecolor='black',color='navy')
plt.title(f'BitGenrator PCG64 Uniform Distribution with {TotalNum} samples \n Seed = {Seed}')
plt.xlabel('Random Values')
plt.ylabel('Occurance of Random values')


plt.figure(2)
SFRandHistOut = plt.hist(SFRand, bins = SFRandBinNum, alpha=0.5,edgecolor='black',color='navy')
plt.title(f'BitGenrator SFC64 Uniform Distribution with {TotalNum} samples \n Seed = {Seed}')
plt.xlabel('Random Values')
plt.ylabel('Occurance of Random values')

#Calcaulted the chi sqaured values for the data in the histograms
PCRandChiSQ = chiSQ(TotalNum,PCRandHistOut[0],PCRandBinNum)
SRRandChiSQ = chiSQ(TotalNum,SFRandHistOut[0],SFRandBinNum)

#Prints out result
print(f'Chi-Squared for PCG64 for {TotalNum} samples with {PCRandBinNum - 1} degress of freedom is {np.around(PCRandChiSQ,2)}')
print(f'Chi-Squared for SFC64 for {TotalNum} samples with {SFRandBinNum - 1} degress of freedom is {np.around(PCRandChiSQ,2)}')

#Correlations
#Numpy AutoCorrelate

#Autocorrelation
PCRandAutoCorrelate = np.correlate(PCRand,PCRand, mode = 'full')
SFRandAutoCorrelate = np.correlate(SFRand,SFRand, mode = 'full')

#Normalised Autocorrelation
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


#I have used a mixture of regular and subplots depending on what would work best


#The data is plotted
Figure, ((SubPlot1,SubPlot2),(SubPlot3,SubPlot4)) = plt.subplots(2,2,figsize=(15,10), constrained_layout=False, sharex='col', sharey='row') 
Figure.suptitle(f"Correlation of data \n Seed = {Seed}")


SubPlot1.title.set_text('BitGenrator PCG64 Correlation output')
SubPlot1.plot(ShiftedXaxis,PCRandAutoCorrelate)

SubPlot2.title.set_text('BitGenrator SFC64 Correlation output')
SubPlot2.plot(ShiftedXaxis,SFRandAutoCorrelate)

SubPlot3.title.set_text('BitGenrator PCG64 Correlation output, normalised')
SubPlot3.scatter(ShiftedXaxis,PCRandAutoCorrelateNorm, s = 1)

SubPlot4.title.set_text('BitGenrator SFC64 Correlation output, normalised')
SubPlot4.scatter(ShiftedXaxis,SFRandAutoCorrelateNorm, s = 1)

SubPlot1.set_ylabel('Correlation')
SubPlot3.set_ylabel('Correlation (Normalised)')

SubPlot3.set_xlabel('X-shift')
SubPlot4.set_xlabel('X-shift')

SubPlot1.grid(b=True, which='both', linestyle='-', linewidth='0.5')
SubPlot2.grid(b=True, which='both', linestyle='-', linewidth='0.5')
SubPlot3.grid(b=True, which='both', linestyle='-', linewidth='0.5')
SubPlot4.grid(b=True, which='both', linestyle='-', linewidth='0.5')

plt.show()


plt.figure(3)
plt.plot(Xaxis2,PCRandLooperCorrelate)
plt.title(f'BitGenrator PCG64 Correlation output with manual shift apllied \n Seed = {Seed}')
plt.xlabel('x-shift')
plt.ylabel('Correlation')


plt.figure(4)
plt.plot(Xaxis2,SFRandLooperCorrelate)
plt.title(f'BitGenrator SFC64 Correlation output with manual shift apllied \n Seed = {Seed}')
plt.xlabel('x-shift')
plt.ylabel('Correlation')


plt.figure(5)
plt.title(f'BitGenrator PCG64 Lag plot with {TotalNum} samples \n Seed = {Seed}')
plt.xlabel('Random Values')
plt.ylabel(f'Random values shifted by + {ShiftVal}')
plt.scatter(PCRand,shiftFunc(PCRand,ShiftVal), s = 1)

plt.figure(6)
plt.title(f'BitGenrator SCF64 Lag plot with {TotalNum} samples \n Seed = {Seed}')
plt.xlabel('Random Values')
plt.ylabel(f'Random values shifted by + {ShiftVal}')
plt.scatter(SFRand,shiftFunc(SFRand,ShiftVal), s = 1)



#Tasks 2-4

#Create a timeaxis for the particles
Timeaxis = np.arange(0,TotalEvents + 1,1)

#Get random particle positions
PCRandBox = PCG64.random(TotalParticles)
SFRandBox = SFC64.random(TotalParticles)

#These matricies will be used to store the location of the particles
PCRandParticleLocY = np.zeros((len(PCRandBox),len(Timeaxis)))
PCRandParticleLocYBox2 = np.zeros((len(PCRandBox),len(Timeaxis)))

SFRandParticleLocY = np.zeros((len(SFRandBox),len(Timeaxis)))
SFRandParticleLocYBox2 = np.zeros((len(SFRandBox),len(Timeaxis)))

#This populates the previous matrices with the location of the particles
#The SFC64 random numbers are given a +1 increase to put it starting in another partition this was in case I decided to try out some methods of data plotting. I did not do anything with this, but I saw no reason to go back and change to +1 gain
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
    
    #Stores the current y-coordinates of the selected particle
    Particle1 = PCRandParticleLocY[Index1][i-1]
    Particle2 = SFRandParticleLocY[Index2][i-1]
    
    Particle3 = PCRandParticleLocY[Index1][i-1]
    Particle4 = SFRandParticleLocY[Index2][i-1]
    
    
    #Moves the random particle in each partition to the oppostie parition
    if Particle1 <= 1:
        Particle1 = Particle1 + 1
    else:
        Particle1 = Particle1 - 1
    
    if Particle2 >= 1:
        Particle2 = Particle2 - 1
    else:
        Particle2 = Particle2 + 1
     
    #Picks a random particle in each partition and prepares it to move it to the opposite partition
    if Particle3 <= 1:
        #A second check occurs to see if it makes the transition, if it does it will cross the partition
        if PCG64.random(1)[0] < P:
            Particle3 = Particle3 + 1
    else:
        #A second check occurs to see if it makes the transition, if it does it will cross the partition
        if PCG64.random(1)[0] >= P:    
            Particle3 = Particle3 - 1
        
    #This does mean that it is possible for no transition to occur in any given 'timeframe'
        
    if Particle4 >= 1:
        if SFC64.random(1)[0] < P:
            Particle4 = Particle4 - 1
    else:
        if PCG64.random(1)[0] >= P:
            Particle4 = Particle4 + 1
      
    #I understand this is not the most efficient or elegant method to do this, but this is the only one that would work
    #This updates the next column in the matrix with the current column’s data
    for k in range(0,len(PCRandBox)):
        PCRandParticleLocY[k][i] = PCRandParticleLocY[k][i-1]
        SFRandParticleLocY[k][i] =  SFRandParticleLocY[k][i-1]
        PCRandParticleLocYBox2[k][i] = PCRandParticleLocYBox2[k][i-1]
        SFRandParticleLocYBox2[k][i] = SFRandParticleLocYBox2[k][i-1]
    
    #These input the selected particle’s new location into the matrices
    PCRandParticleLocY[Index1][i] = Particle1
    SFRandParticleLocY[Index2][i] = Particle2
    
    PCRandParticleLocYBox2[Index3][i] = Particle3
    SFRandParticleLocYBox2[Index4][i] = Particle4


#The data is plotted
Figure, ((SubPlot1,SubPlot2),(SubPlot3,SubPlot4)) = plt.subplots(2,2,figsize=(15,10), constrained_layout=False, sharex='col', sharey='row') 
Figure.suptitle(f"Position of Select Particles in A Box \n Seed = {Seed}")

SubPlot1.title.set_text('Example particles from random selection box (PCG64)')
SubPlot1.hlines(1, 0, TotalEvents, color = 'black')
SubPlot1.plot(Timeaxis, PCRandParticleLocY[0],   color = 'blue', marker = 'x', linestyle = 'dotted', markersize = 1)
SubPlot1.plot(Timeaxis, PCRandParticleLocY[TotalParticles-1],   color ='red', marker = 'x', linestyle = 'dotted', markersize = 1)
SubPlot1.plot(Timeaxis, PCRandParticleLocY[int((TotalParticles-1)/2)],   color = 'orange', marker = 'x', linestyle = 'dotted', markersize = 1)

SubPlot2.title.set_text('Example particles from random selection box (SCF64)')
SubPlot2.hlines(1, 0, TotalEvents, color = 'black')
SubPlot2.plot(Timeaxis, SFRandParticleLocY[0],   color = 'blue', marker = 'x', linestyle = 'dotted', markersize = 1)
SubPlot2.plot(Timeaxis, SFRandParticleLocY[TotalParticles-1],   color ='red', marker = 'x', linestyle = 'dotted', markersize = 1)
SubPlot2.plot(Timeaxis, SFRandParticleLocY[int((TotalParticles-1)/2)],   color = 'orange', marker = 'x', linestyle = 'dotted', markersize = 1)

SubPlot3.title.set_text('Example particles from 75/25 bias box (PCG64)')
SubPlot3.hlines(1, 0, TotalEvents, color = 'black')
SubPlot3.plot(Timeaxis, PCRandParticleLocYBox2[0],   color = 'blue', marker = 'x', linestyle = 'dotted', markersize = 1)
SubPlot3.plot(Timeaxis, PCRandParticleLocYBox2[TotalParticles-1],   color ='red', marker = 'x', linestyle = 'dotted', markersize = 1)
SubPlot3.plot(Timeaxis, PCRandParticleLocYBox2[int((TotalParticles-1)/2)],   color = 'orange', marker = 'x', linestyle = 'dotted', markersize = 1)

SubPlot4.title.set_text('Example particles from 75/25 bias box (SCF64)')
SubPlot4.hlines(1, 0, TotalEvents, color = 'black')
SubPlot4.plot(Timeaxis, SFRandParticleLocYBox2[0],   color = 'blue', marker = 'x', linestyle = 'dotted', markersize = 1)
SubPlot4.plot(Timeaxis, SFRandParticleLocYBox2[TotalParticles-1],   color ='red', marker = 'x', linestyle = 'dotted', markersize = 1)
SubPlot4.plot(Timeaxis, SFRandParticleLocYBox2[int((TotalParticles-1)/2)],   color = 'orange', marker = 'x', linestyle = 'dotted', markersize = 1)

SubPlot1.set_ylabel('Particle Postion')
SubPlot3.set_ylabel('Particle Postion')

SubPlot3.set_xlabel('TimeStep')
SubPlot4.set_xlabel('TimeStep')

SubPlot1.grid(b=True, which='both', linestyle='-', linewidth='0.5')
SubPlot2.grid(b=True, which='both', linestyle='-', linewidth='0.5')
SubPlot3.grid(b=True, which='both', linestyle='-', linewidth='0.5')
SubPlot4.grid(b=True, which='both', linestyle='-', linewidth='0.5')

plt.show()


#These arrays and following loop will count how many particles are in their respective starting partition
#Box 1 corresponds to the starting Box
PCRandBox1Count = np.zeros(len(Timeaxis)) 
SFRandBox1Count = np.zeros(len(Timeaxis)) 
PCRandBox1Count75 = np.zeros(len(Timeaxis)) 
SFRandBox1Count75 = np.zeros(len(Timeaxis)) 

for i in range(0,len(Timeaxis)):
    PCRandBox1Count[i] = len(np.where(PCRandParticleLocY[:,i] < 1)[0])
    SFRandBox1Count[i] = len(np.where(SFRandParticleLocY[:,i] > 1)[0])
    PCRandBox1Count75[i] = len(np.where(PCRandParticleLocYBox2[:,i] < 1)[0])
    SFRandBox1Count75[i] = len(np.where(SFRandParticleLocYBox2[:,i] > 1)[0])
   

#The data is plotted
Figure, ((SubPlot1,SubPlot2),(SubPlot3,SubPlot4)) = plt.subplots(2,2,figsize=(15,10), constrained_layout=False, sharex='col', sharey='row') 
Figure.suptitle(f"Particles In A Box \n Seed = {Seed}")

SubPlot1.plot(Timeaxis,PCRandBox1Count, label = 'Starting Parition')
SubPlot1.plot(Timeaxis,(1000 - PCRandBox1Count), label = 'Other Parition')

SubPlot2.plot(Timeaxis,SFRandBox1Count, label = 'Starting Parition')
SubPlot2.plot(Timeaxis,(1000 - SFRandBox1Count), label = 'Other Parition')

SubPlot3.plot(Timeaxis,PCRandBox1Count75, label = 'Starting Parition')
SubPlot3.plot(Timeaxis,(1000 - PCRandBox1Count75), label = 'Other Parition')
SubPlot3.hlines(750, 0, TotalEvents, color = 'black', linestyle="dotted")
SubPlot3.hlines(250, 0, TotalEvents, color = 'red', linestyle="dotted")

SubPlot4.plot(Timeaxis,SFRandBox1Count75, label = 'Starting Parition')
SubPlot4.plot(Timeaxis,(1000 - SFRandBox1Count75), label = 'Other Parition')
SubPlot4.hlines(750, 0, TotalEvents, color = 'black', linestyle="dotted")
SubPlot4.hlines(250, 0, TotalEvents, color = 'red', linestyle="dotted")

SubPlot1.set_ylabel('Number of Particles')
SubPlot3.set_ylabel('Number of Particles')

SubPlot3.set_xlabel('TimeStep')
SubPlot4.set_xlabel('TimeStep')

SubPlot1.grid(b=True, which='both', linestyle='-', linewidth='0.5')
SubPlot2.grid(b=True, which='both', linestyle='-', linewidth='0.5')
SubPlot3.grid(b=True, which='both', linestyle='-', linewidth='0.5')
SubPlot4.grid(b=True, which='both', linestyle='-', linewidth='0.5')


SubPlot1.legend(loc = 'upper right', fontsize = '10')
SubPlot2.legend(loc = 'upper right', fontsize = '10')
SubPlot3.legend(loc = 'upper right', fontsize = '10')
SubPlot4.legend(loc = 'upper right', fontsize = '10')

plt.show()
