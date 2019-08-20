from artiq.experiment import*                   #imports everything from artiq experiment library

#example code for using with parallel and with sequential

class LED_Parallel(EnvExperiment):
    """LED Parallel"""
    def build(self): #Adds the device drivers as attributes and adds the keys to the kernel invarients
    
        self.setattr_device("core")             #required in all builds   
        self.setattr_device("led0")             #required for using led0
        self.setattr_device("led1")             #required for using led1

        
        
    @kernel #this code is run on the FPGA
    def run(self):
    
        self.core.reset()                       #resets core device
        
        self.core.break_realtime()              #moves timestamp forward to prevent underflow
                                                #this can also be achieved with a fixed delay

        with parallel:                          #instructs core device to run contained code in parallel
        
            self.led0.pulse(4*s)                #led0 turns on for 5s then turns off
            
            with sequential:                    #instructs core device to run contained code sequentially 
            
                self.led1.pulse(2*s)            #led1 turns on for 2s then turns off
                delay(2*s)                      #2s delay