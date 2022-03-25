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


NoSamples = 10000
NoDims = 3


def main():
    
    
    
    return


if __name__ == '__main__':
    main()