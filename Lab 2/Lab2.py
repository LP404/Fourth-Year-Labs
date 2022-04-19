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
    
    return (np.exp(-abs(x))) 

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
    # #Creates a pesudo log spaced NoSamples
    Order = np.logspace(1, 7, 7)
    #BaseNo = np.array([1,2.5,5,7.5])
    BaseNo = np.arange(1,10,1)
    NoSamples = np.outer(Order,BaseNo).flatten()
    
    #Converts all the values in NoSamples to integers if they are not already
    NoSamples = NoSamples.astype(int)
    
    delta = 0.2
    
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
    
    initGuess1 = np.array([1])
    initGuess2 = np.array([1])
    
    

    # NoSamplestxt = open('NoSamples.txt','w')
    # Two1Txt = open('Two1.txt' , 'w')
    # Two2Txt = open('Two2.txt' , 'w')
    # Two3Txt = open('Two3.txt' , 'w')
    # Two4Txt = open('Two4.txt' , 'w')
    # Three1BTxt = open('Three1B.txt' , 'w') 
    # Three2BTxt = open('Three2B.txt' , 'w')
    # Three3BTxt = open('Three3B.txt' , 'w')
    # Four1Txt = open('Four1.txt' , 'w')
    Five1Txt = open('Five1.txt' , 'w')
    Five2Txt = open('Five2.txt' , 'w')
    # Six1Txt = open('Six1.txt' , 'w')
    # Six2Txt = open('Six2.txt' , 'w')

    # Two2ErrorTxt = open('Two2Error.txt' , 'w') 
    # Two3ErrorTxt = open('Two3Error.txt' , 'w')
    # Two4ErrorTxt = open('Two4Error.txt' , 'w')
    # Four1ErrorTxt = open('Four1Error.txt' , 'w')
    Five1ErrorTxt = open('Five1Error.txt' , 'w')
    Five2ErrorTxt = open('Five2Error.txt' , 'w')
    # Six1ErrorTxt = open('Six1Error.txt' , 'w')
    # Six2ErrorTxt = open('Six2Error.txt' , 'w')
    
    for i in range(len(NoSamples)):   
        
        print(NoSamples[i])
        # Two1 = IF.MCIntegrator(NoSamples[i],TwoA,1,Lim1,False)
        # Two2 = IF.MCIntegrator(NoSamples[i],TwoB,1,Lim2,False)
        # Two3 = IF.MCIntegrator(NoSamples[i],TwoC,1,Lim3,False)
        # Two4 = IF.MCIntegrator(NoSamples[i],TwoD,2,Lim4,False)
        
        
        # Three1A = IF.MCIntegrator(NoSamples[i],nDcube,2,Lim5,True)
        # Three1B = IF.nBallVolume(Three1A[1],Three1A[0],2,NoSamples[i])
        
        # Three2A = IF.MCIntegrator(NoSamples[i],nDcube,3,Lim6,True)
        # Three2B = IF.nBallVolume(Three2A[1],Three2A[0],3,NoSamples[i])
        
        # Three3A = IF.MCIntegrator(NoSamples[i],nDcube,5,Lim7,True)
        # Three3B = IF.nBallVolume(Three3A[1],Three3A[0],5,NoSamples[i])
        
         
        
        
        # Four1 = IF.MCIntegrator(NoSamples[i],nineDIntegral,9,Lim8,False)
        
        Five1 = IF.MCISIntegrator(delta,initGuess1,NoSamples[i],FiveA,FiveAWeight,1,Lim9,False)
        Five2 = IF.MCISIntegrator(delta,initGuess2,NoSamples[i],FiveB,FiveBWeight,1,Lim10,False)
        
        
        
        # Six1 = IF.MCIntegrator(NoSamples[i],FiveA,1,Lim11,False)
        # Six2 = IF.MCIntegrator(NoSamples[i],FiveB,1,Lim12,False)
    
    
        # Two1Store = Two1
        # Two2Store = Two2[2]
        # Two3Store = Two3[2]
        # Two4Store = Two4[2]
        # Three1BStore = Three1B[1]
        # Three2BStore = Three2B[1]
        # Three3BStore = Three3B[1]
        # Four1Store = Four1[2]
        Five1Store = Five1[2]
        Five2Store = Five2[2]
        # Six1Store = Six1[2]
        # Six2Store = Six2[2]
    
        # Two2StoreError = Two2[3] 
        # Two3StoreError = Two3[3] 
        # Two4StoreError = Two4[3] 
        # Four1StoreError = Four1[3] 
        Five1StoreError = Five1[3] 
        Five2StoreError = Five2[3]
        # Six1StoreError = Six1[3]
        # Six2StoreError = Six2[3]
        

        
    #Writes the data the TXTs
        #Checks for if it the last append, if so  will not add a semicolon at the end. Semicolon is needed as a delimiter
        if i == (len(NoSamples) - 1):
            pass
            
            # NoSamplestxt.write(f"{NoSamples[i]}")
            # Two1Txt.write(f"{Two1Store}")
            # Two2Txt.write(f"{Two2Store}")
            # Two3Txt.write(f"{Two3Store}")
            # Two4Txt.write(f"{Two4Store}")
            # Three1BTxt.write(f"{Three1BStore}") 
            # Three2BTxt.write(f"{Three2BStore}") 
            # Three3BTxt.write(f"{Three3BStore}") 
            # Four1Txt.write(f"{Four1Store}")
            Five1Txt.write(f"{Five1Store}")
            Five2Txt.write(f"{Five2Store}") 
            # Six1Txt.write(f"{Six1Store}")
            # Six2Txt.write(f"{Six2Store}")
        
            # Two2ErrorTxt.write(f"{Two2StoreError}")
            # Two3ErrorTxt.write(f"{Two3StoreError}") 
            # Two4ErrorTxt.write(f"{Two4StoreError}")
            # Four1ErrorTxt.write(f"{Four1StoreError}")
            Five1ErrorTxt.write( f"{Five1StoreError}")
            Five2ErrorTxt.write(f"{Five2StoreError}")
            # Six1ErrorTxt.write(f"{Six1StoreError}") 
            # Six2ErrorTxt.write(f"{Six2StoreError}")
        
        else:
            pass
            # NoSamplestxt.write(f"{NoSamples[i]};")
            # Two1Txt.write(f"{Two1Store};")
            # Two2Txt.write(f"{Two2Store};")
            # Two3Txt.write(f"{Two3Store};")
            # Two4Txt.write(f"{Two4Store};")
            # Three1BTxt.write(f"{Three1BStore};") 
            # Three2BTxt.write(f"{Three2BStore};") 
            # Three3BTxt.write(f"{Three3BStore};") 
            # Four1Txt.write(f"{Four1Store};")
            Five1Txt.write(f"{Five1Store};")
            Five2Txt.write(f"{Five2Store};") 
            # Six1Txt.write(f"{Six1Store};")
            # Six2Txt.write(f"{Six2Store};")
        
            # Two2ErrorTxt.write(f"{Two2StoreError};")
            # Two3ErrorTxt.write(f"{Two3StoreError};") 
            # Two4ErrorTxt.write(f"{Two4StoreError};")
            # Four1ErrorTxt.write(f"{Four1StoreError};")
            Five1ErrorTxt.write( f"{Five1StoreError};")
            Five2ErrorTxt.write(f"{Five2StoreError};")
            # Six1ErrorTxt.write(f"{Six1StoreError};") 
            # Six2ErrorTxt.write(f"{Six2StoreError};")
            
      
     
    # NoSamplestxt.close()
    # Two1Txt.close()
    # Two2Txt.close()
    # Two3Txt.close()
    # Two4Txt.close()
    # Three1BTxt.close() 
    # Three2BTxt.close() 
    # Three3BTxt.close()
    # Four1Txt.close()
    Five1Txt.close()
    Five2Txt.close()
    # Six1Txt.close()
    # Six2Txt.close()

    # Two2ErrorTxt.close()
    # Two3ErrorTxt.close()
    # Two4ErrorTxt.close()
    # Four1ErrorTxt.close()
    Five1ErrorTxt.close() 
    Five2ErrorTxt.close()
    # Six1ErrorTxt.close()
    # Six2ErrorTxt.close()             

    return


if __name__ == '__main__':
    main()