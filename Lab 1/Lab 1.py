import numpy as np
from numpy import random as nprnd
import random as rnd
import scipy as sp
import time as t



def main():
    
    TotalNum = int(input("How many random numbers would you like to generate? : "))
    
    SeedInt = int(t.time())

    nprnd.seed(SeedInt)
    rnd.seed(SeedInt)

    NumpyRand = nprnd.rand(TotalNum)
    
    PyRand = np.zeros(TotalNum)
    
    for i in range(0,TotalNum):
        
        PyRand[i] = rnd.random()
    
    
    
    return




main()