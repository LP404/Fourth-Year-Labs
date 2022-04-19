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

path, dirs, files = next(os.walk(os.path.dirname(os.path.realpath('Plotter.py')) + '\\Metro'))

path1, dirs1, files1 = next(os.walk(os.path.dirname(os.path.realpath('Plotter.py')) + '\\DataSet150422'))

CirclePath, CircleDirs, CircleFiles = next(os.walk(os.path.dirname(os.path.realpath('Plotter.py')) + '\\circle'))
SpherePath, SphereDirs, SphereFiles = next(os.walk(os.path.dirname(os.path.realpath('Plotter.py')) + '\\sphere'))
HyperspherePath, HypersphereDirs, HypersphereFiles = next(os.walk(os.path.dirname(os.path.realpath('Plotter.py')) + '\\hypersphere'))
NBallSampls = np.array([100,1000,10000,100000,1000000])
NBallDims = np.array([2,3,5])
NBallDimCounter = (1,NBallDims+1,1)

for i in range(len(files)):
    files[i] = files[i].rstrip(".txt")

for i in range(len(files)):
    vars()[files[i]] = np.loadtxt(open(path + "/" + files[i] + ".txt", "rb"), delimiter=";")

BinNum = np.zeros(len(files))

for i in range(len(files)):
    BinNum[i] = FDBinFinder(vars()[files[i]])

for i in range(len(files)):
    plt.figure(i)
    plt.xlabel('Number of Samples')
    plt.ylabel('Final Value')
    plt.title(str(files[i]))
    plt.hist(vars()[files[i]], bins = int(BinNum[i]))


NoSamples = np.loadtxt(open(path + "\\NoSamples\\NoSamples.txt", "rb"), delimiter=";")

# for i in range(len(files)):
#     plt.figure(i)
#     plt.xlabel('Number of Samples')
#     plt.ylabel('Final Value')
#     plt.title(str(files[i]))
    
#     #If statment checks for question five, this is because the metropolis algothim is used which mens there are less samples used in the integrator
#     if "Five" in str(files[i]):
#         plt.semilogx(((NoSamples - (NoSamples * 0.1)) / 2),vars()[files[i]])
#     else:
#         plt.semilogx(NoSamples,vars()[files[i]])


