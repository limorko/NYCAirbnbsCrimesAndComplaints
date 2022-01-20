#!/usr/bin/env python3

import matplotlib.pyplot as plt
import random
import math


# create a figure instance that will later be written to a PDF
f = plt.figure()

# this list will contain all the Airbnb deltas per capita
x = []
# this list will contain all the Crime deltas per capita
y = []
# this list will contain all the areas for the circumferences 
areas = []

# read in the file that compares deltas for Airbnbs and deltas for Crime per each zipcode
file = open("zipAbnbCrime.txt")
line = file.readline()

# for every line of the file
while line:
    fields = line.split("|")
    # add the Airbnb delta to the x values
    x += [float(fields[2])]
    # add the Crime delta to the y values
    y += [float(fields[3].strip("\n"))]
    # add area of the circle according to the population per capita (the bigger the population in that zip, the bigger the circle)
    # divide the population by 1000, otherwise the size is too big
    areas += [float(fields[1])/1000]
    # move on to the next delta comparison
    line = file.readline()


# make a list of random colors
colors = [random.random() for i in range(len(x))]


# do the scatter plot, with specified colors and sizes
plt.scatter(x, y, c = colors, s = areas, alpha = 0.25)

        
# specify the x and y axis labels
plt.xlabel("Abnbs")
plt.ylabel("Crimes")

# Save the plot into a PDF file
f.savefig("AbnbsCrimes.pdf")

