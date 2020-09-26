import heapq


class Recommendations(object):
    
    
    def __init__(self,lat1,lon1):
        
        self.lat1 = lat1
        self.lon1 = lon1
        self.get_places = {}
        self.keywords_filter = ['gas_station','rest_area','food']
        self.topK = 3
        self.heap_builder = []
        heapq.heapify(heap_builder)
        
        
    
    def aerialDist(self,lat1,lon1,lat2,lon2):
    
        #print(lat1,lon1,lat2,lon2)
        
        r = 6371e3
        theta1 = lat1 * math.pi/180
        theta2 = lat2 * math.pi/180

        delta = (lon2 - lon1) * math.pi/180
        d = math.acos(math.sin(theta1) * math.sin(theta2)  + math.cos(theta1) * math.cos(theta2) * math.cos(delta)) * r
        
        #print('Distance ',d)
        return round(d/1e6,2)

    def garbageCleaner(self):
    
        self.heap_builder = []
        self.get_places = []

    def filterType(self,response,id_):

        #proximity = 20 
        types = response['types']
        loc = response['geometry']['location']
        lat2,lon2 = float(loc['lat']),float(loc['lng'])
        name = response['name']
        open_cond = response['opening_hours']['open_now']

        json_obj = {'types':types,'loc':loc,'name':name,'open':open_cond}

        if(open_cond):

            for key in self.keywords_filter:
                
                if(key in types):
                    distance = self.aerialDist(self.lat1,self.lon1,lat2,lon2)
                    heapq.heappush(self.heap_builder,(distance,id_))
                    self.get_places[id_] = json_obj
                        
                        
    def topRec(self):
        
        res = {}
        temp = self.topK
        
        while temp > 0:
            if(self.heap_builder):
                _,id_ = heapq.heappop(self.heap_builder)
                res[temp] = self.get_places[id_]
                temp -=1
            else:
                break
                
        self.garbageCleaner()
        
        return res
                            
if __name__ == '__main__':
    
    #user_coordinates pluge here
    rc = Recommendations(25.869385,80.29136)
    
    #get the nearby places
    
    #google_maps()
        
    for i in range(len(dict_['results'])):
        rc.filterType(dict_['results'][i],i)
        
    print(rc.topRec())
