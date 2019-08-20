from artiq.experiment import *                  #imports everything from artiq experiment library

#minimum working code for using TTL6
#turns output on, off, and then pulses it

#to view the trace from this on a scope, use a single trigger with at least 16ms measured on scope

class TTL_Output_On_Off_Pulse(EnvExperiment):
    """TTL Output On, Off, Pulse"""
    def build(self): #This code rus on host device     

        self.setattr_device("core")             #sets core device drivers as attributes
        self.setattr_device("ttl6")             #sets ttl6 device drivers as attributes
        
    @kernel #this code runs on the FPGA
    def run(self):
    
        self.core.reset()                       #resets core device
        self.ttl6.output()                      #sets TTL6 as an output
        
        self.core.break_realtime()              #moves timestamp forward to prevent underflow
                                                #this can also be achieved with a fixed delay
                                                
        self.ttl6.on()                          #sets TTL6 output to high
        delay(5*ms)                             #5ms delay
        
        self.ttl6.off()                         #sets TTL6 output to low
        delay(5*ms)                             #5ms delay
        
        self.ttl6.pulse(5*ms)                   #sets TTL6 output high for 5ms then sets it to low
        delay(1*ms)                             #1ms delay