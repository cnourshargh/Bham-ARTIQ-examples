from artiq.experiment import *                  #imports everything from artiq experiment library

#This code takes a single read from TTL0 and prints the voltage 

class TTL_Input_Read(EnvExperiment):
    """TTL Input Read"""
    def build(self): #This code runs on the host device

        self.setattr_device("core")             #sets drivers for core device as attributes
        self.setattr_device("ttl0")             #sets drivers for TTL0 as attributes
        
    @kernel #this code runs on the FPGA
    def run(self):                              
        self.core.reset()                       #resets core device
        
        self.ttl0.input()                       #sets TTL0 as an input
        
        self.core.break_realtime()              #moves timestamp forward to prevent underflow
                                                #this can also be achieved with a fixed delay
        
        self.ttl0.sample_input()                #reads current value of TTL0 
        input = self.ttl0.sample_get()          #stores value of TTL0 as input varibale
        print(input)                            #prints value of input variable