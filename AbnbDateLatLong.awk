#!/usr/bin/gawk -f

# input: listings.csv.gz
# output: txt file containing latitudes and longitudes of the Airbnbs and the dates they were posted (host_since) 
#         date|lat|long 
BEGIN{

    # open file to read in lines
    cmd = "zcat listings.csv.gz"
    # set the record separator
    RS = "\n[0-9]+,https://"

    # set the field separator 
    FS = ","

    # check if the Airbnb is a duplicate
    # initialize the array host_ids
    host_ids["None"] = "None"
    # host_id is included between two urls: https://.*jpg, host_id, https://

    # for each record, output the date, lat and long, pipe delimited
    while ((cmd | getline) > 0){

	# match the host_id, date (host_since), lat and long
	match($0, /https:.*,([0-9]+),https:.*([0-9]{4}-[0-9]{2}-[0-9]{2}).*([0-9]{2}\.[^,]+),(-[0-9]{2}[^,]+)/, arr)
	# check the host_id
	host_id = arr[1]
	# if this is not an airbnb duplicate
	if (!(host_id in host_ids)){
		# keep track of this host_id
		host_ids[arr[1]] = arr[1] 

		# prepare output
		datePos = arr[2] "|" arr[3] "|" arr[4]

		#if fields are  not empty export ans to AbnbDateLatLongs
		if (arr[2] != "" || arr[3] != "" || arr[4] != ""){
		print datePos > "AbnbDateLatLongs.txt"
		}
	    }

    }
}
