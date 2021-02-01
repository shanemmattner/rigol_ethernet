from instruments import DS1000Z
import numpy as np
import pandas as pd
import ds1054z_cp as dscp

#from ds1054z import DS1054Z 
def main():

    scope = dscp.DS1054Z('169.254.145.221')
    print("Connected to: ", scope.idn)

    depth = scope.memory_depth_internal_total
    print('Mem depth' + str(depth))
    scope.stop()
    print("currently displayed channels: ", str(scope.displayed_channels))
    scope.single()
    print(str(scope.running))
    #wait until the scope has stopped running
    #TODO: make sure we don't sit here forever
    while(scope.running):
        continue
    samples_list = scope.get_waveform_samples('CHAN1')
    df = pd.DataFrame(samples_list, columns = ['samples'])
    print(df)
 
if __name__ == "__main__":
    main()
