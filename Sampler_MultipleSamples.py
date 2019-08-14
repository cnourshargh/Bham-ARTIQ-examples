from artiq.experiment import *                      #imports everything from experiment library
import numpy as np

#This code takes a single sample from all 8 sampler channels simultaneously 

class KasliTester(EnvExperiment):
    """Sampler Multiple Samples"""
    def build(self): #this code runs on the host device

        self.setattr_device("core")                 #saves core device drivers as attributes
        self.setattr_device("sampler0")             #saves sampler device drivers as attributes
        
    
    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()      #Time break to avoid underflow condition
        self.sampler0.init()                  #initialises sampler
        self.set_dataset("samples", np.full(2000, np.nan), broadcast=True)
        n_channels = 8                  #sets number of channels to read off of
                                        #change this number to alter the nummber of channels being read from          
        self.core.break_realtime()
        for i in range(n_channels):              #loops for each sampler channel
            self.sampler0.set_gain_mu(i, 0)   #sets each channel's gain to 0db        
        smp = [0]*n_channels          #creates list of 8 floating point variables
        

        
        for n in range(2000):
                                   
            self.sampler0.sample_mu(smp)                 #runs sampler and saves to list 
            delay(70*us)                                    #shorter than 500us delays were causing underflow
            self.mutate_dataset("samples",n,smp[0])

        