import sqlite3
import time
import matplotlib.pyplot as plt
import numpy as np

def getData(name, date, race, dbloc):

	#connect to the database, change this to re-create the database.
	connection = sqlite3.connect(dbloc)
	cursor = connection.cursor()
	
	a=time.strptime(date, '%Y-%m-%d')
	nDate = time.strftime('%b %d, %Y',a).replace(' 0', ' ')
	
	query = "SELECT * FROM predictions WHERE candidate LIKE ? AND race = ? AND date = ?"
	cursor.execute(query, ["%"+name+"%", race, nDate])
	predictionResults = cursor.fetchall()
	
	i=-1
	for i,point in enumerate(predictionResults):
		print 'The closing value for',point[3],'on',date,'was',point[1]
	if i == -1:
		print 'There were no results foound for the given date'
		
	
	connection.close()
	
def format_date(x, pos=None):
    thisind = np.clip(int(x+0.5), 0, N-1)
    return r.date[thisind].strftime('%Y-%m-%d')
	
def plotData(name, date, race, dbloc):
	connection = sqlite3.connect(dbloc)
	cursor = connection.cursor()
	
	a=time.strptime(date, '%Y-%m-%d')
	nDate = time.strftime('%b %d, %Y',a).replace(' 0', ' ')
	
	query = "SELECT * FROM predictions WHERE candidate LIKE ? AND race = ?"
	cursor.execute(query, ["%"+name+"%", race])
	predictionResults = cursor.fetchall()
	
	dates = []
	prices = []
	
	for point in predictionResults:
		dates.append(point[0])
		prices.append(point[1])
		
	dates = np.array(dates)
	prices = np.array(prices)
	
	plt.plot(dates, prices)