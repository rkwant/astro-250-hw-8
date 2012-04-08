import sqlite3
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt

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
		t = time.strptime(point[0], '%b %d, %Y')
		d = dt.datetime(t.tm_year, t.tm_mon, t.tm_mday)
		dates.append(d)
		prices.append(point[1])
		
	dates = np.array(dates)
	prices = np.array(prices)
	
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(dates, prices)
	fig.autofmt_xdate()
	plt.show()