import sys
import math
import random
import time
import gzip

# Positive and negative infinity. In Python 3.5 use math.inf and -math.inf
PINF =  math.inf
NINF = -math.inf

# long ~ X coord
# lat  ~ Y coord

# Polar Coordinate Flat-Earth Formula 
# from http://www.cs.nyu.edu/visual/home/proj/tiger/gisfaq.html
#
# a = pi/2 - lat1 
# b = pi/2 - lat2 
# c = sqrt( a^2 + b^2 - 2 * a * b * cos(lon2 - lon1) ) 
# d = R * c 

# Convert latitude and longitude to 
# spherical coordinates in radians.
DEGREES_TO_RADIANS = math.pi/180.0
RADIUS_OF_EARTH = 3956

def flatEarthDistance(lat1, long1, lat2, long2):        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1) * DEGREES_TO_RADIANS
    phi2 = (90.0 - lat2) * DEGREES_TO_RADIANS
         
    # theta = longitude
    theta1 = long1 * DEGREES_TO_RADIANS
    theta2 = long2 * DEGREES_TO_RADIANS
    
    val = phi1*phi1 + phi2*phi2 - 2*phi1*phi2*math.cos(theta2-theta1)

    if val < 0:
        if val < -.00000000001:
            raise Exception("Numerical error in flatEarthDistance: " + val)
        return 0
    
    c = math.sqrt(val)
    
    return RADIUS_OF_EARTH * c

      

# return true if the circle defined by circleLong, circleLat, circleR
# intersects the box defined by l,r,t,b
def intersects(circleLong, circleLat, circleR, left, right, top, bot):
    closestLong = circleLong
    if   circleLong < left:  closestLong = left
    elif circleLong > right: closestLong = right
  
    closestLat = circleLat
    if   circleLat < top: closestLat = top
    elif circleLat > bot: closestLat = bot
  
    return flatEarthDistance(circleLat, circleLong, closestLat, closestLong) <= circleR

class Node(object):
    def __init__(self, latitude, longitude, d):
        self.lat  = latitude
        self.long = longitude
        self.data = d # might be more than one data at this coord        
        self.NE = self.SE = self.SW = self.NW = None
        
    def __str__(self):
        return "(" + str(self.lat) + "," + str(self.long) + str(self.data) + ")"


