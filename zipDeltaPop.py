# input: zip|delta
# output --> dict{zip: delta}
# input parameter:
# zip|delta
# output
# {zip: delta}
def loadZipsToDict(fin):                                                                                                                                
    # open file                                                                                                                                               
    f = open(fin)                                                                                                                                            
    # create dictionary that will contain zips and delta                                                                                        
    zips = {}                                                     
    # read each line in the file we input                                                                                                                     
    line = f.readline().strip("\n")                                                                                                                           
                                                                                                                                                           
    # till there is still another line                                                                                                                        
    while line:                                                                                                                                               
        
        # split to get zips and delta
        fields = line.split("|")
        zip = fields[0]
        delta = fields[1]                                                                                                                                   
        # add zip and delta to dict
        zips[zip] = delta
        
        # move to next date|zip                                                                                                                               
        line = f.readline().strip("\n")                                                                                                                       
    return zips  

# fin: uszipsv to get population per zip
# dict{zip: delta}
# fout zip|DeltaPerCapita|population
def outputZipDeltaPerCapitaPop(zips, fout):
    database = open("/data/raw/latLongToGeo/uszipsv1.4.txt")                                                                                                  
    position = database.readline()                                                                                                                            
    population = ""                                                                                                                                           
                                                                                                                     
    while position:                                                                                                                                           
        fields = position.split("\t")                                                                                                                         
        zip = fields[0]                                                                                                                                       
        state_id = fields[4]                                                                                                                                  
        population = fields[8]

        # only consider the zipcode if the population is greater than 1500 people
        if zip in zips and state_id == "NY" and population != "" and int(population) > 1500:                                                             
            numPerCapita = int(zips[zip])/int(population)
            numPerCapita = '{:.20f}'.format(numPerCapita)
            fout.write(str(zip) + "|" + str(numPerCapita)+ "|" + str(population) + "\n")
        position = database.readline()
        
    database.close() 
    
def main():
    # read from file zip|delta and create dict containing the zips
    # Abnb Data
    abnbZips = loadZipsToDict("deltaAbnbs2015-2019.txt")
    foutAbnb = open("AbnbZipDeltaPerCapitaPop.txt", "w")
    outputZipDeltaPerCapitaPop(abnbZips, foutAbnb)

    # 311 Data
    complaintZips =  loadZipsToDict("deltaComplaints2015-2019.txt")
    foutComplaint = open("311ZipDeltaPerCapitaPop.txt", "w")
    outputZipDeltaPerCapitaPop(complaintZips, foutComplaint)

    # 911 Data
    crimeZips  =  loadZipsToDict("deltaCrimes2015-2019.txt")
    foutCrime = open("911ZipDeltaPerCapitaPop.txt", "w")
    outputZipDeltaPerCapitaPop(crimeZips, foutCrime)
main()
