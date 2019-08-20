from artiq.experiment import*                   #imports everything from artiq experiment library

#minimum working code for using led0
#turns led0 on, off, and then pulses it

class LED_On_Off_Pulse(EnvExperiment):
    """LED On, Off, Pulse"""
    def build(self): #Adds the device drivers as attributes and adds the keys to the kernel invarients
    
        self.setattr_device("core")             #required in all builds   
        self.setattr_device("led0")             #required for using led0

        
        
    @kernel #this code is run on the FPGA
    def run(self):
    
        self.core.reset()                       #resets core device
        
        self.core.break_realtime()              #moves timestamp forward to prevent underflow
                                                #this can alse be achieved with a fixed delay

        self.led0.on()                          #switches led0 on
        delay(5*s)                              #5s delay
        
        self.led0.off()                         #switches led0 off
        delay(5*s)                              #5s delay
        
        self.led0.pulse(5*s)                    #led turns on for 5s then turns off
        
        