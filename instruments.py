import vxi11
 
class DS1000Z(vxi11.Instrument):
    def __init__(self, host, *args, **kwargs):
        super(DS1000Z, self).__init__(host, *args, **kwargs)
    def get_identification(self):
        return self.ask("*IDN?")
    def stop(self):
        self.write(':STOP')

    def autoscale(self):
        self.write(':AUT')
    
    def clear(self):
        self.write(':CLE')
    
    def run(self):
        self.write(':RUN')
        
    def stop(self):
        self.write(':STOP')
    
    def single(self):
        self.write(':SING')
    
    
    

    '''ACQUIRE COMMANDS '''
    def acquire_averages_get(self):
        return self.ask(':ACQ:AVER?')
    
    def acquire_depth_get(self):
        return self.ask(':ACQ:MDEP?')
        
    def acquire_depth_set(self,num):
        self.write(':ACQ:MDEP '+ str(int(num)))
        
    def acquire_type_get(self):
        return self.ask(':ACQ:TYPE?')
    #NORMal, AVERages, PEAK, HRESolution
    def acquire_type_set(self,mode):
        self.write(':ACQ:TYPE '+str(mode))
        
    def acquire_srate_get(self):
        return float(self.ask(':ACQ:SRATe?'))


        
    def channel_coupling_get(self,channel):
        return self.write(':CHAN' + channel + ':COUP?')

    def channel_coupling_set(self,channel):
        return self.write(':CHAN' + channel + ':COUP?')
        
    def channel_display_get(self,channel):
        return self.write(':CHAN'+str(channel)+':DISP?')
#        
    def channel_display_on(self,channel):
        self.write(':CHAN'+str(channel)+':DISP ON')  
        
    def channel_display_off(self,channel):
        self.write(':CHAN'+str(channel)+':DISP OFF') 

    #get the channel scale
    def chan_scale_get(self, channel):
        return self.ask(':CHAN'+channel+':SCAL?')

    def time_scale_get(self):
        return self.ask(':TIM:MAIN:SCALE?')

    def trigger_status(self):
        return self.ask(':TRIG:STAT?')



    '''DISPLAY COMMANDS'''
    #get the channel scale
    def display_data_get(self):
        return self.ask(':DISP:DATA?')
        
    def wave_mode_set(self,chan):
        self.write(':WAV:MODE '+str(chan))
        
    def wave_mode_get(self):
        return self.ask('WAV:MODE?')

    def wave_format_set(self, frmt):
        self.write(':WAV:FORM '+str(frmt))
        
    def wave_format_get(self):
        return self.ask('WAV:FORM?')

        

    def wave_source_set(self,chan):
        self.write(':WAV:SOUR CHAN'+str(chan))
        
    def wave_source_get(self):
        return self.ask('WAV:SOUR?')     
        
    def wave_start_point(self,num):
        self.write(':WAV:STAR '+str(num))
        
    def wave_stop_point(self,num):
        self.write(':WAV:STOP '+str(num))        
#     def autoscale(self):
#         self.write(':AUT')

# scope.write(':WAV:FORM '+ 'ASC') #set form to ascii
# #set the mode
# scope.write(':WAV:MODE '+ 'RAW')
# #we need to initialize the channels before setting the memory depth
# #otherwise if someone has on all 4 channels, but we want to sample 1 channel
# #very high, the scope will limit our memory depth because it thinks we're using 
# # more than 1 channel
# scope.write(':CHAN1'+':DISP ON')
# #to adjust the # of points recorded (depth) we need to have the scope in
# #   Run mode and then change the depth
# scope.write(':RUN')
# #set the memory depth
# scope.write(':ACQ:MDEP '+ str(1200000))
# scope.write(':STOP')   #stop scope
# #set the termination
# scope.read_termination='\n'