from artiq.experiment import*                                   #imports everything from the artiq experiment library

#This code outputs a predefined frequency at a fixed amplitude on a single channel of the urukul
#The ouput persists for 2 seconds and the turns off

class tutorial_urukulFreqScan(EnvExperiment):
    """Urukul Single Frequency Pulse"""
    def build(self): #This code runs on the host device

        self.setattr_device("core")                             #sets core device drivers as attributes
        self.setattr_device("urukul0_ch1")                      #sets urukul0, channel 1 device drivers as attributes
        
    
    @kernel #This code runs on the FPGA
    def run(self):  
        self.core.reset()                                       #resets core device
        self.urukul0_ch1.cpld.init()                            #initialises CPLD on channel 1
        self.urukul0_ch1.init()                                 #initialises channel 1
        delay(10 * ms)                                          #10ms delay
        
        freq = 100*MHz                                          #defines frequency variable
        amp = 1.0                                               #defines amplitude variable as an amplitude scale factor(0 to 1)
        attenuation= 1.0                                        #defines attenuation variable

        
        self.urukul0_ch1.set_att(attenuation)                   #writes attenuation to urukul channel
        self.urukul0_ch1.sw.on()                                #switches urukul channel on
           
            
        self.urukul0_ch1.set(freq, amplitude = amp)             #writes frequency and amplitude variables to urukul channel thus outputting function
        delay(2*s)                                              #2s delay
        self.urukul0_ch1.sw.off()                               #switches urukul channel off