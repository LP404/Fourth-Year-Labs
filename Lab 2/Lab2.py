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

#The metropolis alrotithim necessistaes the inclusion of the if statment
#This is because the metropolis algorithim was developed a little while after the MC Integrator and it does not use a list to store the dimentions
#I know it's a little janky but this is my solution to the problem
def FiveAWeight(DataIn):
    if type(DataIn) == list:
        x = DataIn[0]
    else:
        x = DataIn
    
    return np.exp(-abs(x)) 

def FiveB(DataIn):
    x = DataIn[0]
    return (1.5 * np.sin(x))

def FiveBWeight(DataIn):
    if type(DataIn) == list:
        x = DataIn[0]
    else:
        x = DataIn
        
    return ((4 / np.pi**2) * x * (np.pi - x))   

def nDcube(DataIn):    
    return DataIn


def nineDIntegral(DataIn):
    a = np.array([DataIn[0],DataIn[1],DataIn[2]])
    b = np.array([DataIn[3],DataIn[4],DataIn[5]])
    c = np.array([DataIn[6],DataIn[7],DataIn[8]])
    
    d = a + b
    
    PHolder0 = d[0] * c[0]
    PHolder1 = d[1] * c[1]
    PHolder2 = d[2] * c[2]
    
    DotPro = PHolder0 + PHolder1 + PHolder2

    return 1 / DotPro



def main():
    NoSamples = np.arange(100,1005000,5000)
    delta = 0.1
    
    Lim1 = [[0,1]]
    Lim2 = [[0,1]]
    Lim3 = [[-2,2]]
    Lim4 = [[0,1],[0,1]]
    
    Lim5 = [[-2,2],[-2,2]]
    Lim6 = [[-2,2],[-2,2],[-2,2]]
    Lim7 = [[-2,2],[-2,2],[-2,2],[-2,2],[-2,2]]
    
    Lim8 = [[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1]]
    
    Lim9 = [[-10,10]]
    Lim10 = [[0,np.pi]]
    
    Lim11 = [[-10,10]]
    Lim12 = [[0,np.pi]]
    
    initGuess1 = np.array([3])
    initGuess2 = np.array([3])
    
    
    
    Two1Store = np.zeros(len(NoSamples))
    Two2Store = np.zeros(len(NoSamples))
    Two3Store = np.zeros(len(NoSamples))
    Two4Store = np.zeros(len(NoSamples))
    
    Three1BStore = np.zeros(len(NoSamples))
    Three2BStore = np.zeros(len(NoSamples))
    Three3BStore = np.zeros(len(NoSamples))
     
    Four1Store = np.zeros(len(NoSamples))
    
    Five1Store = np.zeros(len(NoSamples))
    Five2Store = np.zeros(len(NoSamples))
    
    Six1Store = np.zeros(len(NoSamples))
    Six2Store = np.zeros(len(NoSamples))
    
    Two2StoreError = np.zeros(len(NoSamples))
    Two3StoreError = np.zeros(len(NoSamples))
    Two4StoreError = np.zeros(len(NoSamples))
         
    Four1StoreError = np.zeros(len(NoSamples))
    
    Five1StoreError = np.zeros(len(NoSamples))
    Five2StoreError = np.zeros(len(NoSamples))
    
    Six1StoreError = np.zeros(len(NoSamples))
    Six2StoreError = np.zeros(len(NoSamples))

    out = open('Values.txt' , 'w')
    out1 = open('Errors.txt' , 'w')
    for i in range(len(NoSamples)):   
        
        print(NoSamples[i])
        Two1 = IF.MCIntegrator(NoSamples[i],TwoA,1,Lim1,False)
        Two2 = IF.MCIntegrator(NoSamples[i],TwoB,1,Lim2,False)
        Two3 = IF.MCIntegrator(NoSamples[i],TwoC,1,Lim3,False)
        Two4 = IF.MCIntegrator(NoSamples[i],TwoD,2,Lim4,False)
        
        
        Three1A = IF.MCIntegrator(NoSamples[i],nDcube,2,Lim5,True)
        Three1B = IF.nBallVolume(Three1A[0],Three1A[1],2)
        
        Three2A = IF.MCIntegrator(NoSamples[i],nDcube,3,Lim6,True)
        Three2B = IF.nBallVolume(Three2A[0],Three2A[1],3)
        
        Three3A = IF.MCIntegrator(NoSamples[i],nDcube,5,Lim7,True)
        Three3B = IF.nBallVolume(Three3A[0],Three3A[1],5)
        
         
        
        
        Four1 = IF.MCIntegrator(NoSamples[i],nineDIntegral,9,Lim8,False)
        
        Five1 = IF.MCISIntegrator(delta,initGuess1,NoSamples[i],FiveA,FiveAWeight,1,Lim9,False)
        Five2 = IF.MCISIntegrator(delta,initGuess2,NoSamples[i],FiveB,FiveBWeight,1,Lim10,False)
        
        
        
        Six1 = IF.MCIntegrator(NoSamples[i],FiveA,1,Lim11,False)
        Six2 = IF.MCIntegrator(NoSamples[i],FiveB,1,Lim12,False)
    
    
        Two1Store[i] = Two1
        Two2Store[i] = Two2[2]
        Two3Store[i] = Two3[2]
        Two4Store[i] = Two4[2]
        Three1BStore[i] = Three1B[1]
        Three2BStore[i] = Three2B[1]
        Three3BStore[i] = Three3B[1]
        Four1Store[i] = Four1[2]
        Five1Store[i] = Five1[2]
        Five2Store[i] = Five2[2]
        Six1Store[i] = Six1[2]
        Six2Store[i] = Six2[2]
    
        Two2StoreError[i] = Two2[3] 
        Two3StoreError[i] = Two3[3] 
        Two4StoreError[i] = Two4[3] 
        Four1StoreError[i] = Four1[3] 
        Five1StoreError[i] = Five1[3] 
        Five2StoreError[i] = Five2[3]
        Six1StoreError[i] = Six1[3]
        Six2StoreError[i] = Six2[3]
        
    out.write(f"{NoSamples} {Two1Store} {Two2Store} {Two3Store} {Two4Store} {Three1BStore} {Three2BStore} {Three3BStore} {Four1Store} {Five1Store} {Five2Store} {Six1Store} {Six2Store}")           
    out1.write(f"{Two2StoreError} {Two3StoreError} {Two4StoreError} {Four1StoreError} {Five1StoreError} {Five2StoreError} {Six1StoreError} {Six2StoreError}")
    out.close()
    out1.close()
    return


if __name__ == '__main__':
    main()