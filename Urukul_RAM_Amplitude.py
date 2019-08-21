from artiq.experiment import *                                              #Imports everything from experiment library
from artiq.coredevice.ad9910 import (                                       #Imports RAM destination amplitude scale factor and RAM mode bidirectional ramp methods from AD9910 Source
    RAM_DEST_ASF, RAM_MODE_BIDIR_RAMP)

#This code demonstrates use of the urukul RAM. It produces a 125MHz pulse that ramps up in amplitude, holds a fixed amplitude and then ramps back down
    
class AD9910RAM(EnvExperiment):
    '''Urukul RAM Amplitude Ramp'''
    def build(self): #this code runs on the host computer
        self.setattr_device("core")                                         #sets core device drivers as attributes
        self.setattr_device("ttl6")                                         #sets ttl channel 6 device drivers as attributes
        self.u = self.get_device("urukul0_ch1")                             #sets urukul 0, channel 1 device drivers as attributes and renames object self.u 

    @kernel #this code runs on the FPGA
    def run(self):
    
        #produce data to be loaded to RAM
        n = 10                                                              #defines variable n for list length exponent
        data = [0]*(1 << n)                                                 #declares list as 2^n integer values
        for i in range(len(data)//2):                                       #splits list into 2 halves and defines each separately
            data[i] = i << (32 - (n - 1))                                   #first half ramps up to maximum amplitude in machine units
            data[i + len(data)//2] = 0xffff << 16                           #second half holds maximum amplitude
        
        #reset core
        self.core.reset()                                                   #resets core device
        
        #initialise
        self.u.cpld.init()                                                  #initialises CPLD
        self.u.init()                                                       #initialises urukul channel                                     
        delay(1*ms)                                                         #1ms delay 
        
        #set ram profile
        self.u.set_profile_ram(                                             #sets profile in RAM to be used 
            start=0, end=0 + len(data) - 1, step=1,                         #start/end give addresses of ends of ram data, step gives step length
            profile=0, mode=RAM_MODE_BIDIR_RAMP)                            #mode: bidirectional ramp 
        
        self.u.cpld.set_profile(0)                                          #sets CPLD profile pins  
        self.u.cpld.io_update.pulse_mu(8)                                   #I think this clocks all the CPLD registers so they take the values written to them
        delay(1*ms)                                                         #1ms delay
        
        #write to ram
        self.u.write_ram(data)                                              #writes data list to ram
        delay(10*ms)                                                        #10ms delay
        
        #write to cfr 
        self.u.set_cfr1(ram_enable=1, ram_destination=RAM_DEST_ASF)         #writes to CFR1 (control function register 1)
                                                                            #enables ram, sets ram data as amplitude scale factor
        
        #set urukuln parameters and turn channel on
        self.u.set_frequency(125*MHz)                                       #sets frequency
        self.u.cpld.io_update.pulse_mu(8)                                   #I think this clocks all the CPLD registers so they take the values written to them
        self.u.set_att(10*dB)                                               #sets attenuation
        self.u.sw.on()                                                      #turns urukul channel on
        
        self.core.break_realtime()                                          #moves timestamp forward to prevent underflow
                                                                            #this can alse be achieved with a fixed delay                         
        
        self.ttl6.output()                                                  #sets   TTL channel as an output

        self.core.break_realtime()                                          #moves timestamp forward to prevent underflow
                                                                            #this can alse be achieved with a fixed delay 
                                                                            
        while True:                                                         #loops until manually broken
            delay(1*ms)                                                     #1ms delay
            
            with parallel:                                                  #runs indented code in parallel
                self.ttl6.pulse(1*us)                                       #1us TTL pulse for triggering oscilloscope 
                self.u.cpld.set_profile(0)                                  #profile 0 tells CPLD to start ramping up
                
            delay(2*us)                                                     #2us delay
            
            with parallel:                                                  #runs indented code in parallel
                self.ttl6.pulse(1*us)                                       #1us TTL pulse 
                self.u.cpld.set_profile(1)                                  #profile 1 tells CPLD to start ramping back down
                
                