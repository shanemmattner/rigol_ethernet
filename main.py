from instruments import DS1000Z
import numpy as np
import pandas as pd
import ds1054z_cp as dscp

#from ds1054z import DS1054Z 
def main():
    #instrument = DS1000Z('169.254.145.221')
    #print(instrument.get_identification())
    #instrument.stop()

    # Grab the data from channel 1
    #df = instrument.get_data()


    scope = dscp.DS1054Z('169.254.145.221')
    print("Connected to: ", scope.idn)

    print("currently displayed channels: ", str(scope.displayed_channels))

    t_test = scope.get_waveform_samples('CHAN1')
    print(str(len(t_test)))
    #print(str(len(rawdata)))
    #data = np.frombuffer(rawdata, 'S')

    #t_list = rawdata[11:].split(",")
    #for i in t_list:
     #   try:
      #      float(i)
       # except:
        #    print("failed on: " + str(i))
         #   continue
    #[float(i) for i in t_list]
    #print(str(rawdata))
    #df = pd.DataFrame(t_list, columns=['voltage'])
#    data = np.frombuffer(rawdata, 'B')
    #print(str(len(df))) 
 
 
if __name__ == "__main__":
    main()
