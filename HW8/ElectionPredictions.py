import sys
import argparse
sys.path.append("..")

#get the modules from the other problem set
from HW5.politics import plotData
from HW5.politics import getData

#define a location for the politics db
dbloc = 'db/politics.db'

#create the argparse parse
parser = argparse.ArgumentParser(description='Show election prediction data')

#flag to designate the candidate name
parser.add_argument('-c', action='store', dest='candidate',
                    help='Candidate Name')
#flag to designate the date
parser.add_argument('-d', action='store', dest='date',
                    help='What is the date?')
#flag to specify the race, if desired
parser.add_argument('-r', action='store', default='2012 Presidential Election', dest='race',
                    help='What is the race?')
#option to show a graph
parser.add_argument('-p', action='store_true', default=False,
                    dest='plot',
                    help='Plot the results?')
									
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
results = parser.parse_args()

#get the variables
candidate = results.candidate
date = results.date
toPlot = results.plot
race = results.race

#if we're plotting, plot
if toPlot:
	getData(candidate, date, race, dbloc)
	plotData(candidate, date, race, dbloc)
#otherwise just print the result
else:
	getData(candidate, date, race, dbloc)