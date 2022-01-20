# take all the date|zips files and create dictionaries that contain
# key: all zips
# data: how many times the zips appeared
# create diff dicts per year and per file (i.e. 311DateZip, 911DateZips)

# load all zipcodes and how many times they appear in a specific year into a dictionary      
def loadZipsToDict(fin, year):
    # open file
    f = open(fin)

    # create dictionary that will contain zips and times they appeared
    zipsInYear = {}

    # read each line in the file we input
    line = f.readline().strip("\n")

    # till there is still another line
    while line:
        # split to get date and zips
        fields = line.split("|")
        
        # if there's good data (i.e. there are both a date and a zip)
        if len(fields) == 2:
            
            date = fields[0]
            zip = fields[1] 

            # add or increment zip and data (1)
            if year in date:
                if zip in zipsInYear:
                    zipsInYear[zip] += 1
                else: zipsInYear[zip] = 1

        # move to next date|zip
        line = f.readline().strip("\n")
    return zipsInYear 

# takes as parameters two dicts containing all zips and the times they appeared for two different years
# outputs a 3rd dict with the delta for the two years b-a
def deltaZips(a, b):
    c = {}

    # for every zip in the latest year
    for zip in b:
        # if there is the same zip in year a
        if zip in a:
            # subtract them
            c[zip] = b[zip] - a[zip]
        else:
            # else, pretend as its 0 in year a and just add year b
            c[zip] = b[zip]
            
    return c

# takes as parameter a dict and
# writes out to a file key|data
def outputDict(d, foutName):
    # prep output
    fout = open(foutName, "w")
    
    for key in d:
        fout.write(str(key) + "|" + str(d[key]) + "\n")

    
def main():
    #311 data
    fin = "311DateZip.txt"
    #2019
    ComplaintZipsNineteen = loadZipsToDict(fin, "2019")
    #2015
    ComplaintZipsFifteen = loadZipsToDict(fin, "2015")

    #911 data
    fin2 = "911DateZip.txt"
    #2019
    CrimesZipsNineteen = loadZipsToDict(fin2, "2019")
    #2015
    CrimesZipsFifteen = loadZipsToDict(fin2, "2015")

    # find out which zips have increased in number of complaints and number of crimes
    # between 2019 and 2015
    deltaComplaints = deltaZips(ComplaintZipsFifteen, ComplaintZipsNineteen)
    deltaCrimes = deltaZips(CrimesZipsFifteen, CrimesZipsNineteen)

    # store results ZIP|DELTACOMPLAINTS
    complaintsFout = "deltaComplaints2015-2019.txt"
    outputDict(deltaComplaints, complaintsFout)

    # ZIP|DELTACRIMES
    crimesFout = "deltaCrimes2015-2019.txt"
    outputDict(deltaCrimes, crimesFout)
    
main()
