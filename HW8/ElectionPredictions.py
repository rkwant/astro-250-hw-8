import sys
import argparse
sys.path.append("..")

from HW5.politics import foo
from HW5.politics import getData

parser = argparse.ArgumentParser(description='Show election prediction data')

parser.add_argument('-c', action='store', dest='candidate',
                    help='Candidate Name')
parser.add_argument('-d', action='store', dest='date',
                    help='What is the date?')
parser.add_argument('-p', action='store_true', default=False,
                    dest='plot',
                    help='Plot the results?')
					
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
results = parser.parse_args()

candidate = results.candidate
date = results.date
toPlot = results.plot

getData(candidate, date, 'db/politics.db')