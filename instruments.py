import vxi11
import numpy as np


class DS1000Z(vxi11.Instrument):
    def __init__(self, host, *args, **kwargs):
        super(DS1000Z, self).__init__(host, *args, **kwargs)
    def get_identification(self):
        return self.ask("*IDN?")
    def stop(self):
        self.write(':STOP')
    def get_data(self):
        self.write('WAV:POIN:MODE NOR')
        self.write(':WAV:DATA? CHAN1')
        raw = self.read()
        data = np.frombuffer(rawdata, 'B')
        return data
