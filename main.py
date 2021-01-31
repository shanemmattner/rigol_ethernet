from instruments import DS1000Z
import numpy as np

 
def main():
    instrument = DS1000Z('169.254.145.221')
    print(instrument.get_identification())
    instrument.stop()

    # Grab the data from channel 1
    instrument.write(":WAV:POIN:MODE NOR")
    
    instrument.write(":WAV:DATA? CHAN1")
    rawdata = instrument.read(9000)
    print(str(rawdata))
    data = np.frombuffer(rawdata, 'B')
    
 
 
if __name__ == "__main__":
    main()