class GeoQuadTree(object):
    def __init__(self):
        self.__root = None 
        self.__bounds = [None, None, None, None]
     
    # Wrapper method. Always succeeds.
    def insert(self, latitude, longitude, d): 
        # update the bounding box
        if not self.__bounds[0] or latitude  < self.__bounds[0]: self.__bounds[0] = latitude
        if not self.__bounds[1] or latitude  > self.__bounds[1]: self.__bounds[1] = latitude
        if not self.__bounds[2] or longitude < self.__bounds[2]: self.__bounds[2] = longitude
        if not self.__bounds[3] or longitude > self.__bounds[3]: self.__bounds[3] = longitude
        
        self.__root = self.__insert(self.__root, latitude, longitude, d)
    
    # return the bounds of all the points inserted so far
    # [latmin, latmax, longmin, longmax]
    def bounds(self): 
        b = self.__bounds
        # turn the bounds into a tuple, and return it, so that the client
        # can't inadvertantly tamper with our internal list.
        return (b[0], b[1], b[2], b[3])
        
    def __insert(self, n, lat, long, d):
        # return a new Node if we've reached None
        if not n: return Node(lat, long, d)
        
        # if the point to be inserted is identical to the current node, 
        # overwrite the data, but don't recurse any further
        if n.lat == lat and n.long == long:
            n.data = d
            return n
      
        # recurse down into the appropriate quadrant
        if   long >= n.long and lat >= n.lat: n.SE = self.__insert(n.SE, lat, long, d)
        elif long >= n.long and lat <  n.lat: n.NE = self.__insert(n.NE, lat, long, d)
        elif long <  n.long and lat >= n.lat: n.SW = self.__insert(n.SW, lat, long, d)
        else:                                 n.NW = self.__insert(n.NW, lat, long, d)   
           # long <  n.long and lat <  n.lat
        
        return n    

   
    # Wrapper method - returns list of data objects associated with this point
    def find(self, lat, long): return self.__find(self.__root, lat, long)
   
    def __find(self, n, lat, long):
        if not n: return None    # Couldn't find the exact point
      
        # Did we find the exact point? Return the list of data
        if n.long == long and n.lat == lat: return n.data
      
        # recurse down into the appropriate quadrant
        if   long >= n.long and lat >= n.lat: return self.__find(n.SE, lat, long)
        elif long >= n.long and lat <  n.lat: return self.__find(n.NE, lat, long)
        elif long <  n.long and lat >= n.lat: return self.__find(n.SW, lat, long)
        else:                                 return self.__find(n.NW, lat, long)   
           # long <  n.long and lat <  n.lat
   
    # find a nearby (but not necessarily the nearest) point to x,y 
    # by recursing as deep as possible into the tree. 
    def __nearPoint(self, n, lat, long):
        if not n: return None
      
        ans = None
      
        # recurse down into the appropriate quadrant
        if   long >= n.long and lat >= n.lat: ans = self.__nearPoint(n.SE, lat, long)
        elif long >= n.long and lat <  n.lat: ans = self.__nearPoint(n.NE, lat, long)
        elif long <  n.long and lat >= n.lat: ans = self.__nearPoint(n.SW, lat, long)
        else:                                 ans = self.__nearPoint(n.NW, lat, long)
           # long <  n.long and lat <  n.lat:
      
        # if we found a lower Node near this point return it
        # otherwise return the current node
        return ans if ans else n

   
    def __nearest(self, n, lat, long, cand, dist):
        if not n: return cand, dist
      
        # Is the current quad tree point closer than the candidate?
        # If so, update the candidate
        newDist  = flatEarthDistance(lat, long, n.lat, n.long)
        if newDist < dist:
            cand = n  
            dist = newDist

        # descend into the quadrants that intersect the current search circle
        # refining the radius after each better candidate is found
        if intersects(long, lat, dist, n.long, PINF, n.lat, PINF): cand, dist = self.__nearest(n.SE, lat, long, cand, dist)
        if intersects(long, lat, dist, n.long, PINF, NINF, n.lat): cand, dist = self.__nearest(n.NE, lat, long, cand, dist) 
        if intersects(long, lat, dist, NINF, n.long, n.lat, PINF): cand, dist = self.__nearest(n.SW, lat, long, cand, dist)
        if intersects(long, lat, dist, NINF, n.long, NINF, n.lat): cand, dist = self.__nearest(n.NW, lat, long, cand, dist)

        return cand, dist

   
    def nearest(self, lat, long, maxDist = None):
        if not self.__root: return None
        
        # Descend the tree and find the leaf node near 
        # to this query point. This quickly sets an upper 
        # bound on the nearest possible point 
        cand = self.__nearPoint(self.__root, lat, long)
        dist = flatEarthDistance(lat, long, cand.lat, cand.long)
        
        # Now we will descend the tree once more, refining the 
        # candidate by progressively shrinking the radius
        ans, dist = self.__nearest(self.__root, lat, long, cand, dist)
        if maxDist != None and dist > maxDist:
            return None

        return ans.data

    def nearestDist(self, lat, long, maxDist = None):
        if not self.__root: return None
        
        # Descend the tree and find the leaf node near 
        # to this query point. This quickly sets an upper 
        # bound on the nearest possible point 
        cand = self.__nearPoint(self.__root, lat, long)
        dist = flatEarthDistance(lat, long, cand.lat, cand.long)
        
        # Now we will descend the tree once more, refining the 
        # candidate by progressively shrinking the radius
        ans, dist = self.__nearest(self.__root, lat, long, cand, dist)
        if maxDist != None and dist > maxDist:
            return None

        return dist




# Load the ZIP codes into a list of tuples
# (ZIP code, latitude, longitude).
# But only load the ZIP codes that have
# a population associated with them.
def readZIPsWithLatLong():
    ans = []
    f = open("/data/raw/latLongToGeo/uszipsv1.4.txt", "rb")

    first = True
    for l in f:
        l = l.decode()
        words = l.split('\t')
        if not first and words[8] != '':
            t = words[0], float(words[1]), float(words[2])
            ans.append(t)
        first = False

    f.close()
    return ans

# Load the ZIP code file into a GeoQuadTree
def loadZIPs():
    ans = GeoQuadTree()
    zips = readZIPsWithLatLong()
    for z in zips:
        ans.insert(z[1], z[2], z[0])
    return ans


#
# assumes that file inputed contains lines that look like this:
#   DATE|LAT|LONG
# and writes out to a file lines that look like this:
#   DATE|ZIP
# If a ZIP code couldn't be determined, then the line is discarded
def getDateZip(finName, foutName):
    # Get the quad tree containing the zip codes from the 
    # master file
    t = loadZIPs()
    fin = open(finName)
    line = fin.readline()


    fout = open(foutName, "w")      
    # For each line

    # keep track if any conversion fails
    badLatLong = 0
    
    while line:
        fields = line.strip().split('|')
        
        # if it is an acceptable lat, long
        try:
            # get the lat field and long field and convert string to float
            lat = float(fields[1])
            long = float(fields[2])


            #    Get the zip code that is nearest to the input lat/long
            #    But if the nearest ZIP is more than 2.0 miles, None is returned
            ans = t.nearest(lat, long, 2.0)
        
            #    Now write out the date and the zip code if it could be determined
            if fields[0] != "" and ans:
                fout.write(fields[0] + "|" + ans  + "\n")



            # if the conversion did not work, increment the number of bad lat longs
            else: badLatLong += 1


        except:
            badLatLong += 1

        # move on to the next lat long
        line = fin.readline()
            
    fin.close()
    fout.close()
    
def main():
    
    #Abnb
    getDateZip("AbnbDateLatLongs.txt", "AbnbDateZip.txt")

    #911
    getDateZip("911DateLatLong.txt", "911DateZip.txt")

main()
    
    
    
