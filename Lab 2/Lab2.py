import numpy as np
import IntegralFunctions as IF

def TwoA(DataIn):
    return 2

def TwoB(DataIn):
    x = DataIn[0]
    return -1 * x

def TwoC(DataIn):
    x = DataIn[0]
    return x**2

def TwoD(DataIn):

    x = DataIn[0]
    y = DataIn[1]

    return x*y + y

def FiveA(DataIn):
    x = DataIn[0]
    return 2*np.exp((-x**2))

def FiveAWeight(DataIn):
     x = DataIn[0]
     return np.exp(-abs(x)) 

def FiveB(DataIn):
    x = DataIn[0]
    return (1.5 * np.sin(x))

def FiveBWeight(DataIn):
     x = DataIn[0]
     return ((4 / np.pi**2) * x * (np.pi - x))   

def nDcube(DataIn):    
    return DataIn


def nineDIntegral(DataIn):
    ReshData = IF.reshape(DataIn,[3,3])
    
    Add = list(range(len(ReshData)))
    Output = list(range(len(ReshData)))

    for i in range(len(ReshData)):
          Add[i] = ReshData[0][i] + ReshData[1][i]  
    
    for i in range(len(ReshData)):
          Output[i] = 1 / abs(sum(Add[i] * ReshData[2][i]))
              
    return Output



def main():
    NoSamples = 10000
    delta = 0.1
    
    Two1 = IF.MCIntegrator(NoSamples,TwoA,1)
    Two2 = IF.MCIntegrator(NoSamples,TwoB,1)
    Two3 = IF.MCIntegrator(NoSamples,TwoC,1)
    Two4 = IF.MCIntegrator(NoSamples,TwoD,2)
    
    Three1A = IF.MCIntegrator(NoSamples,nDcube,2)
    Three1B = IF.nBallVolume(Three1A[0],Three1A[1])

    Three2A = IF.MCIntegrator(NoSamples,nDcube,3)
    Three2B = IF.nBallVolume(Three2A[0],Three2A[1])
    
    Four1 = IF.MCIntegrator(NoSamples,nineDIntegral,9)
    
    Five1 = IF.MCISIntegrator(delta,NoSamples,FiveA,FiveAWeight,1)
    Five2 = IF.MCISIntegrator(delta,NoSamples,FiveB,FiveBWeight,1)
    
    Six1 = IF.MCIntegrator(NoSamples,FiveA,1)
    Six2 = IF.MCIntegrator(NoSamples,FiveB,1)
    
    
    return


if __name__ == '__main__':
    main()