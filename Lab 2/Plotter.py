import numpy as np
import matplotlib.pyplot as plt
import Lab2 as LB2
import os

#A function that performs calculations relevant to the Freedman–Diaconis rule, which is used to find the number of bins in a histogram should use for a given dataset
def FDBinFinder(RandArray):
    
    #Gets the lower and upper quartiles for the input array
    RandArray25, RandArray75 = np.percentile(RandArray, [25, 75])
    
    #The calcualtion that is the Freedman–Diaconis rule is performed
    BinWidth = 2 * (RandArray75 - RandArray25) * len(RandArray) ** (-1/3)
    
    #Calcualtes number of bins from bin width
    BinNum = round((RandArray.max() - RandArray.min()) / BinWidth)
    
    return BinNum

x5 = np.array([np.linspace(-10,10,10001),np.linspace(0,np.pi,10001)])
y5 = np.array([LB2.FiveAWeight(x5[0]),LB2.FiveBWeight(x5[1])])


path, dirs, files = next(os.walk(os.path.dirname(os.path.realpath('Plotter.py')) + '\\Metro'))
path1, dirs1, files1 = next(os.walk(os.path.dirname(os.path.realpath('Plotter.py')) + '\\DataSet150422'))
CirclePath, CircleDirs, CircleFiles = next(os.walk(os.path.dirname(os.path.realpath('Plotter.py')) + '\\circle'))



NBallSamples = np.array([100,1000,10000,100000,1000000])
NBallDims = np.array([2,3])
NBallDimCounter = (1,NBallDims+1,1)

NoSamples = np.loadtxt(open(path1 + "\\NoSamples\\NoSamples.txt", "rb"), delimiter=";")

MetroNoSamples = (NoSamples - (NoSamples * 0.1)) / 2

for i in range(len(files)):
    files[i] = files[i].rstrip(".txt")
    
for i in range(len(files1)):
    files1[i] = files1[i].rstrip(".txt")
    
for i in range(len(CircleFiles)):
    CircleFiles[i] = CircleFiles[i].rstrip(".txt")
    
for i in range(len(files)):
    vars()[files[i]] = np.loadtxt(open(path + "\\" + files[i] + ".txt", "rb"), delimiter=";")

for i in range(len(files1)):
    vars()[files1[i]] = np.loadtxt(open(path1 + "\\" + files1[i] + ".txt", "rb"), delimiter=";")
    
for i in range(len(CircleFiles)):
    vars()[CircleFiles[i]] = np.loadtxt(open(CirclePath + "\\" + CircleFiles[i] + ".txt", "rb"), delimiter=";")


BinNum = np.zeros(len(files))

for i in range(len(files)):
    BinNum[i] = FDBinFinder(vars()[files[i]])

for i in range(len(files)):
    plt.figure(i)
    plt.xlabel('Number of Samples')
    plt.ylabel('Final Value')
    plt.title(str(files[i]))
    plt.hist(vars()[files[i]], bins = int(BinNum[i]))
    
    plt.figure(i+100)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(str(files[i]) + 'function')
    plt.plot(x5[i],y5[i])


plt.figure(9999)
plt.xlabel('Arb x value')
plt.ylabel('Arb y value')
plt.title('MonteCarlo NBall for 1 million samples')
plt.scatter(vars()[CircleFiles[16]],vars()[CircleFiles[18]], color = 'red', label = 'In Ball')
plt.scatter(vars()[CircleFiles[17]],vars()[CircleFiles[19]], color = 'blue', label = 'Not In Ball')
plt.legend()

for i in range(len(files1)):
    plt.figure(i+10)
    plt.xlabel('Number of Samples')
    plt.ylabel('Final Value')
    plt.title(str(files1[i]))
    
    #If statment checks for question five, this is because the metropolis algothim is used which mens there are less samples used in the integrator
    if "Five" in str(files1[i]):
        plt.semilogx(MetroNoSamples,vars()[files1[i]])
    else:
        plt.semilogx(NoSamples,vars()[files1[i]])


