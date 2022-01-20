import gzip
import sys

#input complaints.txt --> all complaints that interest the hypothesis                                                                                        
#output a set that contains all those complaints (so look up is only O(1))    
def getComplaints(fin):
    # create set of complaints of interest to our hypothesis
    complaints = set()
    
    # open list of complaints of interest
    f = open(fin)

    # read in from file every complaint
    line = f.readline().strip("\n").upper()

    while line:
        # add the complaint
        complaints.add(line)
        # move to the next line
        line = f.readline().strip("\n").upper()
    return complaints

#input 311_Service_Requests_from_2010_to_Present.tsv.gz and set containing complaints of interest
#output txt file with the date and the zip code of the complaint
#                         date|zip
def dateLatLong(finName, fout, complaintsOfInterest):
    #open files
    #input
    f = gzip.open(finName, "rt")                                                                                                                  

    #output
    fout = open(fout, "w")
    

    #read starting from the second line                                                                                                                      
    line = f.readline()
    line = f.readline()
    

    # keep track of "bad records" that we are not considering
    badRecords = 0

    # keep track of "uninteresting records"
    uninterestingRecords = 0

    while line:
        try:
            #split it on tabs and strip spaces
            fields = line.split("\t")

            # if the complaint (field Complaint Type) is part of the list of complaints that are relevant to the hypothesis
            # AND
            # if all fields are valid (non empty)
            if fields[1] != "" and fields[8] != "" and fields[5].upper() in complaintsOfInterest:
                fout.write(fields[1][0:10] + "|" + fields[8] +  "\n")
            # otherwise it's an "uninterestingLine"                                                                                                           
            else: uninterestingLines += 1            
                                                                                                                                                           
            
        except:
            badRecords += 1

        line = f.readline()

    # total discarded records                                                                                                                                 
    totDiscarded = badRecords + uninterestingRecords


    
    #close files
    f.close()
    fout.close()

    
    
def main():
    #only get complaints relevant to our hypothesis
    complaints = getComplaints("complaints.txt")
    # read in complaints data
    finName311 = "311_Service_Requests_from_2010_to_Present.tsv.gz"                                                                                 
    # output date and zip
    fout311 = "311DateZip.txt"                                                                                                          
    keys311 = dateLatLong(finName311, fout311, complaints)
    



main()       
