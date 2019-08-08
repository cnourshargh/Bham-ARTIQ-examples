from artiq.experiment import *                  #imports everything from artiq experiment library

#This code outputs a single voltage on a single Zotino channel

class ZotinoOutputs(EnvExperiment):
    """Zotino Single Output"""
    def build(self): #this code runs on the host device

        self.setattr_device("core")             #adds drivers for core device as attributes
        self.setattr_device("zotino0")          #adds drivers for zotino board as attributes

    @kernel #this code runs on the FPGA
    def run(self): 
    
        self.core.reset()                       #resets core device      
        self.core.break_realtime()              #moves timestamp forward to prevent underflow
                                                #this can also be achieved with a fixed delay    
        
        voltage = 9                             #defines voltage variable in Volts
        
        self.zotino0.init()                     #initialises zotino0
        delay(200*us)                           #200us delay, needed to prevent underflow on initialisation
        
        self.zotino0.write_dac(0,voltage)       #writes voltage variable to DAC, channel 0
        self.zotino0.load()                     #outputs previously loaded voltage
        