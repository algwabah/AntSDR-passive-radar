import geopy.distance
class bistatic_converter:
    def bistatic_converter(lat,lon):
        
        Tx = (59.29759200195321, 18.173494680717763)   #nackamasten
        Rx = (59.41143533269794, 17.835577358398666)    #Antenna at A9 roof

        dTxRx = geopy.distance.distance(Tx, Rx).km #should be 23.something kilometres


        #Calculating bistatic distance
        target = (lat,lon)    #TODO: insert coordinates from ADS-B

        dRxT = geopy.distance.distance(Rx, target).km   #distance between Rx and (T)arget
        dTxT = geopy.distance.distance(Tx, target).km   #distance between Tx and (T)arget

        bistatic_dist = dRxT+dTxT

        print (bistatic_dist)
