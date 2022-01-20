# the two final files to be created are the pdfs that contain the graphs
# one graph represents the correlation between the 911 data set (NYPD_Complaint) and the Airbnb listings in New York data set
# the other graph represents the correlation between the 311 data set (311_Service_Requests) and the Airbnb listings in New York data set
all: AbnbsCrimes.pdf AbnbsComplaints.pdf

# clear all the txt files that will be outputted by the following python and awk scripts
clean:
	rm AbnbDateLatLongs.txt 911DateLatLong.txt 311DateZip.txt AbnbDateZip.txt 911DateZip.txt deltaComplaints2015-2019.txt deltaCrimes2015-2019.txt deltaAbnbs2015-2019.txt AbnbZipDeltaPerCapitaPop.txt 311ZipDeltaPerCapitaPop.txt 911ZipDeltaPerCapitaPop.txt zipAbnbCrime.txt zipAbnbComplaint.txt AbnbsCrimes.pdf AbnbsComplaints.pdf 

# STEP 1a
# reads in all lines from the Abnb listings data set and outputs the host_since date and the latitude and longitude of the Airbnb
# through the Awk script AbnbDateLatLong.awk. Keeps track of the host_ids to check whether the Airbnb is a copy of one already outputted. 
# date|lat|long are outputted to AbnbDateLatLongs.txt
AbnbDateLatLongs.txt: listings.csv.gz AbnbDateLatLong.awk
	gawk -f AbnbDateLatLong.awk

# STEP 1b
# reads in all lines from the NYPD_Complaint data set and outputs to 911DateZip.txt date of the crime|latitude|longitude ONLY for those crimes that
# interest the hypothesis. A list of crimes of interest can be found in offenses.txt (already prepared). Those are uploaded to a set inside the script:
# 911DateLatLong.py that runs everything
# output: date|lat|long
911DateLatLong.txt: offenses.txt NYPD_Complaint_Data_Historic.tsv.gz 911DateLatLong.py
	python3 911DateLatLong.py

# STEP 2a
# reads in all lines from the 311_Service_Requests data set and outputs to 311DateZip.txt date of the crime|zip ONLY for those complaints that
# interest the hypothesis. A list of complaints of interest can be found in complaints.txt (already prepared). Those are uploaded to a set inside the script:
# 311DateZip.py that runs everything
# output: date|zip 
311DateZip.txt: complaints.txt 311_Service_Requests_from_2010_to_Present.tsv.gz 311DateZip.py
	python3 311DateZip.py

# STEP 2b
# reads in the date|lat|longs of the Abnb output and 911 output (made in the previous step), converts them into zip codes (through a quad tree) and outputs
# date|zip to AbnbDateZip.txt and 911DateZip.txt (all done with LatLongToZip.py script provided by prof. Broder) 
# output: date|zip
AbnbDateZip.txt 911DateZip.txt: AbnbDateLatLongs.txt 911DateLatLong.txt LatLongToZip.py
	python3 LatLongToZip.py

# STEP 3a
# reads in the files that contain date|zip for the 311 complaints and 911 crimes, through the script computeDeltas.py it calculates the increase of number of
# crimes/complaints per zipcode from 2015 to 2019
# output zip|delta
deltaComplaints2015-2019.txt deltaCrimes2015-2019: 311DateZip.txt 911DateZip.txt computeDeltas.py
	python3 computeDeltas.py

# STEP 3b
# reads in the files that contain date|zip for the Airbnbs, through the script AbnbComputeDeltas.py it calculates the increase of number of
# Airbnbs per zipcode from 2015 to 2019
# output zip|delta 
deltaAbnbs2015-2019.txt: AbnbDateZip.txt AbnbComputeDeltas.py
	python3 AbnbComputeDeltas.py

# STEP 4
# reads in the files that contain date|delta, loads the population data from uszipsv, computes deltaPerCapita and adds a fields with the population
# output zip|deltaPerCapita|population (through the zipDeltaPop script)
AbnbZipDeltaPerCapitaPop.txt 311ZipDeltaPerCapitaPop.txt 911ZipDeltaPerCapitaPop.txt: deltaComplaints2015-2019.txt deltaCrimes2015-2019 deltaAbnbs2015-2019.txt zipDeltaPop.py
	python3 zipDeltaPop.py

# STEP 5
# reads in the files from the previous step and outputs two files that compare Airbnb deltas and Crime deltas and Airbnb deltas and Complaint deltas
# output zip|population|deltaAbnb|deltaCrime/Complaint 
zipAbnbCrime.txt zipAbnbComplaint.txt: 911ZipDeltaPerCapitaPop.txt 311ZipDeltaPerCapitaPop.txt compare.py
				python3 compare.py

# STEP 6
# graph the two comparisons between Airbnb increase between 2015 and 2019 and Crime/Complaint increase between 2015 and 2019
# 6a Crimes
AbnbsCrimes.pdf: zipAbnbCrime.txt plotAbnbCrimes.py
	python3 plotAbnbCrimes.py
# 6b Complaints
AbnbsComplaints.pdf: zipAbnbComplaint.txt plotAbnbComplaints.py
	python3 plotAbnbComplaints.py

