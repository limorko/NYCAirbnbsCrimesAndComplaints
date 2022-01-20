import gzip
import sys

#input offenses.txt --> all crimes that interest the hypothesis
#output a set that contains all those crimes (so look up is only O(1))
def getCrimes(fName):

    # read in lines from file 911/offenses.txt
    # add each line to the set
    fin = open(fName)

    # read the first line, disregard case
    line = fin.readline().strip("\n").upper()

    # create a set of crimes of interest
    crimes = set()

    # while we haven't finished processing the whole file

    while line:
        # add the crime to the set
        crimes.add(line)
        #read the nextline, disregard case 
        line = fin.readline().strip("\n").upper()

    return crimes 

#input file (NYPD_Complaint_Data_Historic.tsv.gz)
#      set with crimes of interest
#output: txt file with date and latitude and longitude of the crime reported (date of crime not date of phone call)
#                      date|lat|long 
def dateLatLong(finName, fout, crimesOfInterest):
    #open files
    #input
    f = gzip.open(finName, "rt")                                                                                                                  

    #output
    fout = open(fout, "w")
    

    #read starting from the second line                                                                                                                      
    line = f.readline()
    line = f.readline()
    
    # keep track of the num of "bad lines" that we are discarding 
    badLines = 0

    # keep track of the num of "uninteresting" lines that we are discarding 
    uninterestingLines = 0
    
    while line:
        try:
            #split it on tabs and strip spaces
            fields = line.split("\t")

            # if the crime (OFNS_DESC) is part of the list of crimes that are relevant to the hypothesis
            # AND
            # if all fields are valid (not empty)
            if fields[1] != "" and fields[27] != "" and fields[28] != "" and fields[8] in crimesOfInterest:
                fout.write(fields[1] + "|" + fields[27] + "|" + fields[28] + "\n")


            # otherwise it's an "uninterestingLine"
            else: uninterestingLines += 1

            
        except:
            # if an exception occurs then it is a bad line which we discard, increment the count of bad lines
            badLines += 1

        # ready to move on to the next record 
        line = f.readline()

    # total discarded records
    totDiscarded = badLines + uninterestingLines


    
    #close files
    f.close()
    fout.close()

    
    
def main():                                                                                                                                                   
    # create crimes set
    crimes = getCrimes("offenses.txt")

    # read in crime data
    finName911 = "NYPD_Complaint_Data_Historic.tsv.gz"                                                                                 
    # output dates, lat and lot
    fout911 = "911DateLatLong.txt"                                                                                                      
    keys911 = dateLatLong(finName911, fout911, crimes)
    

main()       
