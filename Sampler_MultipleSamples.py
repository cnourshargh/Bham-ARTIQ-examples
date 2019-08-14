from artiq.experiment import *                      #imports everything from experiment library
import numpy as np                                  #imports everything from numpy library

#THis code takes 2000 samples from all 8 channels and saves the samples from channel 0 to a dataset called samples
#an applet can be written in the management system to plot the data from this dataset
#Alternatively, the H5 file can be opened using HDFview and can then be plotted

#sampling frequency = 10.1kHz

class KasliTester(EnvExperiment):
    """Sampler Multiple Samples"""
    def build(self): #this code runs on the host device

        self.setattr_device("core")                 #saves core device drivers as attributes
        self.setattr_device("sampler0")             #saves sampler device drivers as attributes
        
    
    @kernel #this code is run on the FPGA
    def run(self):
        self.core.reset()                                                               #resets core device

        self.core.break_realtime()                                                      #Time break to avoid underflow condition
        self.sampler0.init()                                                            #initialises sampler
        
        n_samples = 2000                                                                #defines number of samples to be taken
        self.set_dataset("samples", np.full(n_samples, np.nan), broadcast=True)         #creates dataset to be filled
                                                                                        #dataset name = "samples", size=n_samples, type = NaN so floating point
                                                                                        #broadcast  = true means data is sent in real time to master
        
        n_channels = 8                                                                  #sets number of channels to read off of
                                                                                        #if 1 channel is used, it is channel 7
                                                                                        #if 2 channels, channel 6 and 7 
                                                    
        self.core.break_realtime()                                                      #Time break to avoid underflow condition
        for i in range(n_channels):                                                     #loops for each sampler channel 
            self.sampler0.set_gain_mu(7-i, 0)                                           #sets each channel's gain to 0db
            
        smp = [0]*n_channels                                                            #creates list of 8 floating point variables
        

        
        for n in range(n_samples):                                                      #loops over number of samples do be taken
        
            delay(50*us)                                                                #90us delay to prevent uderflow in sampling stage                                   
            self.sampler0.sample_mu(smp)                                                #runs sampler and saves to list 
            self.mutate_dataset("samples",n,smp[0])                                     #adds 0th element of list to dataset so voltage from lowest channel being used

        