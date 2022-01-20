# Analysis of the correlation between the density of Airbnbs in a NYC area and the number of specific crimes/complaints reported (in that same area)

**My Hypothesis:**

As a final project for the course Applied Linux Programming and Scripting, Fall 2021, I decided to prove a hypothesis that consist of two parts. The first one, supposes that there is a correlation between the number of Airbnbs per capita in a certain area of New York City and the number of specific crimes per capita reported to NYPD for that same neighborhood. The second part hypothesizes a correlation between the number of Airbnbs per capita in a certain area of New York City and the number of specific complaints per capita reported to 311 for that same neighborhood.
            
            
**What I used and how I got to my conclusion:**

To backup my assumption, I took advantage of three data sets: the historic data for NYPD complaints, the service requests to 311 (phone number for filing complaints) from 2010 to 2021 and the Airbnb listings for New York City. To get to my conclusion, I started by selecting specific crimes and specific complaints that can be linked to the presence of Airbnbs in a neighborhood. Some examples of crimes that I considered relevant to my first hypothesis are: petit larceny, harrassment, assault and dangerous drugs. Examples of complaints that I considered relevant to my second hypothesis are: noise, illegal parking and unsanitary conditions. The full lists can be found at offenses.txt and complaints.txt respectively. Those two text files were pre-prepared and will be utilized in two of the scripts needed to get to the conclusion, therefore they are already present in the “makefile” ‘s directory. I selected the specific key words for complaints and crimes by finding the top 20 reported crimes / types of complaint and checking whether each one was relevant to the hypothesis.
      
**Walk through my code**

**First Step - *AbnbDateLatLong.awk*, *911DateLatLong.py* and *311DateZip.py***

The first operation that is run by the makefile, is completed by three programs, one for each data set. All the dates and locations (latitude and longitude for Airbnb and 911; zipcodes for 311) of Airbnb listings, crimes reported to NYPD and complaints to 311 are outputted to text files.  The first program is “AbnbDateLatLong.awk”, an Awk script that reads in all lines from the Abnb listings data set, scrapes out the host_since date and the latitude and longitude of all Airbnbs and outputs them to “AbnbDateLatLongs.txt”. Because the data set contains duplicates, the program keeps track of the host_ids to check whether the Airbnb is a copy of one already outputted. The second program is “911DateLatLong.py”, a Python script that reads in all lines contained in the NYPD_Complaint data set and outputs to 911DateZip.txt date of the crime|latitude|longitude, only for those crimes that interest the hypothesis. All the interesting offenses are read in from offenses.txt and loaded into a set inside the script. A very similar thing is done in the third program, “311DateZip.py” for the 311_Service_Requests data set. However, in this case, a zip code is outputted, along with the date of complaint, to “311DateZip.txt”.
        
        
**Second Step - *LatLongToZip.py***

As the next step, all latitude and longitudes of the Airbnbs and 911 calls need to be converted into zip codes, so that they can be easily compared to each other. “LatLongToZip.py” reads in the date|lat|longs of the Airbnbs and 911 calls text files (made in the previous step) and converts them into zip codes (through a program provided by Prof. Broder that utilizes a quad tree). The script outputs date|zip to “AbnbDateZip.txt” and “911DateZip.txt”.
        
        
**Third Step - *computeDeltas.py* and *AbnbComputeDeltas.py***

The third step consist of calculating the increase in number of crimes, complaints and Airbnbs per zip code from 2015 to 2019. I chose these two years specifically because 2015 represents the “peak year” for Airbnb and 2019 is the most recent “normal year” that 2015 can be compared to (2020 and 2021 were deeply influenced by the Covid-19 factor).  “computeDeltas.py” computes the delta complaints and the delta crimes for years 2019 and 2015, outputting zip|delta to “deltaComplaints2015-2019.txt” and “deltaCrimes2015-2019”. AbnbComputeDeltas.py does a very similar thing and outputs zip|delta for each Airbnb to “deltaAbnbs2015-2019.txt”. Both scripts use two dictionaries, for years 2019 and 2015, to keep track of all zipcodes and the number of times they appear in each data set. The programs then create a third dictionary that contains the delta of dictionaries 2019 and 2015.
       
       
**Fourth Step - *zipDeltaPop.py***

The fourth step reads in the population per zip data from uszipsv1.4.txt to compute the number of Airbnbs, 911 offenses and 311 complaints per capita. It inputs three files created in the previous step and outputs zip|deltaPerCapita|population for each file.
        
        
**Fifth Step - *compare.py***

Step five is a comparison between the deltas computed for the Airbnb data and crime deltas (as well as complaint deltas). The Python file reads in the output of the fourth step and outputs zip|population|deltaAbnb|deltaCrimeORComplaint to “zipAbnbCrime.txt” and “zipAbnbComplaint.txt”.
        
        
**Sixth Step - *plotAbnbComplaints.py* and *plotAbnbCrimes.py***

The last step is the graphing of the two comparisons between the increase of Airbnbs per capita, per zip code from 2015 to 2019 and the increase in crimes/complaints reporting per capita, per zip code from 2015 to 2019. Using matplotlib.pyplot, I wrote two Python scripts that load all Airbnb deltas per capita to lists of x-axis coordinates and all crimes/complaints deltas per capita to lists of y-axis coordinates. The graphs will be composed of circumferences of different colors, each representing a different zip code and of a different size, related to the size of the population in that zip code. The two final outputs of the entire project will be pdfs containing graphs that plot the relationships between Airbnbs, Crimes and Service Requests: “AbnbsCrimes.pdf” and “AbnbsComplaints.pdf”.
        
        
**My Conclusion**

Unfortunately, I was not able to prove either hypothesis through this data and therefore the graphs don’t project the trend that I was expecting. However, I think this may be caused by the fact that Airbnbs in New York City represent a low percentage of the total housing, are very spread out and are relatively still new to the market. For this reason, it is hard to clearly show the correlation with crimes and complaints, even though it is not so strange to think that there might be a relationship between complaints about noise/loud music/partying and the presence of Airbnbs. Perhaps, it will be possible to prove this hypothesis in another ten years, when the Airbnbs will have grown in number and popularity. 

