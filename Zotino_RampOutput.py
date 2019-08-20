from artiq.experiment import *                                  #imports everything from experiment library

#This code outputs a ramp wave on a single channel of the zotino 
#The wave ramps from -10v to 10v with a frequency of 1.28kHz

class Zotino_Ramp_Generator(EnvExperiment):
    """Zotino: Ramp Generator"""
    def build(self): #this code runs from the host device

        self.setattr_device("core")                             #adds drivers for core device as attributes
        self.setattr_device("zotino0")                          #adds drivers for zotino board as attributes

    @kernel #this code runs on the FPGA
    def run(self):
        self.core.reset()                                       #resets core device
        n_steps = 100                                           #defines number of steps ramp will be broken into
        voltages_mu = [((1<<16)//n_steps)*i                     #defines voltage ramp in machine units, 0.2V steps from -10V to 10V
            for i in range(n_steps)]
    
        
        self.core.break_realtime()                              #moves timestamp forward to prevent underflow
                                                                #this can also be achieved with a fixed delay
                                                                
        self.zotino0.init()                                     #initialises zotino
        delay(200*us)                                           #200us delay, to prevent underflow

        while(1):                                               #loops until manually broken(from bash terminal, this requires closing terminal)
            for voltage in voltages_mu:                         #loops over all voltages in voltages_mu list
                    
                self.zotino0.write_dac_mu(0, voltage)           #writes voltage in machine units to output channel buffer register for v
                self.zotino0.load()                             #loads buffer to DAC channel
                
                delay(7*us)                                     #7us delay
                                                                #for 1 channel, 800ns delay prevents underflow but for voltage to reach level, 7us delay is needed