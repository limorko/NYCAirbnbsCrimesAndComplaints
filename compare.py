# for every zip contained both in the Airbnb deltas file and in the Crime/Complaint deltas file
# output zip|deltaAirbnb|crimeOrComplaint
def compare(fin, fout):
    # open file to compare 
    f = open(fin)
    line = f.readline()

    # prepare output file
    fout= open(fout, "w")

    # load 911 (or 311) zips to a dict key = zip; data = delta
    d = {}
    while line:
        # split fields
        fields = line.split("|")     
        # add to dict
        d[fields[0]] = fields[1].strip("\n")
        # move to the next line
        line = f.readline()
        
    # open Abnb deltas
    Abnbs = open("AbnbZipDeltaPerCapitaPop.txt")
    abnb = Abnbs.readline()


    # compare deltas in crimes (or complaints) and Abnbs
    # for each Abnb
    # look for the zip in the crimes dictionary and output zip, deltaCrime (or deltaComplaint), deltaAbnb
    while abnb:
        # split fields
        fields = abnb.strip("\n").split("|")
        # if the zipcode is contained in both 
        if fields[0] in d:
            # output:
            # zip|population for that zip|deltaAbnb|delta911
            fout.write(fields[0] + "|" + fields[2]+ "|" + fields[1][0:8] + "|" + d[fields[0]][0:8] + "\n")
        abnb = Abnbs.readline()

def main():
    zipAbnbCrime = compare("911ZipDeltaPerCapitaPop.txt", "zipAbnbCrime.txt")
    zipAbnbComplaint = compare("311ZipDeltaPerCapitaPop.txt", "zipAbnbComplaint.txt")
main()
