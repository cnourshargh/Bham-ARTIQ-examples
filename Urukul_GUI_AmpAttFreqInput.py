from artiq.experiment import*                                   #imports everything from the artiq experiment library

#This code outputs a single frequency at a fixed amplitude on a single channel of the urukul
#the output frequency must be inputted in MHz from the dahsboard
#The ouput persists for 2 seconds and the turns off

class tutorial_urukulFreqScan(EnvExperiment):
    """Urukul Selectable Frequency, Amplitude, Attenuation and Pulse Length"""
    def build(self): #This code runs on the host device
        

        print(self.setattr_device("core"))                                  #sets core device drivers as attributes
        self.setattr_device("urukul0_ch1")                                  #sets urukul0, channel 1 device drivers as attributes
        self.setattr_argument("freq", NumberValue(ndecimals=0, unit="MHz", step=1))     #instructs dashboard to take input and set it as an attribute called freq
        self.setattr_argument("amp", NumberValue(ndecimals=2, step=1))     #instructs dashboard to take input and set it as an attribute called freq
        self.setattr_argument("atten", NumberValue(ndecimals=0, step=1))     #instructs dashboard to take input and set it as an attribute called freq
        self.setattr_argument("t_pulse", NumberValue(ndecimals=0, unit = "s" step=1))     #instructs dashboard to take input and set it as an attribute called freq
        
    
    @kernel #This code runs on the FPGA
    def run(self):  
        self.core.reset()                                       #resets core device
        self.urukul0_ch1.cpld.init()                            #initialises CPLD on channel 1
        self.urukul0_ch1.init()                                 #initialises channel 1
        delay(10 * ms)                                          #10ms delay
        
        #amp = 1.0                                               #defines amplitude variable as an amplitude scale factor(0 to 1)
        #attenuation= 1.0                                        #defines attenuation variable
        
        self.urukul0_ch1.set_att(self.atten)                   #writes attenuation to urukul channel
        self.urukul0_ch1.sw.on()                                #switches urukul channel on
           
            
        self.urukul0_ch1.set(self.freq * MHz, amplitude = self.amp)  #writes frequency and amplitude variables to urukul channel thus outputting function
        delay(self.t_pulse)                                              #2s delay
        self.urukul0_ch1.sw.off()                               #switches urukul channel off